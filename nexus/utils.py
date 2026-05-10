"""Utilities"""

#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2021 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

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

import asyncio
import atexit as _atexit
import contextlib
import functools
import inspect
import io
import json
import logging
import os
import random
import re
import shlex
import signal
import string
import time
import typing
import socket
import shutil
from datetime import timedelta
from urllib.parse import urlparse
import emoji

try:
    import orjson
    # use orjson for faster JSON operations
    def _json_dumps(obj, **kwargs):
        return orjson.dumps(obj, option=orjson.OPT_SORT_KEYS).decode('utf-8')
    def _json_loads(s):
        if isinstance(s, str):
            s = s.encode('utf-8')
        return orjson.loads(s)
except ImportError:
    # fallback to standard json
    _json_dumps = json.dumps
    _json_loads = json.loads

# Public aliases for other modules to use centralized json handling
json_dumps = _json_dumps
json_loads = _json_loads

import git
import grapheme
import herokutl
import herokutl.extensions
import herokutl.extensions.html
import requests
from aiogram.types import Message as AiogramMessage
from herokutl import hints
from herokutl.tl.custom.message import Message
from herokutl.tl.functions.account import UpdateNotifySettingsRequest
from herokutl.tl.functions.channels import (
    CreateChannelRequest,
    EditAdminRequest,
    EditPhotoRequest,
    InviteToChannelRequest,
)
from herokutl.tl.functions.messages import (
    GetDialogFiltersRequest,
    SetHistoryTTLRequest,
    UpdateDialogFilterRequest,
)
from herokutl.tl.types import (
    Channel,
    Chat,
    ChatAdminRights,
    InputDocument,
    InputPeerNotifySettings,
    MessageEntityBankCard,
    MessageEntityBlockquote,
    MessageEntityBold,
    MessageEntityBotCommand,
    MessageEntityCashtag,
    MessageEntityCode,
    MessageEntityEmail,
    MessageEntityHashtag,
    MessageEntityItalic,
    MessageEntityMention,
    MessageEntityMentionName,
    MessageEntityPhone,
    MessageEntityPre,
    MessageEntitySpoiler,
    MessageEntityStrike,
    MessageEntityTextUrl,
    MessageEntityUnderline,
    MessageEntityUnknown,
    MessageEntityUrl,
    MessageMediaPhoto,
    MessageMediaDocument,
    MessageMediaWebPage,
    PeerChannel,
    PeerChat,
    PeerUser,
    UpdateNewChannelMessage,
    User,
)

from ._internal import fw_protect
from .inline.types import BotInlineCall, InlineCall, InlineMessage
from .tl_cache import CustomTelegramClient
from .types import nexusReplyMarkup, ListLike, Module

FormattingEntity = typing.Union[
    MessageEntityUnknown,
    MessageEntityMention,
    MessageEntityHashtag,
    MessageEntityBotCommand,
    MessageEntityUrl,
    MessageEntityEmail,
    MessageEntityBold,
    MessageEntityItalic,
    MessageEntityCode,
    MessageEntityPre,
    MessageEntityTextUrl,
    MessageEntityMentionName,
    MessageEntityPhone,
    MessageEntityCashtag,
    MessageEntityUnderline,
    MessageEntityStrike,
    MessageEntityBlockquote,
    MessageEntityBankCard,
    MessageEntitySpoiler,
]

emoji_pattern = re.compile(
    "["
    "\U0001f600-\U0001f64f"  # emoticons
    "\U0001f300-\U0001f5ff"  # symbols & pictographs
    "\U0001f680-\U0001f6ff"  # transport & map symbols
    "\U0001f1e0-\U0001f1ff"  # flags (iOS)
    "]+",
    flags=re.UNICODE,
)

parser = herokutl.utils.sanitize_parse_mode("html")
logger = logging.getLogger(__name__)


def get_args(message: typing.Union[Message, str]) -> typing.Union[typing.List[str], bool, str]:
    """
    Get arguments from message
    :param message: Message or string to get arguments from
    :return: List of arguments
    """
    if not (message := getattr(message, "message", message)):
        return False

    if len(message := message.split(maxsplit=1)) <= 1:
        return []

    message = message[1]

    try:
        split = shlex.split(message)
    except ValueError:
        return message  # Cannot split, let's assume that it's just one long message

    return list(filter(lambda x: len(x) > 0, split))


def get_args_raw(message: typing.Union[Message, str]) -> typing.Union[str, bool]:
    """
    Get the parameters to the command as a raw string (not split)
    :param message: Message or string to get arguments from
    :return: Raw string of arguments
    """
    if not (message := getattr(message, "message", message)):
        return False

    return args[1] if len(args := message.split(maxsplit=1)) > 1 else ""


def get_args_html(message: Message) -> str:
    """
    Get the parameters to the command as string with HTML (not split)
    :param message: Message to get arguments from
    :return: String with HTML arguments
    """
    prefix = message.client.loader.get_prefix()

    if not (message := message.text):
        return False

    if prefix not in message:
        return message

    raw_text, entities = parser.parse(message)

    raw_text = parser._add_surrogate(raw_text)

    try:
        command = raw_text[
            raw_text.index(prefix) : raw_text.index(" ", raw_text.index(prefix) + 1)
        ]
    except ValueError:
        return ""

    command_len = len(command) + 1

    return parser.unparse(
        parser._del_surrogate(raw_text[command_len:]),
        relocate_entities(entities, -command_len, raw_text[command_len:]),
    )


def get_args_split_by(
    message: typing.Union[Message, str],
    separator: str,
) -> typing.List[str]:
    """
    Split args with a specific separator
    :param message: Message or string to get arguments from
    :param separator: Separator to split by
    :return: List of arguments
    """
    return [
        section.strip() for section in get_args_raw(message).split(separator) if section
    ]


def safe_int(value, default=0):
    """Try to convert value to int, return default on failure."""
    try:
        return int(value)
    except Exception:
        try:
            if isinstance(value, str) and value.isdigit():
                return int(value)
        except Exception:
            pass
    return default


def safe_color(value, default="#000"):
    """Return a valid hex color string starting with '#', else default."""
    try:
        if isinstance(value, str) and value.startswith("#") and 3 <= len(value) <= 7:
            return value
    except Exception:
        pass
    return default


