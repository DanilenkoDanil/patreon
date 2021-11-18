import time

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from db import User
import api
import json
import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

with open("setting.json", 'r', encoding='utf8') as out:
    setting = json.load(out)
    print(setting)
    TOKEN = setting['TOKEN']
    admin_list = setting['admin_list']
    channel_id = setting['channel_id']
    lock_channel_id_1 = setting['lock_channel_id_1']
    lock_channel_id_2 = setting['lock_channel_id_2']
    lock_channel_id_3 = setting['lock_channel_id_3']
    lock_channel_id_4 = setting['lock_channel_id_4']


hello_text = """
Start
"""
join_text = """
<b>Welcome!</b> 

Let’s verify your access! 

<b>Please enter your Patreon email</b> from which you have just signed up (https://www.patreon.com/easy_trade)
"""
thank_you = """
Thank you!
"""

db = User('db.db')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class States(StatesGroup):
    Email = State()
    Send = State()


@dp.message_handler(commands=['send'], state="*")
async def process_start_command(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in admin_list:
        print('+')
        await States.Send.set()
        await message.reply('Хорошо! Следуйщее ваше сообщение будет отправлено всем активным подписчикам!', parse_mode='Markdown')


@dp.message_handler(state=States.Send, content_types=['photo', 'document', 'text', 'video'])
async def email_step(message: types.Message, state: FSMContext):
    actual = api.get_active_list()[500]
    actual_channel_users = api.get_active_list()[600]
    base = db.get_email_active_list()
    channel_users = db.get_email_channel_list()
    for i in base:
        if i not in actual:
            db.delete_user(i)

    for channel_user in channel_users:
        if channel_user not in actual_channel_users:
            db.delete_user(channel_user)

    target_list = db.get_active_list()
    await state.finish()
    await bot.send_message(message.from_user.id, 'Отлично! Начинаем рассылку!', parse_mode='Markdown')
    print(target_list)
    for i in target_list:
        time.sleep(0.5)
        print('Идём')
        try:
            try:
                msg = message.text
                caption = message.caption
                print(caption)
            except:
                pass
            try:
                print('Отправляем фото')
                await bot.send_photo(i, message.photo[0].file_id, caption=caption, parse_mode='html')
                continue

            except Exception as e:
                print('Не фото')
                print(e)
                try:
                    await bot.send_photo(i, message.photo.file_id)
                    continue
                except:
                    pass

            try:
                await bot.send_document(i, message.document.file_id, caption=caption, parse_mode='html')
                continue
            except:
                try:
                    await bot.send_document(i, message.document.file_id)
                    continue
                except:
                    pass

            try:
                await bot.send_video(i, message.video.file_id, caption=caption, parse_mode='html')
                continue
            except:
                try:
                    await bot.send_video(i, message.video.file_id)
                    continue
                except:
                    pass

            try:
                await bot.send_message(i, msg, parse_mode='html')
                continue
            except:
                pass
        except:
            continue
    await bot.send_message(message.from_user.id, 'Рассылка окончена!', parse_mode='Markdown')


@dp.channel_post_handler(content_types=['photo', 'document', 'text', 'video'])
async def message(message: types.Message):

    print('+')
    actual = api.get_active_list()[500]
    actual_channel_users = api.get_active_list()[600]
    base = db.get_email_active_list()
    channel_users = db.get_email_channel_list()

    for i in base:
        if i not in actual:
            print('.........................................................')
            print(base)
            print(actual)
            text = """
            Your subscription has ended.
If you want to continue, please sign up with our Patreon again  - https://www.patreon.com/easy_trade"""
            await bot.send_message(db.get_id_by_email(i), text, disable_web_page_preview=True)
            db.delete_user(i)

    print(1)
    for channel_user in channel_users:
        if channel_user not in actual_channel_users:
            user_id = db.get_id_by_email(channel_user)
            try:
                await bot.kick_chat_member(lock_channel_id_1, user_id)
                await bot.unban_chat_member(lock_channel_id_1, user_id)
            except:
                pass
            try:
                await bot.kick_chat_member(lock_channel_id_2, user_id)
                await bot.unban_chat_member(lock_channel_id_2, user_id)
            except:
                pass
            try:
                await bot.kick_chat_member(lock_channel_id_3, user_id)
                await bot.unban_chat_member(lock_channel_id_3, user_id)
            except:
                pass
            try:
                await bot.kick_chat_member(lock_channel_id_4, user_id)
                await bot.unban_chat_member(lock_channel_id_4, user_id)
            except:
                pass
            try:
                text = """
                            Your subscription has ended.
                If you want to continue, please sign up with our Patreon again  - https://www.patreon.com/easy_trade"""
                await bot.send_message(db.get_id_by_email(i), text, disable_web_page_preview=True)
            except:
                pass

            db.delete_user(channel_user)

    print('//////')
    print(str(message.sender_chat.id))
    print(channel_id)

    if str(message.sender_chat.id) == str(channel_id):

        print(2)

        target_list = db.get_active_list()
        print(target_list)
        for i in target_list:
            time.sleep(0.5)
            print('Идём')
            try:
                try:
                    msg = message.text
                    caption = message.caption
                    print(caption)
                except:
                    pass
                try:
                    print('Отправляем фото')
                    await bot.send_photo(i, message.photo[0].file_id, caption=caption, parse_mode='html')
                    continue

                except Exception as e:

                    print(e)
                    try:
                        await bot.send_photo(i, message.photo[0].file_id)
                        continue
                    except:
                        print('Не фото')
                        pass

                try:
                    await bot.send_document(i, message.document.file_id, caption=caption, parse_mode='html')
                    continue
                except:
                    try:
                        await bot.send_document(i, message.document.file_id)
                        continue
                    except:
                        pass

                try:
                    await bot.send_video(i, message.video.file_id, caption=caption, parse_mode='html')
                    continue
                except:
                    try:
                        await bot.send_video(i, message.video.file_id)
                        continue
                    except:
                        pass

                try:
                    await bot.send_message(i, msg, parse_mode='html')
                    continue
                except:
                    pass
            except:
                continue


@dp.message_handler(commands=['start'], state="*")
async def process_start_command(message: types.Message, state: FSMContext):
    await States.Email.set()
    await bot.send_message(message.from_user.id, join_text, parse_mode='html', disable_web_page_preview=True)


@dp.message_handler(state=States.Email)
async def email_step(message: types.Message, state: FSMContext):
    print(message)
    if "@" not in message.text:
        await bot.send_message(message.from_user.id, "This is not email. Please enter correct email!")
    else:
        tg_id = db.get_id_by_email(message.text)
        if tg_id is not False and tg_id != message.from_user.id:
            text = """
            This email is already used in another Telegram account. If you want to have notifications here, please sign up with our Patreon - https://www.patreon.com/easy_trade"""
            await bot.send_message(message.from_user.id, text, disable_web_page_preview=True)
        elif tg_id is not False and tg_id == message.from_user.id:
            text = "You are already subscribed. Stay tuned."
            await bot.send_message(message.from_user.id, text)
            await state.finish()
        else:
            email_list = api.get_active_list()
            if message.text.lower() in email_list[500]:
                text = """
                <b>Your access is verified!</b>
Congratulations! 🥳

From now this bot will send you all trades.

Stay tuned!"""
                await bot.send_message(message.from_user.id, text, parse_mode='html')
                db.register(message.from_user.id, message.text.lower())
                await state.finish()
            elif message.text.lower() in email_list[600]:
                await bot.send_message(message.from_user.id,
                                       "You email is verified, thank you!")
                await asyncio.sleep(2)
                timer = int(time.time()) + 43200
                first_link = await bot.create_chat_invite_link(lock_channel_id_1, member_limit=1, expire_date=timer)
                second_link = await bot.create_chat_invite_link(lock_channel_id_2, member_limit=1, expire_date=timer)
                third_link = await bot.create_chat_invite_link(lock_channel_id_3, member_limit=1, expire_date=timer)
                fourth_link = await bot.create_chat_invite_link(lock_channel_id_4, member_limit=1, expire_date=timer)

                keyboard = InlineKeyboardMarkup()
                button = InlineKeyboardButton('USDT Futures', url=first_link.invite_link)
                button_second = InlineKeyboardButton('USDT Investments', url=second_link.invite_link)
                button_third = InlineKeyboardButton('BTC Investments', url=third_link.invite_link)
                button_fourth = InlineKeyboardButton('EASY Investments', url=fourth_link.invite_link)
                keyboard.add(button)
                keyboard.add(button_second)
                keyboard.add(button_third)
                keyboard.add(button_fourth)
                await bot.send_message(message.from_user.id, 'Please join to every private channel now👇🏼', reply_markup=keyboard)
                db.register(message.from_user.id, message.text, 'channels')
                await asyncio.sleep(120)
                text = """
                Thank you for joining.
Please make sure you have enabled notifications in all private channels.
Keep an eye on notifications."""
                await bot.send_message(message.from_user.id, text)

            else:
                text = """Incorrect email, please enter your email you have used to sign up in Patreon!"""
                await bot.send_message(message.from_user.id, text)

if __name__ == '__main__':
    executor.start_polling(dp)
