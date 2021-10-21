import re
import httpx

from datetime import datetime
from typing import List, Optional, Union

from models import (
    Article,
    MediaSection,
    ImageSection,
    TextSection,
    LeadSection,
    TitleSection,
    HeaderSection,
)


async def fetch_list_of_articles() -> List:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://mapping-test.fra1.digitaloceanspaces.com/data/list.json"
        )
    if r.status_code == 404:
        print("No articles!")
        return []
    return r.json()


async def fetch_details_of_article(article_id: int) -> Optional[dict]:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"https://mapping-test.fra1.digitaloceanspaces.com/data/articles/{article_id}.json"
        )
    if r.status_code == 404:
        print("No details!")
        return None
    return r.json()


async def fetch_media_of_article(article_id: int) -> Optional[dict]:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"https://mapping-test.fra1.digitaloceanspaces.com/data/media/{article_id}.json"
        )
    if r.status_code == 404:
        return None
    return r.json()


async def parse_article(
    article_id: int, 
    details: dict, 
    media: Optional[list[dict]],
) -> Article:
    details["sections"] = await parse_sections(
        sections=details["sections"], 
        media=media,
    )
    
    if details.get("category"):
        details["categories"] = [details.pop("category")]

    if details.get("tag"):
        details["tags"] = [details.pop("tag")]

    details["publication_date"] = datetime.strptime(
        details.pop("pub_date"), 
        "%Y-%m-%d-%H;%M;%S"
    )
    details["modification_date"] = datetime.strptime(
        details.pop("mod_date"), 
        "%Y-%m-%d-%H:%M:%S"
    )
    
    details["url"] = f"https://urls.com/{article_id}.html"

    article = Article(
        **details,
    )

    return article


async def parse_sections(
    sections: list[dict], 
    media: Optional[list[dict]]
) -> list[dict]:
    final_sections = []
    for section in sections:
        if section.get("text"):
            section["text"] = remove_html_tags(section["text"])
        if section["type"] == "text":
            final_sections.append(TextSection(**section))
        elif section["type"] == "title":
            final_sections.append(TitleSection(**section))
        elif section["type"] == "media" and media is not None:
            s = parse_media_section(section=section, media=media)
            if s is not None:
                final_sections.append(s)
        elif section["type"] == "header":
            final_sections.append(HeaderSection(**section))
        elif section["type"] == "image":
            final_sections.append(ImageSection(**section))
        elif section["type"] == "lead":
            final_sections.append(LeadSection(**section))
    return final_sections


def parse_media_section(
    section: dict, 
    media: list
) -> Optional[Union[MediaSection, ImageSection]]:
    for m in media:
        if m["id"] == section["id"]:
            if m["type"] == "media":
                m["publication_date"] = datetime.strptime(
                    m.pop("pub_date"), 
                    "%Y-%m-%d-%H;%M;%S",
                )
                return MediaSection(**m)
            elif m["type"] == "image":
                return ImageSection(**m)
    return None


def remove_html_tags(text: str) -> str:
    pattern = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    return re.sub(pattern, '', text)
