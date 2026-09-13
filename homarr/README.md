# Homarr Config

Snapshots of the Homarr dashboard configuration.

## Files

- **custom.css** — Full custom CSS (Catppuccin Mocha glassmorphism theme)
- **board_meta.json** — Board settings: wallpaper URL, accent colors, border radius
- **layout.json** — All sections, apps, and widget positions (layout snapshot)

## Restoring CSS

1. Stop Homarr: `docker compose stop homarr`
2. Delete Redis cache: `docker run --rm -v docker_homarr-new-appdata:/appdata alpine rm /appdata/redis/dump.rdb`
3. Apply CSS to DB:
   ```
   docker run --rm -v docker_homarr-new-appdata:/appdata -v $(pwd)/homarr:/homarr alpine      sh -c 'apk add python3 -q && python3 - << PY
   import sqlite3, json
   css = open("/homarr/custom.css").read()
   meta = json.load(open("/homarr/board_meta.json"))
   con = sqlite3.connect("/appdata/db/db.sqlite")
   con.execute("UPDATE board SET custom_css=?, background_image_url=?, primary_color=?, secondary_color=?",
               (css, meta["background_image_url"], meta["primary_color"], meta["secondary_color"]))
   con.commit()
   PY'
   ```
4. Start Homarr: `docker compose start homarr`
