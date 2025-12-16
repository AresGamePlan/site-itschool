from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask.views import MethodView

from localization.base import language

main_bp = Blueprint("main", __name__)

class IndexView(MethodView):
    decorators = [language]

    def get(self, **kwargs):
        if current_user.is_authenticated:
            if current_user.is_admin():
                return redirect(url_for("main.admin"))
            elif current_user.is_user():
                return redirect(url_for("user.index"))
            elif current_user.is_teacher():
                return redirect(url_for("teacher.index"))

        return render_template("main/index.html", data = kwargs)

class ProfileView(MethodView):
    decorators = [login_required, language]

    def get(self, **kwargs):
        return render_template("account/profile.html", data = kwargs)


class NoRightView(MethodView):
    decorators = [language]

    def get(self, **kwargs):
        return render_template("main/noright.html", data = kwargs)

class AdminView(MethodView):
    decorators = [login_required, language]

    def get(self, **kwargs):
        if not current_user.is_admin():
            return redirect(url_for("main.noright")), 403
        return render_template("admin/index.html", data = kwargs)

main_bp.add_url_rule("/", view_func=IndexView.as_view("index"))
main_bp.add_url_rule("/noright", view_func=NoRightView.as_view("noright"))
main_bp.add_url_rule("/profile", view_func=ProfileView.as_view("profile"))
main_bp.add_url_rule("/admin", view_func=AdminView.as_view("admin"))