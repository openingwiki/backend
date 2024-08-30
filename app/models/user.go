package models

type User struct {
	ID           int
	Username     string
	PasswordHash string
}

type UserOut struct {
	ID       int    `json:"id"`
	Username string `json:"username"`
}
