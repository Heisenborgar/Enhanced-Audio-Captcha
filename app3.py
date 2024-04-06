import os
import random
import numpy as np
from flask import Flask, render_template, jsonify
from pydub import AudioSegment

app = Flask(__name__)

audio_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'audio_database', 'audio_questions')
audio_files = [file for file in os.listdir(audio_folder) if file.endswith(('.wav'))]
selected_questions = set()

def get_audio_volume(audio_file):
    low_threshold = 40
    high_threshold = 70
    
    audio = AudioSegment.from_file(os.path.join(audio_folder, audio_file))
    raw_audio_data = audio.get_array_of_samples()
    rms = np.sqrt(np.mean(np.square(raw_audio_data)))
    volume_before = 13 * np.log10(rms / (2**16))
    
    if volume_before < low_threshold:
        boost_reduce = 1.5
        result = f"From Low Volume To Normal: ({abs(volume_before):.2f} dB)"
        volume_status = "Low Volume"
    elif low_threshold <= volume_before <= high_threshold:
        boost_reduce = 1
        result = f"Normal Volume: ({abs(volume_before):.2f} dB)"
        volume_status = "Normal Volume"
    else:
        boost_reduce = 0.5
        result = f"From High Volume To Normal: ({abs(volume_before):.2f} dB)"
        volume_status = "High Volume"
    
    # Adjusting volume
    audio += abs(boost_reduce)
    
    raw_audio_data = audio.get_array_of_samples()
    rms = np.sqrt(np.mean(np.square(raw_audio_data)))
    volume_after = 16 * np.log10(rms / (2**16))
    
    print(f"Before volume adjustment: {abs(volume_before):.2f} dB ({volume_status})")
    print(f"After volume adjustment: {abs(volume_after):.2f} dB")
    
    return result, audio

def overlay_noise(audio, noise):
    while len(noise) < len(audio):
        noise = noise + noise
    combined = audio.overlay(noise[:len(audio)], position=0)
    return combined

@app.route('/')
def index():
    # global selected_questions
    # available_audio_files = set(audio_files) - selected_questions
    # if not available_audio_files:
    #     selected_questions.clear()
    #     available_audio_files = set(audio_files)
    # random_audio = random.choice(list(available_audio_files))
    # selected_questions.add(random_audio)
    # audio_path = f'/static/audio_database/audio_questions/{random_audio}'
    # result, audio = get_audio_volume(random_audio)
    
    # noise_path = 'static/noise.wav'
    # noise = AudioSegment.from_file(noise_path, format="wav")
    # audio_with_noise = overlay_noise(audio, noise)
    # audio_with_noise_path = os.path.join(os.path.dirname('static/audio_database/audio_temp/'), f'{random_audio}')
    # audio_with_noise.export(audio_with_noise_path, format="wav")

    # return render_template('prototype.html', audio_path=audio_with_noise_path)
    return render_template('prototype.html')

@app.route('/get_random_audio_question')
def get_random_audio():
    global selected_questions
    available_audio_files = set(audio_files) - selected_questions
    if not available_audio_files:
        selected_questions.clear()
        available_audio_files = set(audio_files)
    random_audio = random.choice(list(available_audio_files))
    selected_questions.add(random_audio)
    audio_path = f'/static/audio_database/audio_questions/{random_audio}'
    result, audio = get_audio_volume(random_audio)

    noise_path = 'static/noise.wav'
    noise = AudioSegment.from_file(noise_path, format="wav")
    audio_with_noise = overlay_noise(audio, noise)

    audio_with_noise_path = os.path.join(os.path.dirname('static/audio_database/audio_temp/'), f'{random_audio}')
    audio_with_noise.export(audio_with_noise_path, format="wav")

    return jsonify({'audio_path': audio_with_noise_path})

@app.route('/welcome_page')
def welcome_page():
    return render_template('welcome.html')
    
if __name__ == '__main__':
    app.run(port=9998, debug=True)