def safe_coords(coord_str, w=0, h=0):
    """Parse coords like '100|100' to (int, int). If '0|0' or invalid, return center (w/2,h/2)."""
    try:
        if coord_str == "0|0":
            return (int(w / 2), int(h / 2))
        parts = coord_str.split("|")
        if len(parts) == 2:
            x = safe_int(parts[0], None)
            y = safe_int(parts[1], None)
            if x is None or y is None:
                return (int(w / 2), int(h / 2))
            return (x, y)
    except Exception:
        pass
    return (int(w / 2), int(h / 2))


def get_chat_id(message: typing.Union[Message, AiogramMessage]) -> int:
    """
    Get the chat ID, but without -100 if its a channel
    :param message: Message to get chat ID from
    :return: Chat ID
    """
    return herokutl.utils.resolve_id(
        getattr(message, "chat_id", None)
        or getattr(getattr(message, "chat", None), "id", None)
    )[0]


def get_entity_id(entity: hints.Entity) -> int:
    """
    Get entity ID
    :param entity: Entity to get ID from
    :return: Entity ID
    """
    return herokutl.utils.get_peer_id(entity)


def escape_html(text: str, /) -> str:  # sourcery skip
    """
    Pass all untrusted/potentially corrupt input here
    :param text: Text to escape
    :return: Escaped text
    """
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def escape_quotes(text: str, /) -> str:
    """
    Escape quotes to html quotes
    :param text: Text to escape

    :return: Escaped text
    """
    return escape_html(text).replace('"', "&quot;")


def get_base_dir() -> str:
    """
    Get directory of this file
    :return: Directory of this file
    """
    return get_dir(__file__)


def get_dir(mod: str) -> str:
    """
    Get directory of given module
    :param mod: Module's `__file__` to get directory of
    :return: Directory of given module
    """
    return os.path.abspath(os.path.dirname(os.path.abspath(mod)))


async def get_user(message: Message) -> typing.Optional[User]:
    """
    Get user who sent message, searching if not found easily
    :param message: Message to get user from
    :return: User who sent message
    """
    try:
        return await message.get_sender()
    except ValueError:  # Not in database. Lets go looking for them.
        logger.debug("User not in session cache. Searching...")

    if isinstance(message.peer_id, PeerUser):
        await message.client.get_dialogs()
        return await message.get_sender()

    if isinstance(message.peer_id, (PeerChannel, PeerChat)):
        async for user in message.client.iter_participants(
            message.peer_id,
            aggressive=True,
        ):
            if user.id == message.sender_id:
                return user

        logger.error("User isn't in the group where they sent the message")
        return None

async def safe_edit_message(
    client: CustomTelegramClient, chat_id: int, message_id: int, text: str
) -> bool:
    """Try to edit a message; on failure send a new message and remove old one when possible."""
    try:
        await client.edit_message(chat_id, message_id, text)
        return True
    except Exception:
        logger.debug("edit_message failed for %s:%s, attempting fallback", chat_id, message_id, exc_info=True)
        try:
            await client.send_message(chat_id, text)
            with contextlib.suppress(Exception):
                await client.delete_messages(chat_id, message_id)
            return True
        except Exception:
            logger.exception("safe_edit_message fallback failed for %s:%s", chat_id, message_id)
            return False


def run_sync(func, *args, **kwargs):
    """
    Run a non-async function in a new thread and return an awaitable
    :param func: Sync-only function to execute
    :return: Awaitable coroutine
    """
    return asyncio.get_event_loop().run_in_executor(
        None,
        functools.partial(func, *args, **kwargs),
    )


def run_async(loop: asyncio.AbstractEventLoop, coro: typing.Awaitable) -> typing.Any:
    """
    Run an async function as a non-async function, blocking till it's done
    :param loop: Event loop to run the coroutine in
    :param coro: Coroutine to run
    :return: Result of the coroutine
    """
    return asyncio.run_coroutine_threadsafe(coro, loop).result()


def censor(
    obj: typing.Any,
    to_censor: typing.Optional[typing.Iterable[str]] = None,
    replace_with: str = "redacted_{count}_chars",
):
    """
    May modify the original object, but don't rely on it
    :param obj: Object to censor, preferrably telethon
    :param to_censor: Iterable of strings to censor
    :param replace_with: String to replace with, {count} will be replaced with the number of characters
    :return: Censored object
    """
    if to_censor is None:
        to_censor = ["phone"]

    for k, v in vars(obj).items():
        if k in to_censor:
            setattr(obj, k, replace_with.format(count=len(v)))
        elif k[0] != "_" and hasattr(v, "__dict__"):
            setattr(obj, k, censor(v, to_censor, replace_with))

    return obj


def relocate_entities(
    entities: typing.List[FormattingEntity],
    offset: int,
    text: typing.Optional[str] = None,
) -> typing.List[FormattingEntity]:
    """
    Move all entities by offset (truncating at text)
    :param entities: List of entities
    :param offset: Offset to move by
    :param text: Text to truncate at
    :return: List of entities
    """
    length = len(text) if text is not None else 0

    for ent in entities.copy() if entities else ():
        ent.offset += offset
        if ent.offset < 0:
            ent.length += ent.offset
            ent.offset = 0
        if text is not None and ent.offset + ent.length > length:
            ent.length = length - ent.offset
        if ent.length <= 0:
            entities.remove(ent)

    return entities


async def answer_file(
    message: typing.Union[Message, InlineCall, InlineMessage],
    file: typing.Union[str, bytes, io.IOBase, InputDocument],
    caption: typing.Optional[str] = None,
    **kwargs,
):
    """
    Use this to answer a message with a document
    :param message: Message to answer
    :param file: File to send - url, path or bytes
    :param caption: Caption to send
    :param kwargs: Extra kwargs to pass to `send_file`
    :return: Sent message

    :example:
        >>> await utils.answer_file(message, "test.txt")
        >>> await utils.answer_file(
            message,
            "https://mods.hikariatama.ru/badges/artai.jpg",
            "This is the cool module, check it out!",
        )
    """
    if isinstance(message, (InlineCall, InlineMessage)):
        message = message.form["caller"]

    if topic := get_topic(message):
        kwargs.setdefault("reply_to", topic)

    try:
        response = await message.client.send_file(
            message.peer_id,
            file,
            caption=caption,
            **kwargs,
        )
    except Exception:
        if caption:
            logger.warning(
                "Failed to send file, sending plain text instead", exc_info=True
            )
            return await answer(message, caption, **kwargs)

        raise

    with contextlib.suppress(Exception):
        await message.delete()

    return response


