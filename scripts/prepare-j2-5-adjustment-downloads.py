"""Promote only the exact J2.5 binaries already tested on Windows; no rebuild.

Temporary URLs grant access only to these intended public distribution archives.
They are supplied at dispatch time, never committed or included in a client.
The expected archive AND executable hashes are pinned to the Windows test run.
"""

import hashlib
import json
import os
import shutil
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path


ARTIFACTS = {
    "portable": {
        "zip": "DYNASTY-0.3.2-Portable-Windows-x64.zip",
        "zip_sha256": "7e6a7f92a463b099dc12c53c5f2277cdb56da120286268752b8119af6f498f5f",
        "exe": "DYNASTY-0.3.2-Windows-x64.exe",
        "exe_sha256": "afed204c08fc6d9a9279ff6e3fe09bface94689fa86175e01077c1cf6552c02e"
    },
    "installer": {
        "zip": "DYNASTY-0.3.2-Installer-Windows-x64.zip",
        "zip_sha256": "b490a26379e8c5da64dc71a9e621ae9c58a0dce70d51500d5cf22a5bd284ca37",
        "exe": "DYNASTY-Setup-0.3.2-x64.exe",
        "exe_sha256": "e85a140703a9617fd7ae90bb084ebe445156a78fbd24cffe9146efd1b89795f8"
    }
}


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def download(url, target):
    parsed = urllib.parse.urlsplit(url)
    if (parsed.scheme != "https" or parsed.username or parsed.password
            or not (parsed.hostname or "").endswith(".oaiusercontent.com")):
        raise ValueError("Expected the temporary HTTPS distribution staging URL")
    with urllib.request.urlopen(url, timeout=120) as response, target.open("wb") as output:
        total = 0
        while chunk := response.read(1024 * 1024):
            total += len(chunk)
            if total > 130_000_000:
                raise ValueError("Archive exceeds the known test archive size limit")
            output.write(chunk)


def prepare(output, local_archives=None):
    output.mkdir(parents=True, exist_ok=False)
    sums = []
    for kind, artifact in ARTIFACTS.items():
        archive = output / artifact["zip"]
        if local_archives:
            shutil.copyfile(local_archives[kind], archive)
        else:
            download(os.environ[f"DYNASTY_{kind.upper()}_URL"], archive)
        if digest(archive) != artifact["zip_sha256"]:
            raise ValueError(f"{kind}: archive SHA-256 does not match the tested file")
        with zipfile.ZipFile(archive) as package:
            # No generic extractall: only the explicitly allowed executable is written.
            with package.open(artifact["exe"]) as source, (output / artifact["exe"]).open("wb") as destination:
                shutil.copyfileobj(source, destination)
        if digest(output / artifact["exe"]) != artifact["exe_sha256"]:
            raise ValueError(f"{kind}: executable SHA-256 does not match the tested file")
        sums.extend([
            f'{artifact["zip_sha256"]}  {artifact["zip"]}',
            f'{artifact["exe_sha256"]}  {artifact["exe"]}',
        ])
        print(f"Verified original Windows-tested {kind}: {artifact['exe_sha256']}")
    (output / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")
    (output / "LIRE-MOI.txt").write_text(Path("README.md").read_text(encoding="utf-8"), encoding="utf-8")
    (output / "verification.json").write_text(json.dumps({
        "version": "0.3.2", "gameBatch": "J2.5",
        "sourceCommit": "5d5ef29e8ef1ac0157c1dd03036e0529839ee366",
        "rebuilt": False, "windowsSigned": False, "automaticUpdatesEnabled": False,
        "artifacts": ARTIFACTS,
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    try:
        if sys.argv[1:] == ["--verify-local"]:
            with tempfile.TemporaryDirectory(prefix="dynasty-publish-check-") as temporary:
                prepare(Path(temporary) / "downloads", {
                    "portable": Path("/tmp/dynasty-032-artifacts/DYNASTY-0.3.2-Portable-Windows-x64.zip"),
                    "installer": Path("/tmp/dynasty-032-artifacts/DYNASTY-0.3.2-Installer-Windows-x64.zip"),
                })
        else:
            prepare(Path("downloads"))
    except Exception as error:
        # Do not echo presigned URLs in tracebacks or error text.
        print(f"Publication preparation failed ({type(error).__name__}); nothing published", file=sys.stderr)
        sys.exit(1)
