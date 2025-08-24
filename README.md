<<<<<<< HEAD
# AI-linkedin-agent
=======
# AI LinkedIn Competitor Monitor & Outreach Agent (Python)

> **Important:** This repository provides a *modular*, ethics-first architecture. 
> It supports compliant data sources (manual CSV, partner APIs) and offers **stubs** for 
> risky methods (browser automation) with explicit warnings. Use only in accordance with LinkedIn's Terms of Service and applicable laws.

## What it does
- Monitors competitor *decision-makers* to discover **new connections** (via compliant data sources).
- Analyzes each new connection’s profile text (About, headline, recent posts).
- Generates **hyper-personalized** connection request messages using templates or an LLM.
- Sends the connection request via an **adapter** (manual, API-based tools like PhantomBuster/TexAu, or a stubbed browser-automation module).

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Copy and edit environment variables
cp .env.example .env

# Run end-to-end in "human-approval" mode (you approve before sending)
python src/main.py run --source=csv --approve
```
# Run Automatic fetching using Selenium__  # Not recommended due to Linkedin TOS
python src/main.py run --source=selenium --approve

### Modes
- `collect` — fetch new connections
- `analyze` — enrich with topics/entities
- `generate` — produce personalized messages
- `outreach` — send (or queue) requests
- `run` — orchestration of the above

Examples:
```bash
# Collect (from CSV) → Analyze → Generate → Queue for review
python src/main.py run --source=csv --no-send

# After manual review, perform outreach (example: phantombuster adapter)
python src/main.py outreach --adapter=phantombuster --batch data/outbox.jsonl
```

## Data sources (choose one)
- **Manual CSV (compliant, recommended to start):** Export new connections as `data/new_connections.csv`.
- **Third-party connectors:** PhantomBuster/TexAu (requires paid plan and their TOS).
- **Browser automation (stub only):** Playwright/Selenium placeholders are provided with warnings. *Use at your own risk.*

## Files
```
src/
  main.py
  agents/
    collector.py       # Pulls profiles from selected data source
    analyzer.py        # NLP tagging/keyword extraction
    generator.py       # Template/LLM-based message generation
    outreach.py        # Adapters to send/queue messages
  services/
    datasources/
      base.py
      manual_csv.py
      phantombuster.py
      playwright_linkedin.py  # stub with warnings
    nlp/nlp_utils.py
    llm/openai_llm.py
    storage/db.py
    utils/{config.py,logging.py,rate_limiter.py}
data/
  new_connections.csv  # input (example)
  outbox.jsonl         # generated messages awaiting approval/sending
docs/
  ARCHITECTURE.md
  ETHICS_COMPLIANCE.md
```

## Environment Variables
Copy `.env.example` to `.env` and set values:
```
# Optional (only if using OpenAI for message generation)
OPENAI_API_KEY=

# Optional PhantomBuster connector
PHANTOMBUSTER_API_KEY=

# Runtime config
APP_ENV=dev
```

## Legal/Ethical Notice
- **Do not** scrape LinkedIn without explicit permission. 
- Prefer compliant sources (manual exports, partner APIs).
- Limit daily connection requests and include *value-first* outreach.

## License
MIT
>>>>>>> 8903e15 (Initial commit: linkedin-agent)
