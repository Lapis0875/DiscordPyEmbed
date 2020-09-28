from __future__ import annotations
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
        if type(item) == self.__class__:
            return super(EmbedType, self).__contains__(item)

        return item in self.__members__


"""
Embed Limit Document
~~~~~~~~~~~~~~~~~~~~
https://discord.com/developers/docs/resources/channel#embed-limits
_______________________________________
title	     |   256 characters
description	 |   2048 characters
fields	     |   Up to 25 field objects
field.name	 |   256 characters
field.value	 |   1024 characters
footer.text	 |   2048 characters
author.name	 |   256 characters
_______________________________________
"""


# URL Validator
def validate_url(value) -> bool:
    return isinstance(value, str) and re.match("^https?", value)


"""
Embed Objects
"""


class EmbedObject(object):
    """
    Represents property object used in discord`s embed structure.
    """

    def __repr__(self) -> str:
        return f"Embed.Object"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EmbedObject:
        raise NotImplementedError("Subclasses should implement the method!")

    def to_dict(self) -> dict:
        return {}


class EmptyObject(EmbedObject):
    """
    Represents `empty` value in embed property.
    """

    def __init__(self, property_name: str, optional: bool = False) -> None:
        self.property_name = property_name
        self.optional = optional

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, bool]]) -> EmptyObject:
        return cls(
            property_name=data.get("property_name"),
            optional=data.get("optional")
        )

    def __str__(self) -> NoReturn:
        if not self.optional:
            raise ValueError(
                f"Embed property '{self.property_name}' cannot be empty!"
            )
        else:
            return f"{self.property_name} is empty."

    def __repr__(self) -> NoReturn:
        return f"Embed.Empty"

    def __len__(self) -> int:
        return 0

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

    def __init__(
            self,
            url: str,
            proxy_url: Optional[str] = None,
            height: Optional[int] = None,
            width: Optional[int] = None
    ) -> None:
        if validate_url(url):
            self.url = url
        else:
            raise ValueError("Invalid url!")

        if validate_url(proxy_url):
            self.proxy_url: Optional[str] = proxy_url
        else:
            self.proxy_url: Optional[str] = None

        self.height = height
        self.width = width

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ImageObject:
        url = data.get("url")
        proxy_url = data.get("proxy_url") or None
        height = data.get("height") or None
        width = data.get("width") or None
        return cls(url, proxy_url, height, width)

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
        return (f"Embed.Image"
                f"(url={self.url}"
                f",proxy_url={self.proxy_url}"
                f",height={self.height}"
                f",width={self.width})")


ThumbnailObject = ImageObject


class VideoObject(EmbedObject):
    """
    Represents video objects on discord Embed.
    """

    def __init__(self, url: str, height: Optional[int] = None, width: Optional[int] = None):
        if validate_url(url):
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
        return f"Embed.Video(url={self.url},height={self.height},width={self.width})"


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
        return f"Embed.Provider(name={self.name},url={self.url})"


class AuthorObject(EmbedObject):
    """
    Represents author objects on discord Embed.
    """

    def __init__(self, name: Optional[str] = None, url: Optional[str] = None, icon_url: Optional[str] = None,
                 proxy_icon_url: Optional[str] = None):
        if type(name) != str or len(name) > 256:
            raise ValueError("Author Object cannot have name longer than 256.")
        self.name = name

        if url is not None and validate_url(url):
            self.url = url
        else:
            raise ValueError("Invalid url!")

        if icon_url is not None and validate_url(icon_url):
            self.icon_url = icon_url
        else:
            raise ValueError("Invalid icon url!")

        if proxy_icon_url is not None and validate_url(proxy_icon_url):
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
        return (f"Embed.Author"
                f"(name={self.name}"
                f",url={self.url}"
                f",icon_url={self.icon_url}"
                f",proxy_icon_url={self.proxy_icon_url})")


class FooterObject(EmbedObject):
    """
    Represents footer objects on discord Embed.
    """

    def __init__(self, text: Optional[str], icon_url: Optional[str],
                 proxy_icon_url: Optional[str] = None):
        self.text = text

        if icon_url is not None and validate_url(icon_url):
            self.icon_url = icon_url
        else:
            raise ValueError("Invalid icon url!")

        if proxy_icon_url is not None and validate_url(proxy_icon_url):
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
        return (f"Embed.Footer"
                f"(text={self.text}"
                f",icon_url={self.icon_url}"
                f",proxy_icon_url={self.proxy_icon_url})")


class Field(EmbedObject):
    """
    Represents field objects on discord Embed.
    """

    def __init__(self, name: str, value: str,
                 inline: Optional[bool] = False):

        if type(name) != str or len(name) > 256:
            raise ValueError("")
        self.name = name
        if type(value) != str or len(value) > 1024:
            raise ValueError("")
        self.value = value
        if type(inline) != bool:
            raise ValueError("")
        self.inline = inline

    def to_dict(self) -> Dict[str, str]:
        result = {
            "name": self.name,
            "value": self.value,
            "inline": self.inline
        }
        return result

    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self) -> str:
        return (f"Embed.Field"
                f"(name={self.name}"
                f",value={self.value}"
                f",inline={self.inline})")


