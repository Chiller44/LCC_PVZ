from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from common import send_start
from status import Exchangerform, Airform, Param_airform

router = Router()

@router.message(Exchangerform.heating1_type)
async def handle_heating1(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text == 'Водяний':
        await state.update_data(heating1_type=message.text)
        await message.answer('Введіть відсоток гліколю в рідині, %', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Exchangerform.heating1_percent_glycol)
    elif message.text == 'Електричний':
        await state.update_data(heating1_type=message.text)
        await message.answer('Температура після нагрівача, °C', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Airform.winter_internal1_temp)
    elif message.text == 'Без нагрівача':
        await state.update_data(heating1_type=message.text)
        kbrd_cooling = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Водяний'), KeyboardButton(text='Фреоновий')],
                [KeyboardButton(text='Без охолоджувача')]
            ],resize_keyboard=True
        )
        await message.answer('Виберіть тип охолоджувача', reply_markup=kbrd_cooling)
        await state.set_state(Exchangerform.cooling1_type)
    else:
        await message.answer('Виберіть з клавіатури')


@router.message(Exchangerform.heating1_param)
async def handle_param(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text in ['150/70', '130/70', '90/70', '80/60', '60/40', '45/40']:
        await state.update_data(heating1_param=message.text)
        await message.answer('Температура після нагрівача, °C', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Airform.winter_internal1_temp)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(Airform.winter_internal1_temp)
async def handle_w_internal_temp(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        data = await state.get_data()
        w_out_temp = float(message.text)
        w_in_temp = float(data.get('winter_outside_temp'))
        if w_in_temp < w_out_temp <= 50:
            await state.update_data(winter_internal1_temp=message.text)
            kbrd_sec_heating = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Так')], [KeyboardButton(text='Ні')]
                ], resize_keyboard=True
            )
            await message.answer('Потрібен другий нагрівач?', reply_markup=kbrd_sec_heating)
            await state.set_state(Exchangerform.confirm_heating2)
        else:
            await message.answer('Введіть коректну температуру після нагрівача, °C')
    except ValueError:
        await message.answer('Введіть числове значення')

@router.message(Exchangerform.confirm_heating2)
async def confirm_heating2(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text == 'Так':
        await state.update_data(confirm_heating2=message.text)
        kbrd_heating = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Водяний')], [KeyboardButton(text='Електричний')]
            ], resize_keyboard=True
        )
        await message.answer('Виберіть тип нагрівача', reply_markup=kbrd_heating)
        await state.set_state(Exchangerform.heating2_type)
    elif message.text == 'Ні':
        kbrd_cooling = ReplyKeyboardMarkup(
           keyboard=[
               [KeyboardButton(text='Водяний'), KeyboardButton(text='Фреоновий')],
               [KeyboardButton(text='Без охолоджувача')]
           ], resize_keyboard=True
        )
        await message.answer('Виберіть тип охолоджувача', reply_markup=kbrd_cooling)
        await state.set_state(Exchangerform.cooling1_type)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(Exchangerform.heating2_type)
async def handle_heating(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text == 'Водяний':
        await state.update_data(heating2_type=message.text)
        await message.answer('Введіть відсоток гліколю в рідині, %', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Exchangerform.heating2_percent_glycol)
    elif message.text == 'Електричний':
        await state.update_data(heating2_type=message.text)
        await message.answer('Температура після нагрівача, °C', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Airform.winter_internal2_temp)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(Exchangerform.heating2_param)
async def handle_param(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text in ['150/70', '130/70', '90/70', '80/60', '60/40', '45/40']:
        await state.update_data(heating2_param=message.text)
        await message.answer('Температура після нагрівача, °C', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Airform.winter_internal2_temp)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(Airform.winter_internal2_temp)
async def handle_w_internal_temp(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        data = await state.get_data()
        w_out_temp = float(message.text)
        w_in_temp = float(data.get('winter_outside_temp'))
        if w_in_temp < w_out_temp <= 50:
            await state.update_data(winter_internal2_temp=message.text)
            kbrd_cooling = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Водяний'), KeyboardButton(text='Фреоновий')],
                    [KeyboardButton(text='Без охолоджувача')]
                ], resize_keyboard=True
            )
            await message.answer('Виберіть тип охолоджувача', reply_markup=kbrd_cooling)
            await state.set_state(Exchangerform.cooling1_type)
        else:
            await message.answer('Введіть коректну температуру після нагрівача, °C')
    except ValueError:
        await message.answer('Введіть числове значення')

@router.message(Exchangerform.cooling1_type)
async def handler_cooling1(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text == 'Водяний':
        await state.update_data(cooling1_type=message.text)
        kbrd_glyc = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Етиленгліколь')], [KeyboardButton(text='Пропіленгліколь')],
                [KeyboardButton(text='Вода')]
            ],resize_keyboard=True
        )
        await message.answer('Виберіть тип хладоагенту', reply_markup=kbrd_glyc)
        await state.set_state(Exchangerform.cooling1_glycol)
    elif message.text == 'Фреоновий':
        await state.update_data(cooling1_type=message.text)
        kbrd_freon = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='R410A'), KeyboardButton(text='R22')],
                [KeyboardButton(text='R134A'), KeyboardButton(text='R407C')]
            ], resize_keyboard=True
        )
        await message.answer('Виберіть тип хладоагенту', reply_markup=kbrd_freon)
        await state.set_state(Exchangerform.freon1)
    elif message.text == 'Без охолоджувача':
        await state.update_data(cooling1_type=message.text)
        await message.answer('Витрата припливного повітря, м³/год', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Param_airform.supply_air)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(Exchangerform.cooling1_glycol)
