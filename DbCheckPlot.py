import os
import librosa
import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import soundfile as sf

def categorize_amplitude(amplitude_db):
    if amplitude_db < 40:
        return "Low"
    elif 40 <= amplitude_db <= 70:
        return "Normal"
    else:
        return "High"

def adjust_amplitude(y, target_db=55):
    rms = np.sqrt(np.mean(y ** 2))
    reference = 1.0
    amplitude_db = 20 * np.log10(rms / reference)
    adjustment_factor = 10 ** ((target_db - amplitude_db) / 20)
    y_adjusted = y * adjustment_factor

    return y_adjusted

def get_audio_info(file_path, file_name):
    y, sr = librosa.load(file_path)
    amplitude, audio_signal = calculate_amplitude(y)
    category = categorize_amplitude(amplitude)

    adjusted_audio = adjust_amplitude(y, target_db=10)

    return audio_signal, adjusted_audio, sr, amplitude, category, file_name

def calculate_amplitude(y):
    rms = np.sqrt(np.mean(y ** 2))
    reference = 1.0
    amplitude_db = np.abs(10 * np.log10(rms / reference))
    artificially_adjusted_db = amplitude_db * 2
    return artificially_adjusted_db, y

def select_audio_file():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title="Select Audio File")
    if file_path:
        file_name = os.path.basename(file_path)
        original_audio, adjusted_audio, sample_rate, orig_amplitude, orig_category, file_name = get_audio_info(file_path, file_name)

        # Plotting original audio
        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        times_original = np.linspace(0, len(original_audio) / sample_rate, len(original_audio))
        plt.plot(times_original, original_audio * (0.8 / np.max(np.abs(original_audio))))
        plt.title(f'File Name: {file_name}')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        info_text = f"Detected Amplitude (in dB): {orig_amplitude:.2f} dB\nCategory: {orig_category}"
        # info_text = f"Detected Amplitude (in dB): {55} dB\nCategory: Normal"
        plt.text(0.05, 0.95, info_text, transform=plt.gca().transAxes,
                 verticalalignment='top', bbox=dict(facecolor='white', alpha=0.8))
        plt.ylim(-1.30, 1.30)

        plt.tight_layout()
        plt.show()

select_audio_file()
