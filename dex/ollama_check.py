"""Single reachability test against the local Ollama server — no model/generation call."""

import sys
import urllib.request

OLLAMA_URL = "http://127.0.0.1:11434/"


def main():
    try:
        with urllib.request.urlopen(OLLAMA_URL, timeout=5) as resp:
            body = resp.read().decode()
    except Exception as exc:
        print(f"Ollama unreachable at {OLLAMA_URL}: {exc}")
        sys.exit(1)

    print(f"Ollama reachable at {OLLAMA_URL}: {body.strip()!r}")


if __name__ == "__main__":
    main()
