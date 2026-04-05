#------------------------------------------------------------------
#      ___           ___       ___                       ___     
#     /\  \         /\__\     /\  \          ___        /\__\    
#    /::\  \       /:/  /    /::\  \        /\  \      /:/  /    
#   /:/\ \  \     /:/  /    /:/\:\  \       \:\  \    /:/__/     
#  _\:\~\ \  \   /:/  /    /::\~\:\  \      /::\__\  /::\__\____ 
# /\ \:\ \ \__\ /:/__/    /:/\:\ \:\__\  __/:/\/__/ /:/\:::::\__\
# \:\ \:\ \/__/ \:\  \    \/__\:\/:/  / /\/:/  /    \/_|:|~~|~   
#  \:\ \:\__\    \:\  \        \::/  /  \::/__/        |:|  |    
#   \:\/:/  /     \:\  \       /:/  /    \:\__\        |:|  |    
#    \::/  /       \:\__\     /:/  /      \/__/        |:|  |    
#     \/__/         \/__/     \/__/                     \|__|   
#------------------------------------------------------------------ 
# meta developer: @Hicota
# requires: pet-pet-gif

import os
from .. import loader, utils
from io import BytesIO
from petpetgif import petpet
import logging

logger = logging.getLogger(__name__)

@loader.tds
class PetPetMod(loader.Module):
    """Сделай фото в гифку, которое гладит изображение или аватар пользователя"""
    
    strings = {
        "name": "PetPet",
        "no_photo_reply": '<emoji document_id=5465665476971471368>❌</emoji><b>Вы ответили не на фото</b><emoji document_id=5465665476971471368>❌</emoji>\nОтветьте на фото, чтобы команда .pet заработала',
        "no_reply": '<emoji document_id=5465665476971471368>❌</emoji><b>Ответьте на сообщение пользователя, чтобы погладить его аву.</b><emoji document_id=5465665476971471368>❌</emoji>',
        "no_user_info": '<emoji document_id=5465665476971471368>❌</emoji><b>Не удалось получить информацию о пользователе из ответа.</b><emoji document_id=5465665476971471368>❌</emoji>',
        "no_avatar": '<emoji document_id=5465665476971471368>❌</emoji><b>У этого пользователя нет аватара для поглаживания!</b><emoji document_id=5465665476971471368>❌</emoji>',
        "gif_error": '<emoji document_id=5465665476971471368>❌</emoji><b>Ошибка при создании гифки:</b> {error}<emoji document_id=5465665476971471368>❌</emoji>',
    }

    @loader.command(ru_doc="- Реплай на фото | Отправить команду с фото")
    async def pet(self, message):
        """- Реплай на фото | Отправить команду с фото"""
        response = None
        media_to_pet = None
        reply_to_id = None

        if message.is_reply:
            response = await message.get_reply_message()
            reply_to_id = response.id
            if hasattr(response, 'photo'):
                media_to_pet = response.photo
            elif hasattr(response, 'media') and hasattr(response.media, 'photo'):
                media_to_pet = response.media.photo
            else:
                await utils.answer(message, self.strings("no_photo_reply"))
                return
            await message.delete()
            if response.from_id == self.tg_id: # Если это мое сообщение, которое я реплаю, удаляем и его
                await response.delete()
        else:
            if hasattr(message, 'media') and hasattr(message.media, 'photo'):
                media_to_pet = message.media.photo
                reply_to_id = message.reply_to_msg_id # Если это инлайн, то может быть реплай на что-то
                await message.delete()
            else:
                await utils.answer(message, self.strings("no_photo_reply"))
                return
        
        if not media_to_pet:
            await utils.answer(message, self.strings("no_photo_reply"))
            return

        temp_file_path = None
        try:
            temp_file_path = await self._client.download_media(media_to_pet, "pet_temp_photo")
            petgif = BytesIO()
            petpet.make(temp_file_path, petgif)
            petgif.name = "pet.gif"
            petgif.seek(0)
        except Exception as e:
            logger.error(f"Error making petpet gif: {e}", exc_info=True)
            await utils.answer(message, self.strings("gif_error").format(error=str(e)))
            return
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path) # Удаляем временный файл
        
        await self._client.send_file(
            message.to_id, 
            file=petgif, 
            force_document=False, 
            reply_to=reply_to_id if message.is_private or reply_to_id else None # Реплай только если в группе или если есть id
        )


    @loader.command(ru_doc="- Реплай на сообщение пользователя, чтобы погладить его аву")
    async def peta(self, message):
        """- Реплай на сообщение пользователя, чтобы погладить его аву"""
        if not message.is_reply:
            await utils.answer(message, self.strings("no_reply"))
            return

        reply_message = await message.get_reply_message()
        if not reply_message or not reply_message.sender:
            await utils.answer(message, self.strings("no_user_info"))
            return

        user_id = reply_message.sender_id
        
        # Получаем объект пользователя (для получения его аватара)
        user = await self._client.get_entity(user_id)
        
        # Получаем его профильные фото, ограничиваем до одной (последней)
        photos = await self._client.get_profile_photos(user, limit=1)

        if not photos:
            await utils.answer(message, self.strings("no_avatar"))
            return

        temp_photo_path = None
        try:
            # Скачиваем аватарку во временный файл
            temp_photo_path = await self._client.download_media(photos[0], "pet_avatar_temp")
            
            petgif = BytesIO()
            petpet.make(temp_photo_path, petgif) # Создаем гифку
            petgif.name = "pet_avatar.gif"
            petgif.seek(0)
        except Exception as e:
            logger.error(f"Error making petpet gif for avatar: {e}", exc_info=True)
            await utils.answer(message, self.strings("gif_error").format(error=str(e)))
            return
        finally:
            if temp_photo_path and os.path.exists(temp_photo_path):
                os.remove(temp_photo_path) # Удаляем временный файл аватарки

        # Отправляем готовую гифку как реплай на оригинальное сообщение
        await self._client.send_file(
            message.to_id, 
            file=petgif, 
            force_document=False, 
            reply_to=reply_message.id if message.chat.forum else None # В группах реплаим на исходное сообщение, в личке просто отправляем
        )
        await message.delete() # Удаляем команду .peta, чтобы не мусорить