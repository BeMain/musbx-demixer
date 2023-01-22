import os

from flask import Flask, send_file, abort, render_template

from pytube import YouTube

app = Flask(__name__)


@app.route("/separate/<youtube_id>", methods=["GET"])
def separate(youtube_id: str):
    separated_files_dir = f"separated/htdemucs_6s/{youtube_id}/"

    if not os.path.exists(separated_files_dir):
        separate_youtube_video(youtube_id)

    return send_file(f"separated/htdemucs_6s/{youtube_id}/other.mp3", as_attachment=True)


def separate_youtube_video(youtube_id: str):
    yt = YouTube(f'https://youtu.be/{youtube_id}')
    audio_streams = yt.streams.filter(only_audio=True, file_extension='mp4')

    if len(audio_streams) == 0:
        return f"No audio found for video with id: {youtube_id}"

    audio_stream = audio_streams[0]
    file_path = audio_stream.download(filename=f"{youtube_id}.mp4")

    os.system(f"demucs {file_path} -n htdemucs_6s --mp3")
    try:
        os.remove(file_path)
    except:
        print(f"Unable to delete file '{file_path}'; file doesn't exist.")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
