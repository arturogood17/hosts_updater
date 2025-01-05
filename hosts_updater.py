import requests
import subprocess #Genera nuevos procesos. Sirve para ejecutar comandos del sistema operativo con Python.
import shutil
import os

def updating(doc_with_update, doc_to_be_updated):
    if  len(doc_with_update) > len(doc_to_be_updated) : #Comprueba que si la lista a act. es más pequeña que la nueva
        doc_to_be_updated.extend([None] * (len(doc_with_update)  - len(doc_to_be_updated))) #extiende la lista a act.
    for j in range(len(doc_with_update)): #actualiza
        doc_to_be_updated[j] = doc_with_update[j]
    return doc_to_be_updated

def copy_to_path(path_origen, path_destino):
    if not os.path.isfile(path_origen):
        print(f"El archivo {path_origen} no existe.")
    try:
        shutil.copy(path_origen, path_destino) #copia el archivo hosts de escritorio a la carpeta root del proyecto
    except Exception as e: #Te da el error si no se pudo copiar
        print(f"Error inesperado: {e}")

    if not os.path.isfile(path_destino):
        print(f"Copy failed. No se logró copiar el archivo {path_destino}")
    else:
        print("Archivo copiado exitosamente a carpeta root.")

def path_converter(path): #convierte la ruta a windows path
    windows_path = subprocess.run(['wslpath', '-w', path], capture_output=True, text=True).stdout.strip() #-w convierte
                                                                                                         # de WSL a Windows
                                                                                                         #Usamos stdout para
                                                                                                         #que solo de info
                                                                                                         # del comando de salida
                                                                                                         # no de errores
    return windows_path    

def final_copy_to_windows(w_path_origen, w_path_destino):
    w_path_origen= w_path_origen.replace('\\', '\\\\').replace('"', '\\"')
    w_path_destino= w_path_destino.replace('\\', '\\\\').replace('"', '\\"')
    check_origin= f'powershell.exe Test-Path "{w_path_origen}"'
    test_origin = subprocess.run(check_origin, capture_output=True, text=True, shell=True)
    if test_origin.stdout.strip().lower() != "true":
        print (f"{w_path_origen} not valid.")
    try:
        powershell_c = f'''if (Test-Path \'{w_path_destino}\') {{ Remove-Item \'{w_path_destino}\' }}; Copy-Item -Path \'{w_path_origen}\' -Destination \'{w_path_destino}\' -Force''' 
        command= [
            'powershell.exe',
            'Start-Process',
            'powershell',
            '-Verb', 'RunAs',
            '-ArgumentList',
            f'-NoProfile -Command "{powershell_c}"'
        ]
        subprocess.run(command, shell=True, check=True)
        check_final= f'powershell.exe Test-Path "{w_path_destino}"'
        test_final = subprocess.run(check_final, capture_output=True, text=True, shell=True)
        if test_final.stdout.strip().lower() != "true":
            print (f"Copia unsuccessful.")
        else:
            print (f"Copia successful.")

    except Exception as e:
        return f"Error code: {e}"

    
def main ():
    url = "https://a.dove.isdumb.one/list.txt"
    with requests.get(url, stream= True) as r: 
        with open("update_to_hosts.txt", "wb") as file: # cuando haces esto,
            for chunk in r.iter_content(chunk_size= 8192): #se crea el archivo de una vez en la ruta donde tienes el proyecto
                file.write(chunk)                          #si el archivo es grande, entonces hay que leerlo en pedacitos
                                                           # de 8 bytes

    path_hosts_desktop= '/mnt/c/Users/artur/OneDrive/Escritorio/hosts' #El hosts debe estar en escritorio
    path_hosts_destino= "/home/nestapon9/workspace/github.com/arturogood17/hots_updater/hosts" #El path de la carpeta
                                                                                               #de nuestro proyecto

    copy_to_path(path_hosts_desktop, path_hosts_destino)

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

    final_hosts_path = "/mnt/c/Windows/System32/drivers/etc/hosts"

    path_root_hosts= path_converter(path_hosts_destino)
    final_hosts_path= path_converter(final_hosts_path) #convierte la ruta de estos archivos en rutas windows
    final_copy_to_windows(path_root_hosts, final_hosts_path)

main()