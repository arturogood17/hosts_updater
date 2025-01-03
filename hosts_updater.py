import requests
import shutil
import os

def updating(doc_with_update, doc_to_be_updated):
    for i in range(len(doc_to_be_updated)):
        for j in range(len(doc_with_update)):
            doc_to_be_updated[i] = doc_with_update[j]
    return doc_to_be_updated
 
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


    with open("hosts", "r+") as hosts: #r+ te permite leer y escribir en un archivo existente
        with open("hosts_updater.py", "r+") as file:
            lines_hosts = hosts.readlines()
            beginning = "# These IPs will only block the telemetry check of Adobe apps,"
            lines_host_updater = file.readlines() #lee por lineas
            for i, line in enumerate(lines_hosts): #Recorre las líneas de hosts
                if beginning in line: #si la línea de inicio del txt está, entra en el bucle y
                    updated = updating(lines_hosts[i:], lines_host_updater) #actualiza la lista lines_hosts

            hosts.seek(0) #vuelve al inicio del archivo
            hosts.writelines(updated) #escribe las líneas de nuevo con los cambios que hizo updating
            hosts.truncate() #elimina líneas viejas si el archivo destino es más pequeño

main()