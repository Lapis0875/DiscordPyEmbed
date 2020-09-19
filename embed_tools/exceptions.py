from typing import Dict, Any


class EmbedFactoryException(Exception):
    @property
    def msg(self) -> str:
        return self._msg

    def __init__(self, msg="An exception was occurred during EmbedFactory operations.", *args, **kwargs):
        self._msg = msg
        super().__init__(*args)

    def __str__(self) -> str:
        return self.msg

    def __repr__(self) -> str:
        return self.__str__()


class UnexpectedKwargsError(EmbedFactoryException):
    def __init__(self, unexpected_kwargs: Dict[str, Any], *args, **kwargs):
        if "msg" in kwargs.keys():
            kwargs.pop("msg")
        self.kwargs = unexpected_kwargs
        import json
        msg = f"`EmbedFactory.__init__()` caught unexpected keyword arguments! : {json.dumps(obj=self.kwargs, indent=4, ensure_ascii=False)}"
        super().__init__(*args, msg=msg, **kwargs)


class InvalidColorError(EmbedFactoryException):
    def __init__(self, invalid_color, *args, **kwargs):
        self.color = invalid_color
        if "msg" in kwargs.keys():
            kwargs.pop("msg")
        super().__init__(
            *args,
            msg="Embed color must be an instance of `discord.Colour`! : ",
            **kwargs
        )


class InvalidFieldError(EmbedFactoryException):
    def __init__(self, invalid_field, *args, **kwargs):
        self.field = invalid_field
        if "msg" in kwargs.keys():
            kwargs.pop("msg")
        super().__init__(
            *args,
            msg="Embed field must have structure of `{'name': name, 'value': value}`",
            **kwargs
        )
