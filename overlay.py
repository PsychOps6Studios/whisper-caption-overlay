import tkinter as tk

class SubtitleOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Whisper Captions")
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.8)
        self.root.configure(bg='black')
        self.root.geometry("800x100+50+800")  # Size and position
        self.root.overrideredirect(True)

        self.label = tk.Label(self.root, text="", font=("Helvetica", 20), fg="white", bg="black", wraplength=780)
        self.label.pack(expand=True, fill='both')

    def update_text(self, text):
        self.label.config(text=text)

    def run(self):
        self.root.mainloop()
