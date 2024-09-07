package handlers

import (
	"database/sql"
	"log"

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
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Сodename not specified",
		})
	}

	user, err := crud.GetUserByUsername(db, username)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{
			"error": "User not found",
		})
	}

	return c.Status(fiber.StatusOK).JSON(models.UserOut{ID: user.ID, Username: user.Username})
}

// GetProfileByUsername godoc
// @Summary      Get user profile
// @Description  Get user profile. Authorization Header needed in format Bearer {token}
// @Tags         profile
// @Accept       json
// @Produce      json
// @Param        username   header     string  true  "Username"
// @Success 200 {object} models.UserOut
// @Failure 401
// @Security BearerAuth
// @Router /me/profile [get]
func GetUserProfile(c *fiber.Ctx, db *sql.DB) error {
	// Get user token.
	authHeader := c.Get("Authorization")

	// Check if the header is present
	if authHeader == "" {
		return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
			"error": "No Authorization header provided",
		})
	}

	// Split the header to extract the token
	token := authHeader[len("Bearer "):]
	user, err := crud.GetUserByToken(db, token)

	if err != nil {
		log.Print(err)
		return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
			"error": "Token not found. Is the format of token header field correct?",
		})
	}

	return c.Status(fiber.StatusOK).JSON(models.UserOut{ID: user.ID, Username: user.Username})
}
