import requests
import shutil
import os


def main ():
    url = "https://a.dove.isdumb.one/list.txt"
    with requests.get(url, stream= True) as r:
        with open("update_to_host.txt", "wb") as file:
            for chunk in r.iter_content(chunk_size= 8192):
                file.write(chunk)

    with open("update_to_host.txt", "r", encoding="utf-8") as file:
        contenido = file.read()
        print(contenido)
    
main()