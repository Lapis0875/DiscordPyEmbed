from discord import Client, Colour, Message
from discord_embeds import Embed, EmbedType, AuthorObject, FooterObject

client = Client()


@client.event
async def on_message(msg):
    if msg.content == "hello":
        embed = Embed(
            title="Hello world!",
            description="Embed extension for discord.py",
            color=Colour.orange(),
            embed_type=EmbedType.RICH,
            timestamp=msg.created_at,
            author=AuthorObject(name=client.user.display_name, url=client.user.avatar_url),
            footer=FooterObject(text="You can create embeds using objects!", icon_url=msg.author.avatar_url)
        )

