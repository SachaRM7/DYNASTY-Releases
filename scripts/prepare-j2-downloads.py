"""Promote only the exact J2 binaries already tested on Windows; no rebuild.

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
        "zip": "DYNASTY-0.3.0-Portable-Windows-x64.zip",
        "zip_sha256": "e63f683730c62b05b3fb6e2615f63a2eab622da3d572461f14034b507fdae315",
        "exe": "DYNASTY-0.3.0-Windows-x64.exe",
        "exe_sha256": "d2546f457247e8f067f7c310dba76cea200f8ef58581bf8d75b4f26e7123e743",
    },
    "installer": {
        "zip": "DYNASTY-0.3.0-Installer-Windows-x64.zip",
        "zip_sha256": "eb6bb6e073cdd29911a03382f46b7d3a8b5761c867e2fff48820035bebd68352",
        "exe": "DYNASTY-Setup-0.3.0-x64.exe",
        "exe_sha256": "4b1a8114a4fcbc4f0c8f5868025787b6290f86323be87ac0946da3da710b176b",
    },
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
                raise ValueError("Archive exceeds the known J2 size limit")
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
        "version": "0.3.0", "gameBatch": "J2",
        "sourceCommit": "aa55d94e77ddf5f57179f21ffb4e222b60afe1cb",
        "rebuilt": False, "windowsSigned": False, "automaticUpdatesEnabled": False,
        "artifacts": ARTIFACTS,
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    try:
        if sys.argv[1:] == ["--verify-local"]:
            with tempfile.TemporaryDirectory(prefix="dynasty-publish-check-") as temporary:
                prepare(Path(temporary) / "downloads", {
                    "portable": Path("/tmp/DYNASTY-portable.zip"),
                    "installer": Path("/tmp/DYNASTY-installer.zip"),
                })
        else:
            prepare(Path("downloads"))
    except Exception as error:
        # Do not echo presigned URLs in tracebacks or error text.
        print(f"Publication preparation failed ({type(error).__name__}); nothing published", file=sys.stderr)
        sys.exit(1)
