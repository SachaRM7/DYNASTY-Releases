"""Promote only archives pinned to a successful Windows run. Never rebuild."""
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path


def digest(file, algorithm="sha256"):
    with file.open("rb") as stream:
        return hashlib.file_digest(stream, algorithm).digest()


def prepare():
    plan = json.loads(Path("tested-release.json").read_text(encoding="utf-8"))
    version = plan["version"]
    assert re.fullmatch(r"\d+\.\d+\.\d+", version)
    assert plan["windowsTestsPassed"] is True and plan["signingKeyVerified"] is True
    assert plan["automaticUpdatePassed"] is True
    output = Path("downloads")
    output.mkdir(exist_ok=False)
    sums, metadata = [], None
    for kind in ("portable", "installer"):
        artifact = plan["artifacts"][kind]
        name = f"DYNASTY-{version}-Windows-x64.exe" if kind == "portable" else f"DYNASTY-Setup-{version}-x64.exe"
        archive = output / f"DYNASTY-{version}-{kind.capitalize()}-Windows-x64.zip"
        url = os.environ[f"DYNASTY_{kind.upper()}_URL"]
        parsed = urllib.parse.urlsplit(url)
        assert parsed.scheme == "https" and not parsed.username and not parsed.password
        assert (parsed.hostname or "").endswith(".oaiusercontent.com")
        with urllib.request.urlopen(url, timeout=120) as response, archive.open("wb") as target:
            count = 0
            while chunk := response.read(1024 * 1024):
                count += len(chunk)
                if count > 300_000_000:
                    raise ValueError("archive size limit")
                target.write(chunk)
        assert digest(archive).hex() == artifact["zipSHA256"]
        with zipfile.ZipFile(archive) as package:
            assert len(package.namelist()) == len(set(package.namelist()))
            assert set(package.namelist()) == {name, "LIRE-MOI.txt", "SHA256SUMS.txt", "update.json"}
            assert package.getinfo(name).file_size <= 300_000_000
            # Explicit names only: never extract arbitrary ZIP paths or source files.
            with package.open(name) as source, (output / name).open("wb") as target:
                shutil.copyfileobj(source, target)
            assert digest(output / name).hex() == artifact["exeSHA256"]
            assert package.getinfo("update.json").file_size < 65536
            signed = package.read("update.json")
            if metadata is not None:
                assert metadata == signed
            metadata = signed
            instructions = package.read("LIRE-MOI.txt")
            (output / f"LIRE-MOI-{kind}.txt").write_bytes(instructions)
        sums += [f"{digest(archive).hex()}  {archive.name}", f"{digest(output / name).hex()}  {name}"]
    (output / "update.json").write_bytes(metadata)
    envelope = json.loads(metadata)
    payload = base64.b64decode(envelope["payload"], validate=True)
    signature = base64.b64decode(envelope["signature"], validate=True)
    Path("payload.bin").write_bytes(payload)
    Path("signature.bin").write_bytes(signature)
    # The pinned PUBLIC key authenticates the exact payload. No publication secret here.
    subprocess.run(["openssl", "pkeyutl", "-verify", "-pubin", "-inkey", "update-public.pem",
                    "-sigfile", "signature.bin", "-rawin", "-in", "payload.bin"], check=True)
    release = json.loads(payload)
    assert release["version"] == version and release["schema"] == 1
    assert release["appId"] == "com.dynasty.prototype"
    assert release["platform"] == "win32" and release["arch"] == "x64" and release["channel"] == "windows-test"
    for kind, info in release["assets"].items():
        assert kind in ("portable", "installer") and Path(info["name"]).name == info["name"]
        file = output / info["name"]
        assert file.stat().st_size == info["size"]
        assert base64.b64encode(digest(file, "sha512")).decode() == info["sha512"]
    assert set(release["assets"]) == {"portable", "installer"}
    (output / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")
    (output / "verification.json").write_text(json.dumps({**plan, "rebuilt": False,
        "authenticodeSigned": False, "manifestSignature": "Ed25519"}, indent=2) + "\n", encoding="utf-8")
    print("Original Windows-tested archives and signed update metadata verified.")


if __name__ == "__main__":
    try:
        prepare()
    except Exception as error:
        # Do not include temporary signed staging URLs in public error messages.
        print(f"Publication preparation failed ({type(error).__name__}); nothing published", file=sys.stderr)
        sys.exit(1)
