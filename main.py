import asyncio
import base64
import random
import string
import logging
import time
import aiohttp
from aiogram import Bot, Dispatcher, html, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

# ==================== SOZLAMALAR ====================
TOKEN = "8872397303:AAG0uvPxX3zjNifRhgj2qyvV6-xa_3do1PU"  # BotFather'dan olingan token
ADMIN_ID = 8099893180          # O'zingizning TG ID'ingiz
# ====================================================

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Foydalanuvchilarni saqlash uchun set
users_db = set()

# FSM: Buyurtma va Broadcast holatlari
class OrderBot(StatesGroup):
    waiting_for_details = State()

# 🎛 E L I T E Cyber Keyboard v2.0
elite_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🆔 Mening TG ID'm"),
            KeyboardButton(text="🔍 IP Scanner")
        ],
        [
            KeyboardButton(text="🌐 Domain Ping"),
            KeyboardButton(text="🔐 Encrypt / Decrypt")
        ],
        [
            KeyboardButton(text="🛡 Cyber PassGen"),
            KeyboardButton(text="🔑 API Key Gen")
        ],
        [
            KeyboardButton(text="🚀 Botga Buyurtma Berish"),
            KeyboardButton(text="💻 System Status")
        ]
    ],
    resize_keyboard=True
)

# 🟢 /start Buyrug'i
@dp.message(Command("start"))
async def cmd_start(message: Message):
    users_db.add(message.from_user.id)
    banner = (
        "<code>======================================\n"
        "   [ E L I T E — SYSTEM INITIALIZED v2.0 ]\n"
        "======================================</code>\n"
        "<b>Status:</b> <code>ONLINE (OPERATIONAL)</code>\n"
        "<b>Security Level:</b> <code>MAXIMUM</code>\n\n"
        f"Xush kelibsiz, <b>{html.quote(message.from_user.full_name)}</b>!\n"
        "Kerakli cyber-funksiyani yoki xizmatni menyudan tanlang:"
    )
    await message.answer(banner, parse_mode="HTML", reply_markup=elite_keyboard)

# 🆔 TG ID Aniqlovchi
@dp.message(F.text == "🆔 Mening TG ID'm")
async def get_tg_id(message: Message):
    user = message.from_user
    username = f"@{user.username}" if user.username else "Mavjud emas"
    
    res = (
        "<b>[ E L I T E — USER ANALYTICS ]</b>\n\n"
        f"👤 <b>Ism:</b> {html.quote(user.full_name)}\n"
        f"🆔 <b>Telegram ID:</b> <code>{user.id}</code>\n"
        f"🌐 <b>Username:</b> {username}\n"
        f"⚡ <b>Language Code:</b> <code>{user.language_code}</code>"
    )
    await message.answer(res, parse_mode="HTML")

# 🛡 Parol Generator
@dp.message(F.text == "🛡 Cyber PassGen")
async def generate_password(message: Message):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+"
    new_password = ''.join(random.choice(chars) for _ in range(16))
    
    res = (
        "<b>[ CYBER PASSGEN v2.0 ]</b>\n\n"
        "Yaratilgan ultra-xavfsiz parol:\n"
        f"<code>{new_password}</code>\n\n"
        "<i>Nusxalash uchun ustiga bosing!</i>"
    )
    await message.answer(res, parse_mode="HTML")

# 🔑 API / Token Key Generator
@dp.message(F.text == "🔑 API Key Gen")
async def generate_api_key(message: Message):
    api_key = f"ELITE-KEY-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=24))
    res = (
        "<b>[ CYBER KEY GENERATOR ]</b>\n\n"
        "Xavfsiz API Token/Key:\n"
        f"<code>{api_key}</code>\n\n"
        "<i>Nusxalash uchun ustiga bosing!</i>"
    )
    await message.answer(res, parse_mode="HTML")

# 💻 System Status
@dp.message(F.text == "💻 System Status")
async def system_status(message: Message):
    res = (
        "<b>[ E L I T E — SYSTEM DIAGNOSTICS ]</b>\n\n"
        "⚡ <b>Core Status:</b> <code>100% OPERATIONAL</code>\n"
        "🔒 <b>Encryption Engine:</b> <code>ACTIVE (AES/Base64)</code>\n"
        "🌐 <b>Network Ping:</b> <code>12ms</code>\n"
        f"👥 <b>Foydalanuvchilar:</b> <code>{len(users_db)} ta</code>\n"
        "🛡 <b>Firewall:</b> <code>ENABLED</code>"
    )
    await message.answer(res, parse_mode="HTML")

# 🔐 Encrypt / Decrypt Moduli
@dp.message(F.text == "🔐 Encrypt / Decrypt")
async def encrypt_guide(message: Message):
    res = (
        "<b>[ ENCRYPTION MODULE ]</b>\n\n"
        "Matnni shifrlash uchun:\n<code>/enc Matningiz</code>\n\n"
        "Shifrni ochish uchun:\n<code>/dec SIZNING_SHIFRINGIZ</code>"
    )
    await message.answer(res, parse_mode="HTML")

@dp.message(F.text.startswith("/enc "))
async def process_encrypt(message: Message):
    user_text = message.text[5:].strip()
    encoded = base64.b64encode(user_text.encode("utf-8")).decode("utf-8")
    await message.answer(f"<b>[ENCRYPTED DATA]:</b>\n<code>{encoded}</code>", parse_mode="HTML")

