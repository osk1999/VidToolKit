import customtkinter as ctk
from customtkinter import filedialog
import threading
from pytube import YouTube, request
import yt_dlp
from yt_dlp.postprocessor import FFmpegPostProcessor
FFmpegPostProcessor._ffmpeg_location.set(R"./")

destination = ""
def main():

    # Set the default appearance
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    request.default_range_size = 1179648

    # Set up the main window
    app = ctk.CTk()
    app.title("Video Downloader Test") 
    app.geometry("600x575")

    # Set up the main frame
    mainFrame = ctk.CTkTabview(master=app)
    mainFrame.pack(fill="both", expand=True, padx=35, pady=35)

    mainFrame.add("Youtube Video Download")
    mainFrame.add("Video / Video Section Download")

    # Title label
    title = ctk.CTkLabel(master=mainFrame.tab("Youtube Video Download"), text="Youtube Video Downloader", font=("Calibri", 34))
    title.pack(padx=15, pady=10)

    # Link form
    linkInput = ctk.CTkEntry(master=mainFrame.tab("Youtube Video Download"), placeholder_text="Video Link...", width=500, height=40, font=("Calibri", 18))
    linkInput.pack(padx=20, pady=10)

    # Threads to download video
    def download_video_pageA():
        progress_label.configure(text="0%")
        progress_bar.set(0.0)

        download_youtube_thread = threading.Thread(target=download_youtube_video_thread, args=(destination, ))
        download_youtube_thread.start()

    def download_video_pageB():
        if section_start_input.get() == "" and section_end_input.get() == "":
            download_video_thread = threading.Thread(target=download_video_regular_thread, args=(destination, ))
            download_video_thread.start()
        else:
            download_video_section = threading.Thread(target=download_video_sections_thread, args=(destination, ))
            download_video_section.start()

    def download_video_regular_thread(dest):
        yt_dlp_options = {
            "format" : "bestvideo[ext=mp4]+bestaudio[ext=mp4]/best[ext=mp4]/best",
            "outtmpl" : dest+r"/%(title)s.%(ext)s"
        }
        finish_label.configure(text="Working...")
        with yt_dlp.YoutubeDL(yt_dlp_options) as ytdlp:
            ytdlp.download(linkInputB.get())
        finish_label.configure(text="Finished!")

    def download_video_sections_thread(dest):
        finish_label.configure(text="Working...")
        start = section_start_input.get()
        end = section_end_input.get()
        start_end = parse_times(start, end)

        yt_dlp_options = {
            "download_ranges" : yt_dlp.utils.download_range_func(None, [(int(start_end["start"]), int(start_end["end"]))]),
            "format" : "bv+ba/b",
            "postprocessors" : [{
                "key" : "FFmpegVideoConvertor",
                "preferedformat" : "mp4",
            }],
            "outtmpl" : dest+r"/%(title)s.%(ext)s"
        }
        with yt_dlp.YoutubeDL(yt_dlp_options) as ytdlp:
            ytdlp.download(linkInputB.get())

        finish_label.configure(text="Finished!")
        
    def parse_times(s, e):
        start_final = 0
        end_final = 0

        start = s.split(":") 
        end = e.split(":") 

        for x in range(0, len(start)):
            for y in range(len(start)-1-x, -1, -1):
                start_final += int(start[x])*(pow(60, y))
                break
        
        for a in range(0, len(end)):
            for b in range(len(end)-1-a, -1, -1):
                end_final += int(end[a])*(pow(60, b))
                break

        times = {
            "start" : start_final,
            "end" : end_final
        }
        return times

    def download_youtube_video_thread(dest):
        status_label_pageA.configure(text="Working...")
        link = linkInput.get()
        videoObj = YouTube(link, on_progress_callback=change_progress)
        videoObj.streams.get_highest_resolution().download(dest)
        status_label_pageA.configure(text="Finished!")

    def change_progress(stream, chunk, bytes_remaining):
        size = stream.filesize
        downloaded = size - bytes_remaining
        percentage = downloaded / size * 100

        progress_label.configure(text=str(round(percentage))+"%")
        progress_bar.set(float(percentage / 100))

    def pick_destination():
        global destination
        destination = str(filedialog.askdirectory())


    confirm_button = ctk.CTkButton(master=mainFrame.tab("Youtube Video Download"), text="Download", command=download_video_pageA, width=300, height=40, font=("Calibri", 20))
    confirm_button.pack(padx=15, pady=15)

    file_destination_btn_pageA = ctk.CTkButton(master=mainFrame.tab("Youtube Video Download"), text="Choose Destination", command=pick_destination, width=200, height=30, font=("Calibri", 16))
    file_destination_btn_pageA.pack(padx=15, pady=10)

    progress_label = ctk.CTkLabel(master=mainFrame.tab("Youtube Video Download"), text="0%", font=("Calibri", 20))
    progress_label.pack(padx=10, pady=5)

    progress_bar = ctk.CTkProgressBar(master=mainFrame.tab("Youtube Video Download"), width=500, height=20)
    progress_bar.set(0.0)
    progress_bar.pack(padx=15, pady=5)

    status_label_pageA = ctk.CTkLabel(master=mainFrame.tab("Youtube Video Download"), text="", font=("Calibri", 30))
    status_label_pageA.pack(padx=10, pady=5)

    
    #Set up 2nd tab

    videolabel = ctk.CTkLabel(master=mainFrame.tab("Video / Video Section Download"), text="Video / Video Section Download", font=("Calibri", 34))
    videolabel.pack(padx=15, pady=15)

    linkInputB = ctk.CTkEntry(master=mainFrame.tab("Video / Video Section Download"), font=("Calibri", 18), width=400, height=40, placeholder_text="Video Link...")
    linkInputB.pack(padx=15, pady=15)

    section_start_input = ctk.CTkEntry(master=mainFrame.tab("Video / Video Section Download"), placeholder_text="Start...", font=("Calibri", 16), width=150, height=40)
    section_start_input.pack(padx=5, pady=15)
    section_end_input = ctk.CTkEntry(master=mainFrame.tab("Video / Video Section Download"), placeholder_text="End...", font=("Calibri", 16), width=150, height=40)
    section_end_input.pack(padx=5, pady=15)

    confirm_buttonB = ctk.CTkButton(master=mainFrame.tab("Video / Video Section Download"), text="Download", font=("Calibri", 20), command=download_video_pageB, width=300, height=40)
    confirm_buttonB.pack(padx=15, pady=15)

    file_destination_btn_pageB = ctk.CTkButton(master=mainFrame.tab("Video / Video Section Download"), text="Choose Destination", command=pick_destination, width=200, height=30, font=("Calibri", 16))
    file_destination_btn_pageB.pack(padx=15, pady=10)

    finish_label = ctk.CTkLabel(master=mainFrame.tab("Video / Video Section Download"), text="", font=("Calibri", 30))
    finish_label.pack(padx=15)

    app.mainloop()

if __name__ == "__main__":
    main()
