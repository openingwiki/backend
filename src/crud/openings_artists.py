from sqlalchemy.orm import Session

from models import openings_artists


def add_openings_artists(db: Session, opening_id: int, artists_id: list[int]):
    """Associate an artist with an opening."""
    values_list = [{'opening_id': opening_id, 'artist_id': artist_id} for artist_id in artists_id]
    stmt = openings_artists.insert().values(values_list)
    db.execute(stmt)
    db.commit()
