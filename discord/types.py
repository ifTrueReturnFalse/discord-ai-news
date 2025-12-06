from typing import TypedDict, List
from datetime import datetime

class EmbedThumbnail(TypedDict, total=False):
    url: str
    proxy_url: str
    height: int
    width: int

class EmbedVideo(TypedDict, total=False):
    url: str
    proxy_url: str
    height: int
    width: int

class EmbedImage(TypedDict, total=False):
    url: str
    proxy_url: str
    height: int
    width: int

class EmbedProvider(TypedDict, total=False):
    name: str
    url: str

class EmbedAuthor(TypedDict, total=False):
    name: str
    url: str
    icon_url: str
    proxy_icon_url: str

class EmbedFooter(TypedDict, total=False):
    text: str
    icon_url: str
    proxy_icon_url: str

class EmbedField(TypedDict, total=False):
    name: str
    value: str
    inline: bool

class DiscordEmbed(TypedDict, total=False):
    title: str
    type: str
    description: str
    url: str
    timestamp: datetime
    color: int
    footer: EmbedFooter
    image: EmbedImage
    thumbnail: EmbedThumbnail
    video: EmbedVideo
    provider: EmbedProvider
    author: EmbedAuthor
    fields: List[EmbedField]

class DiscordPayload(TypedDict, total=False):
    content: str | None
    username: str | None
    embeds: List[DiscordEmbed]