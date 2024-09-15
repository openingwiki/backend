package handlers

import (
	"database/sql"

	"github.com/gofiber/fiber/v2"
	"github.com/openingwiki/backend/crud"
	"github.com/openingwiki/backend/models"
)

// GetProfileByUsername godoc
// @Summary      Check if username exists
// @Description  Check if username exists
// @Tags         profile
// @Accept       json
// @Produce      json
// @Param        username   path     string  true  "Username"
// @Success 200 {object} models.BoolJson
// @Router /username/{username}/check [get]
func CheckUsername(c *fiber.Ctx, db *sql.DB) error {
	// Checking is username already exists.
	username := c.Params("username")

	if username == "" {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Username not specified",
		})
	}

	isUser := crud.IsUsername(db, username)
	result := models.BoolJson{
		Result: isUser,
	}

	return c.Status(fiber.StatusOK).JSON(result)
}
