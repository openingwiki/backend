package crud

import (
	"database/sql"
	"log"

	sq "github.com/Masterminds/squirrel"
	"github.com/openingwiki/backend/models"
)

func GetOpeningsOut(db *sql.DB, limit int, offset int) []models.OpeningOut {
	neededColumns := "openings.id, openings.name, openings.codename, openings.youtube_embed_link, openings.thumbnail_link, anime.name"
	query := sq.Select(neededColumns).From("openings").Join("anime ON anime.id=openings.anime_id").Limit(uint64(limit)).Offset(uint64(offset))

	rows, err := query.RunWith(db).Query()

	if err != nil {
		log.Fatal("Error trying to select openings:", err)
	}

	defer rows.Close()

	openings := []models.OpeningOut{}

	for rows.Next() {
		var opening models.OpeningOut

		if err := rows.Scan(&opening.ID, &opening.Name, &opening.Codename, &opening.YoutubeEmbedLink, &opening.ThumbnailLink, &opening.AnimeName); err != nil {
			log.Fatal("Error trying to scan result:", err)
		}

		openings = append(openings, opening)
	}

	return openings
}
