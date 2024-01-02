from aiogram.filters import Filter
from aiogram.types import Message


class SentFrom(Filter):
    def __init__(self, user_id: int | str) -> None:
        self.user_id = user_id

    async def __call__(self, message: Message) -> bool:
        return str(message.from_user.id) == str(self.user_id)
