from aiogram.types import (
    InlineKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class WhisperModelCallback(CallbackData, prefix="whi_model"):
    mdl_type: str


class ManageTranscriptCallback(CallbackData, prefix="fmt_re"):
    fmt: str


def build_whisper_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for model_type in ["tiny", "base", "small", "medium"]:
        builder.button(
            text=model_type,
            callback_data=WhisperModelCallback(mdl_type=model_type).pack()
        )

    return builder.as_markup()


def build_manage_transcript_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    button_data = [
        ("📜 just text", "text"),
        ("🕒️ timings", "timings"),
        ("🗑️ cleanup", "c_up")
    ]

    for fmt, cb in button_data:
        builder.button(
            text=fmt,
            callback_data=ManageTranscriptCallback(fmt=cb).pack()
        )

    return builder.as_markup()


whisper_kb = build_whisper_kb()
manage_transcript_kb = build_manage_transcript_kb()
