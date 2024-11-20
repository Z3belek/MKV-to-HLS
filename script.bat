@echo off
setlocal enabledelayedexpansion

:: Obtener la cantidad de flujos de audio en el archivo de entrada
for /f %%a in ('ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 S04e01.mkv') do (
  set /a audio_count=%%a+1
)

:: Lista de resoluciones para cada variante (puedes personalizarlas)
set "resolutions=1920x1080 1280x720 854x480 640x360 426x240"

:: Lista de tasas de bits de video correspondientes a las resoluciones (puedes personalizarlas)
set "video_bitrates=3000k 1500k 800k 400k 200k"

:: Lista de tasas de bits de audio (puedes personalizarlas)
set "audio_bitrates=128k 64k 32k"

:: Crear un ciclo para cada variante de calidad
for %%i in (0 1 2 3 4) do (
  set "resolution=!resolutions:%%i=!"
  set "video_bitrate=!video_bitrates:%%i=!"
  
  for %%a in (0 1 2) do (
    set "audio_bitrate=!audio_bitrates:%%a=!"
    
    ffmpeg -i S04e01.mkv -c:v libx265 -b:v !video_bitrate! -vf "scale=!resolution!" -c:a aac -b:a !audio_bitrate! -f hls -master_pl_name master_%%i.m3u8 -hls_time 10 -hls_list_size 0 -hls_segment_filename "output_%%v_%%03d_%%i.ts" output_%%i.m3u8
  )
)

:: Pausa para mantener la ventana abierta
pause
