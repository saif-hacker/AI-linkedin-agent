import argparse
import json
from pathlib import Path
from services.utils.config import get_settings
from agents.collector import collect_profiles
from agents.analyzer import analyze_profiles
from agents.generator import generate_messages
from agents.outreach import dispatch_outreach

# Import the Selenium collector
from services.linkedin.collector_selenium import collect_from_selenium as collect_profiles_selenium


def path_or_none(p):
    return Path(p) if p else None


def main():
    parser = argparse.ArgumentParser(description="AI LinkedIn Competitor Monitor & Outreach Agent")
    sub = parser.add_subparsers(dest="cmd")

    # run
    run_p = sub.add_parser("run")
    run_p.add_argument(
        "--source", 
        choices=["csv", "phantombuster", "playwright", "selenium"], 
        default="csv"
    )
    run_p.add_argument("--no-send", action="store_true", help="Stop before outreach; write to outbox.jsonl")
    run_p.add_argument("--approve", action="store_true", help="Require human approval before sending")
    run_p.add_argument("--limit", type=int, default=25)

    # collect
    c_p = sub.add_parser("collect")
    c_p.add_argument(
        "--source", 
        choices=["csv", "phantombuster", "playwright", "selenium"], 
        default="csv"
    )
    c_p.add_argument("--limit", type=int, default=50)
    c_p.add_argument("--out", default="data/profiles.jsonl")

    # analyze
    a_p = sub.add_parser("analyze")
    a_p.add_argument("--inp", default="data/profiles.jsonl")
    a_p.add_argument("--out", default="data/enriched.jsonl")

    # generate
    g_p = sub.add_parser("generate")
    g_p.add_argument("--inp", default="data/enriched.jsonl")
    g_p.add_argument("--out", default="data/outbox.jsonl")
    g_p.add_argument("--model", choices=["template", "openai"], default="template")

    # outreach
    o_p = sub.add_parser("outreach")
    o_p.add_argument("--adapter", choices=["manual", "phantombuster", "playwright"], default="manual")
    o_p.add_argument("--batch", default="data/outbox.jsonl")

    args = parser.parse_args()
    settings = get_settings()

    if args.cmd == "collect":
        if args.source == "selenium":
            collect_profiles_selenium()
        else:
            collect_profiles(source=args.source, limit=args.limit, out_path=args.out)

    elif args.cmd == "analyze":
        analyze_profiles(inp=args.inp, out=args.out)

    elif args.cmd == "generate":
        generate_messages(inp=args.inp, out=args.out, model=args.model)

    elif args.cmd == "outreach":
        dispatch_outreach(adapter=args.adapter, batch=args.batch, require_approval=True)

    elif args.cmd == "run":
        profiles_path = "data/profiles.jsonl"
        enriched_path = "data/enriched.jsonl"
        outbox_path = "data/outbox.jsonl"

        # Collect profiles
        if args.source == "selenium":
            collect_profiles_selenium()
        else:
            collect_profiles(source=args.source, limit=args.limit, out_path=profiles_path)

        # Analyze & generate
        analyze_profiles(inp=profiles_path, out=enriched_path)
        generate_messages(inp=enriched_path, out=outbox_path, model="template")

        if args.no_send:
            print(f"[run] Skipping outreach; messages queued in {outbox_path}")
            return

        dispatch_outreach(adapter="manual", batch=outbox_path, require_approval=args.approve)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
