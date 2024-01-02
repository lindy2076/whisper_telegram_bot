from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class WhisperModelCallback(CallbackData, prefix="whi_model"):
    mdl_type: str


builder = InlineKeyboardBuilder()

for model_type in ["tiny", "base", "small", "medium"]:
    builder.button(text=model_type, callback_data=WhisperModelCallback(mdl_type=model_type).pack())

whisper_kb = builder.as_markup()
