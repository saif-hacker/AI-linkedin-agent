# Architecture

## Overview
The system is a pipeline of **four agents**:

1. **Collector** — Ingests newly connected profiles (CSV, PhantomBuster, or stubbed browser automation).
2. **Analyzer** — Extracts entities/keywords from About/Headline/Posts to derive topics and intent.
3. **Generator** — Creates a concise, hyper-personalized connection message.
4. **Outreach** — Sends (or queues) messages via adapters. `human-approval` is supported.

## Flow
```
[Collector] -> profiles.jsonl -> [Analyzer] -> enriched.jsonl -> [Generator] -> outbox.jsonl -> [Outreach]
```

- All steps write/read **JSONL** for streaming-friendly processing.
- A **SQLite** DB (optional) deduplicates profiles and logs outcomes.
