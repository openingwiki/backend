package handlers

import (
	"database/sql"
	"fmt"

	fiber "github.com/gofiber/fiber/v3"
	"github.com/openingwiki/backend/crud"
	"github.com/openingwiki/backend/security"
)

type RegistrationBody struct {
	Username string `json:"username" validate:"required,min=1,max=20"`
	// display_name string `validate: min=1, max=20`
	Password string `json:"password" validate:"required,min=1,max=20"`
}

type AuthBody struct {
	Username string `json:"username" validate:"required,min=1,max=20"`
	Password string `json:"password" validate:"required,min=1,max=20"`
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

func Autrhorize(c fiber.Ctx, db *sql.DB) error {
	userAuthData := new(AuthBody)

	if err := c.Bind().Body(userAuthData); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid body parameters",
		})
	}

	if err := validate.Struct(userAuthData); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	user, err := crud.GetUserByUsername(db, userAuthData.Username)
	if err != nil {
		return c.Status(fiber.StatusUnauthorized).SendString("Wrong credentials")
	}

	fmt.Println(userAuthData)
	// Checking that password is correct.
	hashedPassword, _ := security.HashPassword(userAuthData.Password)
	if err := security.ComparePassword(hashedPassword, userAuthData.Password); err != nil {
		return c.Status(fiber.StatusUnauthorized).SendString("Wrong credentials")
	}

	// Creating token.
	tokenStr, _ := security.GenerateToken(256)

	token, err := crud.CreateToken(db, user.ID, tokenStr)

	if err != nil {
		return c.Status(fiber.StatusTeapot).SendString("Something wrong on server side...")
	}

	return c.Status(fiber.StatusCreated).JSON(token)
}