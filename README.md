# YouTube Study Assistant

A smart AI assistant that helps you study and understand YouTube videos by automatically extracting and processing video captions.

## Features

- **Transcript Extraction**: Automatically extracts captions from any YouTube video URL
- **Language Support**: Works with videos in multiple languages
- **Translation**: Can translate captions from other languages to English
- **Summarization**: Summarizes key points from videos to aid understanding
- **Persistent Memory**: Retains conversation history for better context awareness

## How It Works

1. Share a YouTube video URL with the assistant
2. The assistant extracts the video's captions/transcript
3. The text is processed and analyzed by the Gemini AI model
4. The assistant provides a summary and helps you understand the content
5. You can ask follow-up questions about the video

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys (see Environment Variables section)
4. Run the application:
   ```
   python test.py
   ```

## Environment Variables

Create a `.env` file in the project root with the following variables:
- `GOOGLE_API_KEY`: Your Google API key for Gemini model access

## Requirements

See requirements.txt for a list of dependencies.

## License

This project is provided for educational purposes.
