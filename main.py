import yt_dlp, os, subprocess, argparse

class Downloading:
    @staticmethod
    def url_method(url: str, audio_only: bool = False, video_only: bool = False) -> str:
        if audio_only and video_only:
            raise ValueError("Cannot specify both audio_only and video_only at the same time.")
        
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': 'bestaudio/best' if audio_only else 'bestvideo[ext=mp4]/best' if video_only else 'bestvideo+bestaudio/best',
            'noplaylist': True,
            'quiet': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                file_name = ydl.prepare_filename(info_dict)
            return os.path.realpath(file_name)
        except Exception as e:
            raise SystemError("Unable to download video or audio")

    @staticmethod
    def convert_to_mp4(file_path: str) -> str:
        if file_path.endswith('.webm'):
            mp4_path = file_path.rsplit('.', 1)[0] + '.mp4'
            try:
                subprocess.run(
                    ['ffmpeg', '-i', file_path, '-c:v', 'copy', '-c:a', 'aac', mp4_path],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

                # Remove old WEBM file
                os.remove(file_path)
                return mp4_path
            except Exception as e:
                raise SystemError("Failed to convert to MP4")
        return file_path

def main():
    parser = argparse.ArgumentParser(description="Download and optionally convert videos to MP4.")
    parser.add_argument('url', type=str, help="The URL of the media to download.")
    parser.add_argument('--convert', action='store_true', help="Convert the downloaded file to MP4 format.")
    parser.add_argument('--audio', action='store_true', help="Download only the audio of the media.")
    parser.add_argument('--videoonly', action='store_true', help="Download only the video of the media (no audio).")

    args = parser.parse_args()

    try:
        downloaded_path = Downloading.url_method(args.url, audio_only=args.audio, video_only=args.videoonly)
        final_path = downloaded_path
        if args.convert and not args.audio:
            final_path = Downloading.convert_to_mp4(downloaded_path)
        print(final_path or "Couldn't resolve video/audio output path")
    except Exception as e:
        print("Failed to download or convert")

if __name__ == '__main__':
    main()
