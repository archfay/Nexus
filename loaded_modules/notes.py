from .. import loader, utils


@loader.tds
class NotesMod(loader.Module):
    """Quick notes manager"""

    strings = {"name": "Notes"}

    async def notecmd(self, message):
        """<add/list/get/del> [name] [text] - Manage notes"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, "❌ Usage: .note <add/list/get/del> [name] [text]")

        parts = args.split(maxsplit=2)
        action = parts[0].lower()

        if action == "list":
            notes = self.db.get(self.__class__.__name__, "notes", {})
            if not notes:
                return await utils.answer(message, "📝 No notes saved")
            
            text = "📝 <b>Your notes:</b>\n\n"
            for name in notes:
                text += f"• <code>{name}</code>\n"
            return await utils.answer(message, text)

        if len(parts) < 2:
            return await utils.answer(message, "❌ Specify note name")

        name = parts[1]
        notes = self.db.get(self.__class__.__name__, "notes", {})

        if action == "add":
            if len(parts) < 3:
                return await utils.answer(message, "❌ Specify note text")
            notes[name] = parts[2]
            self.db.set(self.__class__.__name__, "notes", notes)
            return await utils.answer(message, f"✅ Note <code>{name}</code> saved")

        if action == "get":
            if name not in notes:
                return await utils.answer(message, f"❌ Note <code>{name}</code> not found")
            return await utils.answer(message, f"📝 <b>{name}:</b>\n\n{notes[name]}")

        if action == "del":
            if name not in notes:
                return await utils.answer(message, f"❌ Note <code>{name}</code> not found")
            del notes[name]
            self.db.set(self.__class__.__name__, "notes", notes)
            return await utils.answer(message, f"🗑 Note <code>{name}</code> deleted")

        await utils.answer(message, "❌ Unknown action. Use: add/list/get/del")
