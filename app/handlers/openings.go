package handlers

import (
	// "strings"

	"database/sql"

	fiber "github.com/gofiber/fiber/v3"
	"github.com/openingwiki/backend/crud"
)

type GetOpeningsQueryParameters struct {
	Limit  int `query:"limit" validate:"gte=0,max=20"`
	Offset int `query:"offset"`
}

// getOpenings godoc
// @Summary      Get list of openings by limit and offset
// @Description  Get list of openings by limit and offset
// @Tags         openings
// @Accept       json
// @Produce      json
// @Param        limit   query     int  false  "Count of resulting rows"
// @Param 		 offset  query	   int	false  "Offset of the query"
// @Success      200 	 {object}  []models.OpeningOut
// @Failure		 400
// @Failure		 500
// @Router       /openings [get]
func GetOpenings(c fiber.Ctx, db *sql.DB) error {
	queryParameters := new(GetOpeningsQueryParameters)

	if err := c.Bind().Query(queryParameters); err != nil {
		return c.Status(fiber.StatusBadRequest).SendString("Invalid query parameters")
	}

	if err := validate.Struct(queryParameters); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	resultOpenings := crud.GetOpeningsOut(db, queryParameters.Limit, queryParameters.Offset)

	return c.JSON(resultOpenings)
}

// getOpening godoc
// @Summary      Get one opening by its codename
// @Description  Get one opening by its codename
// @Tags         openings
// @Accept       json
// @Produce      json
// @Param        codename   path     string  true  "Codename of opening to get"
// @Success      200  {object}  models.OpeningOut
// @Failure 	 400
// @Failure		 404
// @Failure 	 500
// @Router       /openings/{codename} [get]
func GetOpening(c fiber.Ctx, db *sql.DB) error {
	codename := c.Params("codename")

	if codename == "" {
		return c.Status(fiber.StatusBadRequest).JSON("Не передан codename")
	}

	opening, err := crud.GetOpeningOut(db, codename)

	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON("Opening doesn't found.")
	}

	return c.Status(fiber.StatusOK).JSON(opening)
}
