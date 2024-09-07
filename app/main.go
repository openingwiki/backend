package main

import (
	fiber "github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/openingwiki/backend/database"
	_ "github.com/openingwiki/backend/docs" // Import the generated docs
	"github.com/openingwiki/backend/handlers"
	fiberSwagger "github.com/swaggo/fiber-swagger"
)

// @securityDefinitions.apikey BearerAuth
// @in header
// @name Authorization
// @description Bearer token authentication

func main() {
	// Init database.
	db := database.ConnectToDatabase()
	defer db.Close()
	database.CreateTables(db)

	app := fiber.New()

	app.Use(cors.New(cors.Config{
		AllowOrigins: "http://localhost:3000",                       // Frontend origin
		AllowHeaders: "Origin, Content-Type, Accept, Authorization", // Allowed headers
		AllowMethods: "GET, POST, PUT, DELETE, OPTIONS",             // Allowed HTTP methods
	}))

	// Docs route.
	app.Get("/docs/*", fiberSwagger.WrapHandler)

	// Opening routes.
	app.Get("/openings", func(c *fiber.Ctx) error {
		return handlers.GetOpenings(c, db)
	})
	app.Get("/openings/:codename", func(c *fiber.Ctx) error {
		return handlers.GetOpening(c, db)
	})

	// Auth routes.
	app.Post("/register", func(c *fiber.Ctx) error {
		return handlers.Register(c, db)
	})
	app.Post("/auth", func(c *fiber.Ctx) error {
		return handlers.Autrhorize(c, db)
	})

	// Profile routes
	app.Get("/profile/:username", func(c *fiber.Ctx) error {
		return handlers.GetProfileByUsername(c, db)
	})
	app.Get("/me/profile", func(c *fiber.Ctx) error {
		return handlers.GetUserProfile(c, db)
	})

	app.Listen(":8080")
}
