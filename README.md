> 🇬🇧 Also available in English: [README.en.md](README.en.md)

# 3Cat Scraper

Descarrega capítols de sèries de [3Cat](https://www.3cat.cat) organitzats per temporada, utilitzant `yt-dlp`.

## Requisits

- Python 3.7+
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) instal·lat i accessible des del terminal

## Ús

```bash
python tv3_scraper.py https://www.3cat.cat/3cat/<nom-serie>/
```

L'script troba tots els capítols disponibles, desa les URLs a `episodis.txt` i ofereix iniciar la descàrrega amb `yt-dlp`. 

Si decideixes que l'eina descarregui els vídeos directament, es guarden amb l'estructura `NomSerie/Season X/títol.ext` i s'esborra el llistat de capítols.
