from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from common import send_start
from status import Airform, AHUform

router = Router()

@router.message(Airform.winter_outside_temp)
async def winter_outside_temp(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        temp = float(message.text)
        if -35 <= temp <= -5:
            await state.update_data(winter_outside_temp=temp)
            await message.answer('Введіть вологість зовнішнього повітря в зимовий період, %')
            await state.set_state(Airform.winter_outside_humidity)
        else:
            await message.answer('Введіть коректну температуру від -35 до -5, °C')
    except ValueError:
        await message.answer('Введіть, будь ласка, число')


@router.message(Airform.winter_outside_humidity)
async def summer_outside_humidity(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        humidity = float(message.text)
        if 0 < humidity <=100:
            await state.update_data(winter_outside_humidity=humidity)
            await message.answer('Введіть температуру зовнішнього повітря в літній період, °C')
            await state.set_state(Airform.summer_outside_temp)
        else:
            await message.answer('Введіть вологість в діапазоні від 0 до 100%')
    except ValueError:
        await message.answer('Введіть, будь ласка, число')

@router.message(Airform.summer_outside_temp)
async def summer_outside_humidity(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        temp = float(message.text)
        if 21 <= temp <= 38:
            await state.update_data(summer_outside_temp=temp)
            await message.answer('Введіть вологість зовнішнього повітря в літній період, %')
            await state.set_state(Airform.summer_outside_humidity)
        else:
            await message.answer('Введіть коректну температуру від +21 до +38, °C')
    except ValueError:
        await message.answer('Введіть, будь ласка, число')

@router.message(Airform.summer_outside_humidity)
async def summer_outside_humidity(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        humidity = float(message.text)
        if 0 < humidity <= 100:
            kbrd_confirm = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Так')], [KeyboardButton(text='Ні')]
                ], resize_keyboard=True
            )
            await state.update_data(summer_outside_humidity=humidity)
            data = await state.get_data()
            await message.answer(f'Ваші параметри повітря:\nЗима:\n'
                                 f'Температура повітря: {data.get("winter_outside_temp")} °C\n'
                                 f'Вологість повітря: {data.get("winter_outside_humidity")} %\n'
                                 f'Літо:\n'
                                 f'Температура повітря: +{data.get("summer_outside_temp")} °C\n'
                                 f'Вологість повітря: {data.get("summer_outside_humidity")} %')
            await message.answer('Параметри повітря введені вірно?', reply_markup=kbrd_confirm)
            await state.set_state(Airform.confirm)
        else:
            await message.answer('Введіть вологість в діапазоні від 0 до 100%')
    except ValueError:
        await message.answer('Введіть, будь ласка, число')

@router.message(Airform.confirm)
async def confirm(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text == 'Так':
        await message.answer('Ваші дані збережено', reply_markup=ReplyKeyboardRemove())
        kbrd_installation = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Внутрішня')], [KeyboardButton(text='Наружна')]
            ], resize_keyboard=True
        )
        await message.answer('Виберіть розміщення установки', reply_markup=kbrd_installation)
        await state.set_state(AHUform.installation)
    elif message.text == 'Ні':
        await message.answer('Давайте введемо нові дані.\n'
                             'Введіть температуру зовнішнього повітря в зимовій період, °C', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Airform.winter_outside_temp)
    else:
        await message.answer('Будь ласка, виберіть з клавіатури: "Так" або "Ні".')

@router.message(Airform.winter_exhaust_temp)
async def handle_exhaust_winter_temp(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        temp = float(message.text)
        if 5 <= temp <= 45:
            await state.update_data(winter_exhaust_temp=temp)
            await message.answer('Введіть вологість витяжного повітря в зимовий період, %')
            await state.set_state(Airform.winter_exhaust_humidity)
        else:
            await message.answer('Введіть коректну температуру від +5 до +45, °C')
    except ValueError:
        await message.answer('Введіть, будь ласка, число')

@router.message(Airform.winter_exhaust_humidity)
async def winter_exhaust_humidity(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        humidity = float(message.text)
        if 0 < humidity <=100:
            await state.update_data(winter_exhaust_humidity=humidity)
            await message.answer('Введіть температуру витяжного повітря в літній період, °C')
            await state.set_state(Airform.summer_exhaust_temp)
        else:
            await message.answer('Введіть вологість в діапазоні від 0 до 100%')
    except ValueError:
        await message.answer('Введіть, будь ласка, число')

@router.message(Airform.summer_exhaust_temp)
async def handle_summer_exhaust_temp(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        temp = float(message.text)
        if 5 <= temp <= 45:
            await state.update_data(summer_exhaust_temp=temp)
            await message.answer('Введіть вологість витяжного повітря в зимовий період, %')
            await state.set_state(Airform.summer_exhaust_humidity)
        else:
            await message.answer('Введіть коректну температуру від +5 до +45, °C')
    except ValueError:
        await message.answer('Введіть, будь ласка, число')

@router.message(Airform.summer_exhaust_humidity)
async def winter_exhaust_humidity(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        humidity = float(message.text)
        if 0 < humidity <=100:
            await state.update_data(summer_exhaust_humidity=humidity)
            kbrd_recuperator = ReplyKeyboardMarkup(
               keyboard=[
                   [KeyboardButton(text='Роторний'), KeyboardButton(text='Пластинчатий')],
                   [KeyboardButton(text='Гліколевий'), KeyboardButton(text='Без рекуператора')]
               ], resize_keyboard=True
            )
            await message.answer('Виберіть тип рекуператора', reply_markup=kbrd_recuperator)
            await state.set_state(AHUform.recuperation)
        else:
            await message.answer('Введіть вологість в діапазоні від 0 до 100%')
    except ValueError:
        await message.answer('Введіть, будь ласка, число')




