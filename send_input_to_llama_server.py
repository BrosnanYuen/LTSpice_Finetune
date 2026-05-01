#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.error
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Send full input.txt content as one prompt to a running llama-server and save output."
    )
    parser.add_argument("--input", default="./input.txt", help="Input file path")
    parser.add_argument("--output", default="./output.txt", help="Output file path")
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:8080/v1/chat/completions",
        help="llama-server chat completions endpoint",
    )
    parser.add_argument(
        "--model",
        default="Qwen3.6-27B-LTSpice-v64-Q4_K_S.gguf",
        help="Model name string for API payload",
    )
    parser.add_argument("--max-tokens", type=int, default=4000, help="Max output tokens")
    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            prompt = f.read()
    except OSError as exc:
        print(f"Failed to read input file {args.input}: {exc}", file=sys.stderr)
        return 1

    payload = {
        "model": args.model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": args.max_tokens,
        "stream": False,
    }

    req = urllib.request.Request(
        args.url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            response_json = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(f"Server returned HTTP {exc.code}: {body}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"Failed to connect to llama-server at {args.url}: {exc}", file=sys.stderr)
        return 1

    try:
        text = response_json["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        print("Unexpected response format:", file=sys.stderr)
        print(json.dumps(response_json, indent=2), file=sys.stderr)
        return 1

    print(text)

    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    except OSError as exc:
        print(f"Failed to write output file {args.output}: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
