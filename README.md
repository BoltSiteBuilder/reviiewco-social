# reviiewco-social

Public media for ReviiewCo's daily social posts (Instagram @reviiewco, the ReviiewCo Facebook Page, and the ReviiewCo YouTube channel), scheduled through the GoHighLevel Social Planner.

Files here are public on purpose: Instagram and Facebook download each post's image from its raw GitHub URL, for example
`https://raw.githubusercontent.com/BoltSiteBuilder/reviiewco-social/main/posts/2026-10-24.jpg`.
Nothing private belongs in this repo.

## Layout
- `render_post.py` builds a 1080×1350 post image in the reviiewco.com look (Anton + Plus Jakarta Sans, navy and amber). Run `npm install` once for the fonts, then `python3 render_post.py posts/DATE.json posts/DATE.jpg`.
- `assets/` logo, icon and site photos copied from reviiewco.com. Photos are illustrative only; never present them as clients or results.
- `posts/` one spec (`DATE.json`) and image (`DATE.jpg`) per day, plus `log.md`.
- `videos/` Rob's own videos, posted as Reels / YouTube Shorts.
