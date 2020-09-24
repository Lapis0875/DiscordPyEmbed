# discord.py-embed

![py_ver](https://img.shields.io/pypi/pyversions/chronous?label=Python%20Version&logo=python&logoColor=yellow)

![license](https://img.shields.io/github/license/Lapis0875/DiscordPyEmbed?logo=github&logoColor=white)
![issues](https://img.shields.io/github/issues/Lapis0875/DiscordPyEmbed?logo=github&logoColor=white)

![pypi_ver](https://img.shields.io/pypi/v/discord.py-embed?logo=pypi&logoColor=blue)
![pypi_package](https://img.shields.io/pypi/format/discord.py-embed?label=package&logo=pypi)
![pypi_status](https://img.shields.io/pypi/status/discord.py-embed?color=blue&logo=pypi&logoColor=blue)

![discord](https://img.shields.io/discord/622434051365535745?color=blue&label=Discord&logo=Discord&logoColor=White)


**discord.py-embed** is a library for discord.py which expands Embed class, which has several features.
1. You can set multiple fields on embed using a single method, which is not supported in discord.py
2. You can control some attributes like `video`, `provider`, `image`, which cannot be used when initializing Embed class using `__init__`.

[Example]
```python
from discord_embeds import ExtendedEmbed, EmbedType
from discord import Colour
embed = ExtendedEmbed(
    title="Sample Title",
    embed_type=EmbedType.RICH,
    description="Sample Description",
    color=Colour.orange(),
    
)
```
