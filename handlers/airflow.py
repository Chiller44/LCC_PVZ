from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from common import send_start
from status import AHUform, Exchangerform, Airform, Param_airform, Addtinal_components

router = Router()

@router.message(Param_airform.supply_air)
async def handler_supply_air(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        value = float(message.text.replace(',', '.'))
        value = int(value)
    except ValueError:
        await message.answer("Будь ласка, введіть числове значення (наприклад, 500 або 1000).")
        return
    data = await state.get_data()
    await state.update_data(supply_air=value)
    if data.get('type_ahu') == 'Припливна':
        await message.answer('Вільний тиск припливного повітря, Па')
        await state.set_state(Param_airform.supply_pressure)
    elif data.get('type_ahu') == 'Припливно-витяжна':
        await message.answer('Витрата витяжного повітря, м³/год')
        await state.set_state(Param_airform.exhaust_air)


@router.message(Param_airform.exhaust_air)
async def handle_exhaust_air(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        value = float(message.text.replace(',', '.'))
        value = int(value)
    except ValueError:
        await message.answer("Будь ласка, введіть числове значення (наприклад, 500 або 1000).")
        return
    data = await state.get_data()
    await state.update_data(exhaust_air=value)
    if data.get('type_ahu') == 'Витяжна':
        await message.answer('Вільний тиск витяжного повітря, Па')
        await state.set_state(Param_airform.exhaust_pressure)
    else:
        await message.answer('Вільний тиск припливного повітря, Па')
        await state.set_state(Param_airform.supply_pressure)

@router.message(Param_airform.supply_pressure)
async def handle_supply_pressure(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        value = float(message.text.replace(',', '.'))
        value = int(value)
    except ValueError:
        await message.answer("Будь ласка, введіть числове значення (наприклад, 500 або 1000).")
        return
    data = await state.get_data()
    await state.update_data(supply_pressure=value)
    if data.get('type_ahu') == 'Припливна':
        kbrd_valve=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Так')], [KeyboardButton(text='Ні')]
            ],resize_keyboard=True
        )
        await message.answer('Потрібен повітряний клапвн(и)?', reply_markup=kbrd_valve)
        await state.set_state(Addtinal_components.valve)
    elif data.get('type_ahu') == 'Припливно-витяжна':
        await message.answer('Вільний тиск витяжного повітря, Па')
        await state.set_state(Param_airform.exhaust_pressure)

@router.message(Param_airform.exhaust_pressure)
async def handle_exhaust_pressure(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        value = float(message.text.replace(',', '.'))
        value = int(value)
    except ValueError:
        await message.answer("Будь ласка, введіть числове значення (наприклад, 500 або 1000).")
        return
    await state.update_data(exhaust_pressure=value)
    kbrd_valve = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Так')], [KeyboardButton(text='Ні')]
        ], resize_keyboard=True
    )
    await message.answer('Потрібен повітряний клапан(и)?', reply_markup=kbrd_valve)
    await state.set_state(Addtinal_components.valve)



