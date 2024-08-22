package main

import (
	"github.com/go-playground/validator/v10"
	fiber "github.com/gofiber/fiber/v2"
	"github.com/openingwiki/backend/pkg/models"
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
	app := fiber.New()

	app.Get("/openings", getOpenings)

	app.Listen(":8080")
}

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

	var resultOpenings []models.OpeningOut

	for i := queryParameters.Offset; i < i+queryParameters.Limit && i < len(openings); i++ {
		resultOpenings = append(resultOpenings, openings[i])
	}

	return c.JSON(resultOpenings)
}
