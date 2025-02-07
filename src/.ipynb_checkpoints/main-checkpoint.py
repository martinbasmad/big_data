from modules import subtitle_generator

if __name__ == "__main__":
    video_url = input("🔗 Ingresa la URL del video de YouTube: ").strip()
    generator = subtitle_generator.SubtitleGenerator(video_url)
    generator.run()
