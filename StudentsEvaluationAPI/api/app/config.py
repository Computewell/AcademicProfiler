import os


# class Settings:
#     db_hostname: str = os.environ.get('O__HOSTNAME')
#     db_port: str = os.environ.get('O_DB_PORT')
#     db_password: str = os.environ.get('O__PASSWORD')
#     db_username: str = os.environ.get('O__USERNAME')
#     db_name: str = os.environ.get('O__NAME')
#     secret_key: str = os.environ.get('SECRET_KEY')
#     algorithm: str = os.environ.get('ALGORITHM')
#     access_tok_expire_minutes: int = os.environ.get('ACCESS_TOK_EXPIRE_MINUTES')
#     cloudinary_cloud_name: str = os.environ.get('O_CLOUDINARY_CLOUD_NAME')
#     cloudinary_api_key: str = os.environ.get('O_CLOUDINARY_API_KEY')
#     cloudinary_api_secret: str = os.environ.get('O_CLOUDINARY_API_SECRET')
#
#
# settings = Settings()

class Settings:
    db_hostname: str = os.environ.get('O_DB_HOSTNAME')
    db_port: str = os.environ.get('O_DB_PORT')
    db_password: str = os.environ.get('O_DB_PASSWORD')
    db_username: str = os.environ.get('O_DB_USERNAME')
    db_name: str = os.environ.get('O_DB_NAME')
    secret_key: str = os.environ.get('SECRET_KEY')
    algorithm: str = os.environ.get('ALGORITHM')
    access_tok_expire_minutes: int = os.environ.get('ACCESS_TOK_EXPIRE_MINUTES')
    cloudinary_cloud_name: str = os.environ.get('O_CLOUDINARY_CLOUD_NAME')
    cloudinary_api_key: str = os.environ.get('O_CLOUDINARY_API_KEY')
    cloudinary_api_secret: str = os.environ.get('O_CLOUDINARY_API_SECRET')


settings = Settings()
