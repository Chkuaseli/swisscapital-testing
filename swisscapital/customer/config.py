import os
# from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class

basedir = os.path.abspath(os.path.dirname(__file__))
# image = os.path.join(basedir,'static/images')
class Config:
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:user13@localhost/swisscapital'
    SQLALCHEMY_TRACK_MODIFICATIONS =False
    SECRET_KEY = 'swisscapital' 
#     # photos 
    UPLOADED_PHOTOS_DEST = os.path.join(basedir,'static/images')
#     DROPZONE_ALLOWED_FILE_TYPE = 'image/*'
