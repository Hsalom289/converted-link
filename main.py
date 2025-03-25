from telethon.sync import TelegramClient
from telethon import events
import re
import os
import asyncio

# Sozlamalar
api_id = '16072756'
api_hash = '5fc7839a0d020c256e5c901cebd21bb7'
phone_number = '+998947610826'
source_channel = 'hilolbozor'
target_channel = 'toshkent_uy_oldi'

# Standart footer
STANDARD_FOOTER = "\n\n🏡 Уй-жойлар каналимиз: @toshkent_uy_oldi\n📞 Богланиш: +998 90 123 45 67"

async def main():
    client = TelegramClient('session_name', api_id, api_hash)
    
    @client.on(events.NewMessage(chats=source_channel))
    async def handler(event):
        print(f"Yangi xabar qabul qilindi! (ID: {event.message.id})")
        
        # Xabar matnini olish
        text = event.message.text or event.message.caption or ""
        
        # Havola topilgan butun qatorlarni o'chirish
        clean_lines = []
        for line in text.split('\n'):
            # Agar qatorda havola bo'lsa (http, https yoki @HilolBozor)
            if re.search(r'(@[Hh][i1l][i1l][o0][i1l]?[Bb][o0]z[o0]r\b|https?://)', line, re.IGNORECASE):
                continue  # Ushbu qatorni o'tkazib yuboramiz
            clean_lines.append(line)
        
        clean_text = '\n'.join(clean_lines)
        
        # Footer qo'shamiz
        final_text = clean_text + STANDARD_FOOTER
        
        # Rasm bor bo'lsa
        if event.message.media:
            photo_path = await event.message.download_media(file='downloads/')
            await client.send_file(
                target_channel,
                photo_path,
                caption=final_text,
                link_preview=False
            )
            os.remove(photo_path)
        else:
            await client.send_message(
                target_channel,
                final_text,
                link_preview=False
            )
        
        print(f"Xabar tozalandi va jo'natildi!")

    await client.start(phone_number)
    print("Kutish rejimida... Yangi xabarlar kuzatilmoqda.")
    await client.run_until_disconnected()

asyncio.run(main())