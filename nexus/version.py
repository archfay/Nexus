"""Represents current userbot version"""

# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

# ©️ DoNotWeb, 2024-2025
# This file is a part of Nexus Userbot
# 🌐 https://github.com/DoNotWeb/Nexus
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

__version__ = (1, 0, 0)

import os

import git
from ._internal import restart

try:
    branch = git.Repo(
        path=os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    ).active_branch.name
except Exception:
    branch = "master"


async def check_branch(me_id: int, allowed_ids: list):
    if branch != "master" and me_id not in allowed_ids:
        repo = git.Repo(
            path=os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        )
        repo.git.reset("--hard", "HEAD")
        repo.git.checkout("master", force=True)
        restart()
