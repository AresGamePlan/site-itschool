from flask import Flask
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_migrate import Migrate, upgrade
from werkzeug.security import generate_password_hash
from instance.config import Config
from models.database import db, User
from views.auth import auth_bp
from views.main import main_bp
from views.admin import admin_bp
from views.user import user_bp
from views.teacher import teacher_bp

app = Flask(__name__)
app.config.from_object(Config)

migrate = Migrate(app, db)

csrf = CSRFProtect(app)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Регистрация blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(main_bp, url_prefix='/')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(teacher_bp, url_prefix="/teacher")

with app.app_context():
    db.create_all()

    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin_user = User(
            username = Config.ADMIN_LOGIN,
            password=generate_password_hash(Config.ADMIN_PASSWORD, method="pbkdf2:sha256"),
            role="admin"
        )
        db.session.add(admin_user)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)