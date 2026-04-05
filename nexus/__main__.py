"""Entry point. Checks for user and starts main script"""

# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

# ©️ DoNotWeb, 2024-2025
# This file is a part of Nexus Userbot
# 🌐 https://github.com/archfay/Nexus
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

import getpass
import os
import subprocess
import sys
import hashlib

from ._internal import restart


def get_file_hash(filename):
    hasher = hashlib.sha256()
    try:
        with open(filename, "rb") as f:
            hasher.update(f.read())
        return hasher.hexdigest()
    except FileNotFoundError:
        return None


def deps():
    env = os.environ.copy()
    env["PYO3_USE_ABI3_FORWARD_COMPATIBILITY"] = "1"
    
    # Определяем флаги для pip в зависимости от окружения
    pip_flags = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--upgrade",
        "-q",
        "--disable-pip-version-check",
        "--no-warn-script-location",
    ]
    
    # Добавляем --user если не в Docker, не root и не в virtualenv
    if (
        "DOCKER" not in os.environ
        and getpass.getuser() != "root"
        and not hasattr(sys, "real_prefix")
        and sys.base_prefix == sys.prefix
    ):
        pip_flags.append("--user")
    
    pip_flags.extend(["-r", "requirements.txt"])
    
    subprocess.run(pip_flags, check=True, env=env)
    
    with open(".requirements_hash", "w") as f:
        f.write(get_file_hash("requirements.txt"))


if (
    getpass.getuser() == "root"
    and "--root" not in " ".join(sys.argv)
    and all(trigger not in os.environ for trigger in {"DOCKER", "NO_SUDO"})
):
    print("\U0001f6ab" * 15)
    print("You attempted to run Nexus on behalf of root user")
    print("Please, create a new user and restart script")
    print("If this action was intentional, pass --root argument instead")
    print("\U0001f6ab" * 15)
    print()
    print("Type force_insecure to ignore this warning")
    print("Type no_sudo if your system has no sudo (Debian vibes)")
    inp = input("> ").lower()
    if inp != "force_insecure":
        sys.exit(1)
    elif inp == "no_sudo":
        os.environ["NO_SUDO"] = "1"
        print("Added NO_SUDO in your environment variables")
        restart()

if sys.version_info < (3, 9, 0):
    print("\U0001f6ab Error: you must use at least Python version 3.9.0")
elif __package__ != "nexus":
    print(
        "\U0001f6ab Error: you cannot run this as a script; you must execute as a package"
    )
else:
    try:
        import herokutl
    except Exception:
        pass
    else:
        try:
            import herokutl  # noqa: F811

            if tuple(map(int, herokutl.__version__.split("."))) < (1, 1, 0):
                raise ImportError
        except ImportError:
            print("\U0001f504 Installing dependencies...")
            deps()
            restart()

    try:
        from . import log

        log.init()
        from . import main
    except ImportError as e:
        print(
            f"{str(e)}\n\U0001f504 Attempting dependencies installation... Just wait ⏱"
        )
        deps()
        restart()

    if "NEXUS_DO_NOT_RESTART" in os.environ:
        del os.environ["NEXUS_DO_NOT_RESTART"]
    if "NEXUS_DO_NOT_RESTART2" in os.environ:
        del os.environ["NEXUS_DO_NOT_RESTART2"]

    prev_hash = None
    if os.path.exists(".requirements_hash"):
        with open(".requirements_hash", "r") as f:
            prev_hash = f.read().strip()

    if prev_hash != get_file_hash("requirements.txt"):
        print(
            "\U0001f504 Detected changes in requirements.txt, updating dependencies..."
        )
        deps()
        restart()

    main.nexus.main()
