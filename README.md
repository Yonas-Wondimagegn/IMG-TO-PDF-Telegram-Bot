# IMG-TO-PDF-Telegram-Bot
This Telegram bot converts a series of images into a PDF file. Users can send images, and the bot will compile them into a single PDF document.This Telegram bot converts a series of images into a PDF file. Users can send images, and the bot will compile them into a single PDF document.


## Features

- **Convert Images to PDF**: Send multiple images, and the bot will convert them into a PDF.
- **Interactive**: Uses buttons to start the process and informs users about the steps.
- **Error Handling**: Handles errors gracefully and informs the user if something goes wrong.

## Commands

- `/start` - Start the bot and display the welcome message.
- `/help` - Show a help message with instructions.
- `/done` - Finish sending images and generate the PDF.

## Prerequisites

- Python 3.7 or later
- `python-telegram-bot` library
- `Pillow` library

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/telegram-pdf-converter-bot.git
   cd telegram-pdf-converter-bot
2. **Install dependencies**:

pip install -r requirements.txt

3. Set up the environment variables:

Edit config.py and set your Telegram bot token.
TOKEN = 'YOUR_OWN_TOKEN'


4. **Run the bot**:

python main.py


Contributing

Contributions are welcome:)...Feel free to fork the repository make changes and submit a pull request
