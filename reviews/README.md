# Native review records

The review station writes append-only review events to `native_reviews.jsonl`.
Reviewer names or stable pseudonyms are required so the promotion command can
verify two distinct reviewers. A later event from the same reviewer supersedes
their earlier event for promotion decisions; history is retained.

Review data and promoted derivatives are local working artifacts and are not
committed by default. Do not enter personal contact details in reviewer IDs or
notes.
