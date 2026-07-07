# Self-Improvement Notebook (Grow Track Bot)

A Bale/Telegram bot that helps users track personal growth by logging 
daily progress notes, with simple stats to see how consistent they've been.

## Features
- **Add** — log a new progress note (saved with timestamp)
- **List** — view all previously saved notes with date and time
- **Stats** — see the total number of progress entries logged

## How it works
- Built with `pyTelegramBotAPI` (telebot), connected to the Bale API
- Data is stored in **SQLite** with two tables:
  - `users` — stores Telegram/Bale user id and name
  - `progresses` — stores each progress note, linked to the user via foreign key
- Uses `register_next_step_handler` to capture the user's next message as their progress note
- Bot token and database path are read from environment variables (`API_TOKEN`, `BOT_DB`) — no secrets hardcoded

## Tech
- Python
- pyTelebot
- SQLite3