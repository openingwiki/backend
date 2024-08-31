package database

import (
	"database/sql"
	"log"

	"github.com/joho/godotenv"
	_ "github.com/lib/pq"
)

func ConnectToDatabase() *sql.DB {
	envVars, err := godotenv.Read()

	if err != nil {
		log.Fatal("Error loading .env file:", err)
	}

	var databaseUrl string = envVars["DATABASE_URL"]
	db, err := sql.Open("postgres", databaseUrl)

	if err != nil {
		log.Fatal("Eror connecting to database:", err)
	}

	if err := db.Ping(); err != nil {
		log.Fatal("Failed to ping db:", err)
	}

	return db
}

func CreateTables(db *sql.DB) {
	createAnimeTable(db)
	createOpeningsTable(db)
	createUsersTable(db)
	createAccessTokensTable(db)
}

func createAnimeTable(db *sql.DB) {
	query := `
	CREATE TABLE IF NOT EXISTS anime (
		id SERIAL PRIMARY KEY,
		name TEXT NOT NULL
	)`
	_, err := db.Exec(query)

	if err != nil {
		log.Fatal("Erorr creating anime table:", err)
	}
}

func createOpeningsTable(db *sql.DB) {
	query := `
	CREATE TABLE IF NOT EXISTS openings (
		id SERIAL PRIMARY KEY,
		name TEXT NOT NULL,
		anime_id INTEGER,
		codename TEXT UNIQUE,
		youtube_embed_link TEXT,
		thumbnail_link TEXT,

		CONSTRAINT fk_anime FOREIGN KEY (anime_id)
        REFERENCES anime (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
	)`

	_, err := db.Exec(query)

	if err != nil {
		log.Fatal("Erorr creating openings table:", err)
	}
}

func createUsersTable(db *sql.DB) {
	query := `
	CREATE TABLE IF NOT EXISTS users (
		id SERIAL PRIMARY KEY,
		username TEXT NOT NULL UNIQUE,
		password_hash TEXT NOT NULL,
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	)`

	_, err := db.Exec(query)

	if err != nil {
		log.Fatal("Erorr creating users table:", err)
	}
}

func createAccessTokensTable(db *sql.DB) {
	query := `
	CREATE TABLE IF NOT EXISTS access_tokens (
		id SERIAL PRIMARY KEY,
		user_id INTEGER,
		token TEXT,

		CONSTRAINT fk_user FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
	)
	`

	_, err := db.Exec(query)

	if err != nil {
		log.Fatal("Erorr creating access tokens table:", err)
	}
}
