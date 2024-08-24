package models

type Opening struct {
	id               uint64
	name             string
	animeId          uint64
	codename         string
	codenameLower    string
	youtubeEmbedLink string
	thumbnailLink    string
}

type OpeningOut struct {
	Id               uint64 `json:"id"`
	Name             string `json:"name"`
	Codename         string `json:"codename"`
	AnimeName        string `json:"anime_name"`
	YoutubeEmbedLink string `json:"youtube_embed_link"`
	ThumbnailLink    string `json:"thumbnail_link"`
}
