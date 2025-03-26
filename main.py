from telethon.sync import TelegramClient
from telethon import events
import re
import os
import asyncio

# Sozlamalar
api_id = '16072756'
api_hash = '5fc7839a0d020c256e5c901cebd21bb7'
phone_number = '+998947610826'

# Manba kanallar
source_channels = [
    -1002466271207,  # 1-kanal
    -1001384030482   # 2-kanal
]

# Maqsadli kanal
target_channel = 'toshkent_uy_oldi'

# Standart footer
STANDARD_FOOTER = "\n\n🏡 Уй-жойлар каналимиз: @toshkent_uy_oldi\n📞 Богланиш: +998 90 123 45 67"

async def main():
    client = TelegramClient('session_name', api_id, api_hash)
    
    try:
        await client.start(phone_number)
        print("✅ Telegramga muvaffaqiyatli ulandi")

        # Kanallarni tekshirish
        source_entities = []
        for channel in source_channels:
            try:
                entity = await client.get_entity(channel)
                source_entities.append(entity)
                print(f"✅ Manba kanal topildi: {entity.title} (ID: {entity.id})")
            except Exception as e:
                print(f"⚠️ {channel} kanalini topishda xato: {e}")

        if not source_entities:
            print("❌ Hech qanday manba kanal topilmadi!")
            return

        try:
            target_entity = await client.get_entity(target_channel)
            print(f"✅ Maqsad kanal topildi: {target_entity.title}")
        except Exception as e:
            print(f"❌ Maqsad kanal topilmadi: {e}")
            return

        # Xabarlarni qayta ishlash funksiyasi
        async def process_message(event):
            try:
                # Matnni olish va tozalash
                text = event.message.text or event.message.caption or ""
                
                # Reklama va havolalarni olib tashlash
                clean_text = "\n".join(
                    line for line in text.split('\n')
                    if not re.search(r'(@[Hh]ilol[Bb]ozor|https?://|@\w+)', line, re.IGNORECASE)
                )
                
                # Agar matn butunlay tozalanib ketgan bo'lsa
                if not clean_text.strip():
                    clean_text = "🏡 Yangi uy-joy e'lonlari"

                final_text = f"{clean_text}{STANDARD_FOOTER}"

                # Media bilan ishlash
                if event.message.media:
                    os.makedirs('downloads', exist_ok=True)
                    try:
                        file_path = await event.message.download_media('downloads/')
                        await client.send_file(
                            target_entity,
                            file_path,
                            caption=final_text,
                            link_preview=False
                        )
                        os.remove(file_path)
                        print(f"📤 Rasmli xabar jo'natildi")
                    except Exception as e:
                        print(f"❌ Media jo'natishda xato: {e}")
                else:
                    await client.send_message(
                        target_entity,
                        final_text,
                        link_preview=False
                    )
                    print(f"📤 Matnli xabar jo'natildi")

            except Exception as e:
                print(f"❌ Xabar jo'natishda xato: {e}")

        # Har bir kanal uchun handler qo'shish
        for entity in source_entities:
            client.add_event_handler(
                process_message,
                events.NewMessage(chats=entity)
            )
            print(f"🔍 Kuzatish yo'lga qo'yildi: {entity.title}")

        print("\n🔄 Kuzatish boshlandi... (Ctrl+C bosib to'xtatishingiz mumkin)")
        await client.run_until_disconnected()

    except KeyboardInterrupt:
        print("\n👋 Dastur to'xtatildi")
    except Exception as e:
        print(f"\n❌ Asosiy xato: {e}")
    finally:
        await client.disconnect()
        print("✅ Ulanish yopildi")

if __name__ == '__main__':
    if os.path.exists('session_name.session'):
        print("ℹ️ Old session fayli mavjud. Avvalgi session ishlatiladi.")
    asyncio.run(main())