async def handler_cooling1_glycol(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text in ['Етиленгліколь', 'Пропіленгліколь']:
        await state.update_data(cooling1_glycol=message.text)
        await message.answer('Ведіть відсоток гліколю', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Exchangerform.cooling1_percent_glycol)
    elif message.text == 'Вода':
        await state.update_data(cooling1_glycol=message.text)
        kbrd_water = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='7/12'), KeyboardButton(text='6/11')],
                [KeyboardButton(text='5/10'), KeyboardButton(text='4/9')]
            ], resize_keyboard=True
        )
        await message.answer('Оберіть температурний графік', reply_markup=kbrd_water)
        await state.set_state(Exchangerform.cooling1_param)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(Exchangerform.freon1)
async def handler_freon1(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text in ['R410A', 'R22', 'R134A', 'R407C']:
        await state.update_data(freon1=message.text)
        await message.answer('Температура після охолоджувача, °C', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Airform.summer_internal1_temp)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(Exchangerform.cooling1_percent_glycol)
async def handler_cooling1_percent_glycol(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        percent = float(message.text)
        if 1 <= percent <= 100:
            await state.update_data(cooling1_percent_glycol=message.text)
            kbrd_glycol = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='7/12'), KeyboardButton(text='6/11'), KeyboardButton(text='5/10')],
                    [KeyboardButton(text='4/9'), KeyboardButton(text='3/8'), KeyboardButton(text='2/7')],
                    [KeyboardButton(text='1/6'), KeyboardButton(text='0/5'), KeyboardButton(text='-1/4')]
                ], resize_keyboard=True
            )
            await message.answer('Оберіть температурний графік', reply_markup=kbrd_glycol)
            await state.set_state(Exchangerform.cooling1_param)
        else:
            await message.answer('Введіть відсоток гліколю від 1 до 100, %')
    except ValueError:
        await message.answer('Введіть числове значення')

@router.message(Exchangerform.cooling1_param)
async def handler_cooling1_param(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text in ['7/12', '6/11', '5/10', '4/9', '3/8', '2/7', '1/6', '0/5', '-1/4']:
        await state.update_data(cooling1_param=message.text)
        await message.answer('Температура після охолоджувача, °C', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Airform.summer_internal1_temp)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(Airform.summer_internal1_temp)
async def handler_summer_internal1_temp(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        data = await state.get_data()
        sum_out_temp = float(message.text)
        sum_in_temp = float(data.get('summer_outside_temp'))
        if 12 < sum_out_temp < sum_in_temp:
            await state.update_data(summer_internal1_temp=message.text)
            kbrd_sec_cooling = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Так')], [KeyboardButton(text='Ні')]
                ], resize_keyboard=True
            )
            await message.answer('Потрібен другий охолоджувач?', reply_markup=kbrd_sec_cooling)
            await state.set_state(Exchangerform.confirm_cooling2)
        else:
            await message.answer('Введіть коректну температуру після охолоджувача, °C')
    except  ValueError:
        await message.answer('Введіть числове значення')

@router.message(Exchangerform.confirm_cooling2)
async def handler_confirm_cooling2(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text == 'Так':
        await state.update_data(confirm_cooling2=message.text)
        kbrd_cooling = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Водяний')], [KeyboardButton(text='Фреоновий')]
            ], resize_keyboard=True
        )
        await message.answer('Оберіть тип охолоджувача', reply_markup=kbrd_cooling)
        await state.set_state(Exchangerform.cooling2_type)
    elif message.text == 'Ні':
        await state.update_data(confirm_cooling2=message.text)
        await message.answer('Витрата припливного повітря, м³/год', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Param_airform.supply_air)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(Exchangerform.cooling2_type)
async def handler_cooling2(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text == 'Водяний':
        await state.update_data(cooling2_type=message.text)
        kbrd_glyc = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Етиленгліколь')], [KeyboardButton(text='Пропіленгліколь')],
                [KeyboardButton(text='Вода')]
            ],resize_keyboard=True
        )
        await message.answer('Виберіть тип хладоагенту', reply_markup=kbrd_glyc)
        await state.set_state(Exchangerform.cooling2_glycol)
    elif message.text == 'Фреоновий':
        await state.update_data(cooling2_type=message.text)
        kbrd_freon = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='R410A'), KeyboardButton(text='R22')],
                [KeyboardButton(text='R134A'), KeyboardButton(text='R407C')]
            ], resize_keyboard=True
        )
        await message.answer('Виберіть тип хладоагенту', reply_markup=kbrd_freon)
        await state.set_state(Exchangerform.freon2)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(Exchangerform.cooling2_glycol)
