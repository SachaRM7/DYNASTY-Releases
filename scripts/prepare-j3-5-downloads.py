"""Promote only the exact J3.5 binaries already tested on Windows; no rebuild.

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
        "zip": "DYNASTY-0.4.1-Portable-Windows-x64.zip",
        "zip_sha256": "2202b9f963b15d7ae3b143c50e433db9185e9a0ab5e6ed45cd9a2caf28abd8be",
        "exe": "DYNASTY-0.4.1-Windows-x64.exe",
        "exe_sha256": "fd83e5c522618aad78242ecde12ae5dd4f9787bec2a01d0b3402a3d267676657"
    },
    "installer": {
        "zip": "DYNASTY-0.4.1-Installer-Windows-x64.zip",
        "zip_sha256": "a5b129e90b74a4fa99e228bd4378c67ba47f3a52a29f615e013e8c548d3a0cb2",
        "exe": "DYNASTY-Setup-0.4.1-x64.exe",
        "exe_sha256": "be0c95446cdb192070097327f9b64e0e5b4756261dc14fe4110e47b2314f6361"
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
        "version": "0.4.1", "gameBatch": "J3.5",
        "sourceCommit": "60e04a149dcfb4d6a431b8252b05cfd7680527d1",
        "rebuilt": False, "windowsSigned": False, "automaticUpdatesEnabled": False,
        "artifacts": ARTIFACTS,
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    try:
        if sys.argv[1:] == ["--verify-local"]:
            with tempfile.TemporaryDirectory(prefix="dynasty-publish-check-") as temporary:
                prepare(Path(temporary) / "downloads", {
                    "portable": Path("/tmp/dynasty-041-artifacts/DYNASTY-0.4.1-Portable-Windows-x64.zip"),
                    "installer": Path("/tmp/dynasty-041-artifacts/DYNASTY-0.4.1-Installer-Windows-x64.zip"),
                })
        else:
            prepare(Path("downloads"))
    except Exception as error:
        # Do not echo presigned URLs in tracebacks or error text.
        print(f"Publication preparation failed ({type(error).__name__}); nothing published", file=sys.stderr)
        sys.exit(1)
