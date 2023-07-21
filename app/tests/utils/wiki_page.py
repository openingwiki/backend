from app.models import User
from app.schemas import WikiPageAdd


def random_pydantic_wiki_page(user: User) -> WikiPageAdd:
    wiki_page = WikiPageAdd(
        name="Bloody Streem", youtube_url="https://www.youtube.com/watch?v=PcuTPjgMiXw", added_by_user=user.id
    )
    return wiki_page
