import requests
import os


def main ():
    url = "https://a.dove.isdumb.one/list.txt"
    with requests.get(url, stream= True) as r: 
        with open("update_to_host.txt", "wb") as file: # cuando haces esto,
            for chunk in r.iter_content(chunk_size= 8192): #se crea el archivo de una vez en la ruta donde tienes el proyecto
                file.write(chunk)

    with open("update_to_host.txt", "r", encoding="utf-8") as file: #esto abre el archivo para que lo leas,
        contenido = file.read()                                     #pero por alguna razón no lo muestra completo
        print(contenido)

        print("Working")
    
main()