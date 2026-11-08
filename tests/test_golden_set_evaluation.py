import csv
import io
import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from golden_set_evaluation import (
    _extract_json_object,
    _validate,
    load_golden_set,
    build_results_csv,
    calculate_agreement,
    classify_record,
)


class GoldenSetEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.row = {
            "golden_id": "GS01",
            "source_id": "source-1",
            "raw_feedback": "I like the simple SIP setup.",
            "human_relevance_label": "Explicit SIP",
            "human_journey_stage": "Setup/Start",
            "human_primary_theme": "Positive ease of use and SIP controls",
            "human_sentiment": "Positive",
            "human_annotator": "Reviewer",
            "human_label_status": "FRIEND_REVIEWED_REPORTED_BY_PROJECT_OWNER",
        }

    def test_bundled_golden_set_has_20_labeled_records(self):
        path = Path(__file__).resolve().parents[1] / "golden_set.csv"
        rows = load_golden_set(str(path))
        self.assertEqual(len(rows), 20)
        self.assertTrue(all(row["human_relevance_label"] for row in rows))
        self.assertTrue(all(row["human_journey_stage"] for row in rows))
        self.assertTrue(all(row["human_sentiment"] for row in rows))

    def test_extracts_json_from_markdown_fence(self):
        parsed = _extract_json_object('prefix\n```json\n{"relevance":"Explicit SIP"}\n```')
        self.assertEqual(parsed["relevance"], "Explicit SIP")

    def test_validator_rejects_unknown_taxonomy_value(self):
        with self.assertRaises(ValueError):
            _validate({
                "relevance": "Maybe",
                "journey_stage": "Setup/Start",
                "primary_theme": "Theme",
                "sentiment": "Positive",
                "rationale": "Reason",
            })

    @patch("golden_set_evaluation.OpenAI")
    def test_classifies_valid_json_without_json_mode(self, openai_mock):
        payload = {
            "relevance": "Explicit SIP",
            "journey_stage": "Setup/Start",
            "primary_theme": "Positive ease of use and SIP controls",
            "sentiment": "Positive",
            "rationale": "The author reports easy SIP setup.",
        }
        message = SimpleNamespace(content=json.dumps(payload))
        fake = SimpleNamespace(
            chat=SimpleNamespace(
                completions=SimpleNamespace(
                    create=unittest.mock.Mock(return_value=SimpleNamespace(
                        choices=[SimpleNamespace(message=message)]
                    ))
                )
            )
        )
        openai_mock.return_value = fake
        result = classify_record(self.row, "test-key")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["relevance"], "Explicit SIP")
        self.assertEqual(result["attempts"], 1)
        kwargs = fake.chat.completions.create.call_args.kwargs
        self.assertNotIn("response_format", kwargs)

    @patch("golden_set_evaluation.OpenAI")
    def test_retries_malformed_json_and_keeps_final_raw_output(self, openai_mock):
        good = {
            "relevance": "Explicit SIP",
            "journey_stage": "Setup/Start",
            "primary_theme": "Positive ease of use and SIP controls",
            "sentiment": "Positive",
            "rationale": "The author reports easy SIP setup.",
        }
        outputs = ["not json", json.dumps(good)]
        create = unittest.mock.Mock(side_effect=[
            SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=outputs[0]))]),
            SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=outputs[1]))]),
        ])
        fake = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
        openai_mock.return_value = fake
        result = classify_record(self.row, "test-key")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["attempts"], 2)
        self.assertEqual(result["raw_output"], outputs[1])
        self.assertEqual(create.call_count, 2)

    def test_agreement_uses_only_completed_records_and_preserves_human_labels(self):
        results = {
            "GS01": {
                "status": "success",
                "relevance": "Explicit SIP",
                "journey_stage": "Setup/Start",
                "primary_theme": "Positive ease of use and SIP controls",
                "sentiment": "Positive",
                "raw_output": '{"audited":true}',
            }
        }
        agreement = calculate_agreement([self.row], results)
        self.assertEqual(agreement["Relevance"]["matches"], 1)
        self.assertEqual(agreement["Relevance"]["denominator"], 1)
        csv_text = build_results_csv([self.row], results)
        self.assertIn("FRIEND_REVIEWED_REPORTED_BY_PROJECT_OWNER", csv_text)
        exported = next(csv.DictReader(io.StringIO(csv_text)))
        self.assertEqual(exported["ai_raw_output"], '{"audited":true}')
        self.assertIn("Positive ease of use and SIP controls", csv_text)


if __name__ == "__main__":
    unittest.main()
