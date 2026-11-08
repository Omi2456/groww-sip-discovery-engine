GROWW SIP DISCOVERY ENGINE — SUBMISSION EVIDENCE DATA

Contents
- groww_sip_discovery_evidence.csv: unified structured dataset, 3300 evidence rows.
- groww_reviews_sip_subset.csv: 3273 Groww review records used by the app, with original dataset columns retained.
- source_linked_public_discussions.csv: 27 public discussions used by the app, with original post URLs.
- dataset_manifest.json: counts and provenance summary.

Original Groww dataset
https://huggingface.co/datasets/Avaneeshkarthik/groww-app-reviews
The source dataset has approximately 323K total reviews. This project does NOT use all of them. The app's local evidence corpus uses a prepared subset of 3273 SIP-related Groww reviews plus 27 public discussions.

IDs and traceability
The master CSV adds stable evidence IDs R0001 onward. source_record_id retains the original reviewId for Groww records and source_id for public discussions. Groww review IDs are present, but the source dataset does not provide verified individual Google Play review URLs. Therefore source_url for those rows points to the general Groww Play listing, not to an individual review. Reddit rows retain direct original discussion URLs.
Google Play app listing: https://play.google.com/store/apps/details?id=com.nextbillion.groww&hl=en_IN

Master CSV fields
 evidence_id: stable ID for this evidence pack
 source_type, source_name: source class and name
 source_record_id: original review/post identifier from the source file
 text, published_at: feedback text and source date
 rating, thumbs_up, app_version, username: Groww review metadata where available
 subreddit: community name for public discussions
 source_url: direct Reddit source URL, or general Groww Play app page for dataset reviews
 source_url_type, individual_review_url: traceability type; no individual Google Play URLs were supplied
 source_dataset_url: original dataset card for Groww review rows
 matched_terms, nontrivial_text_proxy: prepared-subset metadata where available
 scope, relevance_reason, verification_status: research/provenance notes
 source_platform, source_app, source_url_status: source metadata

Evidence limitations
These records are discovery inputs, not a representative sample of all Groww users. Repeated review text can occur under different original IDs. The IDs are preserved so reviewers can compare records with the dataset; R-numbering is a stable index for this submitted evidence pack. The app itself labels the top results R01–R05 within each search result.
