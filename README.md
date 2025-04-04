# BhashaVaani (भाषावाणी)

BhashaVaani is a real-time voice translation application designed specifically for Indian languages. It enables seamless communication across different Indian languages by providing instant voice-to-voice translation.

**🚀 Live Demo: [https://bhashavaani.onrender.com/](https://bhashavaani.onrender.com/) 🚀**

## Features

- **Voice Input**: Record your voice in any supported Indian language
- **Real-time Translation**: Instant translation to your chosen target language
- **Voice Output**: Hear the translation in a natural voice
- **Multiple Indian Languages**: Supports:
  - Hindi
  - Telugu
  - Tamil
  - Kannada
  - Malayalam
  - Bengali
  - Marathi
  - Gujarati
  - Punjabi
  - Odia

Note: Supports English language too.

## Tech Stack

### Frontend
- HTML5
- TailwindCSS for styling
- Vanilla JavaScript
- Web Audio API for voice recording

### Backend
- Python
- Flask web framework
- Sarvam AI APIs for:
  - Speech-to-Text (ASR)
  - Text Translation
  - Text-to-Speech (TTS)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ravi03071991/BhashaVaani
   cd BhashaVaani
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the backend directory with:
   ```env
   SARVAM_API_KEY=your_api_key
   ```

5. Run the application:
   ```bash
   cd backend
   python app.py
   ```

6. Open your browser and visit:
   ```
   http://localhost:5000
   ```

## Project Structure

```
.
├── frontend/           # Frontend source code
│   └── index.html      # Main application interface
├── backend/            # Backend application
│   ├── app.py         # Flask application
│   ├── requirements.txt # Python dependencies
│   ├── .env           # Environment variables
│   └── static/        # Static files and audio storage
├── .gitignore         # Git ignore rules
└── README.md          # Project documentation
```

## API Integration

This application uses Sarvam AI's APIs for its core functionality:
- Speech-to-Text: Converts recorded voice to text
- Translation: Translates text between Indian languages
- Text-to-Speech: Converts translated text back to voice

---

Built with ❤️ for Indian Languages
