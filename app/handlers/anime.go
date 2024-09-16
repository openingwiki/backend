package handlers

import (
	"database/sql"

	fiber "github.com/gofiber/fiber/v2"
	"github.com/openingwiki/backend/crud"
)

// getOpening godoc
// @Summary      Get one anime by its codename
// @Description  Get one anime by its codename
// @Tags         anime
// @Accept       json
// @Produce      json
// @Param        codename   path     string  true  "Codename of anime to get"
// @Success      200  {object}  models.AnimeOut
// @Failure 	 400
// @Failure		 404
// @Failure 	 500
// @Router       /anime/{codename} [get]
func GetAnime(c *fiber.Ctx, db *sql.DB) error {
	codename := c.Params("codename")

	if codename == "" {
		return c.Status(fiber.StatusBadRequest).JSON("Codename not specified")
	}

	anime, err := crud.GetAnimeOutByCodename(db, codename)

	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON("Anime not found")
	}

	return c.Status(fiber.StatusOK).JSON(anime)
}
