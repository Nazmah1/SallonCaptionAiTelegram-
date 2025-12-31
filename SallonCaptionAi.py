import os
import logging
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ==================== تنظیمات لاگ ====================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),  # برای نمایش در Railway
        logging.FileHandler('bot.log')      # ذخیره در فایل
    ]
)
logger = logging.getLogger(__name__)

# ==================== توکن ربات ====================
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    logger.error("❌ خطا: توکن تلگرام یافت نشد!")
    logger.error("لطفاً در Railway متغیر TELEGRAM_BOT_TOKEN را تنظیم کنید")
    sys.exit(1)

logger.info("=" * 50)
logger.info("🚀 ربات کپشن‌نویس سالن زیبایی")
logger.info(f"✅ توکن دریافت شد: {TOKEN[:10]}...")
logger.info("=" * 50)

# ==================== کپشن‌های آماده ====================
BEAUTY_CAPTIONS = {
    "ناخن": [
        "💅 طراحی ناخن با جدیدترین مدل‌های ۲۰۲۴\n#ناخن #مانیکور #سالن_زیبایی #زیبایی",
        "✨ ناخن‌های فانتزی برای مهمانی‌های خاص\n#طراحی_ناخن #زیبایی_ناخن #ناخن_ایرانی",
        "🌸 ترکیب رنگ‌های بهاری روی ناخن‌های شما\n#بهار #ناخن_رنگی #سالن_زیبایی_تهران"
    ],
    "مو": [
        "💇‍♀️ کوتاهی و استایل مو با مشاوره رایگان\n#آرایشگاه #کوتاهی_مو #رنگ_مو",
        "🌟 هایلایت حرفه‌ای با بهترین رنگ‌های اروپایی\n#مو #هایلایت #بالیاژ",
        "🌺 کراتینه و صاف کردن مو بدون فرمالدهید\n#کراتینه #مو_صاف #سالن_زیبایی"
    ],
    "پوست": [
        "💆‍♀️ فیشیال و پاکسازی عمقی پوست\n#فیشیال #پوست #مراقبت_پوست",
        "✨ میکرونیدلینگ با جدیدترین دستگاه‌ها\n#جوانسازی #میکرونیدلینگ #زیبایی",
        "🌸 پیلینگ شیمیایی با مشاوره پوست‌شناسی\n#پیلینگ #لایه_برداری #پوست_شاداب"
    ],
    "میکاپ": [
        "💄 میکاپ عروس و مهمانی توسط آرایشگران حرفه‌ای\n#میکاپ #عروس #آرایش",
        "🌟 میکاپ طبیعی و روزمره با محصولات اورگانیک\n#میکاپ_طبیعی #آرایش_سبک",
        "🌺 آموزش آرایش خصوصی در سالن ما\n#آموزش_آرایش #میکاپ_آموزشی"
    ]
}

# ==================== دستورات ربات ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /start"""
    user = update.effective_user
    logger.info(f"👤 کاربر جدید: {user.id} ({user.username})")
    
    welcome = f"""
سلام {user.first_name} عزیز! 🌸

به ربات کپشن‌نویس سالن زیبایی خوش آمدید!

🎯 **دستورات:**
/start - راه‌اندازی مجدد
/help - راهنمای استفاده  
/services - خدمات سالن
/caption - دریافت کپشن

💡 **نحوه استفاده:**
کافیست بنویسید: ناخن، مو، پوست یا میکاپ

📞 پشتیبانی: @your_support
    """
    await update.message.reply_text(welcome)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /help"""
    help_text = """
📖 **راهنمای ربات:**

1. برای دریافت کپشن، یکی از کلمات زیر را بنویسید:
   • ناخن
   • مو  
   • پوست
   • میکاپ

2. هر کپشن شامل:
   ✓ متن جذاب
   ✓ هشتگ‌های بهینه
   ✓ مناسب اینستاگرام

3. دستورات:
   /start - شروع
   /help - این راهنما
   /services - لیست خدمات
   /caption - درخواست کپشن

