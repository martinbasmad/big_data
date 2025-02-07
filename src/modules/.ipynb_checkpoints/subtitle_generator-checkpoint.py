import os
import whisper
import yt_dlp


class YouTubeAudioExtractor:
    """
    Clase para extraer el audio de un video de YouTube y guardarlo como audio.wav.
    """

    def __init__(self, video_url, output_file="audio.wav"):
        self.video_url = video_url
        self.output_file = output_file

    def download_audio(self):
        """ Descarga y convierte el audio del video de YouTube a formato WAV. """
        # Eliminar el archivo previo si existe
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

        print(f"🎵 Extrayendo audio del video {self.video_url}...")

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192'
            }],
            'outtmpl': "audio"  # yt_dlp agregará .wav automáticamente
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.video_url])

            if not os.path.exists(self.output_file):
                raise FileNotFoundError("No se pudo extraer el audio.")

            print("✅ Audio extraído correctamente.")

        except Exception as e:
            print(f"❌ Error al extraer el audio: {e}")
            return False

        return True


class WhisperTranscriber:
    """
    Clase para transcribir audio usando Whisper de OpenAI.
    """

    def __init__(self, audio_file="audio.wav", model_size="small"):
        self.audio_file = audio_file
        self.model_size = model_size
        self.transcription = ""

    def transcribe_audio(self):
        print("🔍 Transcribiendo audio con Whisper...")
        
        try:
            model = whisper.load_model(self.model_size)  
            result = model.transcribe(self.audio_file, fp16=False)  
            self.transcription = result["text"]
            print("✅ Transcripción completada.")
        except Exception as e:
            print(f"❌ Error al transcribir el audio: {e}")
            return False

        return True

    def save_transcription(self, output_file="subtitulos.txt"):
        """ Guarda la transcripción en un archivo de texto. """
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(self.transcription)
            print(f"✅ Transcripción guardada en {output_file}")
        except Exception as e:
            print(f"❌ Error al guardar la transcripción: {e}")


class SubtitleGenerator:
    """
    Clase principal que ejecuta todo el flujo: extracción de audio y transcripción.
    """

    def __init__(self, video_url):
        self.video_url = video_url
        self.audio_file = "audio.wav"
        self.subtitle_file = "subtitulos.txt"

    def run(self):
        extractor = YouTubeAudioExtractor(self.video_url, self.audio_file)
        if not extractor.download_audio():
            print("❌ Proceso detenido.")
            return

        transcriber = WhisperTranscriber(self.audio_file)
        if not transcriber.transcribe_audio():
            print("❌ Proceso detenido.")
            return

        transcriber.save_transcription(self.subtitle_file)

        # 🔥 Eliminar el archivo de audio después de la transcripción
        os.remove(self.audio_file)

