from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class EmbedThumbnail(BaseModel):
    url: str
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]


class EmbedVideo(BaseModel):
    url: Optional[str]
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]


class EmbedImage(BaseModel):
    url: str
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]


class EmbedProvider(BaseModel):
    name: Optional[str]
    url: Optional[str]


class EmbedAuthor(BaseModel):
    name: str
    url: Optional[str]
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]


class EmbedFooter(BaseModel):
    text: str
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]


class EmbedField(BaseModel):
    name: str
    value: str
    inline: Optional[bool]


class DiscordEmbed(BaseModel):
    title: Optional[str]
    type: Optional[str]
    description: Optional[str]
    url: Optional[str]
    timestamp: Optional[datetime]
    color: Optional[int]
    footer: Optional[EmbedFooter]
    image: Optional[EmbedImage]
    thumbnail: Optional[EmbedThumbnail]
    video: Optional[EmbedVideo]
    provider: Optional[EmbedProvider]
    author: Optional[EmbedAuthor]
    fields: Optional[List[EmbedField]]


class DiscordPayload(BaseModel):
    content: str
    embeds: List[DiscordEmbed]
