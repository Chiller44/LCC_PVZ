from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from common import send_start
from status import AHUform, Exchangerform, Param_airform, Airform

router = Router()

@router.message(AHUform.installation)
async def handle_installation(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text in ['Внутрішня', 'Наружна']:
        await state.update_data(installation=message.text)
        kbrd_frame = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='На рамі')], [KeyboardButton(text='Без рами')]
            ], resize_keyboard=True
        )
        await message.answer('Виберіть виконання установки', reply_markup=kbrd_frame)
        await state.set_state(AHUform.frame)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(AHUform.frame)
async def handle_frame(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text in ['На рамі', 'Без рами']:
        await state.update_data(frame=message.text)
        kbrd_recycling = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Так')], [KeyboardButton(text='Ні')]
            ], resize_keyboard=True
        )
        await message.answer('З рециркуляцією?', reply_markup=kbrd_recycling)
        await state.set_state(AHUform.recycling)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(AHUform.recycling)
async def handle_recycling(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text == 'Ні':
        await state.update_data(recycling=message.text)
        kbrd_type_ahu = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Припливна'), KeyboardButton(text='Витяжна')],
                [KeyboardButton(text='Припливно-витяжна')]
            ],resize_keyboard=True
        )
        await message.answer('Виберіть тип установки', reply_markup=kbrd_type_ahu)
        await state.set_state(AHUform.type_ahu)
    elif message.text == 'Так':
        await state.update_data(recycling=message.text)
        await message.answer('Введіть відсоток зовнішнього повітря', reply_markup=ReplyKeyboardRemove())
        await state.set_state(AHUform.percent_recycling)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(AHUform.percent_recycling)
async def percent_recycling(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        percent = float(message.text)
        if 1 <= percent <= 100:
            await state.update_data(percent_recycling=message.text)
            await message.answer('Введіть температуру рециркуляційного повітря, °C')
            await state.set_state(AHUform.temp_recycling)
        else:
            await message.answer('Введіть відсоток рециркуляційного повітря від 1 до 100%')
    except ValueError:
        await message.answer('Введіть число')

@router.message(AHUform.temp_recycling)
async def handle_temp_recycling(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        temp = float(message.text)
        if 5 < temp < 50:
            await state.update_data(temp_recycling=message.text)
            kbrd_type_ahu = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Припливна'), KeyboardButton(text='Витяжна')],
                    [KeyboardButton(text='Припливно-витяжна')]
                ], resize_keyboard=True
            )
            await message.answer('Виберіть тип установки', reply_markup=kbrd_type_ahu)
            await state.set_state(AHUform.type_ahu)
        else:
            await message.answer('Введіть температуру рециркуляційного повітря в діапазоні від 5 до 50 °C')
    except ValueError:
        await message.answer('Введіть число')

@router.message(AHUform.type_ahu)
async def handle_type_ahu(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text == 'Припливна':
        await state.update_data(type_ahu=message.text)
        kbrd_heating = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Водяний')], [KeyboardButton(text='Електричний')],
                [KeyboardButton(text='Без нагрівача')]
            ], resize_keyboard=True
        )
        await message.answer('Виберіть тип нагрівача', reply_markup=kbrd_heating)
        await state.set_state(Exchangerform.heating1_type)
    elif message.text == 'Припливно-витяжна':
        await state.update_data(type_ahu=message.text)
        await message.answer('Введіть витияжну температуру в зимовий період, °C', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Airform.winter_exhaust_temp)
    elif message.text == 'Витяжна':
        await state.update_data(type_ahu=message.text)
        await message.answer('Витрата витяжного повітря, м³/год')
        await state.set_state(Param_airform.exhaust_air)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(AHUform.recuperation)
async def handle_recuperation(message: Message, state: FSMContext):
    if message.text in ['Роторний', 'Пластинчатий', 'Без рекуператора']:
        if message.text == "/start":
            await send_start(message, state)
            return
        await state.update_data(recuperation=message.text)
        kbrd_heating = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Водяний')], [KeyboardButton(text='Електричний')],
                [KeyboardButton(text='Без нагрівача')]
            ], resize_keyboard=True
        )
        await message.answer('Виберіть тип нагрівача', reply_markup=kbrd_heating)
        await state.set_state(Exchangerform.heating1_type)
    elif message.text == 'Гліколевий':
        await state.update_data(recuperation=message.text)
        kbrd_type_glyc=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Елиленгліколь')], [KeyboardButton(text='Пропіленгліколь')]
                ], resize_keyboard=True
            )
        await message.answer('Виберіть тип гліколю', reply_markup=kbrd_type_glyc)
        await state.set_state(AHUform.type_glycol)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(AHUform.type_glycol)
async def type_glycol(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text in ['Елиленгліколь','Пропіленгліколь']:
        await state.update_data(type_glycol=message.text)
        await message.answer('Введіть відсоток гліколю в рідині', reply_markup=ReplyKeyboardRemove())
        await state.set_state(AHUform.percent_glycol)
    else:
        await message.answer('Виберіть з клавіатури')


@router.message(AHUform.percent_glycol)
async def percent_glycol(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        percent = float(message.text)
        if 1 <= percent <= 100:
            await state.update_data(percent_glycol=message.text)
            kbrd_heating = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Водяний')], [KeyboardButton(text='Електричний')],
                    [KeyboardButton(text='Без нагрівача')]
                ], resize_keyboard=True
            )
            await message.answer('Виберіть тип нагрівача', reply_markup=kbrd_heating)
            await state.set_state(Exchangerform.heating1_type)
        else:
            await message.answer('Введіть відсоток гліколю від 1 до 100%')
    except ValueError:
        await message.answer('Введіть число')












