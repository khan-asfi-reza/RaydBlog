from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


# Static Storage Amazon - S3
class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION


# Media Storage Amazon - S3
class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
