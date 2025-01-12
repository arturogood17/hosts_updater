import requests
import shutil
import os
import subprocess
import sys

def updating(doc_with_update, doc_to_be_updated):
    if  len(doc_with_update) > len(doc_to_be_updated) : #Comprueba que si la lista a act. es más pequeña que la nueva
        doc_to_be_updated.extend([None] * (len(doc_with_update)  - len(doc_to_be_updated))) #extiende la lista a act.
    for j in range(len(doc_with_update)): #actualiza
        doc_to_be_updated[j] = doc_with_update[j]
    return doc_to_be_updated

def copy_to_path(path_origen, path_destino):
    if not os.path.isfile(path_origen): #comprueba que el path_origen exista
        print(f"El archivo {path_origen} no existe.")
    try:
        shutil.copy(path_origen, path_destino) #copia el archivo
    except Exception as e: #Te da el error si no se pudo copiar
        print(f"Error inesperado: {e}")

    print(f"Archivo copiado exitosamente de {path_origen} a {path_destino}.")

def extract_path(file): #Extrae el path de los archivos
    final_path = [] 
    path_abs = os.path.abspath(file) #Obtiene el path del archivo
    if os.path.exists(path_abs):
        path_divided = path_abs.split("/")
        for i in path_divided:
            if i != file:
                final_path.append(i)
        final_path= "/".join(final_path).strip() 
        return final_path
    raise Exception(f"El path no existe: {path_abs}")

def main ():
    url = "https://a.dove.isdumb.one/list.txt"
    with requests.get(url, stream= True) as r: 
        with open("update_to_hosts.txt", "wb") as file: # cuando haces esto,
            for chunk in r.iter_content(chunk_size= 8192): #se crea el archivo de una vez en la ruta donde tienes el proyecto
                file.write(chunk)                          #si el archivo es grande, entonces hay que leerlo en pedacitos
                                                           # de 8 bytes. Por eso se usa chunk

    path_hosts_windows= '/mnt/c/Windows/System32/drivers/etc/hosts' #Toma el hosts en /System32/drivers/etc/hosts
    path_hosts_destino= extract_path("hosts_updater.py") #El path de la carpeta extraido con extract_path
                                                         #donde se va a copiar el hosts que saquemos de System32

    copy_to_path(path_hosts_windows, path_hosts_destino)

    with open("hosts", "r+") as hosts: #r+ te permite leer y escribir en un archivo existente
        with open("update_to_hosts.txt", "r+") as file:
            lines_hosts = hosts.readlines() #lee las líneas de hosts
            beginning = "# These IPs will only block the telemetry check of Adobe apps,"
            lines_hosts_updater = file.readlines() #lee las líneas de update_to_hosts
            for i, line in enumerate(lines_hosts): #Recorre las líneas de hosts
                if beginning in line: #si la línea de inicio del txt está, entra en el bucle y
                    pos = sum(len(line) for line in lines_hosts[:i+1]) #Guarda los bytes desde el inicio hasta esta línea para
                                                                     #luego actualizar
                    updated = updating(lines_hosts_updater, lines_hosts[i+1:]) #actualiza la lista lines_hosts

            hosts.seek(pos) #vuelve al inicio del archivo
            hosts.truncate(pos)  # Esto limpia el archivo desde la posición hacia adelante
            hosts.writelines(updated) #escribe las líneas de nuevo con los cambios que hizo la función updating
    
    path_hosts_origen = os.path.abspath("hosts")
    copy_to_path(path_hosts_origen, path_hosts_windows)

if __name__ == "__main__":
    try:
        if os.geteuid() != 0: #Obtiene el usuario si es 0 es el administrador, si no, es usuario normal
            print("El script requiere con privilegios de administrador.")
            args= ["sudo", sys.executable] + sys.argv #argumentos de la siguiente línea/sys.executable da la ruta del intérprete python
            os.execvp("sudo", args) #crea un nuevo hilo que corre el programa y mata el anterior
            sys.exit(0)
        else:
            main()
    except PermissionError:
        print("No se pudieron obtener los privilegios de admin.")
        sys.exit(1)
    except subprocess.CalledProcessError:
        print("Error al ejecutar el script con privilegios de administrador.")
        sys.exit(1) 