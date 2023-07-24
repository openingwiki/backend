from app.models import User
from app.schemas import WikiPageCreate


def random_pydantic_wiki_page(user: User) -> WikiPageCreate:
    """
    Creating random pydantic wiki page.

    Parameters:
        user: User - sqlalchemy user model by whom wiki page added.

    Returns:
        wiki_page: WikiPageCreate - random pydantic wiki page create model.
    """
    wiki_page = WikiPageCreate(
        name="Bloody Streem", youtube_url="https://www.youtube.com/watch?v=PcuTPjgMiXw", added_by_user=user.id
    )
    return wiki_page
