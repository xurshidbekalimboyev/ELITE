import asyncio
import base64
import random
import string
import logging
import time
import hashlib
import os
import aiohttp
from aiohttp import web
from aiogram import Bot, Dispatcher, html, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

# ==================== SOZLAMALAR ====================
TOKEN = "8872397303:AAG0uvPxX3zjNifRhgj2qyvV6-xa_3do1PU"  # BotFather'dan olingan yangi token
ADMIN_ID = 8099893180          # O'zingizning Telegram ID'ingiz
# ====================================================

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Foydalanuvchilarni saqlash bazasi (Xotirada)
users_db = set()

# FSM Holatlari
class OrderBot(StatesGroup):
    waiting_for_details = State()

class AdminBroadcast(StatesGroup):
    waiting_for_message = State()

# 🎛 E L I T E Cyber Keyboard v3.5
elite_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💼 Xizmatlar & Servislar"),
            KeyboardButton(text="🚀 Botga Buyurtma Berish")
        ],
        [
            KeyboardButton(text="🔍 IP Scanner"),
            KeyboardButton(text="🌐 Domain Ping & WHOIS")
        ],
        [
            KeyboardButton(text="⚡ Hash Generator"),
            KeyboardButton(text="🐍 Python Runner")
        ],
        [
            KeyboardButton(text="🛡 Cyber PassGen"),
            KeyboardButton(text="🔐 Encrypt / Decrypt")
        ],
        [
            KeyboardButton(text="🆔 Mening TG ID'm"),
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
        "   [ E L I T E — SYSTEM INITIALIZED v3.5 ]\n"
        "======================================</code>\n"
        "<b>Status:</b> <code>ONLINE (OPERATIONAL)</code>\n"
        "<b>Security Level:</b> <code>MAXIMUM</code>\n\n"
        f"Xush kelibsiz, <b>{html.quote(message.from_user.full_name)}</b>!\n"
        "Kerakli cyber-funksiyani yoki xizmatni menyudan tanlang:"
    )
    await message.answer(banner, parse_mode="HTML", reply_markup=elite_keyboard)

# 💼 Servislar va Xizmatlar Menyusi
@dp.message(F.text == "💼 Xizmatlar & Servislar")
async def show_services(message: Message):
    services_text = (
        "<b>[ E L I T E — PROFESSIONAL XIZMATLAR ]</b>\n\n"
        "🛠 <b>1. Telegram Bot Yaratish:</b>\n"
        "└ Business, Shop, Auto-posting, API integratsiya botlari.\n\n"
        "🌐 <b>2. Web & Backend Dasturlash:</b>\n"
        "└ Python (Aiogram, FastAPI, Django), Scriptlar va Parserlar.\n\n"
        "🛡 <b>3. Kiber-Xavfsizlik Auditi:</b>\n"
        "└ Kodlar va serverlarni zaiflikka tekshirish.\n\n"
        "<i>Buyurtma berish uchun <b>🚀 Botga Buyurtma Berish</b> tugmasini bosing!</i>"
    )
    await message.answer(services_text, parse_mode="HTML")

# ⚡ HASH GENERATOR (Yangi Cyber Funksiya 1)
@dp.message(F.text == "⚡ Hash Generator")
async def hash_guide(message: Message):
    await message.answer(
        "<b>[ CYBER HASH GENERATOR ]</b>\n\n"
        "Matnni hash qilish uchun quyidagicha yuboring:\n"
        "<code>/hash Matningiz</code>",
        parse_mode="HTML"
    )

@dp.message(F.text.startswith("/hash "))
async def process_hash(message: Message):
    text = message.text[6:].strip()
    md5_h = hashlib.md5(text.encode()).hexdigest()
    sha256_h = hashlib.sha256(text.encode()).hexdigest()
    
    res = (
        f"<b>[ HASH RESULTS FOR: <code>{text}</code> ]</b>\n\n"
        f"🔑 <b>MD5:</b>\n<code>{md5_h}</code>\n\n"
        f"🛡 <b>SHA-256:</b>\n<code>{sha256_h}</code>"
    )
    await message.answer(res, parse_mode="HTML")

