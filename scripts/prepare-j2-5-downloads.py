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
        "zip": "DYNASTY-0.3.1-Portable-Windows-x64.zip",
        "zip_sha256": "32c07a5da224caf95049e135d8254368d33c6c0cdd05dd71d55852b124614604",
        "exe": "DYNASTY-0.3.1-Windows-x64.exe",
        "exe_sha256": "b0d771848decaa96abd926b5eb0200dea8784b02e81319bb753110cc9b61d013",
    },
    "installer": {
        "zip": "DYNASTY-0.3.1-Installer-Windows-x64.zip",
        "zip_sha256": "1fd2bccfdb3d3dbde6a3acd5dca7d0f7f885c8f586fbcc09f7f59f501e11f878",
        "exe": "DYNASTY-Setup-0.3.1-x64.exe",
        "exe_sha256": "d32916ba0b647eca59e9c4ad74767e0633fb9ed452512b47882a133d27f7c018",
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
        "version": "0.3.1", "gameBatch": "J2.5",
        "sourceCommit": "3edfa84b6138e69ce8a917eda264168a8d790793",
        "rebuilt": False, "windowsSigned": False, "automaticUpdatesEnabled": False,
        "artifacts": ARTIFACTS,
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    try:
        if sys.argv[1:] == ["--verify-local"]:
            with tempfile.TemporaryDirectory(prefix="dynasty-publish-check-") as temporary:
                prepare(Path(temporary) / "downloads", {
                    "portable": Path("/tmp/DYNASTY-j25-portable.zip"),
                    "installer": Path("/tmp/DYNASTY-j25-installer.zip"),
                })
        else:
            prepare(Path("downloads"))
    except Exception as error:
        # Do not echo presigned URLs in tracebacks or error text.
        print(f"Publication preparation failed ({type(error).__name__}); nothing published", file=sys.stderr)
        sys.exit(1)
