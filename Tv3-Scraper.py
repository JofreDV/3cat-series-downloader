import re
import sys
import os
import subprocess
from urllib.parse import urlparse
import urllib.request
from urllib.error import URLError, HTTPError

def fetch_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request) as response:
            return response.read().decode('utf-8')
    except HTTPError as e:
        print(f"El servidor ha retornat un error a {url}: {e.code} - {e.reason}")
        sys.exit(1)
    except URLError as e:
        print(f"Error de connexió (no s'arriba al servidor) a {url}: {e.reason}")
        sys.exit(1)

def main():
    try:
        url = sys.argv[1]
    except IndexError:
        print("Has d'indicar la URL de la sèrie a descarregar.")
        print("Exemple: python tv3_scraper.py https://www.3cat.cat/3cat/plats-bruts/")
        sys.exit(1)

    path_parts = urlparse(url).path.strip('/').split('/')
    if len(path_parts) < 2 or path_parts[0] != '3cat':
        print("Format d'URL no reconegut. Assegura't que és una URL vàlida de 3Cat.")
        sys.exit(1)
    
    show_name = path_parts[1]
    html_text = fetch_url(url)

    show_id_match = re.search(r'programatv_id=(\d+)', html_text)
    if not show_id_match:
        print("No s'ha trobat la ID de la sèrie a la pàgina. Assegura't que la URL sigui correcta o obre un error a GitHub.")
        sys.exit(1)
        
    show_id = show_id_match.group(1)

    api_url = f"https://api.3cat.cat/videos?programatv_id={show_id}&_format=json&agrupar=true&origen=llistat&pagina=1&sdom=img&version=2.0&items_pagina=10000"
    episodis_data = fetch_url(api_url)

    #We search for all the ID with type normal episode and especial episode and de-duplicate the list in case the response came malformed
    episode_ids = re.findall(r'"tipus_contingut":"(PPW|PPD)".*?"id":(\d+)', episodis_data, re.DOTALL)
    unique_episode_ids = list(dict.fromkeys(video_id for _, video_id in episode_ids))    

    if not unique_episode_ids:
        print("No s'han trobat capítols descarregables.")
        sys.exit(1)

    with open("episodis.txt", "w") as f:
        for video_id in unique_episode_ids:
            f.write(f"https://www.3cat.cat/3cat/{show_name}/video/{video_id}/\n")

    command = (
        f'yt-dlp --batch-file episodis.txt '
        f'--parse-metadata "title:T(?P<season_number>\\d+)x" '
        f'-o "{show_name.title()}/Temporada %(season_number)s/%(title)s.%(ext)s"'
    )

    print(f"S'han trobat {len(unique_episode_ids)} capítols de '{show_name.title()}'.")
    print("S'han guardat les URLs a episodis.txt")
    
    user_choice = input("Vols iniciar la descàrrega ara mateix amb yt-dlp? [s/N]: ")
    
    if user_choice.lower() in ['s', 'si', 'y', 'yes']:
        print("\nIniciant yt-dlp...\n")
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError:
            print("\nHi ha hagut un error executant yt-dlp. Comprova que el tens instal·lat.")
            os.remove("episodis.txt")
        except KeyboardInterrupt:
            print("\nDescàrrega interrompuda per l'usuari.")
    else: 
        print("Pots utilitzar la llista de capítols per a fer-ho manualment més tard.")

if __name__ == "__main__":
    main()