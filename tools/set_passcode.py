#!/usr/bin/env python3
"""Update the passcode embedded in docs/assets/passcode.js.

Usage:
  python tools/set_passcode.py                    # interactive (recommended)
  python tools/set_passcode.py <new_passcode>     # CLI

Computes SHA-256 of the passcode and writes it into the EXPECTED_HASH constant.
Run `python tools/build_site.py` afterwards to rebuild the deploy artifacts.

SECURITY: This gate is JavaScript-only and the hash is visible in the page
source. Pick a passcode that resists brute force (15+ characters, mixed types).
For real access control, use Cloudflare Pages + Access or similar server-side
auth — see the README deployment section for details.
"""

from __future__ import annotations

import getpass
import hashlib
import re
import sys
from pathlib import Path

PASSCODE_JS = Path(__file__).resolve().parent.parent / "docs" / "assets" / "passcode.js"


def update_hash(passcode: str) -> None:
    if not passcode or len(passcode) < 6:
        print("ERROR: passcode must be at least 6 characters.", file=sys.stderr)
        sys.exit(1)
    new_hash = hashlib.sha256(passcode.encode()).hexdigest()
    text = PASSCODE_JS.read_text()
    pattern = r'const EXPECTED_HASH = "[0-9a-f]{64}";'
    if not re.search(pattern, text):
        print("ERROR: could not find EXPECTED_HASH constant in passcode.js", file=sys.stderr)
        sys.exit(1)
    new_text = re.sub(pattern, f'const EXPECTED_HASH = "{new_hash}";', text)
    PASSCODE_JS.write_text(new_text)
    print(f"✓ Updated passcode hash in {PASSCODE_JS.relative_to(PASSCODE_JS.parent.parent.parent)}")
    print(f"  Passcode length: {len(passcode)} characters")
    print(f"  SHA-256: {new_hash}")
    print()
    print("Next steps:")
    print("  1. Run `python tools/build_site.py` to rebuild docs/")
    print("  2. Test locally: `cd docs && python -m http.server 8000`")
    print("  3. Share the passcode with board members via a secure channel.")


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        update_hash(argv[1])
    else:
        print("Enter a new passcode (won't be echoed):")
        passcode = getpass.getpass("Passcode: ")
        confirm = getpass.getpass("Confirm:  ")
        if passcode != confirm:
            print("ERROR: passcodes do not match.", file=sys.stderr)
            return 1
        update_hash(passcode)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
