from app.models import User
from app.schemas import WikiPageCreate


def random_pydantic_wiki_page(user: User) -> WikiPageCreate:
    wiki_page = WikiPageCreate(
        name="Bloody Streem", youtube_url="https://www.youtube.com/watch?v=PcuTPjgMiXw", added_by_user=user.id
    )
    return wiki_page
