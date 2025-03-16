from .user import CrudUser
from .access_token import CrudAccessToken
from .anime import CrudAnime
from .opening import CrudOpening
from .artist import CrudArtist
from models import User, AccessToken, Anime, Opening, Artist


crud_user = CrudUser(User)
crud_access_token = CrudAccessToken(AccessToken)
crud_anime = CrudAnime(Anime)
crud_opening = CrudOpening(Opening)
crud_artist = CrudArtist(Artist)
