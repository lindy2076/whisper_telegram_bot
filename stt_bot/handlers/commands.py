import asyncio
import logging
from aiogram import types, Router, F, Bot
from aiogram.filters import Command
from aiogram.enums import ParseMode

from stt_bot.config import Config
from stt_bot.filters import SentFrom
from stt_bot.utils import Converter, model, Response, try_remove, read_from_file
from stt_bot.keyboards import WhisperModelCallback, whisper_kb, start_kb, format_response_kb, FormatResponseCallback


config = Config()
main_router = Router(name="main_router")


async def delete_message_after(message: types.Message, sleep_time: int = 0):
    """delete *message* in *sleep_time* seconds"""
    await asyncio.sleep(sleep_time)
    await message.delete()


@main_router.message(~SentFrom(config.ADMIN_ID))
async def voice_handler(message: types.Message):
    """reply to non admin"""
    await message.reply(Response.NO_ADMIN)


@main_router.message(Command('start'))
async def start_admin_handler(message: types.Message):
    await message.reply(Response.ADMIN_START, reply_markup=start_kb)


@main_router.message(Command('model'))
async def model_select_handler(message: types.Message):
    """selection of Whisper model"""
    await message.answer(Response.select_curr_model(model.mdl), reply_markup=whisper_kb)


@main_router.message(Command('help'))
async def help_handler(message: types.Message):
    """sends help"""
    await message.answer(Response.HELP, reply_markup=start_kb)


@main_router.message(F.voice)
async def voice_handler(message: types.Message, bot: Bot):
    """convert voice message to text"""
    file_id = message.voice.file_id
    tmp_filename = f"tmp/{file_id}.ogg"
    await bot.download(file=file_id, destination=tmp_filename)
    ms = await message.reply(f"msg downloaded!")
    
    cnv = Converter(tmp_filename, model, f"{ms.chat.id}_{ms.message_id}")
    res, lang = cnv.speech_to_text()
    await ms.edit_text(Response.stt_response(res, lang, model.mdl), reply_markup=format_response_kb)
    cnv.cleanup()


@main_router.message(F.video)
async def video_handler(message: types.Message):
    await message.reply(f"this is a video msg!")


@main_router.message(F.video_note)
async def video_note_handler(message: types.Message, bot: Bot):
    file_id = message.video_note.file_id
    tmp_filename = f"tmp/{file_id}.mp4"
    await bot.download(file=file_id, destination=tmp_filename)
    ms = await message.reply(f"video downloaded!")

    cnv = Converter(tmp_filename, model, f"{ms.chat.id}_{ms.message_id}", is_video=True)
    res, lang = cnv.speech_to_text()
    await ms.edit_text(Response.stt_response(res, lang, model.mdl), reply_markup=format_response_kb)
    cnv.cleanup()


@main_router.message()
async def voice_handler(message: types.Message):
    """reply to unconvertable message formats"""
    await message.reply(Response.UNKNOWN_FORMAT, reply_markup=start_kb)


@main_router.callback_query(~SentFrom(config.ADMIN_ID))
async def non_admin_callback_handler(query: types.CallbackQuery):
    """reply to nonadmin callback"""
    await query.answer(Response.NO_ADMIN_CALLBACK)


@main_router.callback_query(WhisperModelCallback.filter())
async def whisper_callback_handler(query: types.CallbackQuery, callback_data: WhisperModelCallback):
    """reply to whisper model selection keyboard callback"""
    new_mdl = callback_data.mdl_type
    await query.answer()

    ans1 = await query.message.answer(Response.MODEL_LOADING)
    model.change_model(new_mdl)

    await ans1.delete()
    ans2 = await query.message.answer(Response.new_model_selected(new_mdl))
    await query.message.edit_text(Response.select_curr_model(model.mdl), reply_markup=whisper_kb)
    await delete_message_after(ans2, 5)


@main_router.callback_query(FormatResponseCallback.filter(F.fmt == "cleanup"))
async def fmt_cleanup_callback_handler(query: types.CallbackQuery, callback_data: WhisperModelCallback):
    """reply to cleanup callback"""
    await query.answer()
    transcript_id = f"{query.from_user.id}_{query.message.message_id}"
    if try_remove(f"tmp/{transcript_id}.txt"):
        await query.message.edit_reply_markup(reply_markup=None)
        q = await query.message.answer(f"{transcript_id} removed", parse_mode=ParseMode.HTML)
        await delete_message_after(q, 3)
    else:
        await query.message.answer(Response.SOMETHING_WRONG)


@main_router.callback_query(FormatResponseCallback.filter())
async def fmt_callback_handler(query: types.CallbackQuery, callback_data: WhisperModelCallback):
    """reply to whisper model selection keyboard callback"""
    await query.answer()
    transcript_id = f"{query.from_user.id}_{query.message.message_id}"

    res = read_from_file(f"tmp/{transcript_id}.txt", callback_data.fmt)
    fmted_res = Response.stt_response(res).strip()
    if fmted_res != query.message.text:
        await query.message.edit_text(fmted_res, reply_markup=format_response_kb)
    else:
        logging.info("same text, didn't edit")
