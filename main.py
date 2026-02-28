import tkinter
import customtkinter
import threading
import subprocess
import os
from tkinter import filedialog
from pytubefix import YouTube

download_path = "files"
fileType = "Audio"

# Downloads Youtube Audio
def downloadAudio(ytObj):
    ytAudio = ytObj.streams.filter(only_audio=True).order_by('abr').desc().first()
    # Get offical path of download
    ytAudioPath = ytAudio.download(output_path=download_path)
    return ytAudioPath

# Downloads Youtube Video
def downloadVideo(ytObj):
    print("Starting Download...")
    ytVideo = ytObj.streams.filter(only_video=True).order_by('resolution').desc().first()
    # Get offical path of download
    ytVideoPath = ytVideo.download(filename="vid_temp",output_path=download_path)
    print("Download Complete!")
    return ytVideoPath

def startDownload():
    try:
        # Get Youtube Links / checks inputed link
        ytLink = link.get()
        ytObj = YouTube(ytLink, on_progress_callback=on_progress)

        title.configure(text=ytObj.title, text_color="white")
        finishLabel.configure(text="")

        # What the user has choosen
        if fileType == "Audio":
            # Get highest Audio quality
            downloadAudio(ytObj)
            #ytVideo = ytObj.streams.get_audio_only()
            #ytVideo = ytObj.streams.get_extra_audio_track()
            #ytVideo = ytObj.streams.filter(only_audio=True, audio_track_name="Klingon").get_audio_only()
            #Klingon_audio = ytObj.streams.filter(only_audio=True, audio_track_name='Klingon').first()
            #ytVideo = Klingon_audio
            #for i, stream in enumerate(ytObj.streams.filter(only_audio=True, mime_type="audio/mp4", audio_track_name="Klingon")):
                # Sanitize the title to avoid filename errors
             #   filename = f"{ytObj.title}_track_{i}.{stream.subtype}"
              #  stream.download(filename=filename)
               # print(stream)
        # Downloads both video and Audio seperatly to download highest quiality
        elif fileType == "Video":
            video_file = downloadVideo(ytObj)
            audio_file = downloadAudio(ytObj)

             # Sanitize title to remove illegal filename characters like / or :
            clean_title = "".join([c for c in ytObj.title if c.isalnum() or c in (' ', '.', '_')]).rstrip()
            output_merged = os.path.join(download_path, f"{clean_title}.mp4")

            # Create output directory if it doesn't exist
            os.makedirs(download_path, exist_ok=True)

            # Use -c:v copy and -c:a aac to ensure compatibility without losing quality
            ffmpeg_command = [
                'ffmpeg', '-y', 
                '-i', video_file, 
                '-i', audio_file, 
                '-c:v', 'copy', 
                '-c:a', 'aac',
                '-b:a', '192k',
                #'-strict', '-2', # To comply with 2013 Version of FFmpeg
                output_merged
            ]

            try:
                subprocess.run(ffmpeg_command, check=True)
                print(f"Successfully merged into: {output_merged}")

                # Clean up temporary files
                os.remove(video_file)
                os.remove(audio_file)
            except subprocess.CalledProcessError as e:
                print(f"FFmpeg merging failed: {e}")
            except FileNotFoundError:
                print("FFmpeg not found. Ensure it is installed and in your system's PATH.")
            
        else:
            print("Error: INCORRECT FILE TYPE!")
            return False

        #ytVideo.download(output_path=download_path)
        finishLabel.configure(text="Downloaded! =)", text_color="green")
    except:
        finishLabel.configure(text="Download ERROR!", text_color="red")
        print("Youtube link is invalid!")

def on_progress(stream, chunk, bytes_remaining):
    progressBar.set(0)
    pPercentage.configure(text="0%")
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pPercentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(pPercentage_of_completion))
    pPercentage.configure(text=per + '%')

    # Update Progress Bar
    progressBar.set(float(pPercentage_of_completion) / 100)
    app.update_idletasks()

# User Chooses file type: Music or Video
def f_type(fType):
    global fileType
    fileType = fType
    print(f"Switched To: {fType}")
    if fType == "Audio":
        audio.configure(fg_color="green", hover_color="dark green")
        video.configure(fg_color="blue", hover_color="dark blue")
    elif fType == "Video":
        video.configure(fg_color="green", hover_color="dark green")
        audio.configure(fg_color="blue", hover_color="dark blue")

# User Chooses Download Path
def fPath():
    global download_path
    download_path = filedialog.askdirectory(title='Select Folder')

# Threading
def threads():
    download_thread = threading.Thread(target=startDownload)
    download_thread.start()

# System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Youtube Downloader")

button_frame = customtkinter.CTkFrame(app, fg_color="transparent")
button_frame.grid(row=6, column=0, columnspan=2, pady=10)

app.grid_columnconfigure(0, weight=1)

# Adding UI Elements
title = customtkinter.CTkLabel(app, text="Insert a youtube link")
title.grid(padx=10, pady=10, row=0, column=0)

# Link input
url_var = tkinter.StringVar()
link= customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.grid()

# Finished Downloading
finishLabel = customtkinter.CTkLabel(app, text ="")
finishLabel.grid()

# Progress percentage
pPercentage = customtkinter.CTkLabel(app, text = "0%")
pPercentage.grid()

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.grid(padx=10, pady=10)

# Select File Type
audio = customtkinter.CTkButton(button_frame, text="Audio Format", fg_color="blue", command=lambda:f_type("Audio"))
audio.grid(padx=10, pady=10, row=6, column=0, sticky="e")

video = customtkinter.CTkButton(button_frame, text="Video Format", fg_color="blue", command=lambda:f_type("Video"))
video.grid(padx=10, pady=10, row=6, column=1, sticky="w")

# Select Path
pDir = customtkinter.CTkButton(app, text="Select File Path", command=fPath, fg_color="green", hover_color="dark green")
pDir.grid(padx=10, pady=10)

# Download button
download = customtkinter.CTkButton(app, text="Download", command=threads)
download.grid(padx=10, pady=10)

# Run APP
app.mainloop()