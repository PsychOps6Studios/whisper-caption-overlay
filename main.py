import whisper
import threading
import time
from overlay import SubtitleOverlay
import pyaudio
import wave

model = whisper.load_model("base")  # You can use "small" or "medium" for better accuracy

def record_audio_chunk(filename="temp.wav", duration=5):
    RATE = 16000
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)

    frames = []
    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filename

def live_transcription(overlay):
    while True:
        audio_file = record_audio_chunk()
        result = model.transcribe(audio_file)
        overlay.update_text(result["text"])
        time.sleep(0.5)

if __name__ == "__main__":
    overlay = SubtitleOverlay()
    thread = threading.Thread(target=live_transcription, args=(overlay,))
    thread.daemon = True
    thread.start()
    overlay.run()