"""
Checks : Check value and return boolean value.
Processes : Process proper object using checks.
"""


def check_title(value) -> bool:
    # Type Check
    return type(value) == str and len(value) <= 256


def process_title(value: str) -> Union[str, NoReturn]:
    if check_title(value):
        return value

    raise ValueError("Embed title must be string object and its length must be lower than 256.")


def check_type(value) -> bool:
    # Type Check
    return value in EmbedType.__members__


def process_type(value: Union[str, EmbedType]) -> Union[EmbedType, NoReturn]:
    if check_type(value):
        return value

    if type(value) == str:
        try:
            return EmbedType[value.upper()]
        except KeyError as e:
            raise KeyError("Unknown Embed Type {}".format(value))

    raise ValueError("Embed type must be EmbedType enum object.")


def check_desc(value) -> bool:
    # Type Check
    return type(value) == str and len(value) <= 2048


def process_desc(value: str) -> str:
    if check_desc(value):
        return value
    raise ValueError("Embed description must be string object and its length must be lower than 2048.")


def process_color(value: Union[Colour, str]) -> Union[Colour, NoReturn]:
    # Type Check
    if isinstance(value, Colour):
        return value
    elif type(value) == str:
        color = getattr(Colour, value, None)
        if isinstance(color, classmethod):
            return color()
        else:
            raise ValueError("Invalid color key is passed.")
    else:
        raise ValueError("Embed color must be discord.Colour object"
                         " or string key which indicates specific discord color.")


def process_author(value: Union[Dict[str, str], AuthorObject]) -> Union[AuthorObject, NoReturn]:
    # Type Check
    if isinstance(value, AuthorObject):
        return value

    elif isinstance(value, dict):
        # Attribute Check
        try:
            name = value.get("name")
            url = value.get("url") or None
            icon_url = value.get("icon_url") or None
            proxy_icon_url = value.get("proxy_icon_url") or None

            return AuthorObject(
                name=name,
                url=url,
                icon_url=icon_url,
                proxy_icon_url=proxy_icon_url
            )

        except KeyError as e:
            raise ValueError(f"Invalid data is passed in Author Object. : {value}. KeyError : {e}")
    else:
        raise TypeError(
            "Author Object must be a dictionary or mapping-like object which contains string keys and string values,"
            " or an AuthorObject."
        )


def process_footer(value) -> Union[FooterObject, NoReturn]:
    # Type Check
    if isinstance(value, FooterObject):
        return value

    elif isinstance(value, dict):
        # Attribute Check
        try:
            text = value.get("text")
            icon_url = value.get("icon_url") or None
            proxy_icon_url = value.get("proxy_icon_url") or None

            return FooterObject(
                text=text,
                icon_url=icon_url,
                proxy_icon_url=proxy_icon_url
            )

        except KeyError as e:
            raise ValueError(f"Invalid data is passed in Footer Object. : {value}. KeyError : {e}")
    else:
        raise TypeError(
            "Footer Object must be a dictionary or mapping-like object which contains string keys and string values,"
            " or an FooterObject."
        )


def process_image(value: Union[ImageObject, Dict[str, str]]) -> Union[ImageObject, NoReturn]:
    if isinstance(value, ImageObject):
        return value
    elif isinstance(value, dict):
        # Attribute Check
        try:
            url = value.get("url")
            proxy_url = value.get("proxy_url") or None
            height = value.get("height") or None
            width = value.get("width") or None

            return ImageObject(
                url=url,
                proxy_url=proxy_url,
                height=height,
                width=width
            )

        except KeyError as e:
            raise ValueError(f"Invalid data is passed in Image Object. : {value}. KeyError : {e}")
    else:
        raise TypeError(
            "Image Object must be a dictionary or mapping-like object which contains string keys and string values,"
            " or an ImageObject."
        )


def process_timestamp(value: datetime) -> Union[datetime, NoReturn]:
    if isinstance(value, datetime):
        return value
    else:
        raise ValueError("Timestamp must be an instance of datetime.")


def check_field(value) -> CHECK:
    if not isinstance(value, dict) or not issubclass(value.__class__, dict):
        raise TypeError(
            "New data must be a dictionary or mapping-like object which contains string keys and string values."
        )
    try:
        e_name = value.get("name")
        if type(e_name) != str or len(e_name) > 256:
            raise ValueError("")
        e_value = value.get("value")
        if type(e_value) != str or len(e_value) > 1024:
            raise ValueError
        e_inline = value.get("inline") or None
    except KeyError:
        raise InvalidFieldError(
            invalid_field=value
        )
    except ValueError as e:
        # Catch embed limit error and throw it to outside.
        raise e

    # All check finished. Return True.
    return True


def check_fields(value) -> CHECK:
    if not isinstance(value, list) or not issubclass(value.__class__, list):
        raise TypeError("New data must be a dictionary which contains string keys and string values.")

    if len(value) > 25:
        raise ValueError("Embed fields limit : the number of fields must be lower than 25.")

    for field in value:
        check = check_field(field)
        if not check:
            raise InvalidFieldError(
                invalid_field=field
            )

    # All check finished. Return True.
    return True