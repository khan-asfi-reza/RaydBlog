import os

from dotenv import load_dotenv

load_dotenv()

IS_PROD = int(os.environ.get("IS_PROD", 0)) == 1
DB_NAME = os.environ.get("DB_NAME", "DB_NAME")
DB_HOST = os.environ.get("DB_HOST", "DB_HOST")
DB_PORT = os.environ.get("DB_PORT", "DB_PORT")
DB_USER = os.environ.get("DB_USER", "DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "DB_PASSWORD")
SECRET_KEY = os.environ.get("SECRET_KEY", "SECRET_KEY")
ENCRYPTION_KEY = bytes(os.environ.get("ENCRYPTION_KEY", "ENCRYPTION_KEY"), "utf-8")
FEND_FP_URL = os.environ.get("FEND_FP_URL", "http:://localhost:3000")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
WHITELIST_URL = os.environ.get("WHITELIST_URL", "http:://localhost:3000")
TEST_EMAIL = os.environ.get("TEST_EMAIL", "")
USE_AWS = int(os.environ.get("USE_AWS", 0)) == 1

if USE_AWS:
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_ID", "")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY", "")
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', "")

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
