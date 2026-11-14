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

Choose menu:
[1] Download Video
[2] Download Audio
"""
print(ascii_art())

input_choice = input("Enter your choice (1/2): ")

if input_choice not in ['1', '2']:
    print("Invalid choice. Please select 1 or 2.")
    exit()
if input_choice == '1':
    url = input("Enter video URL: ")
    output_path = input("Enter the output path (Example: /path/to/save/video.mp4): ")

elif input_choice == '2':
    url = input("Enter the audio URL: ")
    output_path = input("Enter the output path (Example: /path/to/save/audio.mp3): ")
