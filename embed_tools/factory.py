from typing import List, Dict, Union
from .exceptions import *
from .properties import *
from discord import Embed, Member, User, ClientUser
from tools import datetime_tostring


FIELD = Dict[str, Union[str, bool]]
ANY_USER = Union[User, Member, ClientUser]


class EmbedFactory(object):
    # Log colors
    default_color: Colour = Colour.from_rgb(236, 202, 179)  # latte color
    warning_color: Colour = Colour.gold()
    error_color: Colour = Colour.red()

    def __init__(self, **attrs):
        self.target_cls = Embed.__class__
        self._title: str = (
            attrs.pop("title")
            if "title" in attrs and check_title(attrs["title"])
            else EmptyObject("title", optional=False)
        )
        self._type: str = (
            attrs.pop("type")
            if "type" in attrs and check_type(attrs["type"])
            else "rich"
        )
        self._description: str = (
            attrs.pop("description")
            if "description" in attrs and check_desc(attrs["description"])
            else EmptyObject("description", optional=True)
        )
        self._color: Colour = (
            attrs.pop("color")
            if "color" in attrs and check_color(attrs["color"])
            else self.default_color
        )
        self._author: Dict[str, str] = (
            attrs.pop("author")
            if "author" in attrs and check_author(attrs["author"])
            else EmptyObject("author", optional=True)
        )
        self._footer: Dict[str, str] = (
            attrs.pop("footer")
            if "footer" in attrs and check_footer(attrs["footer"])
            else EmptyObject("footer", optional=True)
        )
        self._timestamp: datetime = (
            attrs.pop("timestamp")
            if "timestamp" in attrs and check_timestamp(attrs["timestamp"])
            else EmptyObject("timestamp", optional=True)
        )
        self._url: str = (
            attrs.pop("url")
            if "url" in attrs and check_timestamp(attrs["url"])
            else EmptyObject("url", optional=True)
        )
        self._thumbnail_url: str = (
            attrs.pop("thumbnail_url")
            if "thumbnail_url" in attrs and check_url(attrs["thumbnail_url"])
            else EmptyObject("thumbnail_url", optional=True)
        )
        self._thumbnail: Union[ImageObject, EmptyObject] = (
            attrs.pop("thumbnail")
            if "thumbnail" in attrs and check_image(attrs["thumbnail"])
            else EmptyObject("thumbnail", optional=True)
        )
        self._image: ImageObject = (
            attrs.pop("image")
            if "image" in attrs and check_image(attrs["image"])
            else EmptyObject("image", optional=True)
        )
        self._fields: List[Dict[str, str]] = (
            attrs.pop("fields")
            if "fields" in attrs and check_fields(attrs["fields"])
            else []
        )
        if attrs:
            raise UnexpectedKwargsError(unexpected_kwargs=attrs)

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> NoReturn:
        # Type Check & Value Assign
        if check_title(value):
            self._title = value

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str) -> NoReturn:
        # Type Check & Value Assign
        if check_type(value):
            self._type = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> NoReturn:
        # Type Check & Value Assign
        if check_desc(value):
            self._description = value

    @property
    def color(self) -> Colour:
        return self._color

    @color.setter
    def color(self, value: Colour) -> NoReturn:
        if check_color(value):
            self._color = value
        else:
            raise InvalidColorError(invalid_color=value)

    @property
    def author(self) -> Dict[str, str]:
        return self._author

    @author.setter
    def author(self, value: Dict[str, str]) -> NoReturn:
        if check_author(value):
            # Value Assign
            self._author = {
                "name": value["name"],
                "icon_url": value["icon_url"]
            }
            if "url" in value:
                self._author.update(
                    {
                        "url": value["url"]
                    }
                )

    @property
    def footer(self) -> Dict[str, str]:
        return self._footer

    @footer.setter
    def footer(self, value: Dict[str, str]) -> NoReturn:
        if check_footer(value):
            # Value Assign
            self._author = {
                "text": value["text"],
                "icon_url": value["icon_url"]
            }

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value) -> NoReturn:
        if check_timestamp(value):
            self._timestamp = value

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value) -> NoReturn:
        if check_url(value):
            self._url = value

    @property
    def thumbnail(self) -> ImageObject:
        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, value: Union[ImageObject, str]) -> NoReturn:
        # Type Check & Value Assign
        if check_image(value):
            self._image = value
        elif check_url(value):
            self._image = ImageObject(url=value)

    @property
    def thumbnail_url(self) -> str:
        return self._thumbnail_url

    @thumbnail_url.setter
    def thumbnail_url(self, value: str) -> NoReturn:
        # Type Check & Value Assign
        self._thumbnail_url = value if type(value) == str else str(value)

    @property
    def image(self) -> ImageObject:
        return self._image

    @image.setter
    def image(self, value: Union[ImageObject, str]) -> NoReturn:
        # Type Check & Value Assign
        if check_image(value):
            self._image = value
        elif check_url(value):
            self._image = ImageObject(url=value)

    @property
    def fields(self) -> List[FIELD]:
        return self._fields

    @fields.setter
    def fields(self, value: List[FIELD]) -> NoReturn:
        # Type Check
        if check_fields(value):
            # Value Assign
            self._fields.extend(value)

    async def add_field(self, name, value, inline=False):
        if type(name) != str or type(value) != str:
            raise TypeError("Invalid type of parameter was passed in method : "
                            "EmbedFactory.add_field(str, str, bool")
        self.fields.append({"name": name, "value": value, "inline": inline})

    async def add_fields(self, *fields: FIELD) -> NoReturn:
        for field in fields:
            if check_fields(field):

                # Instead of appending `field` itself, append values using "name" and "value" key
                # to prevent unexpected key in field.
                await self.add_field(
                    name=field["name"],
                    value=field["value"],
                    inline=field["inline"] if "inline" in field.keys() else False
                )
            else:
                raise InvalidFieldError(invalid_field=field)

    async def build(self) -> Embed:
        embed = Embed(
            title=self.title,
            description=self.description,
            color=self.color
        )

        if self.thumbnail_url != "":
            embed.set_thumbnail(url=self.thumbnail_url)

        if self.image:
            embed.set_image(url=self.image.url)

        if self.author["name"] != "" and self.author["icon_url"] != "":
            embed.set_author(name=self.author["name"], icon_url=self.author["icon_url"])

        for field in self.fields:
            embed.add_field(name=field["name"], value=field["value"],
                            inline=bool(field["inline"]) if "inline" in field else False)

        if self.footer["text"] != "" and self.footer["icon_url"] != "":
            embed.set_footer(text=self.footer["text"], icon_url=self.footer["icon_url"])

        return embed

    async def build(self) -> Embed:
        data: Dict[str, Union[str, Colour, Dict[str, Union[str, bool]], datetime]] = {
            "title": self.title,
            "type": self.type,
            "color": self.color
        }
        if self.description:
            data["description"] = self.description
        if self.author:
            data["author"] = self.author
        if self.footer:
            data["footer"] = self.footer
        if self.timestamp:
            data["timestamp"] = datetime_tostring(self.timestamp)
        if self.url:
            data["url"] = self.url
        if self.thumbnail_url:
            data["thumbnail"] = {
                "url": self.thumbnail_url
            }
        if self.image:
            data["image"] = self.image.to_dict()
        return Embed.from_dict(
            data=data
        )

    @classmethod
    def get_user_info(cls, user: ANY_USER, contain_id: bool = True) -> Optional[str]:
        if user is None:
            return None
        return f"{user.name}#{user.discriminator}" + f" ({user.id})" if contain_id else ''

    @classmethod
    def get_command_caller(cls, user: ANY_USER) -> Dict[str, str]:
        return {
            "text": f"command executed by {cls.get_user_info(user=user)}",
            "icon_url": user.avatar_url
        }

    @classmethod
    def LOG_EMBED(cls, title: str, description: str) -> Embed:
        return Embed(
            title=title,
            description=description,
            colour=cls.default_color
        )

    @classmethod
    def COMMAND_LOG_EMBED(cls, title: str, description: str, user: ANY_USER) -> Embed:
        embed = cls.LOG_EMBED(title=title, description=description)
        command_caller_info: Dict[str, str] = cls.get_command_caller(user)
        embed.set_footer(text=command_caller_info["text"], icon_url=command_caller_info["icon_url"])
        return embed

    @classmethod
    def WARN_EMBED(cls, title: str, description: str) -> Embed:
        return Embed(
            title=title,
            description=description,
            colour=cls.error_color
        )

    @classmethod
    def ERROR_EMBED(cls, e: Exception) -> Embed:
        return Embed(
            title="오류가 발생했습니다!",
            description=f"Error content : \n{e.with_traceback(e.__traceback__)}",
            colour=cls.error_color
        )

    def __str__(self) -> str:
        text = (
            f"title={self.title}\n"
            f"description={self.description}\n"
            f"author={self.author}\n"
            f"thumbnail={self.thumbnail.to_dict()}\n"
            f"image={self.image.to_dict()}\n"
            f"footer={self.footer}\n"
            f"fields=[\n")
        text += '  \n'.join(str(field) for field in self.fields) + "\n]"
        return text

    def to_string(self) -> str:
        return self.__str__()