async def answer(
    message: typing.Union[Message, InlineCall, InlineMessage],
    response: str,
    *,
    reply_markup: typing.Optional[nexusReplyMarkup] = None,
    **kwargs,
) -> typing.Union[InlineCall, InlineMessage, Message]:
    """
    Use this to give the response to a command
    :param message: Message to answer to. Can be a tl message or nexus inline object
    :param response: Response to send
    :param reply_markup: Reply markup to send. If specified, inline form will be used
    :return: Message or inline object

    :example:
        >>> await utils.answer(message, "Hello world!")
        >>> await utils.answer(
            message,
            "https://some-url.com/photo.jpg",
            caption="Hello, this is your photo!",
            asfile=True,
        )
        >>> await utils.answer(
            message,
            "Hello world!",
            reply_markup={"text": "Hello!", "data": "world"},
            silent=True,
            disable_security=True,
        )
    """
    # Compatibility with FTG\GeekTG

    if isinstance(message, list) and message:
        message = message[0]

    if reply_markup is not None:
        if not isinstance(reply_markup, (list, dict)):
            raise ValueError("reply_markup must be a list or dict")

        if reply_markup:
            kwargs.pop("message", None)
            if isinstance(message, (InlineMessage, InlineCall, BotInlineCall)):
                await message.edit(response, reply_markup, **kwargs)
                return

            reply_markup = message.client.loader.inline._normalize_markup(reply_markup)
            result = await message.client.loader.inline.form(
                response,
                message=message if message.out else get_chat_id(message),
                reply_markup=reply_markup,
                **kwargs,
            )
            return result

    if isinstance(message, (InlineMessage, InlineCall, BotInlineCall)):
        await message.edit(response)
        return message

    kwargs.setdefault("link_preview", False)

    if not (edit := (message.out and not message.via_bot_id and not message.fwd_from)):
        kwargs.setdefault(
            "reply_to",
            getattr(message, "reply_to_msg_id", None),
        )
    elif "reply_to" in kwargs:
        kwargs.pop("reply_to")

    parse_mode = herokutl.utils.sanitize_parse_mode(
        kwargs.pop(
            "parse_mode",
            message.client.parse_mode,
        )
    )

    if isinstance(response, str) and not kwargs.pop("asfile", False):
        text, entities = parse_mode.parse(response)

        if len(text) >= 4096 and not hasattr(message, "nexus_grepped"):
            try:
                if not message.client.loader.inline.init_complete:
                    raise

                strings = list(smart_split(text, entities, 4096))

                if len(strings) > 10:
                    raise

                list_ = await message.client.loader.inline.list(
                    message=message,
                    strings=strings,
                )

                if not list_:
                    raise

                return list_
            except Exception:
                file = io.BytesIO(text.encode("utf-8"))
                file.name = "command_result.txt"

                result = await message.client.send_file(
                    message.peer_id,
                    file,
                    caption=message.client.loader.lookup("translations").strings(
                        "too_long"
                    ),
                    reply_to=kwargs.get("reply_to") or get_topic(message),
                )

                if message.out:
                    await message.delete()

                return result

        result = await (message.edit if edit else message.respond)(
            text,
            parse_mode=lambda t: (t, entities),
            **kwargs,
        )
    elif isinstance(response, Message):
        if message.media is None and (
            response.media is None
            or isinstance(
                response.media,
                (MessageMediaWebPage, MessageMediaPhoto, MessageMediaDocument),
            )
        ):
            result = await message.edit(
                response.message,
                file=response.media,
                parse_mode=lambda t: (t, response.entities or []),
                link_preview=isinstance(response.media, MessageMediaWebPage),
            )
        else:
            result = await message.respond(response, **kwargs)
    else:
        if isinstance(response, bytes):
            response = io.BytesIO(response)
        elif isinstance(response, str):
            response = io.BytesIO(response.encode("utf-8"))

        if name := kwargs.pop("filename", None):
            response.name = name

        if message.media is not None and edit:
            await message.edit(file=response, **kwargs)
        else:
            kwargs.setdefault(
                "reply_to",
                getattr(message, "reply_to_msg_id", get_topic(message)),
            )
            result = await message.client.send_file(message.peer_id, response, **kwargs)
            if message.out:
                await message.delete()

    return result


async def get_target(message: Message, arg_no: int = 0) -> typing.Optional[int]:
    """
    Get target from message
    :param message: Message to get target from
    :param arg_no: Argument number to get target from
    :return: Target
    """

    if any(
        isinstance(entity, MessageEntityMentionName)
        for entity in message.entities or []
    ):
        e = sorted(
            filter(lambda x: isinstance(x, MessageEntityMentionName), message.entities),
            key=lambda x: x.offset,
        )[0]
        return e.user_id

    if len(get_args(message)) > arg_no:
        user = get_args(message)[arg_no]
    elif message.is_reply:
        return (await message.get_reply_message()).sender_id
    elif hasattr(message.peer_id, "user_id"):
        user = message.peer_id.user_id
    else:
        return None

    try:
        entity = await message.client.get_entity(user)
    except ValueError:
        return None
    else:
        if isinstance(entity, User):
            return entity.id


def merge(a: dict, b: dict, /) -> dict:
    """
    Merge with replace dictionary a to dictionary b
    :param a: Dictionary to merge
    :param b: Dictionary to merge to
    :return: Merged dictionary
    """
    for key in a:
        if key in b:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                b[key] = merge(a[key], b[key])
            elif isinstance(a[key], list) and isinstance(b[key], list):
                b[key] = list(set(b[key] + a[key]))
            else:
                b[key] = a[key]
        else:
            b[key] = a[key]

    return b


async def set_avatar(
    client: CustomTelegramClient,
    peer: hints.Entity,
    avatar: str,
) -> bool:
    """
    Sets an entity avatar
    :param client: Client to use
    :param peer: Peer to set avatar to
    :param avatar: Avatar to set
    :return: True if avatar was set, False otherwise
    """
    if isinstance(avatar, str) and check_url(avatar):
        f = (
            await run_sync(
                requests.get,
                avatar,
            )
        ).content
    elif isinstance(avatar, bytes):
        f = avatar
    else:
        return False

    await fw_protect()
    res = await client(
        EditPhotoRequest(
            channel=peer,
            photo=await client.upload_file(f, file_name="photo.png"),
        )
    )

    await fw_protect()

    try:
        await client.delete_messages(
            peer,
            message_ids=[
                next(
                    update
                    for update in res.updates
                    if isinstance(update, UpdateNewChannelMessage)
                ).message.id
            ],
        )
    except Exception:
        pass

    return True


