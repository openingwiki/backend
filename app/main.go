package main

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"

	fiber "github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/gofiber/fiber/v2/middleware/logger"
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

	app.Use(logger.New(logger.Config{
		Format:     "[${time}] ${status} - ${method} ${path}\n",
		TimeFormat: "2006-01-02 15:04:05",
		TimeZone:   "Local",
	}))
	app.Use(cors.New(cors.Config{
		AllowOrigins:     "http://localhost:3000,http://localhost:8080", // Frontend origin
		AllowHeaders:     "Origin, Content-Type, Accept, Authorization", // Allowed headers
		AllowMethods:     "GET, POST, PUT, DELETE, OPTIONS",             // Allowed HTTP methods
		AllowCredentials: true,
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
	app.Get("/username/:username/check", func(c *fiber.Ctx) error {
		return handlers.CheckUsername(c, db)
	})

	// Create a channel to receive OS signals
	signalChan := make(chan os.Signal, 1)
	signal.Notify(signalChan, syscall.SIGINT, syscall.SIGTERM)

	// Start the Fiber server in a separate goroutine
	go func() {
		if err := app.Listen(":8080"); err != nil {
			fmt.Printf("Server error: %v\n", err)
		}
	}()

	// Wait for a signal
	sig := <-signalChan
	fmt.Printf("Received signal: %s\n", sig)

	// Gracefully stop the Fiber app
	fmt.Println("Shutting down gracefully...")
	if err := app.Shutdown(); err != nil {
		fmt.Printf("Shutdown error: %v\n", err)
	}

	fmt.Println("Cleanup complete. Exiting...")
}
