from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from flask.views import MethodView
from models.database import User, db
import qrcode
import io
import base64
from forms.user_forms import EditDataForm

from localization.base import language

user_bp = Blueprint("user", __name__)

class UserIndexView(MethodView):
    decorators = [language, login_required]

    def get(self, **kwargs):
        return render_template("user/index.html", data = kwargs)
    
class UserSignView(MethodView):
    decorators = [language, login_required]

    def get(self, **kwargs):
        return render_template("user/sign.html", data = kwargs)
    
    def post(self, **kwargs):

        return redirect("user.sented", data = kwargs)
    
class UserSentedView(MethodView):
    decorators = [language, login_required]

    def get(self, **kwargs):
        return render_template("user/sented.html", data = kwargs)
    
class UserAccountView(MethodView):
    decorators = [language, login_required]

    def get(self, **kwargs):
        user = User.query.get(current_user.id)

        kwargs["user"] = user

        return render_template("user/account.html", data = kwargs)
    
class UserQrView(MethodView):
    decorators = [language, login_required]

    def get(self, **kwargs):
        user_id = current_user.id 
        
        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(user_id)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        img_b64 = base64.b64encode(buffer.read()).decode("utf-8")

        kwargs["qr"] = img_b64

        return render_template("user/qrcode.html", data=kwargs)

class UserEditView(MethodView):
    decorators = [language, login_required]

    def get(self, **kwargs):
        form = EditDataForm()
        user = User.query.get(current_user.id)

        kwargs["user"] = user

        return render_template("user/edit.html", data = kwargs, form = form)
    
    def post(self, **kwargs):
        form = EditDataForm(request.form)
        user = User.query.get(form.user_id.data)

        if user.fullname != form.fullname.data:
            user.fullname = form.fullname.data
        if user.username != form.login.data:
            user.username = form.login.data

        db.session.commit()

        return redirect(url_for("user.account"))
        
    
user_bp.add_url_rule("/", view_func=UserIndexView.as_view("index"))
user_bp.add_url_rule("/sign", view_func=UserSignView.as_view("sign"))
user_bp.add_url_rule("/sented", view_func=UserSentedView.as_view("sented"))
user_bp.add_url_rule("/account", view_func=UserAccountView.as_view("account"))
user_bp.add_url_rule("/qrcode", view_func=UserQrView.as_view("qrcode"))
user_bp.add_url_rule("/edit", view_func=UserEditView.as_view("edit"))