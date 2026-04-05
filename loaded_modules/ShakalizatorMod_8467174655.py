#   _   _  _               _         
#  | | | |(_)             | |        
#  | |_| | _  ___   ___   | | __  __ _ 
#  |  _  || |/ __| / _ \  | |/ / / _` |
#  | | | || |\__ \| (_) | |   < | (_| |
#  \_| |_/|_||___/ \___/  |_|\_\ \__,_|
#
# meta developer: @xyecoder
# meta banner: https://pomf2.lain.la/f/jhep1ua2.jpg
# scope: hikka_only
# scope: hikka_min 1.6.3
# requires: Pillow

import logging
import os
import subprocess
import asyncio
import io
from PIL import Image
from .. import loader, utils
from telethon.tl.types import Message, DocumentAttributeVideo

logger = logging.getLogger(__name__)

@loader.tds
class ShakalizatorMod(loader.Module):
    """Цэ потужни шакализатор для всего медиа"""
    
    strings = {
        "name": "Shakalizator",
        "processing": "⏳ <b>Потужна деградация запущена...</b>",
        "no_reply": "<b>❌ Нужно ответить на медиафайл.</b>",
        "error": "<b>❌ Ошибка при уничтожении качества.</b>",
        "no_ffmpeg": "<b>❌ FFmpeg не найден в системе.</b>\nДля обработки видео/гифок его нужно установить.",
        "caption": "ШакаліZOVaно✅"
    }

    strings_ru = {
        "processing": "⏳ <b>Уничтожение качества контента...</b>",
        "no_reply": "<b>❌ Ответь на медиафайл, чтобы применить шакализатор.</b>",
        "no_ffmpeg": "<b>❌ FFmpeg не установлен.</b>\nОбработка видео невозможна без него.",
        "caption": "ШакаліZOVaно✅"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "pixel_size",
                10,
                "Размер пикселя. Чем выше число, тем сильнее пикселизация.",
                validator=loader.validators.Integer(minimum=2, maximum=50)
            ),
            loader.ConfigValue(
                "video_bitrate",
                "32k",
                "Битрейт видео для максимальных шакалов."
            ),
            loader.ConfigValue(
                "audio_bitrate",
                "8k",
                "Битрейт аудио."
            )
        )

    @loader.command(
        ru_doc="Шакализируй это дерьмо (фото, видео, гифки, кружочки)",
        en_doc="Shakalize this shit (photo, video, gif, video notes)"
    )
    async def shakalcmd(self, message: Message):
        """Шакализируй это дерьмо"""
        reply = await message.get_reply_message()
        if not reply or not (reply.photo or reply.video or reply.sticker or reply.document or reply.gif or reply.video_note):
            await utils.answer(message, self.strings("no_reply"))
            return

        status = await utils.answer(message, self.strings("processing"))
        
        # Определение типа медиа
        is_video = bool(reply.video or reply.video_note or reply.gif)
        if reply.document and not is_video:
            mime = reply.file.mime_type or ""
            if mime.startswith("video/"):
                is_video = True
            elif mime == "image/gif":
                is_video = True

        path = await self._client.download_media(reply)
        output = f"shakal_{'v' if is_video else 'p'}.{'mp4' if is_video else 'jpg'}"

        try:
            p_size = self.config["pixel_size"]

            if not is_video:
                # Обработка фото / стикеров / документов-картинок
                img = Image.open(path)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                w, h = img.size
                # Пикселизация через ресайз
                img_small = img.resize((max(w // p_size, 1), max(h // p_size, 1)), resample=Image.NEAREST)
                img_pixel = img_small.resize((w, h), resample=Image.NEAREST)
                img_pixel.save(output, "JPEG", quality=5, subsampling=2)
                
            else:
                # Обработка видео / гиф / кружочков
                # Используем scale с neighbor для пикселизации в ffmpeg
                v_bitrate = self.config["video_bitrate"]
                a_bitrate = self.config["audio_bitrate"]
                
                # Сложный фильтр для ffmpeg: сначала уменьшаем, потом увеличиваем обратно для эффекта пикселей
                # Важно: для x264 размеры должны быть четными
                vf = (
                    f"scale='iw/{p_size}':'ih/{p_size}':flags=neighbor,"
                    f"scale='trunc(iw*{p_size}/2)*2':'trunc(ih*{p_size}/2)*2':flags=neighbor,"
                    "format=yuv420p"
                )

                cmd = [
                    "ffmpeg", "-y", "-i", path,
                    "-vf", vf,
                    "-vcodec", "libx264", "-crf", "51",
                    "-b:v", v_bitrate,
                    "-acodec", "aac", "-b:a", a_bitrate, "-ar", "8000", "-ac", "1",
                    "-preset", "veryfast",
                    output
                ]
                
                try:
                    process = await asyncio.create_subprocess_exec(
                        *cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                    )
                    await process.communicate()
                except FileNotFoundError:
                    await utils.answer(message, self.strings("no_ffmpeg"))
                    return

            if os.path.exists(output) and os.path.getsize(output) > 0:
                await self._client.send_file(
                    message.chat_id,
                    output,
                    reply_to=reply.id,
                    caption=self.strings("caption"),
                    video_note=bool(reply.video_note)
                )
                await status.delete()
                await message.delete()
            else:
                await utils.answer(message, self.strings("error"))

        except Exception as e:
            logger.exception("Shakalizator failure")
            await utils.answer(message, f"{self.strings('error')}\n<code>{e}</code>")
        
        finally:
            for f in [path, output]:
                if f and os.path.exists(f):
                    try:
                        os.remove(f)
                    except:
                        pass