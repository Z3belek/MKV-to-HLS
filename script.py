import os
import subprocess
import json
from colorama import Fore, Style
import datetime
import time

# Directorio actual donde se encuentran los archivos MKV
directorio_actual = "./"

# Listar todos los archivos MKV en el directorio actual
archivos_mkv = [archivo for archivo in os.listdir(directorio_actual) if archivo.endswith(".mkv")]

def print_colored(text, color=Fore.WHITE):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{color}{current_time} - {text}{Style.RESET_ALL}")

def remove_file(file_path):
    try:
        os.remove(file_path)
        return True
    except Exception as e:
        return False

for archivo_mkv in archivos_mkv:
    # Nombre del archivo sin extensión
    nombre_base = os.path.splitext(archivo_mkv)[0]

    print_colored(f"Procesando archivo: {archivo_mkv}...", Fore.YELLOW)

    # Crear directorio para cada archivo MKV
    if not os.path.exists(nombre_base):
        os.mkdir(nombre_base)

    print_colored(f"Creando directorio para {nombre_base}...", Fore.GREEN)

    # Comando para extraer video en formato MP4 sin audio
    comando_video = (
        f"ffmpeg -loglevel quiet -i {archivo_mkv} -preset slow -b:v 7000k -an -c:v copy -map_metadata -1 {nombre_base}/{nombre_base}.mp4"
    )

    # Ejecutar el comando de extracción de video
    subprocess.run(comando_video, shell=True)

    print_colored(f"Video extraído y guardado en {nombre_base}/{nombre_base}.mp4", Fore.GREEN)

    # Obtener información sobre las pistas de audio
    comando_info_audio = f"ffprobe -v quiet -print_format json -show_streams {archivo_mkv}"
    info_audio = subprocess.check_output(comando_info_audio, shell=True)
    info_audio = json.loads(info_audio)

    # Contador para nombrar las pistas de audio
    contador_audio = 1

    # Lista para almacenar los comandos de pistas de audio
    comandos_audio = []

    # Recorrer las pistas de audio y generar los comandos
    for stream in info_audio["streams"]:
        if stream["codec_type"] == "audio":
            idioma = stream.get("tags", {}).get("language", f"Audio{contador_audio}")
            nombre_audio = f"{nombre_base}_Audio{contador_audio}_{idioma}.aac"
            comando_audio = (
                f"ffmpeg -loglevel quiet -i {archivo_mkv} -map 0:a:{contador_audio-1} -c:a copy -map_metadata -1 {nombre_base}/{nombre_audio}"
            )
            comandos_audio.append(comando_audio)
            contador_audio += 1

    # Ejecutar los comandos de pistas de audio
    for i, comando_audio in enumerate(comandos_audio, start=1):
        subprocess.run(comando_audio, shell=True)
        print_colored(f"Pista de audio {i} extraída y guardada en {nombre_base}/{nombre_audio}", Fore.GREEN)

    # Crear carpetas para las resoluciones
    resoluciones = [("1080p", "1920:1080", "1920x1080", 7000), ("720p", "1280:720", "1280x720", 4000), ("480p", "854:480", "854x480", 2000)]

    for resolucion, resolucion_str, resolucion_m3u8, bitrate in resoluciones:
        resolucion_dir = os.path.join(nombre_base, resolucion)
        os.mkdir(resolucion_dir)

        print_colored(f"Creando carpeta para {resolucion}...", Fore.CYAN)

        # Comando para convertir a HLS para cada resolución
        comando_hls = (f"ffmpeg -loglevel quiet -hwaccel cuda -i {nombre_base}.mp4 ")

        # Filtrar las pistas de audio
        archivos_aac = [archivo for archivo in os.listdir(nombre_base) if archivo.endswith(".aac")]

        # Ordenar las pistas de audio por el index
        archivos_aac.sort(key=lambda x: int(x.split("_")[1][5:]))

        # Agregar las pistas de audio ordenadas al comando HLS
        for archivo_aac in archivos_aac:
            comando_hls += f"-i {archivo_aac} "

        # Agregar la resolución, preset y bitrate al comando HLS
        comando_hls += (
            f"-vf scale={resolucion_str} -c:v h264_nvenc -preset fast -b:v {bitrate}k "
        )

        # Agregar el mapa del video
        comando_hls += f"-map 0 "

        # Agregar los mapas de audio con su metadata
        for archivo_aac in archivos_aac:
            idioma = archivo_aac.split("_")[2][:-4]
            comando_hls += f"-map {archivos_aac.index(archivo_aac) + 1} -metadata:s:a:{archivos_aac.index(archivo_aac)} language={idioma} "

        # Agregar el formato HLS al comando, y el nombre del archivo de salida acorde a la resolución
        comando_hls += (f"-f hls -hls_time 10 -hls_playlist_type vod -hls_segment_filename {resolucion}/%03d.ts {resolucion}/{resolucion}.m3u8")

        # Entrar al directorio del archivo MKV
        os.chdir(nombre_base)

        # Ejecutar el comando HLS
        subprocess.run(comando_hls, shell=True)

        print_colored(f"Archivo HLS creado para {resolucion} en {resolucion}/{resolucion}.m3u8", Fore.GREEN)

        # Salir del directorio del archivo MKV
        os.chdir("..")

    # Crear archivo master.m3u8
    archivo_master = open(f"{nombre_base}/master.m3u8", "w")
    archivo_master.write("#EXTM3U\n")
    for resolucion, _, resolucion_m3u8, bitrate in resoluciones:
        archivo_master.write(f"#EXT-X-STREAM-INF:BANDWIDTH={bitrate}000,RESOLUTION={resolucion_m3u8}\n")
        archivo_master.write(f"{resolucion}/{resolucion}.m3u8\n")
    archivo_master.close()
    
    print_colored(f"Archivo master.m3u8 creado en {nombre_base}/master.m3u8", Fore.GREEN)

    # Eliminar archivos temporales
    for archivo_aac in archivos_aac:
        while True:
            if remove_file(f"{nombre_base}/{archivo_aac}"):
                break  # Archivo eliminado con éxito
            else:
                print(f"El archivo {nombre_base}/{archivo_aac} está en uso. Esperando 5 segundos...")
                time.sleep(5)  # Esperar 5 segundos y volver a intentar

    # Eliminar el archivo de video MP4
    while True:
        if remove_file(f"{nombre_base}/{nombre_base}.mp4"):
            break  # Archivo eliminado con éxito
        else:
            print(f"El archivo {nombre_base}/{nombre_base}.mp4 está en uso. Esperando 5 segundos...")
            time.sleep(5)  # Esperar 5 segundos y volver a intentar

    # Eliminar el archivo MKV
    while True:
        if remove_file(f"{archivo_mkv}"):
            break  # Archivo eliminado con éxito
        else:
            print(f"El archivo {archivo_mkv} está en uso. Esperando 5 segundos...")
            time.sleep(5)  # Esperar 5 segundos y volver a intentar

    print_colored(f"Archivos eliminados: {nombre_base}.mp4, {', '.join(archivos_aac)} y {archivo_mkv}", Fore.RED)

    print_colored(f"Se completó el procesamiento de {archivo_mkv}", Fore.YELLOW)

print_colored("Proceso finalizado", Fore.YELLOW)
