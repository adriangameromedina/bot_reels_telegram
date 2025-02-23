import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import instaloader

# Obtener el token de la variable de entorno
TOKEN = os.getenv('TOKEN_TELEGRAM')

if not TOKEN:
    raise ValueError("El token de Telegram no está configurado correctamente.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hola! Envíame una URL de Instagram y te mostraré el video.')

def get_instagram_video_url(url: str) -> str:
    L = instaloader.Instaloader()
    shortcode = url.split("/")[-2]
    post = instaloader.Post.from_shortcode(L.context, shortcode)

    # Obtener la URL del video
    video_url = post.video_url
    if not video_url:
        raise ValueError("No se encontró ningún video en la URL proporcionada.")

    return video_url

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text
    if "instagram.com" in url:
        try:
            video_url = get_instagram_video_url(url)
            await update.message.reply_text(f'Aquí tienes el video: {video_url}')
        except Exception as e:
            await update.message.reply_text(f'Error al obtener el video: {str(e)}')
    else:
        await update.message.reply_text('Por favor, envíame una URL válida de Instagram.')

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
