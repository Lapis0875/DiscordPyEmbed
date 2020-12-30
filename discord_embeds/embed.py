from typing import List, Dict, Union, Optional
from .exceptions import *
from .objects import *
from discord import Member, User, ClientUser, Colour
from discord import Embed as DiscordEmbed

ANY_USER = Union[User, Member, ClientUser]

"""
ExtendedEmbed Structure
________________________________________________________________________________________________
Field         | Type                          | Description
________________________________________________________________________________________________
title?        | string (<=256 characters)     | title of embed
type?         | string (<=2048 characters)    | type of embed (always "rich" for webhook embeds)
description?  | string                        | description of embed
url?          | string                        | url of embed
timestamp?    | ISO8601 timestamp             | timestamp of embed content
color?        | integer                       | color code of the embed
footer?       | embed footer object           | footer information
image?        | embed image object            | image information
thumbnail?    | embed thumbnail object        | thumbnail information
video?        | embed video object            | video information
provider?     | embed provider object         | provider information
author?       | embed author object           | author information
fields?       | array of embed field objects  | fields information
________________________________________________________________________________________________
* fields must contain same or less than 25 field objects. (Discord limit)
"""


class Embed(DiscordEmbed):
    def __init__(self,
                 embed_type: Optional[EmbedType] = EmbedType.RICH,
                 title: Optional[str] = "",
                 url: Optional[str] = None,
                 description: Optional[str] = "",
                 color: Optional[Colour] = Colour.blurple(),
                 timestamp: Optional[datetime] = None,
                 author: Optional[Union[AuthorObject, Dict[str, str], None]] = None,
                 footer: Optional[Union[FooterObject, Dict[str, str], None]] = None,
                 thumbnail: Optional[Union[ThumbnailObject, Dict[str, Union[str, int]], None]] = None,
                 image: Optional[Union[ThumbnailObject, Dict[str, Union[str, int]], None]] = None,
                 provider: Optional[Union[ProviderObject, Dict[str, Any]]] = None,
                 fields: Optional[Union[Fields, List[Field]]] = None
                 ):
        self._type: EmbedType = embed_type if embed_type in EmbedType else EmbedType.from_value(embed_type)
        self._title: str = process_title(title)
        self._url: str = url if validate_url(url) else None
        self._description: str = process_desc(description)

        if isinstance(color, Colour):
            self._color = color
        elif isinstance(color, str):
            color = getattr(Colour, color, None)
            if isinstance(color, classmethod):
                self._color = color()
            else:
                self._color = Colour.blurple()
                raise ValueError("Invalid color key is passed.")

        self._timestamp: datetime = timestamp if type(timestamp) == datetime else None
        self._author: AuthorObject = author if isinstance(author, AuthorObject) else AuthorObject.fromDict(author)
        self._footer: FooterObject = footer if isinstance(footer, FooterObject) else FooterObject.fromDict(footer)
        self._thumbnail: ImageObject = thumbnail if isinstance(thumbnail, ImageObject) else ImageObject.fromDict(
            thumbnail)
        self._image: ImageObject = image if isinstance(image, ImageObject) else ImageObject.fromDict(image)
        self._provider: ProviderObject = provider if isinstance(provider,
                                                                ProviderObject) else ProviderObject.fromDict(provider)
        self._fields: Fields = Fields.fromDict(fields)

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> NoReturn:
        # Type Check & Value Assign
        self._title = process_title(value)

    @property
    def type(self) -> EmbedType:
        return self._type

    @type.setter
    def type(self, value: str) -> NoReturn:
        # Type Check & Value Assign
        self._type = EmbedType.from_value(value)

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
        if isinstance(value, Colour):
            self._color = value
        else:
            self._color = process_color(value)

    @property
    def author(self) -> AuthorObject:
        return self._author

    @author.setter
    def author(self, value: AuthorObject) -> NoReturn:
        self._author = AuthorObject.fromDict(value)

    @property
    def footer(self) -> Dict[str, str]:
        return self._footer

    @footer.setter
    def footer(self, value: Dict[str, str]) -> NoReturn:
        self._footer = FooterObject.fromDict(value)

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value) -> NoReturn:
        if isinstance(value, datetime):
            self._timestamp = value
        else:
            raise TypeError("Timestamp object must be an instance of datetime")

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value) -> NoReturn:
        if validate_url(value):
            self._url = value

    @property
    def thumbnail(self) -> ImageObject:
        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, value: Union[ImageObject, str]) -> NoReturn:
        # Type Check & Value Assign
        try:
            self._thumbnail = ImageObject.fromDict(value)
        except:
            if validate_url(value):
                self._thumbnail = ImageObject(url=value)
            else:
                raise

    @property
    def image(self) -> ImageObject:
        return self._image

    @image.setter
    def image(self, value: Union[ImageObject, str]) -> NoReturn:
        # Type Check & Value Assign
        try:
            self._image = ImageObject.fromDict(value)
        except:
            if validate_url(value):
                self._image = ImageObject(url=value)
            else:
                raise

    @property
    def fields(self) -> List[Field]:
        return self._fields

    @fields.setter
    def fields(self, value: List[Field]) -> NoReturn:
        # Type Check
        self._fields = Fields.fromDict(value)

        if check_fields(value):
            # Value Assign
            self._fields.extend(value)

    async def add_field(self, name, value, inline=False):
        if type(name) != str or type(value) != str:
            raise TypeError("Invalid type of parameter was passed in method : "
                            "EmbedFactory.add_field(str, str, bool")
        self.fields.append({"name": name, "value": value, "inline": inline})

    async def add_fields(self, *fields: Field) -> NoReturn:
        for field in fields:
            field = Field.fromDict(field)
            # Instead of appending `field` itself, append values using "name" and "value" key
            # to prevent unexpected key in field.
            await self.add_field(
                name=field["name"],
                value=field["value"],
                inline=field["inline"]
            )

    async def convert(self) -> DiscordEmbed:
        """
        Convert this embed object to discord.py's embed object.
        :return:
        """
        embed = DiscordEmbed(
            title=self.title,
            description=self.description,
            color=self.color
        )

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

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Union[str, Colour, Dict[str, Union[str, bool]], datetime]] = {
            "title": self.title,
            "type": self.type,
            "color": self.color
        }
        if self.description:
            data["description"] = self.description
        if self.author:
            data["author"] = self.author.toDict()
        if self.footer:
            data["footer"] = self.footer.to_dict()
        if self.timestamp:
            data["timestamp"] = str(self.timestamp)
        if self.url:
            data["url"] = self.url
        if self.thumbnail:
            data["thumbnail"]
        if self.image:
            data["image"] = self.image.toDict()
        return data

    @classmethod
    def LOG_EMBED(cls, title: str, description: str) -> "Embed":
        return Embed(
            title=title,
            description=description,
            color=Colour.gold()
        )

    @classmethod
    def WARN_EMBED(cls, title: str, description: str) -> "Embed":
        return Embed(
            title=title,
            description=description,
            color=Colour.orange()
        )

    @classmethod
    def ERROR_EMBED(cls, title: str, e: Exception) -> "Embed":
        return Embed(
            title="오류가 발생했습니다!",
            description=f"Error content : \n{e.with_traceback(e.__traceback__)}",
            color=Colour.red()
        )

    def __str__(self) -> str:
        text = (
            f"title={self.title}\n"
            f"description={self.description}\n"
            f"author={self.author}\n"
            f"thumbnail={self.thumbnail.toDict()}\n"
            f"image={self.image.toDict()}\n"
            f"footer={self.footer}\n"
            f"fields=[\n")
        text += '  \n'.join(str(field) for field in self.fields) + "\n]"
        return text

    def to_string(self) -> str:
        return self.__str__()
