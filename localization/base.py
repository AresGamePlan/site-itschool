from flask import request
from flask_login import current_user
from localization.languages import text

def language(func):
    def out_func(*args, **kwargs):
        lang = request.cookies.get("lang") or "ru"
        kwargs["lang"] = lang
        kwargs["text"] = text
        kwargs["user"] = current_user
        return func(*args, **kwargs)
    return out_func