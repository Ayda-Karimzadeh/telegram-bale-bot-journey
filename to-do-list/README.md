# To-Do List Bot

A Bale/Telegram to-do list bot with interactive inline buttons, task 
status tracking, and a conversation state machine — available in both 
English and Persian versions.

## Features
- **Add Task** — add up to 10 tasks per user
- **Tasks List** — view tasks as inline buttons; tap to mark done/undone (●/○)
- **Delete** — delete a single task by tapping it, or clear the entire list
- **Stats** — see how many tasks are still pending
- Persian localized version available (`fa_main.py`)

## How it works
- Built with `pyTelegramBotAPI`, connected to the Bale API
- **Conversation flow** is managed through a `user_state` column in SQLite 
  (e.g. `adding task`, `deleting tasks`, `to do list`) so the bot knows how 
  to interpret the next message from each user
- Task status (done/not done) is toggled with a single SQL `NOT status` update
- Tasks are shown as **inline keyboard buttons** that update live when tapped, 
  using `edit_message_text` instead of sending new messages each time
- A 10-task limit per user is enforced in code

## Tech
- Python
- pyTelebot
- SQLite3

## Note
An alternative in-memory state approach (`state/state_manager.py`, a simple 
dict-based state store) was also explored during development, alongside the 
database-driven approach used in the final version.