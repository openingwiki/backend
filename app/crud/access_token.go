package crud

import (
	"database/sql"
	"log"

	sq "github.com/Masterminds/squirrel"
	"github.com/openingwiki/backend/models"
)

func CreateToken(db *sql.DB, userId int, token string) (*models.AccessTokenOut, error) {
	neededColumns := "user_id, token"
	query := sq.Insert("access_tokens").Columns(neededColumns).Values(userId, token).Suffix("RETURNING token").PlaceholderFormat(sq.Dollar)

	row := query.RunWith(db).QueryRow()
	var accessToken models.AccessTokenOut

	if err := row.Scan(&accessToken.Token); err != nil {
		log.Println("error:", err)
		return nil, err
	}

	return &accessToken, nil
}

func GetUserByToken(db *sql.DB, token string) (*models.User, error) {
	neededColumns := "users.id, users.username, users.password_hash"
	query := sq.Select(neededColumns).From("access_tokens").Where(sq.Eq{"token": token}).Join("users ON users.id=access_tokens.user_id").PlaceholderFormat(sq.Dollar)

	row := query.RunWith(db).QueryRow()
	var user models.User

	if err := row.Scan(&user.ID, &user.Username, &user.PasswordHash); err != nil {
		log.Println("error:", err)
		return nil, err
	}

	return &user, nil
}
