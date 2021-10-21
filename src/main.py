import uvicorn

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from services import (
    fetch_details_of_article,
    fetch_list_of_articles,
    fetch_media_of_article,
    parse_article,
)


app = FastAPI()


@app.on_event("startup")
@repeat_every(seconds=300, raise_exceptions=True)
async def fetch_articles_task():
    articles = await fetch_list_of_articles()
    for article in articles:
        details = await fetch_details_of_article(article["id"])
        if details is None:
            continue
        media = await fetch_media_of_article(article_id=article["id"])
        parsed_article = await parse_article(
            article_id=article["id"], 
            details=details, 
            media=media,
        )
        print(parsed_article)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)

    
