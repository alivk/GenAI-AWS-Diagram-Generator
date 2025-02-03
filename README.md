# GenAI Best English to Chinese Dictionary

A Streamlit application that provides detailed dictionary explanations for words and sentences, including:
- Word definitions
- UK pronunciations
- English and Chinese explanations
- Example sentences
- Audio pronunciation

## Features
- Get detailed word explanations
- UK English pronunciation
- Bilingual explanations (English & Chinese)
- Example sentences with alternatives
- Markdown formatted output

## Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run src/main.py
   ```

## Requirements
- Python 3.8+
- Streamlit
- boto3
- gTTS

## File Structure
```
project/
├── src/                # Source code
│   ├── main.py         # Main application
│   ├── prompts.py      # Prompt templates
│   ├── audio_utils.py  # Audio generation utilities
│   ├── bedrock_utils.py# Bedrock API utilities
├── temp/               # Temporary files
├── README.md           # Documentation
```

## Usage
1. Enter a word or sentence in the input field
2. View the detailed explanation
3. Click "Pronounce (UK English)" to hear the pronunciation

## Example Usecases

> If we input - I have a Nintendo `switch`

[Alt text of the image](https://github.com/alivk/GenAI-Best-English-to-Chinese-Dictionary/blob/main/temp/example_001.png)

> If we input - I have a cisco `switch`

[Alt text of the image](https://github.com/alivk/GenAI-Best-English-to-Chinese-Dictionary/blob/main/temp/example_002.png)