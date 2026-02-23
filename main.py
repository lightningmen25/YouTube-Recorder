import tkinter
import customtkinter
from pytubefix import YouTube

download_path = "__main__"
#file_type = "ytObj.streams.get_highest_resolution()" #Not yet done...

def startDownload():
    try:
        ytLink = link.get()
        ytObj = YouTube(ytLink, on_progress_callback=on_progress)
        #ytVideo = ytObj.streams.get_highest_resolution()
        ytVideo = ytObj.streams.get_audio_only()

        title.configure(text=ytObj.title, text_color="white")
        finishLabel.configure(text="")
        ytVideo.download(output_path=download_path)
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

    # Update Prrogress Bar
    progressBar.set(float(pPercentage_of_completion) / 100)
    app.update()

def f_type(): # Not YET...
    pass

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

# Adding UI Elements
title = customtkinter.CTkLabel(app, text="Insert a youtube link")
title.pack(padx=10, pady=10)

# Link input
url_var = tkinter.StringVar()
link= customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

# Finished Downloading
finishLabel = customtkinter.CTkLabel(app, text ="")
finishLabel.pack()

# Progress percentage
pPercentage = customtkinter.CTkLabel(app, text = "0%")
pPercentage.pack()

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)

# Select File Type
fType = customtkinter.CTkButton(app, text="Select File Type", command=f_type, fg_color="yellow", hover_color="black")
fType.pack(padx=10, pady=10)

# Select Path
pDir = customtkinter.CTkButton(app, text="Select File Path", command=fPath, fg_color="green", hover_color="dark green")
pDir.pack(padx=10, pady=10)

# Download button
download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.pack(padx=10, pady=10)

# Run APP
app.mainloop()