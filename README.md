# Chess-LLM

A project that uses the OpenRouter API to allow two different LLM models to play chess.

## Gallery

### llama-4-maverick(White) vs. llama-3.3-70b-instruct(Black)

![llama-4-maverick vs. llama-3.3-70b-instruct](https://images.chesscomfiles.com/uploads/game-gifs/90px/green/neo/0/cc/0/0/bUMhVGd2MEtic1RKbEI5MGZBMFRlZ0tCdks1UXNKVEtkRVpSSlQ4OUUyOTBBMVF6ZmV6UWdoM1ZlZ1JKQ0pRemNWS0RKUjdSVEpSSjFVMDcyWjdaVTFaUjFKUktWTTZTSlNLQ1NKekphZUR1TXVKMHVCQ0pCSzBVZUNVREsyP1YyS1ZOS1JKUkMwUjBweDQhb3dORndFRk5udk5GZ29GTmhnMDFFTU5GZ24hOW9wRk54RjkhcG8hMm9FMlVuZzEhRURVTWdwWVFERU5GcHdNRXduRjNuZVFJdkVJQUVNWEhNVUh6VTIzTmVuTjNudVdHaXl6cmtyQXJ1QjNOQnVORnVuRj8yfSE_bnU_IXV0ITl0QTk4QUg4WkhHWjhHejg3ekk3WUlIWTV5RzU2R082Wk9XWjhXfjgxNDkxOUhROTFRWDE5WFE5OFFIODdIUDcwUFgwMVhQMVRQWFQyWFAyVVBIVTJIUDJUUEhUS0hJS0NJekNLenJLQ3JBQ0tBdEtTdENTMGpyMDhyejgwQ0owWg,,.gif)

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