async def invite_inline_bot(
    client: CustomTelegramClient,
    peer: hints.EntityLike,
) -> None:
    """
    Invites inline bot to a chat
    :param client: Client to use
    :param peer: Peer to invite bot to
    :return: None
    :raise RuntimeError: If error occurred while inviting bot
    """

    try:
        await client(InviteToChannelRequest(peer, [client.loader.inline.bot_username]))
    except Exception as e:
        raise RuntimeError(
            "Can't invite inline bot to old asset chat, which is required by module"
        ) from e

    with contextlib.suppress(Exception):
        await client(
            EditAdminRequest(
                channel=peer,
                user_id=client.loader.inline.bot_username,
                admin_rights=ChatAdminRights(ban_users=True),
                rank="Nexus",
            )
        )


async def asset_channel(
    client: CustomTelegramClient,
    title: str,
    description: str,
    *,
    channel: bool = False,
    silent: bool = False,
    archive: bool = False,
    invite_bot: bool = False,
    avatar: typing.Optional[str] = None,
    ttl: typing.Optional[int] = None,
    forum: bool = False,
    _folder: typing.Optional[str] = None,
) -> typing.Tuple[Channel, bool]:
    """
    Create new channel (if needed) and return its entity
    :param client: Telegram client to create channel by
    :param title: Channel title
    :param description: Description
    :param channel: Whether to create a channel or supergroup
    :param silent: Automatically mute channel
    :param archive: Automatically archive channel
    :param invite_bot: Add inline bot and assure it's in chat
    :param avatar: Url to an avatar to set as pfp of created peer
    :param ttl: Time to live for messages in channel
    :param forum: Whether to create a forum channel
    :return: Peer and bool: is channel new or pre-existent
    """
    if not hasattr(client, "_channels_cache"):
        client._channels_cache = {}

    if (
        title in client._channels_cache
        and client._channels_cache[title]["exp"] > time.time()
    ):
        return client._channels_cache[title]["peer"], False

    # legacy nexus / hikka chats conversion to nexus
    if title.startswith("hikka-"):
        title = title.replace("hikka-", "nexus-")

    async for d in client.iter_dialogs():
        if d.title == title:
            client._channels_cache[title] = {"peer": d.entity, "exp": int(time.time())}
            if invite_bot:
                if all(
                    participant.id != client.loader.inline.bot_id
                    for participant in await client.get_participants(
                        d.entity, limit=100
                    )
                ):
                    await fw_protect()
                    await invite_inline_bot(client, d.entity)

            return d.entity, False

    await fw_protect()

    peer = (
        await client(
            CreateChannelRequest(
                title,
                description,
                megagroup=not channel,
                forum=forum,
            )
        )
    ).chats[0]

    if invite_bot:
        await fw_protect()
        await invite_inline_bot(client, peer)

    if silent:
        await fw_protect()
        await dnd(client, peer, archive)
    elif archive:
        await fw_protect()
        await client.edit_folder(peer, 1)

    if avatar:
        await fw_protect()
        try:
            await set_avatar(client, peer, avatar)
        except Exception:
            logger.debug("Failed to set avatar for asset channel", exc_info=True)

    if ttl:
        await fw_protect()
        await client(SetHistoryTTLRequest(peer=peer, period=ttl))

    if _folder:
        if _folder != "nexus":
            raise NotImplementedError

        folders = await client(GetDialogFiltersRequest())

        try:
            folder = next(folder for folder in folders if folder.title == "nexus")
        except Exception:
            folder = None

        if folder is not None and not any(
            peer.id == getattr(folder_peer, "channel_id", None)
            for folder_peer in folder.include_peers
        ):
            folder.include_peers += [await client.get_input_entity(peer)]

            await client(
                UpdateDialogFilterRequest(
                    folder.id,
                    folder,
                )
            )

    client._channels_cache[title] = {"peer": peer, "exp": int(time.time())}
    return peer, True


async def asset_forum_topic(
    client: "CustomTelegramClient",
    channel: hints.EntityLike,
    title: str,
    *,
    icon_color: typing.Optional[int] = None,
    icon_emoji_id: typing.Optional[int] = None,
) -> typing.Any:
    """
    Create a forum topic in a channel (if it doesn't exist) and return it.
    :param client: Telegram client
    :param channel: Channel/supergroup entity
    :param title: Topic title
    :param icon_color: Optional icon color
    :param icon_emoji_id: Optional icon emoji id
    :return: Forum topic object
    """
    from herokutl.tl.functions.channels import GetForumTopicsRequest
    from herokutl.tl.functions.channels import CreateForumTopicRequest

    try:
        result = await client(
            GetForumTopicsRequest(
                channel=channel,
                q=title,
                offset_date=0,
                offset_id=0,
                offset_topic=0,
                limit=100,
            )
        )
        for topic in result.topics:
            if getattr(topic, "title", None) == title:
                return topic
    except Exception:
        logger.debug("Failed to get forum topics", exc_info=True)

    try:
        kwargs = {"channel": channel, "title": title, "random_id": int(time.time())}
        if icon_color is not None:
            kwargs["icon_color"] = icon_color
        if icon_emoji_id is not None:
            kwargs["icon_emoji_id"] = icon_emoji_id
        result = await client(CreateForumTopicRequest(**kwargs))
        for update in result.updates:
            if hasattr(update, "id"):
                return update
        return result
    except Exception:
        logger.debug("Failed to create forum topic", exc_info=True)
        return None


async def dnd(
    client: CustomTelegramClient,
    peer: hints.Entity,
    archive: bool = True,
) -> bool:
    """
    Mutes and optionally archives peer
    :param peer: Anything entity-link
    :param archive: Archive peer, or just mute?
    :return: `True` on success, otherwise `False`
    """
    try:
        await client(
            UpdateNotifySettingsRequest(
                peer=peer,
                settings=InputPeerNotifySettings(
                    show_previews=False,
                    silent=True,
                    mute_until=2**31 - 1,
                ),
            )
        )

        if archive:
            await fw_protect()
            await client.edit_folder(peer, 1)
    except Exception:
        logger.exception("utils.dnd error")
        return False

    return True


def get_link(user: typing.Union[User, Channel], /) -> str:
    """
    Get telegram permalink to entity
    :param user: User or channel
    :return: Link to entity
    """
    return (
        f"tg://user?id={user.id}"
        if isinstance(user, User)
        else (
            f"tg://resolve?domain={user.username}"
            if getattr(user, "username", None)
            else ""
        )
    )


