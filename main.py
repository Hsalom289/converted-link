from telethon.sync import TelegramClient
from telethon import events
import re
import os
import asyncio

# Sozlamalar
api_id = '16072756'  # O'z API ID'ingizni kiriting
api_hash = '5fc7839a0d020c256e5c901cebd21bb7'  # O'z API HASH'ingizni kiriting
phone_number = '+998947610826'  # O'z telefon raqamingizni kiriting
source_channel = 'hilolbozor'  # Manba kanal username yoki ID (-100...)
target_channel = 'toshkent_uy_oldi'  # Maqsadli kanal username yoki ID

# Standart footer
STANDARD_FOOTER = "\n\n🏡 Уй-жойлар каналимиз: @toshkent_uy_oldi\n📞 Богланиш: +998 90 123 45 67"

async def main():
    client = TelegramClient('session_name', api_id, api_hash)
    
    try:
        # Kanal mavjudligini tekshirish
        source_entity = await client.get_entity(source_channel)
        target_entity = await client.get_entity(target_channel)
        print(f"✅ Manba kanal topildi: {source_entity.title}")
        print(f"✅ Maqsad kanal topildi: {target_entity.title}")
    except Exception as e:
        print(f"❌ Xatolik: Kanal topilmadi! {e}")
        return

    @client.on(events.NewMessage(chats=source_entity))
    async def handler(event):
        print(f"✉️ Yangi xabar qabul qilindi! (ID: {event.message.id})")
        
        # Xabar matnini olish
        text = event.message.text or event.message.caption or ""
        
        # Havola va @HilolBozor so'zini o'chirish
        clean_lines = []
        for line in text.split('\n'):
            if re.search(r'(@[Hh][i1l][i1l][o0][i1l]?[Bb][o0]z[o0]r\b|https?://)', line, re.IGNORECASE):
                continue  # Havola bor qatorni tashlab ketamiz
            clean_lines.append(line)
        
        clean_text = '\n'.join(clean_lines)
        final_text = clean_text + STANDARD_FOOTER
        
        # Rasm yoki media bor bo'lsa
        if event.message.media:
            os.makedirs('downloads', exist_ok=True)
            photo_path = await event.message.download_media(file='downloads/')
            await client.send_file(
                target_entity,
                photo_path,
                caption=final_text,
                link_preview=False
            )
            os.remove(photo_path)  # Faylni o'chiramiz
        else:
            await client.send_message(
                target_entity,
                final_text,
                link_preview=False
            )
        print(f"✅ Xabar tozalandi va {target_entity.title} ga jo'natildi!")

    await client.start(phone_number)
    print("🔍 Kutish rejimida... Yangi xabarlar kuzatilmoqda.")
    await client.run_until_disconnected()

asyncio.run(main())
