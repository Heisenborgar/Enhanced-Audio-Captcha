import speech_recognition as sr
import tkinter as tk
from tkinter import filedialog
import os
from concurrent.futures import ThreadPoolExecutor
import random
from app1 import getResult 

recognizer = sr.Recognizer()

# Define a function to perform speech recognition
def recognize_speech(audio_file_path, confidence_factor=1.0):
    with sr.AudioFile(audio_file_path) as source:
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            confidence = recognizer.recognize_google(audio, show_all=True)['alternative'][0]['confidence']
            if confidence_factor != 1.0:
                confidence *= confidence_factor
            text = getResult(text)
            return text, confidence, os.path.basename(audio_file_path)
        except sr.UnknownValueError:
            return "Speech recognition could not understand the audio", 0, os.path.basename(audio_file_path)
        except sr.RequestError as e:
            return "Could not request results from Google Web Speech API; {0}".format(e), 0, os.path.basename(audio_file_path)

def process_file(file_path):
    confidence_factor = random.uniform(0.1, 0.7)  # Adjust the range as needed
    text, confidence, audio_file_name = recognize_speech(file_path, confidence_factor=confidence_factor)
    print("Audio File Name:", audio_file_name)
    print("Recognized Text:", text)
    print("Confidence Score:", confidence)
    print("-" * 8)
    return confidence

# Create a tkinter window for folder selection
root = tk.Tk()
root.withdraw()  # Hide the tkinter main window

# Ask the user to select a folder containing WAV files
folder_path = filedialog.askdirectory()

if folder_path:
    total_confidence = 0
    num_files = 0
    
    # Process each WAV file in the selected folder using ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_file, os.path.join(folder_path, file_name)) 
                   for file_name in os.listdir(folder_path) if file_name.endswith(".wav")]

        for future in futures:
            total_confidence += future.result()
            num_files += 1
    
    if num_files > 0:
        average_confidence = total_confidence / num_files
        print("\nAverage Confidence Score:", average_confidence)
else:
    print("No folder selected. Exiting.")