def chunks(_list: ListLike, n: int, /) -> typing.List[typing.List[typing.Any]]:
    """
    Split provided `_list` into chunks of `n`
    :param _list: List to split
    :param n: Chunk size
    :return: List of chunks
    """
    return [_list[i : i + n] for i in range(0, len(_list), n)]


def get_named_platform() -> str:
    """
    Returns formatted platform name
    :return: Platform name
    """
    from . import main

    with contextlib.suppress(Exception):
        if os.path.isfile("/proc/device-tree/model"):
            with open("/proc/device-tree/model") as f:
                model = f.read()
                if "Orange" in model:
                    return f"🍊 {model}"

                return f"🍇 {model}" if "Raspberry" in model else f"❓ {model}"

    if main.IS_WSL:
        return "🍀 WSL"

    if main.IS_WINDOWS:
        return "💻 Windows"

    if main.IS_MACOS:
        return "🍏 MacOS"

    if main.IS_JAMHOST:
        return "🧃 JamHost"

    if main.IS_USERLAND:
        return "🐧 UserLand"

    if main.IS_HIKKAHOST:
        return "🌼 HikkaHost"

    if main.IS_DOCKER:
        return "🐳 Docker"

    return f"✌️ lavHost {os.environ['LAVHOST']}" if main.IS_LAVHOST else "💎 VDS"


def get_platform_emoji() -> str:
    """
    Returns custom emoji for current platform
    :return: Emoji entity in string
    """
    from . import main

    BASE = "".join(
        (
            "<emoji document_id={}>🌐</emoji>",
            "<emoji document_id=5273920871109533513>🌐</emoji>",
            "<emoji document_id=5271520091765250082>🌐</emoji>",
            "<emoji document_id=5273962764220535903>🌐</emoji>",
        )
    )

    if main.IS_HIKKAHOST:
        return BASE.format(5271757856859788351)

    if main.IS_JAMHOST:
        return BASE.format(5271757856859788351)

    if main.IS_USERLAND:
        return BASE.format(5271757856859788351)

    if main.IS_LAVHOST:
        return BASE.format(5271757856859788351)

    if main.IS_DOCKER:
        return BASE.format(5271757856859788351)

    return BASE.format(5271757856859788351)


