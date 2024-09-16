package crud

import (
	"database/sql"

	sq "github.com/Masterminds/squirrel"
	"github.com/openingwiki/backend/models"
)

func GetAnimeOutByCodename(db *sql.DB, codename string) (*models.AnimeOut, error) {
	neededColumns := "anime.id, anime.name, anime.codename"
	query := sq.Select(neededColumns).From("anime").Where(sq.Expr("LOWER(anime.codename) = LOWER($1)", codename))

	row := query.RunWith(db).QueryRow()

	var anime models.AnimeOut
	if err := row.Scan(&anime.ID, &anime.Name, &anime.Codename); err != nil {
		return nil, err
	}

	return &anime, nil
}
