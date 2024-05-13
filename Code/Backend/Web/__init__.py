from flask import Flask
from flask_cors import CORS
from .packages import db, mail
from flask_jwt_extended import JWTManager
from .api import api_bp
from werkzeug.security import generate_password_hash



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'My_secret_key'
    app.config["JWT_SECRET_KEY"] = "super-secret"  
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///music.sqlite"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

    
    db.init_app(app)
    CORS(app)
    
#--------------- Configuring mail----------------- 
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'ayshagrwl@gmail.com' # Change it from your mail id
    app.config['MAIL_PASSWORD'] = 'mcyljnpxdbjqyywv' # Change the password accordingly.
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    mail.mail.init_app(app)

    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    app.register_blueprint(api_bp, url_prefix='/')



# ----------------- JWT Implementation-----------------
    from .models import User

    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(user_id=identity).one_or_none()

# ----------------- Database Implementation-----------------
    with app.app_context():

        db.create_all()
        user = User.query.filter_by(email='admin@gmail.com').first()
        if user:
            pass
        else:
            first_user = User(email = 'admin@gmail.com', name = 'Admin', password = generate_password_hash('admin', method='scrypt'), role='admin')
            db.session.add(first_user)
            db.session.commit()

    app.app_context().push()


    return app