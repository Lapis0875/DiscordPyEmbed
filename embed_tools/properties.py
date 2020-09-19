from .exceptions import *
from typing import Dict, Optional
from datetime import datetime
from enum import Enum
from typing import Union, NoReturn
from discord import Colour
import re

"""
Checks
~~~~~~
Check values to build proper embed property.
"""

CHECK = Union[bool, NoReturn]


class EmbedType(Enum):
    RICH = "rich"
    IMAGE = "image"
    VIDEO = "video"
    GIFV = "gifv"
    ARTICLE = "article"
    LINK = "link"

    def __contains__(self, item):
        """
        Override `in` keyword to check Embed`s type value.
        :param item:
        :return:
        """
        return item in self._member_map_


def check_title(value) -> bool:
    # Type Check
    # TODO : add a check to count text length (embed title limit)
    return isinstance(value, str)


def check_type(value) -> bool:
    # Type Check
    return isinstance(value, EmbedType) and value in EmbedType


def check_desc(value) -> bool:
    # Type Check
    return isinstance(value, str)


def check_color(value) -> bool:
    # Type Check
    if isinstance(value, Colour):
        return True


def check_author(value) -> CHECK:
    # Type Check
    if not isinstance(value, dict) or not issubclass(value.__class__, dict):
        raise TypeError(
            "New data must be a dictionary or mapping-like object which contains string keys and string values."
        )

    # Attribute Check
    if "name" not in value.keys() or "icon_url" not in value.keys():
        raise AttributeError(f"Invalid data is passed in author property. : {value}")

    # All check finished. Return True.
    return True


def check_footer(value) -> CHECK:
    # Type Check
    if not isinstance(value, dict) or not issubclass(value.__class__, dict):
        raise TypeError(
            "New data must be a dictionary or mapping-like object which contains string keys and string values."
        )

    # Attribute Check
    if not ("text" in value.keys() and "icon_url" in value.keys()):
        raise AttributeError(f"Invalid data is passed in footer property. : {value}")

    # All check finished. Return True.
    return True


def check_url(value) -> bool:
    return isinstance(value, str) and re.match("^https?", value)


def check_image(value) -> bool:
    return isinstance(value, ImageObject)


def check_timestamp(value) -> bool:
    return isinstance(value, datetime)


def check_field(value) -> CHECK:
    if not isinstance(value, dict) or not issubclass(value.__class__, dict):
        raise TypeError(
            "New data must be a dictionary or mapping-like object which contains string keys and string values."
        )
    try:
        e_name = value.get("name")
        e_value = value.get("value")
    except KeyError:
        raise InvalidFieldError(
            invalid_field=value
        )

    # All check finished. Return True.
    return True


def check_fields(value) -> CHECK:
    if not isinstance(value, list) or not issubclass(value.__class__, list):
        raise TypeError("New data must be a dictionary which contains string keys and string values.")

    for field in value:
        check = check_field(field)
        if not check:
            raise InvalidFieldError(
                invalid_field=field
            )

    # All check finished. Return True.
    return True


"""
Embed Objects
~~~~~~~~~~~~~

"""


class EmbedObject(object):
    """
    Represents property object used in discord`s embed structure.
    """

    def __repr__(self) -> str:
        return f"<EmbedProperty:Base>"


class EmptyObject(EmbedObject):
    """
    Represents `empty` value in embed property.
    """

    def __init__(self, property_name: str, optional: bool = False) -> None:
        self.property_name = property_name
        self.optional = optional

    def __str__(self) -> NoReturn:
        if not self.optional:
            raise ValueError(
                f"Embed property '{self.property_name}' cannot be empty!"
            )
        else:
            return f"{self.property_name} is empty."

    def __repr__(self) -> NoReturn:
        return f"<EmbedProperty:Empty>"

    def __bool__(self) -> bool:
        """
        Tool to check whether property is empty or not.
        :return: Always True, because this class always represents empty value.
        """
        return False


class ImageObject(EmbedObject):
    """
    Represents image objects on discord Embed.
    Can be used at 'image', 'thumbnail' property (They share same options)
    """

    def __init__(self, url: str, proxy_url: Optional[str] = None, height: Optional[int] = None,
                 width: Optional[int] = None):
        if check_url(url):
            self.url = url
        else:
            raise ValueError("Invalid url!")

        if check_url(proxy_url):
            self.proxy_url: Optional[str] = proxy_url
        else:
            self.proxy_url: Optional[str] = None

        self.height = height
        self.width = width

    def to_dict(self) -> Dict[str, str]:
        result = {
            "url": self.url
        }
        if self.proxy_url is not None:
            result["proxy_url"] = self.proxy_url
        if self.height is not None:
            result["height"] = self.height
        if self.width is not None:
            result["width"] = self.width
        return result

    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self) -> str:
        return (f"<EmbedProperty:Image"
                f",url={self.url}"
                f",proxy_url={self.proxy_url}"
                f",height={self.height}"
                f",width={self.width}>")


