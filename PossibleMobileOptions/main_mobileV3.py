## AI Vertion

import flet as ft
from pytubefix import YouTube
import os
import threading # Add this

async def main(page: ft.Page):
    page.title = "Youtube Downloader"
    page.window_width = 720
    page.window_height = 550
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    state = {"path": os.getcwd()}

    # Initialize FilePicker
   
    async def select_folder(e):
        await file_picker.get_directory_path()
    file_picker = ft.FilePicker()

    # Add FilePicker to overlay
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

    file_picker.on_result = pick_folder_result

    # Move the heavy lifting to a background function
    def download_task(url, export_path):
        try:
            yt = YouTube(url, on_progress_callback=on_progress)
            video = yt.streams.get_audio_only()
            title_label.value = f"Downloading: {yt.title}"
            page.update()
            
            video.download(output_path=export_path)
            
            finish_label.value = "Downloaded Successfully!"
            finish_label.color = "green"
        except Exception as ex:
            finish_label.value = "Download ERROR!"
            finish_label.color = "red"
            print(f"Error: {ex}")
        
        # Re-enable button after finished
        download_button.disabled = False
        page.update()

    def start_download(e):
        if not link_input.value:
            finish_label.value = "Please enter a link!"
            finish_label.color = "orange"
            page.update()
            return

        finish_label.value = "Downloading..."
        finish_label.color = "blue"
        download_button.disabled = True # Prevent double clicks
        page.update()

        # Start the thread
        page.update(target=download_task, args=(link_input.value, state["path"]), daemon=True).start()

    # UI Elements
    title_label = ft.Text("Insert a YouTube link", size=20, weight="bold")
    link_input = ft.TextField(label="URL", width=400)
    finish_label = ft.Text("")
    p_percentage = ft.Text("0%")
    progress_bar = ft.ProgressBar(width=400, value=0, color="blue")
    path_text = ft.Text(f"Default Path: {state['path']}", size=12, italic=True)
    download_button = ft.Button("Start Download", on_click=start_download, width=200)

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
                    icon=ft.Icons.FOLDER_OPEN, 
                    on_click=select_folder, # Now calling the async helper
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