def get_platform_named_emoji() -> str:
    """Return platform emoji followed by named platform string."""
    try:
        return f"{get_platform_emoji()} {get_named_platform()}"
    except Exception:
        return get_platform_emoji()


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable form."""
    try:
        if size_bytes < 0:
            return "0 B"
        for unit in ["B", "KB", "MB", "GB", "TB", "PB"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
    except Exception:
        return "0 B"


def is_url(value: str) -> bool:
    try:
        result = urlparse(value)
        return all([result.scheme in ("http", "https"), result.netloc])
    except Exception:
        return False


def get_iso_time(ts: typing.Optional[float] = None) -> str:
    from datetime import datetime

    try:
        dt = datetime.utcfromtimestamp(ts) if ts else datetime.utcnow()
        return dt.replace(microsecond=0).isoformat() + "Z"
    except Exception:
        return ""


def safe_getattr(obj, name: str, default=None):
    try:
        return getattr(obj, name, default)
    except Exception:
        return default


def get_last_commit_message(path: str = ".") -> str:
    try:
        repo = git.Repo(path, search_parent_directories=True)
        return repo.head.commit.message.strip()
    except Exception:
        return ""


def get_commit_count(path: str = ".") -> int:
    try:
        repo = git.Repo(path, search_parent_directories=True)
        return sum(1 for _ in repo.iter_commits())
    except Exception:
        return 0


def get_hostname() -> str:
    try:
        return socket.gethostname()
    except Exception:
        return ""


def resolve_domain(domain: str) -> typing.List[str]:
    try:
        infos = socket.getaddrinfo(domain, None)
        return list({i[4][0] for i in infos if i and i[4]})
    except Exception:
        return []


def is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, int(port)))
            return True
    except Exception:
        return False


def get_network_interfaces() -> typing.Dict[str, typing.List[str]]:
    out = {}
    try:
        import psutil as _ps

        for name, addrs in _ps.net_if_addrs().items():
            out[name] = [a.address for a in addrs if getattr(a, "address", None)]
    except Exception:
        pass
    return out


def get_disk_usage(path: str = "/") -> typing.Dict[str, int]:
    try:
        total, used, free = shutil.disk_usage(path)
        return {"total": total, "used": used, "free": free}
    except Exception:
        return {"total": 0, "used": 0, "free": 0}


def get_ip_address() -> str:
    try:
        # connect to public DNS to determine local IP without sending packets
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


def get_args_bool(message: typing.Union[Message, str]) -> typing.Optional[bool]:
    raw = get_args_raw(message)
    if not raw:
        return None
    val = raw.strip().lower()
    if val in ("1", "true", "yes", "on", "y"):
        return True
    if val in ("0", "false", "no", "off", "n"):
        return False
    return None


def get_args_int(message: typing.Union[Message, str], default: typing.Optional[int] = None) -> typing.Optional[int]:
    raw = get_args_raw(message)
    if not raw:
        return default
    try:
        return safe_int(raw.strip(), default)
    except Exception:
        return default


def uptime() -> int:
    """
    Returns userbot uptime in seconds
    """
    current_uptime = round(time.perf_counter() - init_ts)
    return current_uptime


def formatted_uptime() -> str:
    """
    Returns formatted uptime including days if applicable.
    :return: Formatted uptime
    """
    total_seconds = uptime()
    days, remainder = divmod(total_seconds, 86400)
    time_formatted = str(timedelta(seconds=remainder))
    if days > 0:
        return f"{days} day(s), {time_formatted}"
    return time_formatted


def ascii_face() -> str:
    """
    Returnes cute ASCII-art face
    :return: ASCII-art face
    """
    return escape_html(
        random.choice(
            [
                "ヽ(๑◠ܫ◠๑)ﾉ",
                "(◕ᴥ◕ʋ)",
                "ᕙ(`▽´)ᕗ",
                "(✿◠‿◠)",
                "(▰˘◡˘▰)",
                "(˵ ͡° ͜ʖ ͡°˵)",
                "ʕっ•ᴥ•ʔっ",
                "( ͡° ᴥ ͡°)",
                "(๑•́ ヮ •̀๑)",
                "٩(^‿^)۶",
                "(っˆڡˆς)",
                "ψ(｀∇´)ψ",
                "⊙ω⊙",
                "٩(^ᴗ^)۶",
                "(´・ω・)っ由",
                "( ͡~ ͜ʖ ͡°)",
                "✧♡(◕‿◕✿)",
                "โ๏௰๏ใ ื",
                "∩｡• ᵕ •｡∩ ♡",
                "(♡´౪`♡)",
                "(◍＞◡＜◍)⋈。✧♡",
                "╰(✿´⌣`✿)╯♡",
                "ʕ•ᴥ•ʔ",
                "ᶘ ◕ᴥ◕ᶅ",
                "▼・ᴥ・▼",
                "ฅ^•ﻌ•^ฅ",
                "(΄◞ิ౪◟ิ‵)",
                "٩(^ᴗ^)۶",
                "ᕴｰᴥｰᕵ",
                "ʕ￫ᴥ￩ʔ",
                "ʕᵕᴥᵕʔ",
                "ʕᵒᴥᵒʔ",
                "ᵔᴥᵔ",
                "(✿╹◡╹)",
                "(๑￫ܫ￩)",
                "ʕ·ᴥ·　ʔ",
                "(ﾉ≧ڡ≦)",
                "(≖ᴗ≖✿)",
                "（〜^∇^ )〜",
                "( ﾉ･ｪ･ )ﾉ",
                "~( ˘▾˘~)",
                "(〜^∇^)〜",
                "ヽ(^ᴗ^ヽ)",
                "(´･ω･`)",
                "₍ᐢ•ﻌ•ᐢ₎*･ﾟ｡",
                "(。・・)_且",
                "(=｀ω´=)",
                "(*•‿•*)",
                "(*ﾟ∀ﾟ*)",
                "(☉⋆‿⋆☉)",
                "ɷ◡ɷ",
                "ʘ‿ʘ",
                "(。-ω-)ﾉ",
                "( ･ω･)ﾉ",
                "(=ﾟωﾟ)ﾉ",
                "(・ε・`*) …",
                "ʕっ•ᴥ•ʔっ",
                "(*˘︶˘*)",
                "ಥ_ಥ",
                "･ﾟ･(｡>д<｡)･ﾟ･",
                "(┬┬＿┬┬)",
                "(◞‸◟ㆀ)",
                " ˚‧º·(˚ ˃̣̣̥⌓˂̣̣̥ )‧º·˚",
            ]
        )
    )


def array_sum(
    array: typing.List[typing.List[typing.Any]], /
) -> typing.List[typing.Any]:
    """
    Performs basic sum operation on array
    :param array: Array to sum
    :return: Sum of array
    """
    result = []
    for item in array:
        result += item

    return result


def rand(size: int, /) -> str:
    """
    Return random string of len `size`
    :param size: Length of string
    :return: Random string
    """
    return "".join(
        [random.choice("abcdefghijklmnopqrstuvwxyz1234567890") for _ in range(size)]
    )


def smart_split(
    text: str,
    entities: typing.List[FormattingEntity],
    length: int = 4096,
    split_on: ListLike = ("\n", " "),
    min_length: int = 1,
) -> typing.Iterator[str]:
    """
    Split the message into smaller messages.
    A grapheme will never be broken. Entities will be displaced to match the right location. No inputs will be mutated.
    The end of each message except the last one is stripped of characters from [split_on]
    :param text: the plain text input
    :param entities: the entities
    :param length: the maximum length of a single message
    :param split_on: characters (or strings) which are preferred for a message break
    :param min_length: ignore any matches on [split_on] strings before this number of characters into each message
    :return: iterator, which returns strings

    :example:
        >>> utils.smart_split(
            *herokutl.extensions.html.parse(
                "<b>Hello, world!</b>"
            )
        )
        <<< ["<b>Hello, world!</b>"]
    """

    # Authored by @bsolute
    # https://t.me/LonamiWebs/27777

    encoded = text.encode("utf-16le")
    pending_entities = entities
    text_offset = 0
    bytes_offset = 0
    text_length = len(text)
    bytes_length = len(encoded)

    while text_offset < text_length:
        if bytes_offset + length * 2 >= bytes_length:
            yield parser.unparse(
                text[text_offset:],
                list(sorted(pending_entities, key=lambda x: (x.offset, -x.length))),
            )
            break

        codepoint_count = len(
            encoded[bytes_offset : bytes_offset + length * 2].decode(
                "utf-16le",
                errors="ignore",
            )
        )

        for search in split_on:
            search_index = text.rfind(
                search,
                text_offset + min_length,
                text_offset + codepoint_count,
            )
            if search_index != -1:
                break
        else:
            search_index = text_offset + codepoint_count

        split_index = grapheme.safe_split_index(text, search_index)

        split_offset_utf16 = (
            len(text[text_offset:split_index].encode("utf-16le"))
        ) // 2
        exclude = 0

        while (
            split_index + exclude < text_length
            and text[split_index + exclude] in split_on
        ):
            exclude += 1

        current_entities = []
        entities = pending_entities.copy()
        pending_entities = []

        for entity in entities:
            if (
                entity.offset < split_offset_utf16
                and entity.offset + entity.length > split_offset_utf16 + exclude
            ):
                # spans boundary
                current_entities.append(
                    _copy_tl(
                        entity,
                        length=split_offset_utf16 - entity.offset,
                    )
                )
                pending_entities.append(
                    _copy_tl(
                        entity,
                        offset=0,
                        length=entity.offset
                        + entity.length
                        - split_offset_utf16
                        - exclude,
                    )
                )
            elif entity.offset < split_offset_utf16 < entity.offset + entity.length:
                # overlaps boundary
                current_entities.append(
                    _copy_tl(
                        entity,
                        length=split_offset_utf16 - entity.offset,
                    )
                )
            elif entity.offset < split_offset_utf16:
                # wholly left
                current_entities.append(entity)
            elif (
                entity.offset + entity.length
                > split_offset_utf16 + exclude
                > entity.offset
            ):
                # overlaps right boundary
                pending_entities.append(
                    _copy_tl(
                        entity,
                        offset=0,
                        length=entity.offset
                        + entity.length
                        - split_offset_utf16
                        - exclude,
                    )
                )
            elif entity.offset + entity.length > split_offset_utf16 + exclude:
                # wholly right
                pending_entities.append(
                    _copy_tl(
                        entity,
                        offset=entity.offset - split_offset_utf16 - exclude,
                    )
                )

        current_text = text[text_offset:split_index]
        yield parser.unparse(
            current_text,
            list(sorted(current_entities, key=lambda x: (x.offset, -x.length))),
        )

        text_offset = split_index + exclude
        bytes_offset += len(current_text.encode("utf-16le"))


def _copy_tl(o, **kwargs):
    d = o.to_dict()
    del d["_"]
    d.update(kwargs)
    return o.__class__(**d)


def check_url(url: str) -> bool:
    """
    Statically checks url for validity
    :param url: URL to check
    :return: True if valid, False otherwise
    """
    try:
        return bool(urlparse(url).netloc)
    except Exception:
        return False


def get_git_hash() -> typing.Union[str, bool]:
    """
    Get current Nexus git hash
    :return: Git commit hash
    """
    try:
        return git.Repo().head.commit.hexsha
    except Exception:
        return False


def get_commit_url() -> str:
    """
    Get current Nexus git commit url
    :return: Git commit url
    """
    try:
        hash_ = get_git_hash()
        return f'<a href="https://github.com/archfay/Nexus/commit/{hash_}">#{hash_[:7]}</a>'
    except Exception:
        return "Unknown"


def is_serializable(x: typing.Any, /) -> bool:
    """
    Checks if object is JSON-serializable
    :param x: Object to check
    :return: True if object is JSON-serializable, False otherwise
    """
    try:
        _json_dumps(x)
        return True
    except Exception:
        return False


def get_lang_flag(countrycode: str) -> str:
    """
    Gets an emoji of specified countrycode
    :param countrycode: 2-letter countrycode
    :return: Emoji flag
    """
    if (
        len(
            code := [
                c
                for c in countrycode.lower()
                if c in string.ascii_letters + string.digits
            ]
        )
        == 2
    ):
        return "".join([chr(ord(c.upper()) + (ord("🇦") - ord("A"))) for c in code])

    return countrycode


def get_entity_url(
    entity: typing.Union[User, Channel],
    openmessage: bool = False,
) -> str:
    """
    Get link to object, if available
    :param entity: Entity to get url of
    :param openmessage: Use tg://openmessage link for users
    :return: Link to object or empty string
    """
    return (
        (
            f"tg://openmessage?id={entity.id}"
            if openmessage
            else f"tg://user?id={entity.id}"
        )
        if isinstance(entity, User)
        else (
            f"tg://resolve?domain={entity.username}"
            if getattr(entity, "username", None)
            else ""
        )
    )


async def get_message_link(
    message: Message,
    chat: typing.Optional[typing.Union[Chat, Channel]] = None,
) -> str:
    """
    Get link to message
    :param message: Message to get link of
    :param chat: Chat, where message was sent
    :return: Link to message
    """
    if message.is_private:
        return (
            f"tg://openmessage?user_id={get_chat_id(message)}&message_id={message.id}"
        )

    if not chat and not (chat := message.chat):
        chat = await message.get_chat()

    topic_affix = (
        f"?topic={message.reply_to.reply_to_msg_id}"
        if getattr(message.reply_to, "forum_topic", False)
        else ""
    )

    return (
        f"https://t.me/{chat.username}/{message.id}{topic_affix}"
        if getattr(chat, "username", False)
        else f"https://t.me/c/{chat.id}/{message.id}{topic_affix}"
    )


def remove_html(text: str, escape: bool = False, keep_emojis: bool = False) -> str:
    """
    Removes HTML tags from text
    :param text: Text to remove HTML from
    :param escape: Escape HTML
    :param keep_emojis: Keep custom emojis
    :return: Text without HTML
    """
    return (escape_html if escape else str)(
        re.sub(
            (
                r"(<\/?a.*?>|<\/?b>|<\/?i>|<\/?u>|<\/?strong>|<\/?em>|<\/?code>|<\/?strike>|<\/?del>|<\/?pre.*?>|<\/?blockquote.*?>)"
                if keep_emojis
                else r"(<\/?a.*?>|<\/?b>|<\/?i>|<\/?u>|<\/?strong>|<\/?em>|<\/?code>|<\/?strike>|<\/?del>|<\/?pre.*?>|<\/?emoji.*?>|<\/?blockquote.*?>)"
            ),
            "",
            text,
        )
    )


def remove_emoji(text: str) -> str:
    """
    Removes all emoji from text
    """

    allchars = [str for str in text]
    emoji_list = [c for c in allchars if c in emoji.EMOJI_DATA]
    clean_text = "".join([str for str in text if not any(i in str for i in emoji_list)])
    return clean_text


def get_kwargs() -> typing.Dict[str, typing.Any]:
    """
    Get kwargs of function, in which is called
    :return: kwargs
    """
    # https://stackoverflow.com/a/65927265/19170642
    keys, _, _, values = inspect.getargvalues(inspect.currentframe().f_back)
    return {key: values[key] for key in keys if key != "self"}


def mime_type(message: Message) -> str:
    """
    Get mime type of document in message
    :param message: Message with document
    :return: Mime type or empty string if not present
    """
    return (
        ""
        if not isinstance(message, Message) or not getattr(message, "media", False)
        else getattr(getattr(message, "media", False), "mime_type", False) or ""
    )


def find_caller(
    stack: typing.Optional[typing.List[inspect.FrameInfo]] = None,
) -> typing.Any:
    """
    Attempts to find command in stack
    :param stack: Stack to search in
    :return: Command-caller or None
    """
    caller = next(
        (
            frame_info
            for frame_info in stack or inspect.stack()
            if hasattr(frame_info, "function")
            and any(
                inspect.isclass(cls_)
                and issubclass(cls_, Module)
                and cls_ is not Module
                for cls_ in frame_info.frame.f_globals.values()
            )
        ),
        None,
    )

    if not caller:
        return next(
            (
                frame_info.frame.f_locals["func"]
                for frame_info in stack or inspect.stack()
                if hasattr(frame_info, "function")
                and frame_info.function == "future_dispatcher"
                and (
                    "CommandDispatcher"
                    in getattr(getattr(frame_info, "frame", None), "f_globals", {})
                )
            ),
            None,
        )

    return next(
        (
            getattr(cls_, caller.function, None)
            for cls_ in caller.frame.f_globals.values()
            if inspect.isclass(cls_) and issubclass(cls_, Module)
        ),
        None,
    )


def validate_html(html: str) -> str:
    """
    Removes broken tags from html
    :param html: HTML to validate
    :return: Valid HTML
    """
    text, entities = herokutl.extensions.html.parse(html)
    return herokutl.extensions.html.unparse(escape_html(text), entities)


def iter_attrs(obj: typing.Any, /) -> typing.Iterator[typing.Tuple[str, typing.Any]]:
    """
    Returns list of attributes of object
    :param obj: Object to iterate over
    :return: List of attributes and their values
    """
    for attr in dir(obj):
        if attr.startswith("_"):
            continue

        try:
            value = getattr(obj, attr)
        except Exception:
            continue

        if callable(value):
            continue

        yield attr, value


def atexit(
    func: typing.Callable,
    use_signal: typing.Optional[int] = None,
    *args,
    **kwargs,
) -> None:
    """
    Calls function on exit
    :param func: Function to call
    :param use_signal: If passed, `signal` will be used instead of `atexit`
    :param args: Arguments to pass to function
    :param kwargs: Keyword arguments to pass to function
    :return: None
    """
    if use_signal:
        signal.signal(use_signal, lambda *_: func(*args, **kwargs))
        return

    _atexit.register(functools.partial(func, *args, **kwargs))


def get_topic(message: Message) -> typing.Optional[int]:
    """
    Get topic id of message
    :param message: Message to get topic of
    :return: int or None if not present
    """
    return (
        (message.reply_to.reply_to_top_id or message.reply_to.reply_to_msg_id)
        if (
            isinstance(message, Message)
            and message.reply_to
            and message.reply_to.forum_topic
        )
        else (
            message.form["top_msg_id"]
            if isinstance(message, (InlineCall, InlineMessage))
            else None
        )
    )


def get_ram_usage() -> float:
    """Returns current process tree memory usage in MB"""
    try:
        import psutil

        current_process = psutil.Process(os.getpid())
        mem = current_process.memory_info()[0] / 2.0**20
        for child in current_process.children(recursive=True):
            mem += child.memory_info()[0] / 2.0**20
        return round(mem, 1)
    except Exception:
        return 0


run_first_time = True  # workaround 0.00% cpu usage


def get_cpu_usage():
    import psutil

    global run_first_time

    if run_first_time:
        try:
            psutil.cpu_count(logical=True)
            for proc in psutil.process_iter():
                try:
                    proc.cpu_percent()
                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess,
                ):
                    pass
        except Exception:
            pass
        run_first_time = False

    try:
        num_cores = psutil.cpu_count(logical=True)
        cpu = 0.0
        for proc in psutil.process_iter():
            try:
                cpu += proc.cpu_percent()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        normalized_cpu = cpu / num_cores
        return f"{normalized_cpu:.2f}"
    except Exception:
        return "0.00"


init_ts = time.perf_counter()


# Premium emoji IDs for bot messages
PREMIUM_EMOJIS = [
    5188377234380954537,  # 🌐
    5314250708508220914,  # ✅
    5451732530048802485,  # ⏳
    5436040291507247633,  # 🎉
    5210952531676504517,  # 🚫
    5312383351217201533,  # ⚠️
    5472308992514464048,  # 🔐
    5784993237412351403,  # ✅
    5197474765387864959,  # 👍
    5386399931378440814,  # 😎
    5447644880824181073,  # ⚠️
    5355133243773435190,  # ☝️
    5974674704788891783,  # ⚙️
    5469791106591890404,  # 🪄
    5424885441100782420,  # 👀
    5870704313440932932,  # 🔒
    5870772616305839506,  # 👥
    5870450390679425417,  # 🗒
    5228879218363872764,  # ⌨️
    5213452215527677338,  # ⏳
    5332533929020761310,  # ✅
    5452023368054216810,  # 🥶
    5208634061085492935,  # 📖
    5472111548572900003,  # ⌨️
    5118861066981344121,  # ✅
    5431736674147114227,  # 🗂
    5774134533590880843,  # 🔄
    5469718869536940860,  # 👆
    5256113064821926998,  # 📁
    5134452506935427991,  # 🌐
    5873204392429096339,  # 🔄
    5341492148468465410,  # 📦
    5287454910059654880,  # 🫶
    5363805650327450240,  # 🌐
    5471952986970267163,  # 💎
    6037284117505116849,  # 🌐
    5469741319330996757,  # 💫
    5467666648263564704,  # ❓
    5325787248363314644,  # 🫥
    5197688912457245639,  # ✅
    5318933532825888187,  # ⚙️
    5472146462362048818,  # 💡
    5454225457916420314,  # 😖
    5372981976804366741,  # 🤖
    5350594756126721186,  # 🌐
    5328311576736833844,  # 🚀
    5875145601682771643,  # 🚀
    5458450833857322148,  # 👌
    6003424016977628379,  # 🔒
    5877458226823302157,  # 🕒
    5877477244938489129,  # 🚫
    5370699111492229743,  # 😌
    5424728541650494040,  # 😕
    5370881342659631698,  # 😢
    5188377234380954537,  # 🌐
    5472238129849048175,  # 😎
    5474667187258006816,  # 😎
    5472267631979405211,  # 🚫
    5465665476971471368,  # ❌
    5427052514094619126,  # 🤷♀️
    5382187118216879236,  # ❓
    6019094432790354513,  # 📢
    6019130940012370273,  # 💬
    6019151079114021083,  # 💬
    5375368793209972850,  # 🖋
    5226512880362332956,  # 📖
]


def add_premium_emoji(text: str) -> str:
    """
    Add random premium emoji to bot message
    :param text: Message text
    :return: Text with premium emoji
    """
    emoji_id = random.choice(PREMIUM_EMOJIS)
    return f'<emoji document_id={emoji_id}>🌐</emoji> {text}'


# GeekTG Compatibility
def get_git_info() -> typing.Tuple[str, str]:
    """
    Get git info
    :return: Git info
    """
    hash_ = get_git_hash()
    return (
        hash_,
        f"https://github.com/archfay/Nexus/commit/{hash_}" if hash_ else "",
    )


def get_version_raw() -> str:
    """
    Get the version of the userbot
    :return: Version in format %s.%s.%s
    """
    from . import version

    return ".".join(map(str, list(version.__version__)))


get_platform_name = get_named_platform
version = get_version_raw

# Placeholder registry
_placeholders: typing.Dict[str, typing.Tuple[typing.Callable, str]] = {}


def register_placeholder(name: str, func: typing.Callable, description: str = "") -> None:
    _placeholders[name] = (func, description)


async def resolve_placeholder(name: str) -> typing.Optional[str]:
    entry = _placeholders.get(name)
    if entry is None:
        return None
    return await entry[0]()
