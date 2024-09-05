package handlers

import (
	"database/sql"

	"github.com/gofiber/fiber/v2"
	"github.com/openingwiki/backend/crud"
	"github.com/openingwiki/backend/models"
)

// GetProfileByUsername godoc
// @Summary      Get profile by username
// @Description  Get profile by username
// @Tags         profile
// @Accept       json
// @Produce      json
// @Param        username   path     string  true  "Username"
// @Success      200  {object}  models.UserOut
// @Failure 	 400
// @Failure		 404
// @Failure 	 500
// @Router       /profile/{username} [get]
func GetProfileByUsername(c *fiber.Ctx, db *sql.DB) error {
	// Parsing username from query parameter.
	username := c.Params("username")
	if username == "" {
		return c.Status(fiber.StatusBadRequest).JSON("Не передан codename")
	}

	user, err := crud.GetUserByUsername(db, username)
	if err != nil {
		return c.Status(fiber.StatusNotFound).SendString("User not found")
	}

	return c.Status(fiber.StatusOK).JSON(models.UserOut{ID: user.ID, Username: user.Username})
}
