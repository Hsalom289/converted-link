from telethon.sync import TelegramClient
from telethon import events
import re
import os
import asyncio

# Sozlamalar
api_id = '16072756'  # Haqiqiy API ID kiriting
api_hash = '5fc7839a0d020c256e5c901cebd21bb7'  # Haqiqiy API HASH
phone_number = '+998947610826'  # Haqiqiy telefon raqam
source_channel = -1001384030482  # Kanal ID
target_channel = 'toshkent_uy_oldi'  # Maqsadli kanal

STANDARD_FOOTER = "\n\n🏡 Уй-жойлар каналимиз: @toshkent_uy_oldi\n📞 Богланиш: +998 90 123 45 67"

async def main():
    # Session faylini avval o'chirish tavsiya etiladi
    if os.path.exists('session_name.session'):
        os.remove('session_name.session')
        
    client = TelegramClient('session_name', api_id, api_hash)
    
    try:
        # Clientni ishga tushirish
        await client.start(phone_number)
        print("✅ Muvaffaqiyatli ulandi")
        
        # Kanal mavjudligini tekshirish
        source_entity = await client.get_entity(source_channel)
        target_entity = await client.get_entity(target_channel)
        print(f"✅ Manba kanal: {source_entity.title}")
        print(f"✅ Maqsad kanal: {target_entity.title}")

        @client.on(events.NewMessage(chats=source_entity))
        async def handler(event):
            try:
                print(f"✉️ Yangi xabar: {event.message.id}")
                text = event.message.text or event.message.caption or ""
                
                # Matnni tozalash
                clean_text = "\n".join(
                    line for line in text.split('\n')
                    if not re.search(r'(@[Hh]ilol[Bb]ozor|https?://)', line, re.IGNORECASE)
                )
                final_text = clean_text + STANDARD_FOOTER

                # Jo'natish
                if event.message.media:
                    os.makedirs('downloads', exist_ok=True)
                    file = await event.message.download_media('downloads/')
                    await client.send_file(target_entity, file, caption=final_text)
                    os.remove(file)
                else:
                    await client.send_message(target_entity, final_text)
                print("✅ Xabar jo'natildi!")
            except Exception as e:
                print(f"❌ Xabar jo'natishda xato: {e}")

        print("🔍 Kuzatish boshlandi...")
        await client.run_until_disconnected()
        
    except Exception as e:
        print(f"❌ Asosiy xato: {e}")
    finally:
        await client.disconnect()

asyncio.run(main())
