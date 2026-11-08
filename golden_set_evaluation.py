"""Batch Groq classification for the 20-record SIP discovery Golden Set.

Run only from the Streamlit app. Never log or return the API key.
"""
from __future__ import annotations
import csv, io, json
from datetime import datetime, timezone
from openai import OpenAI

MODEL_NAME = "openai/gpt-oss-20b"
BASE_URL = "https://api.groq.com/openai/v1"
TAXONOMY = {
 "relevance": ["Explicit SIP", "Adjacent SIP", "Not relevant"],
 "journey_stage": ["Discover/Choose", "Setup/Start", "Pay/AutoPay", "Manage/Pause/Cancel", "Track/Status/Allocation", "Change/Step-up", "Withdraw/Sell", "Other/Unclear"],
 "sentiment": ["Positive", "Negative", "Mixed", "Neutral/Question"],
}
def classify_golden_set(csv_text: str, api_key: str) -> tuple[str, dict]:
    reader = csv.DictReader(io.StringIO(csv_text))
    rows = list(reader)
    if len(rows) != 20:
        raise ValueError(f"Expected 20 Golden Set records; found {len(rows)}.")
    client = OpenAI(api_key=api_key, base_url=BASE_URL, timeout=30.0, max_retries=1)
    results=[]
    prompt_template = """Classify the supplied single customer-feedback record for product discovery.
Use only the record text. Do not infer facts or causes. Choose exactly one relevance,
journey_stage, sentiment and a concise primary_theme. If unclear use Other/Unclear
and/or Neutral/Question. Keep theme specific to the text.
Allowed relevance: Explicit SIP | Adjacent SIP | Not relevant.
Allowed journey_stage: Discover/Choose | Setup/Start | Pay/AutoPay | Manage/Pause/Cancel |
Track/Status/Allocation | Change/Step-up | Withdraw/Sell | Other/Unclear.
Allowed sentiment: Positive | Negative | Mixed | Neutral/Question.
Return JSON only with keys: relevance, journey_stage, primary_theme, sentiment, rationale.
"""
    for row in rows:
        payload={"golden_id":row["golden_id"],"source_id":row["source_id"],"text":row["raw_feedback"]}
        response=client.chat.completions.create(
          model=MODEL_NAME,
          messages=[
            {"role":"system","content":"You are a cautious research data annotator. Return valid JSON only."},
            {"role":"user","content":prompt_template+"\nRecord:\n"+json.dumps(payload,ensure_ascii=False)}
          ],
          response_format={"type":"json_object"},
          max_completion_tokens=350,
        )
        raw=response.choices[0].message.content or "{}"
        try: parsed=json.loads(raw)
        except json.JSONDecodeError: parsed={"parse_error":True,"raw_output":raw}
        results.append({
          "golden_id":row["golden_id"],"source_id":row["source_id"],
          "ai_relevance_label":parsed.get("relevance",""),
          "ai_journey_stage":parsed.get("journey_stage",""),
          "ai_primary_theme":parsed.get("primary_theme",""),
          "ai_sentiment":parsed.get("sentiment",""),
          "ai_rationale":parsed.get("rationale",""),
          "ai_raw_output":raw,
        })
    fields=list(results[0].keys())
    buf=io.StringIO(); writer=csv.DictWriter(buf,fieldnames=fields);writer.writeheader();writer.writerows(results)
    metadata={"provider":"Groq","model":MODEL_NAME,"base_url":BASE_URL,"records":len(results),
      "evaluated_at_utc":datetime.now(timezone.utc).isoformat(),
      "prompt_version":"golden-set-classifier-v1","note":"AI outputs only; agreement is calculated separately after human reference labels are verified."}
    return buf.getvalue(),metadata
