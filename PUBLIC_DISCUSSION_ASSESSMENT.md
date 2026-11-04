# Groww SIP Discovery Engine — pilot build

**Purpose:** demonstrate a source-linked feedback discovery workflow on the manually checked pilot the researcher already assembled. This is a pilot system and evidence set, not a representative study.

## What went into this build

The provided CSV and source-check log contained **30 records** checked on 2026-11-02: 27 Reddit records and 3 Apple App Store reviews. I then searched targeted Reddit discussions and opened three additional source pages, adding two Groww-specific records and one general SIP mandate/penalty record. The expanded working set has **33 records**: 30 Reddit records and 3 Apple App Store reviews. It has no blank review text or source URLs, and no duplicate `record_id` or `dedupe_key` values. The original log reports 28 unique source pages; the three new pages make 31 opened pages total. Text was visible on the source page for all 33 records. Stable per-review IDs were unavailable for the 3 App Store reviews; some Reddit dates are relative or conflict with indexed dates; no reporter claim was independently verified.

The source relevance labels classify **28 as explicitly SIP-related** and **5 as adjacent but not explicit SIP**. The new general SIP mandate/penalty record is SIP-related but not Groww-specific; the other two additions explicitly concern Groww. Those distinctions are retained in the additions log and relevance reason. I added one primary journey stage, one primary theme, a short reported impact, a reported workaround/need, evidence type, and a coding-confidence field. These are manual analyst codes based on the visible text; confidence describes how clear the coding was, not whether the user's claim is true.

## Early signals visible in the pilot

These are counts inside this manually assembled sample only. They are not estimates of prevalence among Groww customers.

- **6 records** describe status, allocation, transaction-history, or SIP-list visibility uncertainty across Groww, an AMC, or an external registrar.
- **6 records** concern changing SIP amount or format, including step-up timing and demat/SOA uncertainty.
- **7 records** concern AutoPay or mandate setup, failure, penalty, or removal: 6 Groww-specific and 1 general SIP category example. One additional adjacent App Store review mentions AutoPay while describing a wallet issue.
- The set also contains **5 positive counterexamples** about beginner usability, setup, or continued use. Keeping these matters: the engine should not make every record a complaint.

The repeat signal worth investigating first is **uncertainty about whether an SIP is active, paid, allocated, or continuing when Groww and another system show different information**. That is a hypothesis for interviews and more evidence, not a validated opportunity or a causal claim.

## How to use the engine

Open `groww_sip_discovery_engine.html` in a browser. Search the record text, filter by relevance class, journey stage, or source, and open the cited source. The page keeps the source's SIP/adjacent decision visible and calls out that report claims remain unverified.

To load a larger export, use **Load another CSV**. The page accepts source-style review columns and uses supplied relevance fields when present. For rows without a relevance label, it marks literal SIP/mutual-fund/mandate matches as **keyword candidates**; that is a recall-oriented screen and needs human review. It does not silently treat those matches as relevant findings.

The page now has a separate **Official help for common how-to questions** section. It links to Groww's published guidance for pausing/skipping/cancelling SIPs, AutoPay setup, checking SIP/order status, unit allocation, and confirming instalment debits. These are answer/action references, not evidence that a reported problem is common. User-experience claims should link to the cited public feedback record. The 323K Hugging Face export has review IDs but no individual source URLs or app/package identifier, so its rows cannot currently be presented as individually source-cited public feedback. Do not attach a Reddit post to an unrelated row as if it were that row's source.

## Question-answering MVP

`groww_sip_discovery_mvp.html` adds a question/search box over the 3,273 explicit-SIP review candidates. It retrieves matching excerpts, displays dataset review IDs, shows rating/date/app version, calculates rating summaries only for the retrieved set, and suggests relevant official help links. Common query words such as “SIP” are excluded from ranking so they do not match the entire SIP-only corpus. Each review cites the Hugging Face dataset page and explicitly says an original per-review Google Play URL was not supplied or verified. Search and summaries are keyword-based. The **Ask AI** action sends retrieved excerpts to a local Ollama model for a grounded draft answer.

The remaining setup is to install/run Ollama, download a local model, start the local server, and evaluate representative questions for unsupported claims. The server sends only retrieved excerpts and official-help titles/URLs; it will link users to the official page rather than inventing procedure steps from a title. Search works without Ollama; AI answers require the local model service, but do not require an OpenAI API key.

## Limits and next research step

This pilot is self-selected and heavily Reddit-weighted, with only three App Store reviews and no SIP-specific Google Play items in the source log. The record count cannot support comparisons of how common problems are. Dates are not consistently precise, and a visible source post verifies only that the post text exists at that page. It does not establish the financial facts, the author's representativeness, or Groww-wide product behavior.

Use the engine to identify candidate interview prompts, then broaden collection around the observed areas: mandate/autopay control, step-up and format changes, and status/allocation mismatches. Preserve source URL, platform ID, date precision, collection method, explicit/adjacent decision, and human review status. Add interviews before asserting causes, segments, or product prevalence.

## Files

- `groww_sip_discovery_engine.html` — interactive, self-contained evidence explorer.
- `groww_sip_discovery_mvp.html` — question-led review retrieval prototype with dataset citations and official help suggestions.
- `build_groww_discovery_mvp.py` — regenerates the retrieval prototype from the explicit-SIP candidate CSV.
- `groww_discovery_server.py` — serves the page and grounds local-model AI answers in retrieved reviews and official help references.
- `groww_sip_support_sources.json` — the official help links shown separately in the explorer.
- `groww_sip_pilot_tagged.csv` — 33 original/additional records plus first-pass manual codes.
- `build_groww_sip_engine.py` — rebuilds the tagged CSV and HTML using Python standard library only.
- `source_checked_pilot.csv` and `source_check_log.json` — copies of the supplied input and provenance log used in the build.
- `source_additions_2026-11-02.csv` and `source_additions_log_2026-11-02.json` — 3 targeted, manually opened additions and their verification notes.
