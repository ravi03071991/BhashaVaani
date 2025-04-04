from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
import os
import uuid
import requests
import base64
import wave
import io

load_dotenv()

app = Flask(__name__)

# Sarvam AI API configuration
SARVAM_SPEECH_TO_TEXT_URL = 'https://api.sarvam.ai/speech-to-text'
SARVAM_TEXT_TO_SPEECH_URL = 'https://api.sarvam.ai/text-to-speech'
SARVAM_TRANSLATE_URL = 'https://api.sarvam.ai/translate'
SARVAM_API_KEY = os.getenv('SARVAM_API_KEY')

# Language code mapping
LANGUAGE_CODES = {
    'en': 'en-IN',
    'hi': 'hi-IN',
    'bn': 'bn-IN',
    'kn': 'kn-IN',
    'ml': 'ml-IN',
    'mr': 'mr-IN',
    'te': 'te-IN',
    'ta': 'ta-IN',
    'gu': 'gu-IN',
    'pa': 'pa-IN',
    'od': 'od-IN'
}

def convert_speech_to_text(audio_file, source_lang):
    """Convert speech to text using Sarvam AI API"""
    headers = {
        "api-subscription-key": SARVAM_API_KEY
    }
    
    data = {
        "language_code": LANGUAGE_CODES.get(source_lang, source_lang),
        "model": "saarika:v2",
        "with_timestamps": False
    }
    
    files = {
        'file': ('audio.wav', audio_file, 'audio/wav')
    }
    
    response = requests.post(SARVAM_SPEECH_TO_TEXT_URL, headers=headers, files=files, data=data)
    
    if response.status_code not in [200, 201]:
        raise Exception(f"Speech-to-text API error: {response.text}")
    
    response_data = response.json()
    return response_data.get('transcript', '')

def translate_text(text, source_lang, target_lang):
    """Translate text using Sarvam AI API"""
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        'input': text,
        'source_language_code': LANGUAGE_CODES.get(source_lang, source_lang),
        'target_language_code': LANGUAGE_CODES.get(target_lang, target_lang),
        'mode': 'classic-colloquial',
        'model': 'mayura:v1',
        'enable_preprocessing': False
    }
    
    response = requests.post(SARVAM_TRANSLATE_URL, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Translation API error: {response.text}")
    
    return response.json().get('translated_text', 'Translation not available')

def convert_text_to_speech(text, target_lang):
    """Convert text to speech using Sarvam AI API"""
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": [text],
        "target_language_code": LANGUAGE_CODES.get(target_lang, target_lang),
        "speaker": "meera",
        "model": "bulbul:v1",
        "pitch": 0,
        "pace": 0.9,
        "loudness": 0.8,
        "enable_preprocessing": True
    }
    
    response = requests.post(SARVAM_TEXT_TO_SPEECH_URL, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Text-to-speech API error: {response.text}")
    
    # Get the base64-encoded audio data
    audio_data = response.json()["audios"][0]
    audio_bytes = base64.b64decode(audio_data)
    
    # Create WAV in memory
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono audio
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(22050)  # Sample rate
        wav_file.writeframes(audio_bytes)
    
    wav_buffer.seek(0)
    return wav_buffer

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/convert-speech', methods=['POST'])
def convert_speech():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio']
    source_lang = request.form.get('source_lang', 'en')
    target_lang = request.form.get('target_lang', 'en')
    
    # Save the audio file temporarily
    temp_filename = f"temp_{uuid.uuid4()}.wav"
    file.save(temp_filename)
    
    try:
        # Read the audio file
        with open(temp_filename, 'rb') as audio_file:
            # 1. Convert speech to text
            original_text = convert_speech_to_text(audio_file, source_lang)
            
            # 2. Translate the text
            translated_text = translate_text(original_text, source_lang, target_lang)
            
            # 3. Convert translated text to speech
            output_wav = convert_text_to_speech(translated_text, target_lang)
            
            # 4. Send audio data directly in response
            audio_base64 = base64.b64encode(output_wav.getvalue()).decode('utf-8')
            
            return jsonify({
                'original_text': original_text,
                'translated_text': translated_text,
                'audio_data': f'data:audio/wav;base64,{audio_base64}'
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Clean up temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

if __name__ == '__main__':
    app.run(debug=True)