ThumbnailObject = ImageObject


class VideoObject(EmbedObject):
    """
    Represents video objects on discord Embed.
    """

    def __init__(self, url: str, height: Optional[int] = None, width: Optional[int] = None):
        if check_url(url):
            self.url = url
        else:
            raise ValueError("Invalid url!")

        self.height = height
        self.width = width

    def to_dict(self) -> Dict[str, str]:
        result = {
            "url": self.url
        }
        if self.height is not None:
            result["height"] = self.height
        if self.width is not None:
            result["width"] = self.width
        return result

    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self) -> str:
        return f"<EmbedProperty:Video,url={self.url},height={self.height},width={self.width}>"


class ProviderObject(EmbedObject):
    """
    Represents provider objects on discord Embed.
    """
    def __init__(self, name: str, url: str) -> None:
        self.name = name
        self.url = url

    def to_dict(self) -> Dict[str, str]:
        result = {
            "name": self.name,
            "url": self.url
        }
        return result

    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self) -> str:
        return f"<EmbedProperty:Provider,name={self.name},url={self.url}>"


class AuthorObject(EmbedObject):
    """
    Represents author objects on discord Embed.
    """

    def __init__(self, name: Optional[str], url: Optional[str], icon_url: Optional[str],
                 proxy_icon_url: Optional[str] = None):
        self.name = name

        if url is not None and check_url(url):
            self.url = url
        else:
            raise ValueError("Invalid url!")

        if icon_url is not None and check_url(icon_url):
            self.icon_url = icon_url
        else:
            raise ValueError("Invalid icon url!")

        if proxy_icon_url is not None and check_url(proxy_icon_url):
            self.proxy_icon_url = proxy_icon_url
        else:
            raise ValueError("Invalid proxy icon url!")

    def to_dict(self) -> Dict[str, str]:
        result = {
            "name": self.name,
            "url": self.url,
            "icon_url": self.icon_url,
            "proxy_icon_url": self.proxy_icon_url
        }
        return result

    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self) -> str:
        return (f"<EmbedProperty:Author"
                f",name={self.name}"
                f",url={self.url}"
                f",icon_url={self.icon_url}"
                f",proxy_icon_url={self.proxy_icon_url}>")


class FooterObject(EmbedObject):
    """
    Represents footer objects on discord Embed.
    """

    def __init__(self, text: Optional[str], icon_url: Optional[str],
                 proxy_icon_url: Optional[str] = None):
        self.text = text

        if icon_url is not None and check_url(icon_url):
            self.icon_url = icon_url
        else:
            raise ValueError("Invalid icon url!")

        if proxy_icon_url is not None and check_url(proxy_icon_url):
            self.proxy_icon_url = proxy_icon_url
        else:
            raise ValueError("Invalid proxy icon url!")

    def to_dict(self) -> Dict[str, str]:
        result = {
            "text": self.text,
            "icon_url": self.icon_url,
            "proxy_icon_url": self.proxy_icon_url
        }
        return result

    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self) -> str:
        return (f"<EmbedProperty:Footer"
                f",text={self.text}"
                f",icon_url={self.icon_url}"
                f",proxy_icon_url={self.proxy_icon_url}>")


class Field(EmbedObject):
    """
    Represents field objects on discord Embed.
    """

    def __init__(self, text: Optional[str], icon_url: Optional[str],
                 proxy_icon_url: Optional[str] = None):
        self.text = text

        if icon_url is not None and check_url(icon_url):
            self.icon_url = icon_url
        else:
            raise ValueError("Invalid icon url!")

        if proxy_icon_url is not None and check_url(proxy_icon_url):
            self.proxy_icon_url = proxy_icon_url
        else:
            raise ValueError("Invalid proxy icon url!")

    def to_dict(self) -> Dict[str, str]:
        result = {
            "text": self.text,
            "icon_url": self.icon_url,
            "proxy_icon_url": self.proxy_icon_url
        }
        return result

    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self) -> str:
        return (f"<EmbedObject:Field"
                f",text={self.text}"
                f",icon_url={self.icon_url}"
                f",proxy_icon_url={self.proxy_icon_url}>")

