import requests
import shutil
import os

def updating(doc_with_update, doc_to_be_updated):
    if  len(doc_with_update) > len(doc_to_be_updated) : #Comprueba que si la lista a act. es más pequeña que la nueva
        doc_to_be_updated.extend([None] * (len(doc_with_update)  - len(doc_to_be_updated))) #extiende la lista a act.
    for j in range(len(doc_with_update)): #actualiza
        doc_to_be_updated[j] = doc_with_update[j]
    return doc_to_be_updated
 
def main ():
    url = "https://a.dove.isdumb.one/list.txt"
    with requests.get(url, stream= True) as r: 
        with open("update_to_hosts.txt", "wb") as file: # cuando haces esto,
            for chunk in r.iter_content(chunk_size= 8192): #se crea el archivo de una vez en la ruta donde tienes el proyecto
                file.write(chunk)                          #si el archivo es grande, entonces hay que leerlo en pedacitos
                                                           # de 8 bytes

    path_hosts_desktop= "" #El hosts debe estar en escritorio
    path_hosts_destino= "" #El path de la carpeta
                                                                                               #de nuestro proyecto

    if not os.path.isfile(path_hosts_desktop):
        print("Archivo no existe.")
    else:
        shutil.copy(path_hosts_desktop, path_hosts_destino) #copia el archivo hosts de escritorio a la carpeta root del proyecto

    if not os.path.isfile(path_hosts_destino):
        print("Copy failed.")


    with open("hosts", "r+") as hosts: #r+ te permite leer y escribir en un archivo existente
        with open("update_to_hosts.txt", "r+") as file:
            lines_hosts = hosts.readlines() #lee las líneas de hosts
            beginning = "# These IPs will only block the telemetry check of Adobe apps,"
            lines_host_updater = file.readlines() #lee las líneas de update_to_hosts
            for i, line in enumerate(lines_hosts): #Recorre las líneas de hosts
                if beginning in line: #si la línea de inicio del txt está, entra en el bucle y
                    pos = sum(len(line) for line in lines_hosts[:i+1]) #Guarda los bytes desde el inicio hasta esta línea para
                                                                     #luego actualizar
                    updated = updating(lines_host_updater, lines_hosts[i+1:]) #actualiza la lista lines_hosts

            hosts.seek(pos) #vuelve al inicio del archivo
            hosts.truncate(pos)  # Esto limpia el archivo desde la posición hacia adelante
            hosts.writelines(updated) #escribe las líneas de nuevo con los cambios que hizo la función updating
main()