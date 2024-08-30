package main

import (
	fiber "github.com/gofiber/fiber/v3"
	"github.com/openingwiki/backend/database"
	_ "github.com/openingwiki/backend/docs" // Import the generated docs
	"github.com/openingwiki/backend/handlers"
	"github.com/openingwiki/backend/swagger"
)

func main() {
	// Init database.
	db := database.ConnectToDatabase()
	defer db.Close()
	database.CreateTables(db)

	app := fiber.New()

	// Docs route.
	app.Get("/docs/*", swagger.HandlerDefault)

	app.Get("/openings", func(c fiber.Ctx) error {
		return handlers.GetOpenings(c, db)
	})
	app.Get("/openings/:codename", func(c fiber.Ctx) error {
		return handlers.GetOpening(c, db)
	})

	app.Post("/register", func(c fiber.Ctx) error {
		return handlers.Register(c, db)
	})

	app.Listen(":8080")
}
