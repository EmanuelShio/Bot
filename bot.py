import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ✅ O Railway injeta o token nas variáveis de ambiente
TOKEN = os.getenv("BOT_TOKEN")

MENU_TEXT = "♻️ Para divulgar seu canal ou grupo, siga os passos abaixo:"

def build_menu():
    keyboard = [
        [InlineKeyboardButton("📦 Adicionar Canal", callback_data="add_channel")],
        [InlineKeyboardButton("🚀 Adicionar Grupo", callback_data="add_group")],
        [InlineKeyboardButton("🔍 Mais Detalhes", callback_data="details")],
        [InlineKeyboardButton("🏠 Voltar ao Menu Principal", callback_data="menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = build_menu()
    if update.message:
        await update.message.reply_text(MENU_TEXT, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text(MENU_TEXT, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "add_channel":
        await query.edit_message_text("👉 Instruções para adicionar canal...\n1️⃣ Adicione o bot como admin do canal\n2️⃣ Dê permissão para postar mensagens.")
    elif data == "add_group":
        await query.edit_message_text("👉 Instruções para adicionar grupo...\n1️⃣ Adicione o bot ao grupo\n2️⃣ Dê as permissões necessárias.")
    elif data == "details":
        await query.edit_message_text("📋 Mais detalhes sobre como participar e regras de divulgação.")
    elif data == "menu":
        await query.edit_message_text(MENU_TEXT, reply_markup=build_menu())
    else:
        await query.edit_message_text("❌ Opção não reconhecida.")

def main():
    if not TOKEN:
        raise ValueError("❌ ERRO: variável BOT_TOKEN não configurada!")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("✅ Bot iniciado e rodando no Railway!")
    app.run_polling()

if __name__ == "__main__":
    main()
