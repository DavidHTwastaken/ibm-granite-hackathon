import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk, StringVar
import sounddevice as sd
import numpy as np

class AudioRecorder(ttk.LabelFrame):
    def __init__(self, master, fs=44100):
        super().__init__(master, text="Audio Recorder")
        self.fs = fs
        self.recording = False
        self.frames = []
        self.stream = None
        self.audio_data = None

        # Status display
        self.status_var = StringVar(value="Idle")
        lbl_status = ttk.Label(self, textvariable=self.status_var)
        lbl_status.pack(fill='x', pady=(5, 5))

        # Record/Stop toggle button
        self.btn_record = ttk.Button(self, text="Start Recording", command=self.toggle_record)
        self.btn_record.pack(fill='x', pady=(0, 5))

        # Play button
        self.btn_play = ttk.Button(self, text="Play Recording", command=self.play_audio)
        self.btn_play.pack(fill='x', pady=(0, 5))

    def toggle_record(self):
        if sd is None:
            messagebox.showerror("Error", "sounddevice library is required for audio recording.")
            return
        if not self.recording:
            # Start recording
            self.frames = []
            self.stream = sd.InputStream(samplerate=self.fs, channels=1, callback=self._callback)
            self.stream.start()
            self.recording = True
            self.status_var.set("Recording...")
            self.btn_record.config(text="Stop Recording")
        else:
            # Stop recording
            self.recording = False
            if self.stream:
                self.stream.stop()
                self.stream.close()
            if self.frames:
                self.audio_data = np.concatenate(self.frames, axis=0)
            self.status_var.set("Idle")
            self.btn_record.config(text="Start Recording")

    def _callback(self, indata, frames, time, status):
        if self.recording:
            self.frames.append(indata.copy())

    def play_audio(self):
        if sd is None:
            messagebox.showerror("Error", "sounddevice library is required for playback.")
            return
        if self.audio_data is not None:
            sd.play(self.audio_data, self.fs)
        else:
            messagebox.showwarning("Warning", "No audio recorded yet.")

class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(padx=10, pady=10)
        master.title("Code Gen")
        master.geometry("600x400")

        # Project zip selection
        self.project_var = StringVar(value="No file selected")
        btn_select = ttk.Button(self, text="Select Project Zip", command=self.select_project)
        btn_select.pack(fill='x')
        lbl_project = ttk.Label(self, textvariable=self.project_var)
        lbl_project.pack(fill='x', pady=(5, 10))

        # Audio recorder widget
        self.audio_widget = AudioRecorder(self)
        self.audio_widget.pack(fill='x', pady=(0, 10))

        # Generate button
        btn_generate = ttk.Button(self, text="Generate", command=self.generate)
        btn_generate.pack(fill='x')

    def select_project(self):
        file = filedialog.askopenfilename(filetypes=[("Zip files", "*.zip")])
        if file:
            self.project_var.set(file)
        else:
            self.project_var.set("No file selected")

    def generate(self):
        # Placeholder for generate functionality
        messagebox.showinfo("Generate", "Generate button clicked.")


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
