import tkinter
import customtkinter
from pytubefix import YouTube

download_path = "__main__"
fileType = "Audio"

def startDownload():
    try:
        ytLink = link.get()
        ytObj = YouTube(ytLink, on_progress_callback=on_progress)
        if fileType == "Audio":
            ytVideo = ytObj.streams.get_audio_only()
        elif fileType == "Video":
            ytVideo = ytObj.streams.get_highest_resolution()
        else:
            print("Error: INCORRECT FILE TYPE!")

        title.configure(text=ytObj.title, text_color="white")
        finishLabel.configure(text="")
        ytVideo.download(output_path=download_path)
        finishLabel.configure(text="Downloaded! =)", text_color="green")
    except:
        finishLabel.configure(text="Download ERROR!", text_color="red")
        print("Youtube link is invalid!")

def on_progress(stream, bytes_remaining):
    progressBar.set(0)
    pPercentage.configure(text="0%")
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pPercentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(pPercentage_of_completion))
    pPercentage.configure(text=per + '%')

    # Update Prrogress Bar
    progressBar.set(float(pPercentage_of_completion) / 100)
    app.update()

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

# Download file
def fPath():
    global download_path
    download_path = tkinter.filedialog.askdirectory(title='Select Folder')

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
download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.grid(padx=10, pady=10)

# Run APP
app.mainloop()