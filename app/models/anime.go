package models

type Anime struct {
	ID   uint64
	Name string
}

type AnimeOut struct {
	ID       uint64 `json:"id"`
	Name     string `json:"name"`
	Codename string `json:"codename"`
}
