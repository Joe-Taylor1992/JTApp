
# Create a class containing application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'secretkey123'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///pbmisdata.sqlite'    # Database naming structure
    SQLALCHEMY_TRACK_MODIFICATIONS = False                    # Avoids SQLAlchemy warning

    # Flask-User settings
    USER_APP_NAME = "DWP - PBMIS Application Fault Logging System"      # Title of application shown on various pages
    USER_ENABLE_EMAIL = False                                           # Disable email authentication
    USER_ENABLE_USERNAME = True                                         # Authentication performed via username checks and allows users to change their own username
    USER_ENABLE_CHANGE_PASSWORD = True                                  # Enables users to change their own password
    USER_CHANGE_PASSWORD_URL = '/user/change-password'                  # URL to change user password
    USER_AUTO_LOGIN_AFTER_RESET_PASSWORD = True                         # Keeps users logged in upon password reset
    USER_REQUIRE_RETYPE_PASSWORD = True                                 # Forces users to confirm their password upon changing/registering to avoid lockouts
