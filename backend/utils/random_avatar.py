import io
import random

import py_avataaars
from PIL import Image
from django.core.files import File

from utils.model_utils import create_random_text


class GirlTopType(py_avataaars.AvatarEnum):
    HIJAB = 'HIJAB'
    WINTER_HAT4 = 'WINTER_HAT4'
    LONG_HAIR_BIG_HAIR = 'LONG_HAIR_BIG_HAIR'
    LONG_HAIR_BOB = 'LONG_HAIR_BOB'
    LONG_HAIR_BUN = 'LONG_HAIR_BUN'
    LONG_HAIR_CURLY = 'LONG_HAIR_CURLY'
    LONG_HAIR_CURVY = 'LONG_HAIR_CURVY'
    LONG_HAIR_DREADS = 'LONG_HAIR_DREADS'
    LONG_HAIR_FRIDA = 'LONG_HAIR_FRIDA'
    LONG_HAIR_FRO = 'LONG_HAIR_FRO'
    LONG_HAIR_FRO_BAND = 'LONG_HAIR_FRO_BAND'
    LONG_HAIR_NOT_TOO_LONG = 'LONG_HAIR_NOT_TOO_LONG'
    LONG_HAIR_MIA_WALLACE = 'LONG_HAIR_MIA_WALLACE'
    LONG_HAIR_SHAVED_SIDES = 'LONG_HAIR_SHAVED_SIDES'
    LONG_HAIR_STRAIGHT = 'LONG_HAIR_STRAIGHT'
    LONG_HAIR_STRAIGHT2 = 'LONG_HAIR_STRAIGHT2'
    LONG_HAIR_STRAIGHT_STRAND = 'LONG_HAIR_STRAIGHT_STRAND'


class BoyTopType(py_avataaars.AvatarEnum):
    NO_HAIR = 'NO_HAIR'
    EYE_PATCH = 'EYE_PATCH'
    HAT = 'HAT'
    TURBAN = 'TURBAN'
    WINTER_HAT1 = 'WINTER_HAT1'
    WINTER_HAT2 = 'WINTER_HAT2'
    WINTER_HAT3 = 'WINTER_HAT3'
    SHORT_HAIR_DREADS_01 = 'SHORT_HAIR_DREADS_01'
    SHORT_HAIR_DREADS_02 = 'SHORT_HAIR_DREADS_02'
    SHORT_HAIR_FRIZZLE = 'SHORT_HAIR_FRIZZLE'
    SHORT_HAIR_SHAGGY_MULLET = 'SHORT_HAIR_SHAGGY_MULLET'
    SHORT_HAIR_SHORT_CURLY = 'SHORT_HAIR_SHORT_CURLY'
    SHORT_HAIR_SHORT_FLAT = 'SHORT_HAIR_SHORT_FLAT'
    SHORT_HAIR_SHORT_ROUND = 'SHORT_HAIR_SHORT_ROUND'
    SHORT_HAIR_SHORT_WAVED = 'SHORT_HAIR_SHORT_WAVED'
    SHORT_HAIR_SIDES = 'SHORT_HAIR_SIDES'
    SHORT_HAIR_THE_CAESAR = 'SHORT_HAIR_THE_CAESAR'
    SHORT_HAIR_THE_CAESAR_SIDE_PART = 'SHORT_HAIR_THE_CAESAR_SIDE_PART'


class GirlFacialHairType(py_avataaars.AvatarEnum):
    DEFAULT = 'DEFAULT'


class FacialHairType(py_avataaars.AvatarEnum):
    BEARD_MEDIUM = 'BEARD_MEDIUM'
    BEARD_LIGHT = 'BEARD_LIGHT'
    BEARD_MAJESTIC = 'BEARD_MAJESTIC'
    MOUSTACHE_FANCY = 'MOUSTACHE_FANCY'
    MOUSTACHE_MAGNUM = 'MOUSTACHE_MAGNUM'


def random_avatar(gender):

    def r(enum_):
        return random.choice(list(enum_))

    if gender == 'male':
        avatar_kwargs = dict(
            facial_hair_type=r(FacialHairType),
            top_type=r(BoyTopType),
        )
    elif gender == 'female':
        avatar_kwargs = dict(
            facial_hair_type=GirlFacialHairType.DEFAULT,
            top_type=r(GirlTopType),
        )
    else:
        avatar_kwargs = dict(
            facial_hair_type=r(py_avataaars.FacialHairType),
            top_type=r(py_avataaars.TopType),
        )

    avatar = py_avataaars.PyAvataaar(
        style=py_avataaars.AvatarStyle.CIRCLE,
        skin_color=r(py_avataaars.SkinColor),
        hair_color=r(py_avataaars.HairColor),
        mouth_type=r(py_avataaars.MouthType),
        eye_type=r(py_avataaars.EyesType),
        eyebrow_type=r(py_avataaars.EyebrowType),
        nose_type=r(py_avataaars.NoseType),
        accessories_type=r(py_avataaars.AccessoriesType),
        clothe_type=r(py_avataaars.ClotheType),
        clothe_graphic_type=r(py_avataaars.ClotheGraphicType),
        **avatar_kwargs
    )
    __bytes = io.BytesIO()
    avatar.render_png_file(__bytes)
    img = Image.open(__bytes)
    # Save Image
    img.resize((500, 500))
    img.save(__bytes, "PNG", quality=80)
    final = File(__bytes)
    # Get Extension
    ext = img.get_format_mimetype().split("/")[-1]
    return final, create_random_text(10) + "." + ext