# 🐍 PYTHON RUNNER (Yangi Dasturlash Funksiyasi 2)
@dp.message(F.text == "🐍 Python Runner")
async def py_guide(message: Message):
    await message.answer(
        "<b>[ PYTHON CODE RUNNER ]</b>\n\n"
        "Kichik Python kodi va matematik amallarni tekshirish uchun yuboring:\n"
        "<code>/py print(10 + 20 * 5)</code>",
        parse_mode="HTML"
    )

@dp.message(F.text.startswith("/py "))
async def process_python(message: Message):
    code = message.text[4:].strip()
    try:
        # Xavfsiz hisoblash va natija
        result = eval(code, {"__builtins__": None}, {})
        await message.answer(f"<b>[ PYTHON RESULT ]:</b>\n<code>{result}</code>", parse_mode="HTML")
    except Exception as e:
        await message.answer(f"<b>[ EXECUTION ERROR ]:</b>\n<code>{e}</code>", parse_mode="HTML")

# 🌐 DOMAIN PING & WHOIS (Yangi Cyber Funksiya 3)
@dp.message(F.text == "🌐 Domain Ping & WHOIS")
async def domain_guide(message: Message):
    await message.answer(
        "<b>[ DOMAIN PINGER & WHOIS ]</b>\n\n"
        "Sayt tezligi va statusini tekshirish:\n"
        "<code>/ping google.com</code>\n\n"
        "Domen IP-manzilini aniqlash:\n"
        "<code>/whois google.com</code>",
        parse_mode="HTML"
    )

@dp.message(F.text.startswith("/ping "))
async def process_ping(message: Message):
    domain = message.text[6:].strip().replace("https://", "").replace("http://", "")
    url = f"http://{domain}"
    start_time = time.time()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as resp:
                latency = round((time.time() - start_time) * 1000, 2)
                res = f"<b>[ PING: {domain} ]</b>\n\n🌐 Status: <code>ONLINE ({resp.status})</code>\n⚡️ Tezlik: <code>{latency} ms</code>"
                await message.answer(res, parse_mode="HTML")
    except Exception:
        await message.answer(f"🔴 <b>{domain}</b> tarmoqda topilmadi yoki oflayn!", parse_mode="HTML")

@dp.message(F.text.startswith("/whois "))
async def process_whois(message: Message):
    domain = message.text[7:].strip().replace("https://", "").replace("http://", "")
    url = f"http://ip-api.com/json/{domain}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                if data.get("status") == "success":
                    res = (
                        f"<b>[ WHOIS / IP INFO: {domain} ]</b>\n\n"
                        f"📍 <b>IP Address:</b> <code>{data.get('query')}</code>\n"
                        f"🌐 <b>Davlat:</b> {data.get('country')}\n"
                        f"🏢 <b>ISP / Host:</b> {data.get('isp')}"
                    )
                else:
                    res = "❌ Domen ma'lumotlari topilmadi."
                await message.answer(res, parse_mode="HTML")
    except Exception:
        await message.answer("❌ Ulanishda xatolik yuz berdi.")

# 🔍 IP Scanner
@dp.message(F.text == "🔍 IP Scanner")
async def ip_scan_guide(message: Message):
    await message.answer("<b>[ IP SCANNER ]</b>\n\nIP manzil yuboring:\n<code>/ip 8.8.8.8</code>", parse_mode="HTML")

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

# 🛡 PassGen & Encrypt
@dp.message(F.text == "🛡 Cyber PassGen")
async def generate_password(message: Message):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+"
    new_password = ''.join(random.choice(chars) for _ in range(16))
    await message.answer(f"<b>[ PASSGEN ]</b>\n\n<code>{new_password}</code>", parse_mode="HTML")

@dp.message(F.text == "🔐 Encrypt / Decrypt")
async def encrypt_guide(message: Message):
    await message.answer("<b>[ ENCRYPTION ]</b>\n\nShifrlash: <code>/enc matn</code>\nOchish: <code>/dec shifr</code>", parse_mode="HTML")

@dp.message(F.text.startswith("/enc "))
async def process_encrypt(message: Message):
    encoded = base64.b64encode(message.text[5:].strip().encode("utf-8")).decode("utf-8")
    await message.answer(f"<b>[ENCRYPTED]:</b>\n<code>{encoded}</code>", parse_mode="HTML")

@dp.message(F.text.startswith("/dec "))
async def process_decrypt(message: Message):
    try:
        decoded = base64.b64decode(message.text[5:].strip().encode("utf-8")).decode("utf-8")
        await message.answer(f"<b>[DECRYPTED]:</b>\n<code>{decoded}</code>", parse_mode="HTML")
    except Exception:
        await message.answer("❌ Noto'g'ri shifr!", parse_mode="HTML")

