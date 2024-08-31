package crud

import (
	"database/sql"
	"fmt"
	"log"

	sq "github.com/Masterminds/squirrel"
	"github.com/openingwiki/backend/models"
)

func GetUserByUsername(db *sql.DB, username string) (*models.User, error) {
	neededColumns := "id, username, password_hash"
	query := sq.Select(neededColumns).From("users").Where(sq.Eq{"username": username}).PlaceholderFormat(sq.Dollar)

	row := query.RunWith(db).QueryRow()
	fmt.Println(query.ToSql())

	var user models.User

	if err := row.Scan(&user.ID, &user.Username, &user.PasswordHash); err != nil {
		log.Println("Error while checking if user exists:", err)
		return nil, err
	}

	return &user, nil
}

func CreateUser(db *sql.DB, username string, password_hash string) (*models.UserOut, error) {
	query := sq.Insert("users").Columns("username", "password_hash").Values(username, password_hash).Suffix("RETURNING id, username").PlaceholderFormat(sq.Dollar)

	row := query.RunWith(db).QueryRow()
	var user models.UserOut

	if err := row.Scan(&user.ID, &user.Username); err != nil {
		log.Println("error:", err)
		return nil, err
	}

	return &user, nil
}
