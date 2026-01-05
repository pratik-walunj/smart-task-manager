from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # 🔹 Configuration
    app.config["SECRET_KEY"] = "dev-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 🔹 Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # 🔹 User loader
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 🔹 Register blueprints
    from .auth import auth
    from .routes import routes
    app.register_blueprint(auth)
    app.register_blueprint(routes)

    # 🔹 Create database tables
    with app.app_context():
        from .models import User, Task
        db.create_all()

    # 🔹 Home route
    @app.route("/")
    def home():
        return "Backend Running Successfully 🚀"

    return app
