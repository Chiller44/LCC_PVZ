from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    kbrd_start = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Почнемо')]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "Привіт!\nДопоможу заповнити опитувальний лист.\nТисни \"Почнемо\"!",
        reply_markup=kbrd_start
    )