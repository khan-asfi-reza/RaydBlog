import os
import random
import string
import time
import urllib.request
from io import BytesIO
from tempfile import NamedTemporaryFile
import cairosvg
from PIL import Image
from cairosvg import svg2png
from django.core.files import File
from Main import settings
import re


# User Name Validation Function, checks if username is correct or not
# Valid format :- Username can contain letters and characters along with underscore(_)
# Cannot be digit or start with _ or -
def username_validator(username: str):
    from Main.username_blacklist import blacklisted_usernames

    if username[0] == "_" or username[0] == "-":
        return False

    if username.isdigit():
        return False

    if username == any(blacklisted_usernames):
        return False

    rx = "^[A-Za-z0-9_]*$"

    return bool(re.match(rx, username))


def has_chars(text: str):
    return any(s.isalpha() for s in text)


def file_location(instance, file: str):
    file_ext = file.split(".")[-1]
    new_file = str(instance.user.id) + \
               str(random.randrange(0, 100)) + str(
        int(time.time()) + int(10 * 16 * time.time() - int(time.time()))) + str(create_random_text(15)) + "." + \
               file_ext
    return f"{instance.user.id}/{new_file}"


EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def is_email(email):
    return re.fullmatch(EMAIL_REGEX, email)


def compress(image) -> File:
    extension = image.name.split(".")[-1]

    if extension == "svg":
        __byte = BytesIO()
        svg2png(bytestring=image, write_to=__byte)
        img = Image.open(__byte)
    else:
        img = Image.open(image)

    # Create BytesIo Object
    img_io = BytesIO()
    # Save Image to bytes io obj
    img.save(img_io, "PNG", quality=70)
    # New Image
    return File(img_io, name=image.name)


def create_random_text(length: int = 20) -> str:
    ascii_lower = string.ascii_lowercase
    text = "".join([ascii_lower[random.randrange(len(ascii_lower))] for i in range(length)])
    text.capitalize()
    return text


def create_random_length_number(length: int = 10) -> int:
    return random.randrange((10 ** length) - 1)


def generate_random_image(*args):
    url = f"https://avatars.dicebear.com/api/avataaars/{create_random_text(10)}.svg"
    url = urllib.request.urlopen(url)
    # Created Temporary File
    img_temp = NamedTemporaryFile(delete=False, suffix=".svg", dir=settings.FILE_UPLOAD_TEMP_DIR)
    # Write To file
    img_temp.write(url.read())
    # Flush Temporary
    img_temp.flush()
    # Return File
    file = File(img_temp)
    __byte = BytesIO()
    img_temp.close()
    # Convert To Png
    cairosvg.svg2png(file_obj=open(file.name, "rb"), write_to=__byte)
    # Open Image and compress
    img = Image.open(__byte)
    # Save Image
    img.resize((500, 500))
    img.save(__byte, "PNG", quality=80)
    # Remove Temp
    os.remove(img_temp.name)
    final = File(__byte)
    # Get Extension
    ext = img.get_format_mimetype().split("/")[-1]
    return final, create_random_text(10) + "." + ext


def as_dict(cls):
    return {key: value for key, value in cls.__dict__.items() if not key.startswith('__') and not callable(key)}


def check_email(email):
    # Make a regular expression
    # for validating an Email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, email)
