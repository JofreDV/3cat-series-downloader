> 🇨🇦 També disponible en català: [README.md](README.md)

# 3Cat Scraper

Downloads episodes from [3Cat](https://www.3cat.cat) TV series, organised by season, using `yt-dlp`.

## Requirements

- Python 3.7+
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) installed and available in your terminal

## Usage

```bash
python tv3_scraper.py https://www.3cat.cat/3cat/<series-name>/
```

The script finds all available episodes, saves the URLs to `episodis.txt`, and offers to start the download with `yt-dlp`. 

If you choose to download directly, files are saved as `SeriesName/Season X/title.ext` and the episode list is deleted afterwards.