async def handler_cooling2_glycol(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text in ['Етиленгліколь', 'Пропіленгліколь']:
        await state.update_data(cooling2_glycol=message.text)
        await message.answer('Введіть відсоток гліколю', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Exchangerform.cooling2_percent_glycol)
    elif message.text == 'Вода':
        await state.update_data(cooling2_glycol=message.text)
        kbrd_water = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='7/12'), KeyboardButton(text='6/11')],
                [KeyboardButton(text='5/10'), KeyboardButton(text='4/9')]
            ], resize_keyboard=True
        )
        await message.answer('Оберіть температурний графік', reply_markup=kbrd_water)
        await state.set_state(Exchangerform.cooling2_param)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(Exchangerform.freon2)
async def handler_freon2(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text in ['R410A', 'R22', 'R134A', 'R407C']:
        await state.update_data(freon2=message.text)
        await message.answer('Температура після охолоджувача, °C', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Airform.summer_internal2_temp)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(Exchangerform.cooling2_percent_glycol)
async def handler_cooling2_percent_glycol(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        percent = float(message.text)
        if 1 <= percent <= 100:
            await state.update_data(cooling2_percent_glycol=message.text)
            kbrd_glycol = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='7/12'), KeyboardButton(text='6/11'), KeyboardButton(text='5/10')],
                    [KeyboardButton(text='4/9'), KeyboardButton(text='3/8'), KeyboardButton(text='2/7')],
                    [KeyboardButton(text='1/6'), KeyboardButton(text='0/5'), KeyboardButton(text='-1/4')]
                ], resize_keyboard=True
            )
            await message.answer('Оберіть температурний графік', reply_markup=kbrd_glycol)
            await state.set_state(Exchangerform.cooling2_param)
        else:
            await message.answer('Введіть відсоток гліколю від 1 до 100, %')
    except ValueError:
        await message.answer('Введіть числове значення')

@router.message(Exchangerform.cooling2_param)
async def handler_cooling2_param(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text in ['7/12', '6/11', '5/10', '4/9', '3/8', '2/7', '1/6', '0/5', '-1/4']:
        await state.update_data(cooling2_param=message.text)
        await message.answer('Температура після охолоджувача, °C', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Airform.summer_internal2_temp)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(Airform.summer_internal2_temp)
async def handler_summer_internal2_temp(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        data = await state.get_data()
        sum_out_temp = float(message.text)
        sum_in_temp = float(data.get('summer_outside_temp'))
        if 12 < sum_out_temp < sum_in_temp:
            await state.update_data(summer_internal2_temp=message.text)
            await message.answer('Витрата припливного повітря, м³/год', reply_markup=ReplyKeyboardRemove())
            await state.set_state(Param_airform.supply_air)
        else:
            await message.answer('Введіть коректну температуру після охолоджувача, °C')
    except  ValueError:
        await message.answer('Введіть числове значення')

@router.message(Exchangerform.heating1_percent_glycol)
async def handle_heating1_percent_glycol(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        percent = float(message.text)
        if 0 <= percent <= 100:
            await state.update_data(heating1_percent_glycol=message.text)
            kbrd_param = ReplyKeyboardMarkup(
               keyboard=[
                   [KeyboardButton(text='150/70'), KeyboardButton(text='130/70')],
                   [KeyboardButton(text='90/70'), KeyboardButton(text='80/60')],
                   [KeyboardButton(text='60/40'), KeyboardButton(text='45/40')],
               ], resize_keyboard=True
            )
            await message.answer('Оберіть температурний графік', reply_markup=kbrd_param)
            await state.set_state(Exchangerform.heating1_param)
        else:
            await message.answer('Введіть відсоток гліколю від 0 до 100, %')
    except  ValueError:
        await message.answer('Введіть числове значення')

@router.message(Exchangerform.heating2_percent_glycol)
async def handle_heating2_percent_glycol(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    try:
        percent = float(message.text)
        if 0 <= percent <= 100:
            await state.update_data(heating2_percent_glycol=message.text)
            kbrd_param = ReplyKeyboardMarkup(
               keyboard=[
                   [KeyboardButton(text='150/70'), KeyboardButton(text='130/70')],
                   [KeyboardButton(text='90/70'), KeyboardButton(text='80/60')],
                   [KeyboardButton(text='60/40'), KeyboardButton(text='45/40')],
               ], resize_keyboard=True
            )
            await message.answer('Оберіть температурний графік', reply_markup=kbrd_param)
            await state.set_state(Exchangerform.heating2_param)
        else:
            await message.answer('Введіть відсоток гліколю від 0 до 100, %')
    except  ValueError:
        await message.answer('Введіть числове значення')



































