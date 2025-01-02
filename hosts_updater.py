import requests
import shutil
import os


def main ():
    url = "https://a.dove.isdumb.one/list.txt"
    with requests.get(url, stream= True) as r: 
        with open("update_to_host.txt", "wb") as file: # cuando haces esto,
            for chunk in r.iter_content(chunk_size= 8192): #se crea el archivo de una vez en la ruta donde tienes el proyecto
                file.write(chunk)                          #el arhcivo es grande entonces hay que leerlo en pedacitos de 8 bytes

    path_hosts_desktop= "" #El hosts debe estar en escritorio
    path_hosts_destino= "" #El path de la carpeta
                                                                                               #de nuestro proyecto

    if not os.path.isfile(path_hosts_desktop):
        print("Archivo no existe.")
    else:
        shutil.copy(path_hosts_desktop, path_hosts_destino)

    if not os.path.isfile(path_hosts_destino):
        print("Copy failed.")


    with open("hosts", "r+") as file: #r+ te permite leer y escribir en un archivo existente
        beginning = "# These IPs will only block the telemetry check of Adobe apps,"
        lines = file.readlines() #lee por lineas
        for i, line in enumerate(lines):
            if beginning in line.strip():
                lines[i] = "Hice este cambio\n" #agregrar el \n al final porque si no, pega la línea

        file.seek(0) # vuelve al inicio del archivo
        file.writelines(lines) #escribe las líneas de nuevo con los cambios
        file.truncate() #elimina líneas viejas si el archivo destino es más pequeño

main()