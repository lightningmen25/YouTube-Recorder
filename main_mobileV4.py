# AI Vertion

import flet as ft
from pytubefix import AsyncYouTube
import os

async def main(page: ft.Page):
    page.title = "Youtube Downloader"
    page.window_width = 720
    page.window_height = 550
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    state = {"path": os.getcwd()}

    # FilePicker is now handled as a service in Flet 1.0
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    async def select_folder(e):
        # Await the result directly from the service call
        path = await file_picker.get_directory_path()
        if path:
            state["path"] = path
            path_text.value = f"Selected Path: {path}"
            page.update()

    def on_progress(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        percentage = (total_size - bytes_remaining) / total_size
        progress_bar.value = percentage
        p_percentage.value = f"{int(percentage * 100)}%"
        page.update()

    async def start_download(e):
        if not link_input.value:
            finish_label.value = "Please enter a link!"
            finish_label.color = "orange"
            page.update()
            return

        download_button.disabled = True
        finish_label.value = "Downloading..."
        finish_label.color = "blue"
        page.update()

        try:
            yt = AsyncYouTube(link_input.value, on_progress_callback=on_progress)
            title_label.value = f"Downloading: {yt.title}"
            page.update()
            
            streams = await yt.streams
            video = streams.get_audio_only()
            await video.download(output_path=state["path"])
            
            finish_label.value = "Downloaded Successfully!"
            finish_label.color = "green"
        except Exception as ex:
            finish_label.value = f"Download ERROR: {ex}"
            finish_label.color = "red"
        
        download_button.disabled = False
        page.update()

    # UI Elements using the new ft.Button class
    title_label = ft.Text("Insert a YouTube link", size=20, weight="bold")
    link_input = ft.TextField(label="URL", width=400)
    finish_label = ft.Text("")
    p_percentage = ft.Text("0%")
    progress_bar = ft.ProgressBar(width=400, value=0, color="blue")
    path_text = ft.Text(f"Default Path: {state['path']}", size=12, italic=True)
    
    # ElevatedButton -> Button
    download_button = ft.Button("Start Download", on_click=start_download, width=200)

    page.add(
        ft.Column(
            [
                title_label,
                link_input,
                finish_label,
                p_percentage,
                progress_bar,
                ft.Button( # ElevatedButton -> Button
                    "Select Download Folder", 
                    icon=ft.Icons.FOLDER_OPEN, 
                    on_click=select_folder, 
                    bgcolor="green",
                    color="white"
                ),
                download_button,
                path_text
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.run(main)
