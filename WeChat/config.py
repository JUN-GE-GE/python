import os

config_path = os.path.abspath(os.path.dirname(__file__))
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL","sqlite:///" + os.path.join(config_path, 'WeChat.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'abc123')
    CHAT_PER_PAGE = os.environ.get('CHAT_PER_PAGE', 5)

    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@WeChst.com')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 1)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'username')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'password')
    MAIL_SUBJECT_RESET_PASSWORD = '[WeChst] Please Reset Your Password'
    MAIN_SUBJECT_USER_ACTIVATE = '[WeChst] Please Activate Your Accout'