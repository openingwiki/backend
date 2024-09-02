#!/bin/bash
# File containing SQL commands
# Execute the SQL file
echo $DATABASE_URL
psql $DATABASE_URL -c \
"
INSERT INTO anime (name) VALUES ('JoJo''s Bizzare Adventure');
INSERT INTO anime (name) VALUES ('Tokyo Ghoul');

INSERT INTO openings (name, anime_id, codename, youtube_embed_link, thumbnail_link) SELECT 'Great Days', anime.id, 'Great_Days', 'https://www.youtube.com/embed/mU3vgXUKeFM', 'https://static.jojowiki.com/images/8/8a/latest/20210831055754/JoJo_OP7.png' FROM anime where name='JoJo''s Bizzare Adventure';
INSERT INTO openings (name, anime_id, codename, youtube_embed_link, thumbnail_link) SELECT 'Unravel', anime.id, 'Unravel', 'https://www.youtube.com/embed/7aMOurgDB-o', 'https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/79479f19016951.562d38d2394d3.png' FROM anime where name='Tokyo Ghoul';
"

# Check if the command was successful
if [ $? -eq 0 ]; then
    echo "Data inserted successfully."
else
    echo "Failed to insert data."
fi
