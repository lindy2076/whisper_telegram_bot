from aiogram import types, Router, F
from aiogram.filters import Command

from stt_bot.config import Config


config = Config()
main_router = Router(name="main_router")


@main_router.message(Command('start'))
async def start_handler(message: types.Message):
    if str(message.from_user.id) != config.ADMIN_ID:
        await message.reply("sorry my owner said i shouldn't talk to anyone except him...")
        return
    await message.reply('hello master')


@main_router.message(F.voice)
async def voice_handler(message: types.Message):
    await message.reply(f"this is a voice msg!")


@main_router.message(F.video)
async def video_handler(message: types.Message):
    await message.reply(f"this is a video msg!")


@main_router.message(F.video_note)
async def video_note_handler(message: types.Message):
    await message.reply(f"this is a video\_note msg!")


@main_router.message()
async def voice_handler(message: types.Message):
    await message.reply("I can't convert this message type. It is not a voice message, video or video note.")
