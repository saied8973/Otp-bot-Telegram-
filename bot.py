from telethon import TelegramClient, events, Button
import asyncio
import re
from datetime import datetime

# 🔑 API DETAILS
api_id = 36995933
api_hash = "6d4ded59e4401706397fc93ecadad3d4"

# 👑 ADMIN ID
ADMIN_ID = 7024903436

# 📥 SOURCE GROUPS
source_chats = [
    -1003400610239,
    -1002222222222
]

# 📤 TARGET GROUPS
target_chats = [
    -1003854624728,
    -1004444444444
]

# 🔗 BUTTON LINKS
PANEL_LINK = "https://t.me/your_panel"
UPDATES_LINK = "https://t.me/your_updates"

client = TelegramClient('session', api_id, api_hash)

# 🧠 MEMORY (duplicate block)
sent_otps = set()

# 🌍 COUNTRY FLAG DETECT
def get_flag(text):
    if "+263" in text or "ZW" in text:
        return "🇿🇼 Zimbabwe"
    elif "+91" in text:
        return "🇮🇳 India"
    elif "+60" in text:
        return "🇲🇾 Malaysia"
    elif "+1" in text:
        return "🇺🇸 USA"
    else:
        return "🌍 Unknown"

# 🔢 MASK NUMBER
def mask_number(text):
    return re.sub(r'(\d{3})\d{2,}(\d{3})', r'\1★★\2', text)

# 🔍 OTP EXTRACT
def extract_otp(text):
    match = re.findall(r'\b\d{4,6}\b', text)
    return match[0] if match else None

# 🔘 BUTTON
def get_buttons():
    return [
        [Button.url("PANEL 🎀", PANEL_LINK)],
        [Button.url("Join For Work 💫", UPDATES_LINK)]
    ]

# 🧾 LOG SAVE
def save_log(text):
    with open("otp_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {text}\n")

# ⏱ AUTO DELETE
async def auto_delete(chat_id, msg_id, delay=300):
    await asyncio.sleep(delay)
    try:
        await client.delete_messages(chat_id, msg_id)
    except:
        pass

# 📩 MAIN HANDLER
@client.on(events.NewMessage(chats=source_chats))
async def handler(event):
    msg = event.message.message

    if not msg:
        return

    otp = extract_otp(msg)

    # ❌ Normal message ignore
    if not otp:
        return

    # ❌ Duplicate block
    if otp in sent_otps:
        return

    sent_otps.add(otp)

    # 🌍 Flag detect
    flag = get_flag(msg)

    # 🔢 Mask
    msg = mask_number(msg)

    # 🧠 Final format
    final_msg = f"""
{flag}

📩 OTP CODE DETECTED

{msg}

🔐 OTP: {otp}

⏳ Auto-delete in 5 min
"""

    # 🧾 Save log
    save_log(final_msg)

    # 📤 Send
    for target in target_chats:
        sent = await client.send_message(
            target,
            final_msg,
            buttons=get_buttons()
        )

        client.loop.create_task(auto_delete(target, sent.id))


# 🔧 ADMIN COMMANDS
@client.on(events.NewMessage(pattern=r'/setpanel (.+)'))
async def set_panel(event):
    global PANEL_LINK
    if event.sender_id == ADMIN_ID:
        PANEL_LINK = event.pattern_match.group(1)
        await event.reply("✅ Panel link updated")

@client.on(events.NewMessage(pattern=r'/setupdates (.+)'))
async def set_updates(event):
    global UPDATES_LINK
    if event.sender_id == ADMIN_ID:
        UPDATES_LINK = event.pattern_match.group(1)
        await event.reply("✅ Updates link updated")


print("🔥 GOD MODE BOT RUNNING...")
client.start()
client.run_until_disconnected()