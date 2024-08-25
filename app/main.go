package main

import (
	"strings"

	"github.com/go-playground/validator/v10"
	fiber "github.com/gofiber/fiber/v2"
	"github.com/gofiber/swagger"
	"github.com/openingwiki/backend/database"
	_ "github.com/openingwiki/backend/docs" // Import the generated docs
	"github.com/openingwiki/backend/models"
)

var openings = [2]models.OpeningOut{
	{Id: 1, Name: "Unravel", Codename: "Unravel", AnimeName: "Tokyo Ghoul", YoutubeEmbedLink: "https://www.youtube.com/embed/7aMOurgDB-o", ThumbnailLink: "https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/79479f19016951.562d38d2394d3.png"},
	{Id: 2, Name: "Great Days", Codename: "Great_Days", AnimeName: "Jojo's Bizzare Adventure", YoutubeEmbedLink: "https://www.youtube.com/embed/mU3vgXUKeFM", ThumbnailLink: "https://static.jojowiki.com/images/8/8a/latest/20210831055754/JoJo_OP7.png"},
}
var validate = validator.New()

type GetOpeningsQueryParameters struct {
	Limit  int `query:"limit" validate:"gte=0,max=20"`
	Offset int `query:"offset"`
}

func main() {
	// Init database.
	db := database.ConnectToDatabase()
	defer db.Close()
	database.CreateTables(db)

	app := fiber.New()

	// Docs route.
	app.Get("/docs/*", swagger.HandlerDefault)

	app.Get("/openings", getOpenings)
	app.Get("/openings/:codename", getOpening)

	app.Listen(":8080")
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
func getOpenings(c *fiber.Ctx) error {
	queryParameters := new(GetOpeningsQueryParameters)

	if err := c.QueryParser(queryParameters); err != nil {
		return c.Status(fiber.StatusBadRequest).SendString("Invalid query parameters")
	}

	if err := validate.Struct(queryParameters); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	resultOpenings := []models.OpeningOut{}

	for i := queryParameters.Offset; i < i+queryParameters.Limit && i < len(openings); i++ {
		resultOpenings = append(resultOpenings, openings[i])
	}

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
func getOpening(c *fiber.Ctx) error {
	codename := c.Params("codename")

	if codename == "" {
		return c.Status(fiber.StatusBadRequest).JSON("Фигнбю не делай.")
	}

	for _, opening := range openings {
		if strings.EqualFold(codename, opening.Codename) {
			return c.JSON(opening)
		}
	}

	return c.Status(fiber.StatusNotFound).JSON("Opening not found")
}
