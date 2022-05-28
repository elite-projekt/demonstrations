#!/usr/bin/env python3

import requests

from argparse import ArgumentParser, RawTextHelpFormatter


def main():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("--host", dest="host", help="Host to use",
                        type=str, default="http://localhost:5000")
    parser.add_argument("demo", help="Name of the demo",
                        type=str)
    parser.add_argument("action", help="Action to take", type=str,
                        choices=["start", "stop"])

    args = parser.parse_args()

    session = requests.Session()
    session.trust_env = False

    url = f"{args.host}/orchestration/{args.action}/demo/{args.demo}"
    params = {"secureMode": "false"}

    req = session.get(url=url, json=params)

    print(f"Result: {req.status_code}")


if __name__ == "__main__":
    main()
