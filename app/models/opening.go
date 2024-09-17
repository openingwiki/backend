package models

type Opening struct {
	ID               uint64
	Name             string
	AnimeId          uint64
	Codename         string
	YoutubeEmbedLink string
	ThumbnailLink    string
}

type OpeningOut struct {
	ID               uint64 `json:"id"`
	Name             string `json:"name"`
	Codename         string `json:"codename"`
	AnimeCodename    string `json:"anime_codename"`
	YoutubeEmbedLink string `json:"youtube_embed_link"`
	ThumbnailLink    string `json:"thumbnail_link"`
}

type OpeningsOut struct {
	ID               uint64 `json:"id"`
	Name             string `json:"name"`
	Codename         string `json:"codename"`
	AnimeName        string `json:"anime_name"`
	YoutubeEmbedLink string `json:"youtube_embed_link"`
	ThumbnailLink    string `json:"thumbnail_link"`
}
