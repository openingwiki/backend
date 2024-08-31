package models

type AccessToken struct {
	ID     int
	UserId int
	Token  string
}

type AccessTokenOut struct {
	Token string `json:"token"`
}
