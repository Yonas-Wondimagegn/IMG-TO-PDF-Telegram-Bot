import os
import logging
from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext, CallbackQueryHandler, filters
from config import TOKEN  # Import the config

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Dictionary to keep track of images sent by each user
user_images = {}

# Function to "New" button
async def start(update: Update, context: CallbackContext):
    user_info = update.message.from_user
    first_name = user_info.first_name
    keyboard = [[InlineKeyboardButton("New", callback_data='new')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f'''
Hello {first_name},

Welcome to PDF CONVERTER bot📃 \n\n Click "New" to start converting images to PDF🖇

/start - Show this message

/help - Get help using the bot

''', reply_markup=reply_markup)

# Handle the "New" button click
async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text('''
                                    
Click "New" and send an image to convert it into a PDF. Once you have finished sending images, type or click /done, and your PDF will be delivered shortly⚡️🌪

''')


async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if user_id not in user_images:
        user_images[user_id] = []

    await query.edit_message_text(text="Okay, send images now. When you're done, type /done🌚")

# Handle photo messages
async def handle_photo(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    photo_file = await update.message.photo[-1].get_file()
    photo_path = f'temp_{user_id}_{len(user_images[user_id])}.jpg'
    await photo_file.download_to_drive(photo_path)
    
    user_images[user_id].append(photo_path)
    await update.message.reply_text(f'Image {len(user_images[user_id])} added. Send more images or type /done.')

# Handle the /done command
async def done(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in user_images or not user_images[user_id]:
        await update.message.reply_text('Keshke there is no images to convert')
        return

    try:
        # Create a PDF from all pics
        images = [Image.open(img_path) for img_path in user_images[user_id]]
        pdf_path = f'{user_id}_output.pdf'
        images[0].save(pdf_path, save_all=True, append_images=images[1:], resolution=100.0)

        with open(pdf_path, 'rb') as pdf_file:
            await context.bot.send_document(
                chat_id=user_id,
                document=pdf_file,
                filename='converted.pdf'
            )

        for img_path in user_images[user_id]:
            os.remove(img_path)
        os.remove(pdf_path)
        del user_images[user_id]

        await update.message.reply_text('Conversion completed!  \n\n Thanks for using my bot🤛🏽   \n \n @A13XBOTZ\n\nJoin this channel to make me smile:)')

    except Exception as e:
        logger.error(f'Exception: {e}')
        await update.message.reply_text(f'An error occurred try again keshke: {str(e)}')

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("done", done))
    application.add_handler(CallbackQueryHandler(button_handler, pattern='new'))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    logger.info('Starting bot')
    application.run_polling()

if __name__ == '__main__':
    main()