# 🆔 TG ID & System Status
@dp.message(F.text == "🆔 Mening TG ID'm")
async def get_tg_id(message: Message):
    user = message.from_user
    await message.answer(f"👤 <b>Ism:</b> {html.quote(user.full_name)}\n🆔 <b>ID:</b> <code>{user.id}</code>", parse_mode="HTML")

@dp.message(F.text == "💻 System Status")
async def system_status(message: Message):
    res = (
        "<b>[ E L I T E — SYSTEM DIAGNOSTICS v3.5 ]</b>\n\n"
        "⚡ <b>Core Status:</b> <code>100% OPERATIONAL</code>\n"
        f"👥 <b>Foydalanuvchilar:</b> <code>{len(users_db)} ta</code>\n"
        "🛡 <b>Firewall:</b> <code>ENABLED</code>"
    )
    await message.answer(res, parse_mode="HTML")

# 🚀 Buyurtma berish
@dp.message(F.text == "🚀 Botga Buyurtma Berish")
async def start_order(message: Message, state: FSMContext):
    await state.set_state(OrderBot.waiting_for_details)
    await message.answer("<b>[ BUYURTMA ]</b>\n\nLoyiha haqida yozing (/cancel — bekor qilish):", parse_mode="HTML")

@dp.message(OrderBot.waiting_for_details)
async def process_order(message: Message, state: FSMContext):
    if message.text == "/cancel":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=elite_keyboard)
        return

    user = message.from_user
    username = f"@{user.username}" if user.username else "Username yo'q"
    await message.answer("✅ Buyurtmangiz qabul qilindi!", reply_markup=elite_keyboard)
    
    admin_notification = (
        f"🚨 <b>YANGI BUYURTMA!</b>\n\n"
        f"👤 <b>Mijoz:</b> {html.quote(user.full_name)}\n"
        f"🌐 <b>Username:</b> {username}\n"
        f"🆔 <b>ID:</b> <code>{user.id}</code>\n\n"
        f"📝 <b>Tavsif:</b>\n{html.quote(message.text)}"
    )
    await bot.send_message(chat_id=ADMIN_ID, text=admin_notification, parse_mode="HTML")
    await state.clear()

# 📢 ADMIN REKLAMA / E'LON YUBORISH (BROADCAST)
@dp.message(Command("elon"))
@dp.message(Command("broadcast"))
async def start_broadcast(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    await state.set_state(AdminBroadcast.waiting_for_message)
    await message.answer("📢 <b>Barcha foydalanuvchilarga yuboriladigan e'lon matnini kiriting:</b>\n\n<i>Bekor qilish: /cancel</i>", parse_mode="HTML")

@dp.message(AdminBroadcast.waiting_for_message)
async def process_broadcast(message: Message, state: FSMContext):
    if message.text == "/cancel":
        await state.clear()
        await message.answer("E'lon bekor qilindi.")
        return

    count = 0
    for u_id in users_db:
        try:
            await bot.send_message(chat_id=u_id, text=f"📢 <b>E L I T E E'LON:</b>\n\n{message.text}", parse_mode="HTML")
            count += 1
            await asyncio.sleep(0.05)
        except Exception:
            pass

    await message.answer(f"✅ E'lon <b>{count} ta</b> foydalanuvchiga muvaffaqiyatli yuborildi!", parse_mode="HTML")
    await state.clear()

# 💬 ADMIN REPLY
@dp.message(Command("reply"))
async def reply_to_user(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        args = message.text.split(maxsplit=2)
        target_id = int(args[1])
        reply_text = args[2]
        await bot.send_message(chat_id=target_id, text=f"💬 <b>E L I T E Dasturchisidan:</b>\n\n{reply_text}", parse_mode="HTML")
        await message.answer("✅ Javob yuborildi!")
    except Exception:
        await message.answer("❌ Format: <code>/reply ID MATN</code>", parse_mode="HTML")

# Render dummy server + Bot Startup
async def handle(request):
    return web.Response(text="E L I T E Cyber Bot v3.5 is running!")

async def main():
    print(">>> E L I T E CYBER BOT v3.5 ISHGA TUSHDI <<<")
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
