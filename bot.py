from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import re

# تنظیمات
BOT_TOKEN = "7987303902:AAGfI2AB0C9D-T8RXgVZP7iLrlQNWPkJqLI"
TARGET_CHANNEL = "@jahanmoney"

logging.basicConfig(level=logging.INFO)
print("🤖 ربات فوروارد خودکار فعال شد...")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔄 ربات فوروارد فعال است!\n\n"
        "📨 روش استفاده:\n"
        "1. از کانال‌های مورد نظر پیام رو فوروارد کن به این ربات\n"
        "2. ربات به طور خودکار به کانالت ارسال می‌کنه"
    )

async def handle_forwarded_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message and update.message.forward_origin:
            print("✅ پیام فوروارد شده دریافت شد!")
            await send_to_channel(context, update.message)
    except Exception as e:
        print(f"خطا: {e}")

def clean_content(text):
    """تمیز کردن محتوا از لینک‌ها، آیدی‌ها و مربع‌های رنگی"""
    if not text:
        return ""
    
    # حذف لینک‌ها
    text = re.sub(r'https://t\.me/\S+', '', text)
    text = re.sub(r't\.me/\S+', '', text)
    
    # حذف آیدی‌ها
    text = re.sub(r'@\w+', '', text)
    
    # حذف مربع‌های رنگی و ایموجی‌های اضافی
    text = re.sub(r'[🟩🟧🟥🟨🔴🟢🔵🟣🟠🟤⚫⚪🟡🟢🔴🟠🟡🟢🔵🟣🟤⚫⚪■□▪️▫️◼️◻️◾◽️▬▭▮▯]+', '', text)
    
    # پردازش خطوط
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if (line and 
            not line.startswith('http') and 
            not line.startswith('t.me') and
            not re.match(r'^[🔴🟢🔵🟣🟠🟤⚫⚪■□▪️▫️◼️◻️◾◽️\s]+$', line) and
            len(line) > 1):
            cleaned_lines.append(line)
    
    cleaned_text = '\n'.join(cleaned_lines)
    cleaned_text = re.sub(r'\n\s*\n', '\n\n', cleaned_text)
    
    return cleaned_text.strip()

async def send_to_channel(context, original_message):
    try:
        print("🔄 در حال پردازش و ارسال...")
        
        if original_message.photo:
            photo = original_message.photo[-1]
            if original_message.caption:
                cleaned_caption = clean_content(original_message.caption)
                new_caption = f"💱 نرخ لحظه‌ای:\n\n{cleaned_caption}\n\n📊 منبع: {TARGET_CHANNEL}" if cleaned_caption else f"💱 نرخ لحظه‌ای ارز\n\n📊 منبع: {TARGET_CHANNEL}"
            else:
                new_caption = f"💱 نرخ لحظه‌ای ارز\n\n📊 منبع: {TARGET_CHANNEL}"
            
            await context.bot.send_photo(
                chat_id=TARGET_CHANNEL,
                photo=photo.file_id,
                caption=new_caption
            )
        
        elif original_message.video:
            video = original_message.video
            if original_message.caption:
                cleaned_caption = clean_content(original_message.caption)
                new_caption = f"💱 نرخ لحظه‌ای:\n\n{cleaned_caption}\n\n📊 منبع: {TARGET_CHANNEL}" if cleaned_caption else f"💱 نرخ لحظه‌ای ارز\n\n📊 منبع: {TARGET_CHANNEL}"
            else:
                new_caption = f"💱 نرخ لحظه‌ای ارز\n\n📊 منبع: {TARGET_CHANNEL}"
            
            await context.bot.send_video(
                chat_id=TARGET_CHANNEL,
                video=video.file_id,
                caption=new_caption
            )
        
        elif original_message.text:
            cleaned_text = clean_content(original_message.text)
            new_text = f"💱 نرخ لحظه‌ای:\n\n{cleaned_text}\n\n📊 منبع: {TARGET_CHANNEL}" if cleaned_text else f"💱 نرخ لحظه‌ای ارز\n\n📊 منبع: {TARGET_CHANNEL}"
            
            await context.bot.send_message(
                chat_id=TARGET_CHANNEL,
                text=new_text
            )
        
        print("✅ پیام ارسال شد")
        
    except Exception as e:
        print(f"❌ خطا: {e}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL, handle_forwarded_message))
    print("🎯 ربات آماده دریافت پیام...")
    application.run_polling()

if __name__ == "__main__":
    main()