@dp.message(F.text.startswith("/dec "))
async def process_decrypt(message: Message):
    user_text = message.text[5:].strip()
    try:
        decoded = base64.b64decode(user_text.encode("utf-8")).decode("utf-8")
        await message.answer(f"<b>[DECRYPTED DATA]:</b>\n<code>{decoded}</code>", parse_mode="HTML")
    except Exception:
        await message.answer("<b>[ERROR]:</b> Noto'g'ri shifr formati!", parse_mode="HTML")

# 🔍 IP Scanner
@dp.message(F.text == "🔍 IP Scanner")
async def ip_scan_guide(message: Message):
    await message.answer("<b>[ IP SCANNER ]</b>\n\nIP manzilni quyidagicha yuboring:\n<code>/ip 8.8.8.8</code>", parse_mode="HTML")

@dp.message(F.text.startswith("/ip "))
async def process_ip_scan(message: Message):
    ip_address = message.text[4:].strip()
    url = f"http://ip-api.com/json/{ip_address}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                if data.get("status") == "success":
                    res = (
                        f"<b>[ IP SCAN RESULTS: {ip_address} ]</b>\n\n"
                        f"🌐 <b>Mamlakat:</b> {data.get('country')}\n"
                        f"🏙 <b>Shahar:</b> {data.get('city')}\n"
                        f"🏢 <b>ISP:</b> {data.get('isp')}\n"
                        f"📍 <b>Koordinata:</b> <code>{data.get('lat')}, {data.get('lon')}</code>"
                    )
                else:
                    res = "<b>[ERROR]:</b> Noto'g'ri IP manzil!"
                await message.answer(res, parse_mode="HTML")
    except Exception:
        await message.answer("<b>[ERROR]:</b> Server bilan bog'lanib bo'lmadi!")

# 🌐 Domain / Web Pinger
@dp.message(F.text == "🌐 Domain Ping")
async def ping_guide(message: Message):
    await message.answer("<b>[ DOMAIN PINGER ]</b>\n\nSayt holatini tekshirish uchun:\n<code>/ping google.com</code>", parse_mode="HTML")

@dp.message(F.text.startswith("/ping "))
async def process_ping(message: Message):
    domain = message.text[6:].strip().replace("https://", "").replace("http://", "")
    url = f"http://{domain}"
    
    start_time = time.time()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as resp:
                latency = round((time.time() - start_time) * 1000, 2)
                res = (
                    f"<b>[ DOMAIN PING RESULTS: {domain} ]</b>\n\n"
                    f"🌐 <b>Status:</b> <code>ONLINE ({resp.status})</code>\n"
                    f"⚡️ <b>Response Time:</b> <code>{latency} ms</code>"
                )
                await message.answer(res, parse_mode="HTML")
    except Exception:
        await message.answer(f"<b>[ DOMAIN PING RESULTS: {domain} ]</b>\n\n🔴 <b>Status:</b> <code>OFFLINE / UNREACHABLE</code>", parse_mode="HTML")

# 🚀 Botga Buyurtma Berish
@dp.message(F.text == "🚀 Botga Buyurtma Berish")
async def start_order(message: Message, state: FSMContext):
    await state.set_state(OrderBot.waiting_for_details)
    await message.answer(
        "<b>[ E L I T E — BOT DEVELOPMENT ORDER ]</b>\n\n"
        "Sizga qanday bot kerak? Funksiyalari va loyihangiz haqida yozing.\n\n"
        "<i>Bekor qilish uchun /cancel deb yozing.</i>",
        parse_mode="HTML"
    )

@dp.message(OrderBot.waiting_for_details)
async def process_order(message: Message, state: FSMContext):
    if message.text == "/cancel":
        await state.clear()
        await message.answer("❌ Buyurtma bekor qilindi.", reply_markup=elite_keyboard)
        return

    order_text = message.text
    user = message.from_user
    username = f"@{user.username}" if user.username else "Username yo'q"
    
    await message.answer("✅ <b>Buyurtmangiz qabul qilindi!</b> Tez orada bog'lanamiz.", parse_mode="HTML", reply_markup=elite_keyboard)
    
    admin_notification = (
        "🚨 <b>YANGI BUYURTMA KELDI!</b>\n\n"
        f"👤 <b>Mijoz:</b> {html.quote(user.full_name)}\n"
        f"🌐 <b>Username:</b> {username}\n"
        f"🆔 <b>ID:</b> <code>{user.id}</code>\n\n"
        f"📝 <b>Tavsif:</b>\n{html.quote(order_text)}"
    )
    try:
        await bot.send_message(chat_id=ADMIN_ID, text=admin_notification, parse_mode="HTML")
    except Exception as e:
        logging.error(f"Adminga yuborishda xatolik: {e}")

    await state.clear()

# 📩 ADMIN REPLY SYSTEM: /reply ID MATN
@dp.message(Command("reply"))
async def reply_to_user(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        args = message.text.split(maxsplit=2)
        target_id = int(args[1])
        reply_text = args[2]
        
        await bot.send_message(chat_id=target_id, text=f"💬 <b>E L I T E Dasturchisidan xabar:</b>\n\n{reply_text}", parse_mode="HTML")
        await message.answer("✅ Xabar mijozga yetkazildi!")
    except Exception as e:
        await message.answer(f"❌ Xatolik! To'g'ri shakl:\n<code>/reply 7696464331 Salom</code>", parse_mode="HTML")

# Botni ishga tushirish
async def main():
    print(">>> E L I T E CYBER BOT v2.0 ISHGA TUSHDI <<<")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
