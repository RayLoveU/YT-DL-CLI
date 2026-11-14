import os
import pathlib
import yt_dlp
import ffmpeg

def ascii_art():
    return """
==============================    
__   _______     ____  _     
\ \ / /_   _|   |  _ \| |    
 \ V /  | |_____| | | | |    
  | |   | |_____| |_| | |___ 
  |_|   |_|     |____/|_____|

==============================
         By: RayLoveU

Pilih menu:
[1] Download Video
[2] Download Audio
"""
print(ascii_art())

input_choice = input("Masukkan pilihan (1/2): ")

if input_choice not in ['1', '2']:
    print("Pilihan tidak valid. Silakan pilih 1 atau 2.")
    exit()
if input_choice == '1':
    url = input("Masukkan URL video: ")
    output_path = input("Masukkan path output (misal: /path/to/save/video.mp4): ")

elif input_choice == '2':
    url = input("Masukkan URL audio: ")
    output_path = input("Masukkan path output (misal: /path/to/save/audio.mp3): ")