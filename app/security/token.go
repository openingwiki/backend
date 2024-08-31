package security

import (
	"crypto/rand"
	"encoding/hex"
)

func GenerateToken(length int) (string, error) {
	// Create a byte slice of the desired length
	bytes := make([]byte, length)

	// Read random bytes into the slice
	if _, err := rand.Read(bytes); err != nil {
		return "", err
	}

	// Convert the byte slice to a hexadecimal string
	return hex.EncodeToString(bytes), nil
}
