package handlers

import (
	"database/sql"
	"fmt"

	fiber "github.com/gofiber/fiber/v3"
	"github.com/openingwiki/backend/crud"
	"github.com/openingwiki/backend/security"
)

type RegistrationBody struct {
	Username string `json:"username" validate:"required"`
	// display_name string `validate: min=1, max=20`
	Password string `json"password" validate:"required"`
}

// getOpening godoc
// @Summary      Register user
// @Description  Register user
// @Tags         auth
// @Accept       json
// @Produce      json
// @Param        username   body     string  true  "Username"
// @Param 		 password 	body	 string  true  "Password"
// @Success      201  {object}  models.UserOut
// @Failure 	 400
// @Failure 	 500
// @Router       /register [post]
func Register(c fiber.Ctx, db *sql.DB) error {
	userRegisterData := new(RegistrationBody)

	if err := c.Bind().Body(userRegisterData); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid body parameters",
		})
	}

	if err := validate.Struct(userRegisterData); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	hashedPassword, _ := security.HashPassword(userRegisterData.Password)
	fmt.Println(userRegisterData.Username, userRegisterData.Password)
	user, err := crud.CreateUser(db, userRegisterData.Username, hashedPassword)

	if err != nil {
		return c.Status(fiber.StatusConflict).SendString("User already eixsts")
	}

	return c.Status(fiber.StatusCreated).JSON(user)
}

func Autrhorize(c fiber.Ctx, db *sql.DB) {
}
