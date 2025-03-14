import vosk
import sounddevice as sd
import queue
import json
import tkinter as tk
from threading import Thread

model = vosk.Model("vosk-model-small-en-us-0.15")  # Change model path if needed
q = queue.Queue()

listening = False

def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    q.put(bytes(indata))

def recognize_speech():
    global listening
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        while listening:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "[No speech detected]")
                subtitle_label.config(text=text)

def start_listening():
    global listening, thread
    if not listening:
        listening = True
        subtitle_label.config(text="Listening...")
        thread = Thread(target=recognize_speech, daemon=True)
        thread.start()

def stop_listening():
    global listening
    listening = False
    subtitle_label.config(text="Stopped")

# Create Tkinter GUI
root = tk.Tk()
root.title("Speech To Text")
root.geometry("600x250")

subtitle_label = tk.Label(root, text="Click 'Start' to begin", font=("Arial", 16), wraplength=500)
subtitle_label.pack(pady=20)

start_button = tk.Button(root, text="Start", font=("Arial", 14), command=start_listening)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop", font=("Arial", 14), command=stop_listening)
stop_button.pack(pady=5)

root.mainloop()
