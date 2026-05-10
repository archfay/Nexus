"""Banner list management module"""

# ©️ DoNotWeb, 2024-2025
# This file is a part of Nexus Userbot
# 🌐 https://github.com/archfay/Nexus

import os
import random
from herokutl.tl.types import Message
from .. import loader, utils

@loader.tds
class BannerListMod(loader.Module):
    """Manage banners for info and ping commands"""

    strings = {"name": "BannerList"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "info_banner_mode",
                "default",
                "Banner mode for .info command: default/random/specific/none",
                validator=loader.validators.Choice(["default", "random", "specific", "none"]),
            ),
            loader.ConfigValue(
                "info_banner_id",
                0,
                "Banner ID for .info (when mode is 'specific')",
                validator=loader.validators.Integer(minimum=0),
            ),
            loader.ConfigValue(
                "ping_banner_mode",
                "default",
                "Banner mode for .ping command: default/random/specific/none",
                validator=loader.validators.Choice(["default", "random", "specific", "none"]),
            ),
            loader.ConfigValue(
                "ping_banner_id",
                0,
                "Banner ID for .ping (when mode is 'specific')",
                validator=loader.validators.Integer(minimum=0),
            ),
            loader.ConfigValue(
                "restart_banner_mode",
                "none",
                "Banner mode for .restart command: default/random/specific/none",
                validator=loader.validators.Choice(["default", "random", "specific", "none"]),
            ),
            loader.ConfigValue(
                "restart_banner_id",
                0,
                "Banner ID for .restart (when mode is 'specific')",
                validator=loader.validators.Integer(minimum=0),
            ),
            loader.ConfigValue(
                "default_info_banner",
                "https://raw.githubusercontent.com/archfay/assets/refs/heads/main/nexus/nexus_info.png",
                "Default banner URL for .info",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "default_ping_banner",
                "",
                "Default banner URL for .ping",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "default_restart_banner",
                "",
                "Default banner URL for .restart",
                validator=loader.validators.String(),
            ),
        )

    def _get_banner_by_mode(self, mode: str, banner_id: int, default: str):
        """Get banner based on mode"""
        if mode == "none":
            return None
        elif mode == "default":
            return default if default else None
        elif mode == "random":
            banners = self._db.get("BannerList", "banners", [])
            return random.choice(banners) if banners else default
        elif mode == "specific":
            banners = self._db.get("BannerList", "banners", [])
            if 0 <= banner_id < len(banners):
                return banners[banner_id]
            return default
        return default

    @loader.command()
    async def addblcmd(self, message: Message):
        """Add banner to list (reply to photo/video/gif)"""
        if not message.is_reply:
            await utils.answer(message, "❌ Ответьте на фото/видео/гиф")
            return

        reply = await message.get_reply_message()
        if not (reply.photo or reply.video or reply.gif or reply.document):
            await utils.answer(message, "❌ Это не медиа файл")
            return

        banner_dir = f"{os.getcwd()}/assets/banners"
        os.makedirs(banner_dir, exist_ok=True)

        banners = self._db.get("BannerList", "banners", [])
        banner_id = len(banners)
        
        if reply.photo:
            ext = "jpg"
        elif reply.gif:
            ext = "gif"
        elif reply.video:
            ext = "mp4"
        else:
            ext = reply.document.mime_type.split("/")[-1]

        banner_path = f"{banner_dir}/banner_{banner_id}.{ext}"
        await reply.download_media(banner_path)

        banners.append(banner_path)
        self._db.set("BannerList", "banners", banners)

        await utils.answer(
            message,
            f"✅ Баннер добавлен в список\n📊 ID баннера: {banner_id}\n📊 Всего баннеров: {len(banners)}"
        )

    @loader.command()
    async def bannerlistcmd(self, message: Message):
        """Show all saved banners with preview"""
        banners = self._db.get("BannerList", "banners", [])
        
        if not banners:
            await utils.answer(message, "📋 Список баннеров пуст")
            return

        text = f"📋 <b>Список баннеров ({len(banners)}):</b>\n\n"
        text += "<b>Настройки:</b>\n"
        text += f"🖼 .info: <code>{self.config['info_banner_mode']}</code>"
        if self.config['info_banner_mode'] == 'specific':
            text += f" (ID: {self.config['info_banner_id']})"
        text += f"\n🌐 .ping: <code>{self.config['ping_banner_mode']}</code>"
        if self.config['ping_banner_mode'] == 'specific':
            text += f" (ID: {self.config['ping_banner_id']})"
        text += f"\n🔄 .restart: <code>{self.config['restart_banner_mode']}</code>"
        if self.config['restart_banner_mode'] == 'specific':
            text += f" (ID: {self.config['restart_banner_id']})"
        text += "\n\n<b>Баннеры:</b>\n"
        
        for i, banner in enumerate(banners):
            text += f"{i}. <code>{os.path.basename(banner)}</code>\n"

        await utils.answer(message, text)

    @loader.command()
    async def previewblcmd(self, message: Message):
        """Preview banner by ID"""
        args = utils.get_args_raw(message)
        if not args or not args.isdigit():
            await utils.answer(message, "❌ Укажите ID баннера\n\nИспользование: <code>.previewbl 0</code>")
            return

        banners = self._db.get("BannerList", "banners", [])
        banner_id = int(args)

        if banner_id < 0 or banner_id >= len(banners):
            await utils.answer(message, f"❌ Баннер #{banner_id} не найден")
            return

        banner_path = banners[banner_id]
        
        if not os.path.exists(banner_path):
            await utils.answer(message, f"❌ Файл баннера не найден: {banner_path}")
            return

        await utils.answer_file(
            message,
            banner_path,
            caption=f"🖼 <b>Баннер #{banner_id}</b>\n📁 {os.path.basename(banner_path)}"
        )

    @loader.command()
    async def delblcmd(self, message: Message):
        """Delete banner from list by ID"""
        args = utils.get_args_raw(message)
        if not args or not args.isdigit():
            await utils.answer(message, "❌ Укажите ID баннера\n\nИспользование: <code>.delbl 0</code>")
            return

        banners = self._db.get("BannerList", "banners", [])
        banner_id = int(args)

        if banner_id < 0 or banner_id >= len(banners):
            await utils.answer(message, f"❌ Баннер #{banner_id} не найден")
            return

        banner_path = banners[banner_id]
        
        if os.path.exists(banner_path):
            os.remove(banner_path)

        banners.pop(banner_id)
        self._db.set("BannerList", "banners", banners)

        await utils.answer(message, f"✅ Баннер #{banner_id} удален\n📊 Осталось баннеров: {len(banners)}")

    @loader.command()
    async def clearblcmd(self, message: Message):
        """Clear all banners"""
        banners = self._db.get("BannerList", "banners", [])
        
        if not banners:
            await utils.answer(message, "📋 Список баннеров уже пуст")
            return

        for banner in banners:
            if os.path.exists(banner):
                os.remove(banner)

        self._db.set("BannerList", "banners", [])
        await utils.answer(message, "✅ Все баннеры удалены")

    async def client_ready(self):
        info_mod = self.lookup("nexusInfo")
        test_mod = self.lookup("Tester")
        restarter_mod = self.lookup("Restarter")

        if info_mod:
            original_info = info_mod.infocmd

            async def patched_info(msg: Message):
                banner = self._get_banner_by_mode(
                    self.config["info_banner_mode"],
                    self.config["info_banner_id"],
                    self.config["default_info_banner"]
                )
                if banner:
                    info_mod.config["banner_url"] = banner
                elif banner is None:
                    info_mod.config["banner_url"] = ""
                await original_info(msg)

            info_mod.infocmd = patched_info

        if test_mod:
            original_ping = test_mod.pingcmd

            async def patched_ping(msg: Message):
                banner = self._get_banner_by_mode(
                    self.config["ping_banner_mode"],
                    self.config["ping_banner_id"],
                    self.config["default_ping_banner"]
                )
                if banner:
                    test_mod.config["banner_url"] = banner
                elif banner is None:
                    test_mod.config["banner_url"] = None
                await original_ping(msg)

            test_mod.pingcmd = patched_ping

        if restarter_mod:
            original_restart = restarter_mod.restart

            async def patched_restart(msg: Message):
                banner = self._get_banner_by_mode(
                    self.config["restart_banner_mode"],
                    self.config["restart_banner_id"],
                    self.config["default_restart_banner"]
                )
                if banner:
                    restarter_mod._restart_banner = banner
                await original_restart(msg)

            restarter_mod.restart = patched_restart
