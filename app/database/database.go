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
		log.Fatal("Error loading .env file.")
	}

	var databaseUrl string = envVars["DATABASE_URL"]
	db, err := sql.Open("postgres", databaseUrl)

	if err != nil {
		log.Fatal("Eror connecting to database.")
	}

	if err := db.Ping(); err != nil {
		log.Fatal("Failed to ping db.")
	}

	return db
}

func CreateTables(db *sql.DB) {
	createAnimeTable(db)
	createOpeningsTable(db)
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
}