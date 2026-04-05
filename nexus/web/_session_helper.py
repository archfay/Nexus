"""Helper для сохранения сессий в БД"""

def save_session_to_db(web_instance, session):
    """Сохранить сессию в БД"""
    if web_instance.client_data:
        client_id = list(web_instance.client_data.keys())[0]
        _, _, db = web_instance.client_data[client_id]
        db.set("nexus.web.core", "web_sessions", web_instance._sessions)
