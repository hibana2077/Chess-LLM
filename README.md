# Chess-LLM

A project that uses the OpenRouter API to allow two different LLM models to play chess.

## Features

- 🤖 Supports multiple LLM models for gameplay
- ♟️ Complete implementation of chess rules
- 🧠 Records the reasoning behind each move
- 📝 Automatically generates PGN game records
- 🎨 Colorful terminal interface
- 📊 Board analysis and statistics

## System Architecture

### Chess Core
- Handles board state and move validation
- Implements game rules
- PGN export functionality

### LLM Inference Core
- Communicates with the OpenRouter API
- Generates structured prompts
- Records reasoning processes

### Main
Gameplay flow: White moves first → White thinks → White moves → Black thinks → Black moves

## Installation Steps

1. Clone the project:

```bash
git clone <repository-url>
cd Chess-LLM
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure the API key:

```bash
cp .env.example .env
# Edit the .env file and enter your OpenRouter API key
```

## Usage

```bash
python main.py
```

## Configuration Options

In `config.py`, you can adjust the following settings:

- `WHITE_MODEL`: Model used for White
- `BLACK_MODEL`: Model used for Black
- `MAX_MOVES`: Maximum number of moves
- `THINKING_TIMEOUT`: Thinking timeout duration

## Output Files

Each game generates the following files:

- `game_YYYYMMDD_HHMMSS.pgn`: Game record in PGN format
- `thinking_logs_YYYYMMDD_HHMMSS.json`: Detailed record of the reasoning process
- `game_log.txt`: Real-time game log

## Supported Models

Models available through OpenRouter include:

- `meta-llama/llama-4-maverick`
- `meta-llama/llama-3.3-70b-instruct`
- `google/gemini-2.5-pro-preview`
- and many more...

## System Requirements

- Python 3.8+
- OpenRouter API key
- Internet connection