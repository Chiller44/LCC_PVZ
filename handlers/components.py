from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from common import send_start
from status import Addtinal_components



router = Router()

@router.message(Addtinal_components.valve)
async def handle_valve(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    data = await state.get_data()
    if message.text in ['Так', 'Ні']:
        await state.update_data(valve=message.text)
        if data.get('type_ahu') in ['Припливна', 'Припливно-витяжна']:
            kbrd_silenc = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='910'), KeyboardButton(text='1090')],
                    [KeyboardButton(text='1390'), KeyboardButton(text='1600')],
                    [KeyboardButton(text='Немає')]
                ], resize_keyboard=True
            )
            await message.answer('Виберіть шумогасник на притоку', reply_markup=kbrd_silenc)
            await state.set_state(Addtinal_components.supply_silence)
        else:
            kbrd_silenc = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='910'), KeyboardButton(text='1090')],
                    [KeyboardButton(text='1390'), KeyboardButton(text='1600')],
                    [KeyboardButton(text='Немає')]
                ], resize_keyboard=True
            )
            await message.answer('Виберіть шумогасник на витоку', reply_markup=kbrd_silenc)
            await state.set_state(Addtinal_components.exhaust_silence)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(Addtinal_components.supply_silence)
async def handle_supply_silence(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    await state.update_data(supply_silence=message.text)
    data = await state.get_data()
    if message.text in ['910', '1090', '1390', '1600']:
        if data.get('type_ahu') == 'Припливно-витяжна':
            kbrd_silenc = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='910'), KeyboardButton(text='1090')],
                    [KeyboardButton(text='1390'), KeyboardButton(text='1600')],
                    [KeyboardButton(text='Немає')]
                ], resize_keyboard=True
            )
            await message.answer('Виберіть шумогасник на витоку', reply_markup=kbrd_silenc)
            await state.set_state(Addtinal_components.exhaust_silence)
        elif data.get('type_ahu') == 'Припливна':
            kbrd_filter = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Панельний G4'), KeyboardButton(text='Кишеньковий G4')],
                    [KeyboardButton(text='M5'), KeyboardButton(text='F7')],
                    [KeyboardButton(text='F8'), KeyboardButton(text='F9')],
                    [KeyboardButton(text='Без фільтрів')]
                ], resize_keyboard=True
            )
            await message.answer('Виберіть фільтр першого ступеню припливного повітря', reply_markup=kbrd_filter)
            await state.set_state(Addtinal_components.supply_first_filter)
    elif message.text == 'Немає':
        if data.get('type_ahu') == 'Припливна':
            kbrd_filter = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Панельний G4'), KeyboardButton(text='Кишеньковий G4')],
                    [KeyboardButton(text='M5'), KeyboardButton(text='F7')],
                    [KeyboardButton(text='F8'), KeyboardButton(text='F9')],
                    [KeyboardButton(text='Без фільтрів')]
                ], resize_keyboard=True
            )
            await message.answer('Виберіть фільтр першого ступеню припливного повітря', reply_markup=kbrd_filter)
            await state.set_state(Addtinal_components.supply_first_filter)
        else:
            kbrd_silenc = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='910'), KeyboardButton(text='1090')],
                    [KeyboardButton(text='1390'), KeyboardButton(text='1600')],
                    [KeyboardButton(text='Немає')]
                ], resize_keyboard=True
            )
            await message.answer('Виберіть шумогасник на витоку', reply_markup=kbrd_silenc)
            await state.set_state(Addtinal_components.exhaust_silence)

    else:
        await message.answer('Виберіть з клавіатури')

@router.message(Addtinal_components.exhaust_silence)
async def handle_exhaust_silence(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text in ['910', '1090', '1390', '1600']:
        await state.update_data(exhaust_silence=message.text)
        data = await state.get_data()
        if data.get('type_ahu') == 'Припливно-витяжна':
            kbrd_filter = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Панельний G4'), KeyboardButton(text='Кишеньковий G4')],
                    [KeyboardButton(text='M5'), KeyboardButton(text='F7')],
                    [KeyboardButton(text='F8'), KeyboardButton(text='F9')],
                    [KeyboardButton(text='Без фільтрів')]
                ], resize_keyboard=True
            )
            await message.answer('Виберіть фільтр першого ступеню припливного повітря', reply_markup=kbrd_filter)
            await state.set_state(Addtinal_components.supply_first_filter)
        else:
            kbrd_filter = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Панельний G4'), KeyboardButton(text='Кишеньковий G4')],
                    [KeyboardButton(text='M5'), KeyboardButton(text='F7')],
                    [KeyboardButton(text='F8'), KeyboardButton(text='F9')],
                    [KeyboardButton(text='Без фільтрів')]
                ], resize_keyboard=True
            )
            await message.answer('Виберіть фільтр першого ступеню витяжного повітря', reply_markup=kbrd_filter)
            await state.set_state(Addtinal_components.exhaust_first_filter)
    elif message.text == 'Немає':
        await state.update_data(exhaust_silence=message.text)
        data = await state.get_data()
        if data.get('type_ahu') == 'Припливно-витяжна':
            kbrd_filter = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Панельний G4'), KeyboardButton(text='Кишеньковий G4')],
                    [KeyboardButton(text='M5'), KeyboardButton(text='F7')],
                    [KeyboardButton(text='F8'), KeyboardButton(text='F9')],
                    [KeyboardButton(text='Без фільтрів')]
                ], resize_keyboard=True
            )
            await message.answer('Виберіть фільтр першого ступеню припливного повітря', reply_markup=kbrd_filter)
            await state.set_state(Addtinal_components.supply_first_filter)
        else:
            kbrd_filter = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Панельний G4'), KeyboardButton(text='Кишеньковий G4')],
                    [KeyboardButton(text='M5'), KeyboardButton(text='F7')],
                    [KeyboardButton(text='F8'), KeyboardButton(text='F9')],
                    [KeyboardButton(text='Без фільтрів')]
                ], resize_keyboard=True
            )
            await message.answer('Виберіть фільтр першого ступеню витяжного повітря', reply_markup=kbrd_filter)
            await state.set_state(Addtinal_components.exhaust_first_filter)
    else:
        await message.answer('Виберіть з клавіатури')









