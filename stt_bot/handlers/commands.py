import asyncio
from aiogram import types, Router, F, Bot
from aiogram.filters import Command
from aiogram.enums import ParseMode

from stt_bot.config import Config
from stt_bot.filters import SentFrom
from stt_bot.utils import Converter, model
from stt_bot.keyboards import whisper_kb, WhisperModelCallback


config = Config()
main_router = Router(name="main_router")


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    await message.delete()


@main_router.message(SentFrom(config.ADMIN_ID), Command('start'))
async def start_admin_handler(message: types.Message):
    await message.reply('Hello Mr. Admin!')


@main_router.message(Command('start'))
async def start_default_handler(message: types.Message):
    await message.reply("I don't know you.")


@main_router.message(~SentFrom(config.ADMIN_ID))
async def voice_handler(message: types.Message):
    await message.reply("Sorry, my owner said i shouldn't talk to anyone except him...")


@main_router.message(SentFrom(config.ADMIN_ID), Command('model'))
async def start_admin_handler(message: types.Message):
    await message.answer(f"Select model!\nCurrent model is *{model.mdl}*", reply_markup=whisper_kb, parse_mode=ParseMode.MARKDOWN)


@main_router.message(F.voice)
async def voice_handler(message: types.Message, bot: Bot):
    file_id = message.voice.file_id
    tmp_filename = f"tmp/{file_id}.ogg"
    await bot.download(file=file_id, destination=tmp_filename)
    await message.reply(f"msg downloaded!")
    
    cnv = Converter(tmp_filename, model.model)
    res, lang = cnv.speech_to_text()
    await message.reply(res + "\n"*2 + f"Detected language: {lang}")
    cnv.cleanup()


@main_router.message(F.video)
async def video_handler(message: types.Message):
    await message.reply(f"this is a video msg!")


@main_router.message(F.video_note)
async def video_note_handler(message: types.Message, bot: Bot):
    file_id = message.video_note.file_id
    tmp_filename = f"tmp/{file_id}.mp4"
    await bot.download(file=file_id, destination=tmp_filename)
    await message.reply(f"video downloaded!")
    cnv = Converter(tmp_filename, model.model, is_video=True)
    res, lang = cnv.speech_to_text()
    await message.reply(res + "\n"*2 + f"Detected language: {lang}")
    cnv.cleanup()


@main_router.message()
async def voice_handler(message: types.Message):
    await message.reply("I can't convert this message type. It is not a voice message, video or video note.")


@main_router.callback_query(WhisperModelCallback.filter())
async def whisper_callback_handler(query: types.CallbackQuery, callback_data: WhisperModelCallback):
    new_mdl = callback_data.mdl_type
    model.change_model(new_mdl)
    ans = await query.message.answer(f"{new_mdl} model selected!\nThis message will disappear in 5 seconds")
    await query.answer()
    await query.message.edit_text(f"Select model!\nCurrent model is *{model.mdl}*", reply_markup=whisper_kb, parse_mode=ParseMode.MARKDOWN)

    await delete_message(ans, 5)
