from typing import List, Optional, Annotated
from pydantic import BaseModel, BeforeValidator
from datetime import datetime


def truncate_string(max_length: int):
    def validator(v: str | None) -> str | None:
        if v and len(v) > max_length:
            return v[: max_length - 3] + "..."
        return v

    return validator

DiscordTitle = Annotated[str, BeforeValidator(truncate_string(256))]
DiscordDesc = Annotated[str, BeforeValidator(truncate_string(4096))]
DiscordFieldVal = Annotated[str, BeforeValidator(truncate_string(1024))]
DiscordFooterText = Annotated[str, BeforeValidator(truncate_string(2048))]
DiscordName = Annotated[str, BeforeValidator(truncate_string(256))]
DiscordContent = Annotated[str, BeforeValidator(truncate_string(2000))]

class EmbedThumbnail(BaseModel):
    url: str
    proxy_url: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None


class EmbedVideo(BaseModel):
    url: Optional[str] = None
    proxy_url: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None


class EmbedImage(BaseModel):
    url: str
    proxy_url: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None


class EmbedProvider(BaseModel):
    name: Optional[DiscordName] = None
    url: Optional[str] = None


class EmbedAuthor(BaseModel):
    name: DiscordName
    url: Optional[str] = None
    icon_url: Optional[str] = None
    proxy_icon_url: Optional[str] = None


class EmbedFooter(BaseModel):
    text: DiscordFooterText
    icon_url: Optional[str] = None
    proxy_icon_url: Optional[str] = None


class EmbedField(BaseModel):
    name: DiscordName
    value: DiscordFieldVal
    inline: Optional[bool] = False


class DiscordEmbed(BaseModel):
    title: Optional[DiscordTitle] = None
    type: Optional[str] = "rich"
    description: Optional[DiscordDesc] = None
    url: Optional[str] = None
    timestamp: Optional[datetime] = None
    color: Optional[int] = None
    footer: Optional[EmbedFooter] = None
    image: Optional[EmbedImage] = None
    thumbnail: Optional[EmbedThumbnail] = None
    video: Optional[EmbedVideo] = None
    provider: Optional[EmbedProvider] = None
    author: Optional[EmbedAuthor] = None
    fields: Optional[List[EmbedField]] = []


class DiscordPayload(BaseModel):
    content: DiscordContent
    embeds: List[DiscordEmbed] = []
