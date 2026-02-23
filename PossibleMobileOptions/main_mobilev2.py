import flet as ft
from pytubefix import YouTube
import os

def main(page: ft.Page):
    page.title = "Youtube Downloader"
    page.window_width = 720
    page.window_height = 550
    
    # Use a dictionary to store state so it's accessible everywhere
    state = {"path": os.getcwd()}

    # Initialize FilePicker safely
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    def on_progress(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = bytes_downloaded / total_size
        progress_bar.value = percentage
        p_percentage.value = f"{int(percentage * 100)}%"
        page.update()

    def pick_folder_result(e: ft.FilePickerResultEvent):
        if e.path:
            state["path"] = e.path
            path_text.value = f"Selected Path: {e.path}"
            page.update()

    # Assign event handler after initialization
    file_picker.on_result = pick_folder_result

    def start_download(e):
        try:
            if not link_input.value:
                finish_label.value = "Please enter a link!"
                finish_label.color = "orange"
                page.update()
                return

            finish_label.value = "Downloading..."
            finish_label.color = "blue"
            page.update()

            yt = YouTube(link_input.value, on_progress_callback=on_progress)
            # Defaulting to audio as in your original request
            video = yt.streams.get_audio_only()
            
            title_label.value = f"Downloading: {yt.title}"
            video.download(output_path=state["path"])
            
            finish_label.value = "Downloaded Successfully!"
            finish_label.color = "green"
        except Exception as ex:
            finish_label.value = "Download ERROR!"
            finish_label.color = "red"
            print(f"Error: {ex}")
        page.update()

    # UI Elements using string-based colors/icons for compatibility
    title_label = ft.Text("Insert a YouTube link", size=20, weight="bold")
    link_input = ft.TextField(label="URL", width=400, border_color="blue")
    finish_label = ft.Text("")
    p_percentage = ft.Text("0%")
    progress_bar = ft.ProgressBar(width=400, value=0, color="blue")
    path_text = ft.Text(f"Default Path: {state['path']}", size=12, italic=True)

    page.add(
        ft.Column(
            [
                title_label,
                link_input,
                finish_label,
                p_percentage,
                progress_bar,
                ft.Button(
                    "Select Download Folder", 
                    icon="FOLDER_OPEN", 
                    on_click=lambda _: file_picker.get_directory_path(),
                    bgcolor="green",
                    color="white"
                ),
                ft.Button("Start Download", on_click=start_download, width=200),
                path_text
            ],
            alignment="center",
            horizontal_alignment="center",
        )
    )

ft.run(main)