4. تماس:
   📱 ۰۹۱۲XXXXXXX
   📍 تهران، میدان ولیعصر
    """
    await update.message.reply_text(help_text)

async def services_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /services"""
    services = """
💎 **خدمات سالن زیبایی:**

1. **ناخن‌کاری:**
   • طراحی ناخن
   • ژل و اکریلیک
   • ناخن عروس

2. **آرایش مو:**
   • کوتاهی و استایل
   • رنگ، هایلایت، بالیاژ
   • کراتینه و صاف

3. **مراقبت پوست:**
   • پاکسازی و فیشیال
   • میکرونیدلینگ
   • پیلینگ شیمیایی

4. **آرایش صورت:**
   • میکاپ عروس
   • میکاپ مهمانی
   • آموزش آرایش

⏰ ساعت کاری: ۹ صبح تا ۹ شب
    """
    await update.message.reply_text(services)

async def caption_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /caption"""
    await update.message.reply_text(
        "لطفاً نوع خدمت را انتخاب کنید:\n\n"
        "ناخن 💅\nمو 💇‍♀️\nپوست 💆‍♀️\nمیکاپ 💄"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش پیام‌های متنی"""
    user_input = update.message.text.strip().lower()
    user_id = update.effective_user.id
    
    logger.info(f"📩 پیام از {user_id}: {user_input}")
    
    # بررسی خدمت درخواستی
    found_service = None
    for service in BEAUTY_CAPTIONS:
        if service in user_input:
            found_service = service
            break
    
    if found_service:
        import random
        from datetime import datetime
        
        # انتخاب کپشن تصادفی
        caption = random.choice(BEAUTY_CAPTIONS[found_service])
        
        # افزودن تاریخ
        now = datetime.now().strftime("%Y/%m/%d %H:%M")
        caption += f"\n\n📅 {now}"
        
        # افزودن اطلاعات تماس
        caption += "\n📍 تهران، میدان ولیعصر"
        caption += "\n📱 ۰۹۱۲XXXXXXX"
        caption += "\n🌸 @beauty_salon_iran"
        
        await update.message.reply_text(caption)
        logger.info(f"✅ ارسال کپشن {found_service} به {user_id}")
        
        # ارسال پیشنهاد اضافی
        await update.message.reply_text(
            f"💡 برای {found_service} می‌توانید از خدمات زیر استفاده کنید:\n"
            f"• مشاوره رایگان\n• نوبت آنلاین\n• تخفیف ویژه"
        )
    else:
        await update.message.reply_text(
            "لطفاً یکی از خدمات زیر را بنویسید:\n"
            "• ناخن\n• مو\n• پوست\n• میکاپ\n\n"
            "یا از /help کمک بگیرید."
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت خطاها"""
    logger.error(f"⚠️ خطا: {context.error}")
    if update and update.message:
        await update.message.reply_text("⚠️ خطایی رخ داد. لطفاً دوباره تلاش کنید.")

# ==================== تابع اصلی ====================
def main():
    """تابع اصلی اجرای ربات"""
    try:
        # ایجاد اپلیکیشن
        app = Application.builder().token(TOKEN).build()
        logger.info("✅ اپلیکیشن ساخته شد")
        
        # افزودن دستورات
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("services", services_command))
        app.add_handler(CommandHandler("caption", caption_command))
        
        # افزودن هندلر پیام متنی
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # افزودن هندلر خطا
        app.add_error_handler(error_handler)
        
        # شروع ربات
        logger.info("🤖 شروع ربات تلگرام...")
        print("\n" + "="*50)
        print("🤖 ربات فعال شد!")
        print(f"🆔 توکن: {TOKEN[:15]}...")
        print("📡 در حال دریافت پیام‌ها...")
        print("="*50 + "\n")
        
        app.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES,
            timeout=30,
            pool_timeout=30
        )
        
    except Exception as e:
        logger.error(f"🔥 خطای بحرانی: {e}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()
