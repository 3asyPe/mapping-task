from datetime import datetime
from typing import Optional, Set, List, Union, Literal
from pydantic import BaseModel, HttpUrl, Field


class Section(BaseModel):
    pass


class HeaderSection(Section):
    type: Literal["header"] = Field(..., description="Section type - 'header'", example="header")
    level: int = Field(
        ...,
        description="The level of the header. The higher the number, the less important.",
        example="1",
    )
    text: str = Field(
        ...,
        description="Content of the header.",
        example="This is how you define a header",
    )


class TitleSection(Section):
    type: Literal["title"] = Field(..., description="Section type - 'title'", example="title")
    text: str = Field(
        ...,
        description="Content of the title.",
        example="This is how you define a title.",
    )


class LeadSection(Section):
    type: Literal["lead"] = Field(..., description="Section type - 'lead'", example="lead")
    text: str = Field(
        ...,
        description="Content of the lead.",
        example="This is how you define a lead.",
    )


class TextSection(Section):
    type: Literal["text"] = Field(..., description="Section type - 'text'", example="text")
    text: str = Field(
        ...,
        description="Content of the text.",
        example="This is how you define a text.",
    )


class ImageSection(Section):
    type: Literal["image"] = Field(..., description="Section type - 'image'", example="image")
    url: HttpUrl = Field(
        ..., description="Url to the image", example="https://url.to.image/image.jpg"
    )
    alt: Optional[str] = Field(
        None,
        description="Alternative text to display if image does not appear.",
        example="The alternative text.",
    )
    caption: Optional[str] = Field(
        None,
        description="The description of the image.",
        example="The description of the image.",
    )
    source: Optional[str] = Field(
        None,
        description="An Author or Organization Name",
        example="Pawel Glimos",
    )


class MediaSection(Section):
    type: Literal["media"] = Field(..., description="Section type - 'media'", example="media")
    id: str = Field(
        ...,
        description="Provider internal id of the media",
        example="media_id",
    )
    url: HttpUrl = Field(
        ..., description="Url to the media", example="https://some.website/media.mp4"
    )
    thumbnail: Optional[HttpUrl] = Field(
        None,
        description="Url to the thumbnail of the media",
        example="https://some.website/article/thumb.jpg",
    )
    caption: Optional[str] = Field(
        None, description="Caption of the media", example="This video shows a tutorial"
    )
    author: Optional[str] = Field(
        None, description="Name of the author of the media", example="Some Author"
    )
    publication_date: datetime = Field(
        ..., description="Datetime of media publication", example="2020-07-08T20:50:43Z"
    )
    modification_date: Optional[datetime] = Field(
        None, description="Datetime of media modification", example="2020-07-08T20:50:43Z"
    )
    duration: Optional[int] = Field(
        None, description="Duration of the media in seconds", example=120
    )


SECTION_TYPES = Union[
    TextSection,
    TitleSection,
    LeadSection,
    HeaderSection,
    ImageSection,
    MediaSection
]


class Article(BaseModel):
    id: str = Field(..., description="Internal provider id", example="article_id")
    original_language: str = Field(
        ..., description="Article original language", example="en"
    )
    url: HttpUrl = Field(
        ...,
        description="Url to the article",
        example="https://some.website/article.html",
    )
    thumbnail: Optional[HttpUrl] = Field(
        None,
        description="Url to the thumbnail of the article",
        example="https://some.website/article/thumb.jpg",
    )
    categories: Optional[Set[str]] = Field(
        None, description="List of article categories", example=["news", "local"]
    )
    tags: Optional[Set[str]] = Field(
        None, description="List of article tags", example=["news", "local"]
    )
    author: Optional[str] = Field(
        None, description="Name of the author of the article", example="Some Author"
    )
    publication_date: datetime = Field(
        ..., description="Datetime of article publication", example="2020-07-08T20:50:43Z"
    )
    modification_date: Optional[datetime] = Field(
        description="Datetime of article modification", default_factory=datetime.now
    )
    sections: List[Union[SECTION_TYPES]]