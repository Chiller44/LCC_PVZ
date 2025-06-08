from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from common import send_start
from status import Addtinal_components
from aiogram.types import FSInputFile
from utills.excel_writer import generate_excel_file



router = Router()

@router.message(Addtinal_components.supply_first_filter)
async def handle_supply_first_filter(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text in ['Панельний G4', 'Кишеньковий G4', 'M5', 'F7', 'F8', 'F9']:
        await state.update_data(supply_first_filter=message.text)
        data = await state.get_data()
        if data.get('type_ahu') == 'Припливна':
            kbrd_second_filter = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Так')], [KeyboardButton(text='Ні')]
                ], resize_keyboard=True
            )
            await message.answer('Потрібен фільтр другого ступеню припливного повітря?', reply_markup=kbrd_second_filter)
            await state.set_state(Addtinal_components.confirm_supply_second_filter)
        elif data.get('type_ahu') == 'Припливно-витяжна':
            kbrd_second_filter = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Так')], [KeyboardButton(text='Ні')]
                ], resize_keyboard=True
            )
            await message.answer('Потрібен фільтр другого ступеню припливного повітря?', reply_markup=kbrd_second_filter)
            await state.set_state(Addtinal_components.confirm_supply_second_filter)
    elif message.text == 'Без фільтрів':
        await state.update_data(supply_first_filter=message.text)
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
            await message.answer('Виберіть фільтр першого ступеню витяжного повітря', reply_markup=kbrd_filter)
            await state.set_state(Addtinal_components.exhaust_first_filter)
        else:
            kbrd_automation = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Так')], [KeyboardButton(text='Ні')]
                ], resize_keyboard=True
            )
            await message.answer('Потрібна автоматика для установки?', reply_markup=kbrd_automation)
            await state.set_state(Addtinal_components.automation)

    else:
        await message.answer('Виберіть з клавіатури')

@router.message(Addtinal_components.exhaust_first_filter)
async def handle_exhaust_first_filter(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text in ['Панельний G4', 'Кишеньковий G4', 'M5', 'F7', 'F8', 'F9']:
        await state.update_data(exhaust_first_filter=message.text)
        data = await state.get_data()
        if data.get('type_ahu') =='Витяжна':
            kbrd_second_filter = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Так')], [KeyboardButton(text='Ні')]
                ], resize_keyboard=True
            )
            await message.answer('Потрібен фільтр другого ступеню витяжного повітря?', reply_markup=kbrd_second_filter)
            await state.set_state(Addtinal_components.confirm_exhaust_second_filter)
        else:
            kbrd_second_filter = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Так')], [KeyboardButton(text='Ні')]
                ], resize_keyboard=True
            )
            await message.answer('Потрібен фільтр другого ступеню витяжного повітря?', reply_markup=kbrd_second_filter)
            await state.set_state(Addtinal_components.confirm_exhaust_second_filter)
    elif message.text == 'Без фільтрів':
        await state.update_data(exhaust_first_filter=message.text)
        kbrd_automation = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Так')], [KeyboardButton(text='Ні')]
            ], resize_keyboard=True
        )
        await message.answer('Потрібна автоматика для установки?', reply_markup=kbrd_automation)
        await state.set_state(Addtinal_components.automation)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(Addtinal_components.confirm_supply_second_filter)
async def handle_confirm_supply_second_filter(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    data = await  state.get_data()
    if message.text == 'Так':
        await state.update_data(confirm_supply_second_filter=message.text)
        kbrd_filter = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Панельний G4'), KeyboardButton(text='Кишеньковий G4')],
                [KeyboardButton(text='M5'), KeyboardButton(text='F7')],
                [KeyboardButton(text='F8'), KeyboardButton(text='F9')],
                [KeyboardButton(text='Без фільтрів')]
            ], resize_keyboard=True
        )
        await message.answer('Виберіть фільтр другого ступеню припливного повітря', reply_markup=kbrd_filter)
        await state.set_state(Addtinal_components.supply_second_filter)
    elif message.text == 'Ні':
        await state.update_data(confirm_supply_second_filter=message.text)
        if data.get('type_ahu') == 'Припливна':
            kbrd_automation = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Так')], [KeyboardButton(text='Ні')]
                ], resize_keyboard=True
            )
            await message.answer('Потрібна автоматика для установки?', reply_markup=kbrd_automation)
            await state.set_state(Addtinal_components.automation)
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

@router.message(Addtinal_components.confirm_exhaust_second_filter)
async def handle_confirm_supply_second_filter(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text =='Так':
        await state.update_data(confirm_exhaust_second_filter=message.text)
        kbrd_filter = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Панельний G4'), KeyboardButton(text='Кишеньковий G4')],
                [KeyboardButton(text='M5'), KeyboardButton(text='F7')],
                [KeyboardButton(text='F8'), KeyboardButton(text='F9')]
            ], resize_keyboard=True
        )
        await message.answer('Виберіть фільтр другого ступеню витяжного повітря', reply_markup=kbrd_filter)
        await state.set_state(Addtinal_components.exhaust_second_filter)
    elif message.text == 'Ні':
        await state.update_data(confirm_exhaust_second_filter=message.text)
        kbrd_automation = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Так')], [KeyboardButton(text='Ні')]
            ], resize_keyboard=True
        )
        await message.answer('Потрібна автоматика для установки?', reply_markup=kbrd_automation)
        await state.set_state(Addtinal_components.automation)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(Addtinal_components.supply_second_filter)
async def handle_supply_second_filter(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text in ['Панельний G4', 'Кишеньковий G4', 'M5', 'F7', 'F8', 'F9']:
        await state.update_data(supply_second_filter=message.text)
        data = await state.get_data()
        if data.get('type_ahu') == 'Припливна':
            kbrd_automation = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Так')], [KeyboardButton(text='Ні')]
                ], resize_keyboard=True
            )
            await message.answer('Потрібна автоматика для установки?', reply_markup=kbrd_automation)
            await state.set_state(Addtinal_components.automation)
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
    elif message.text == 'Без фільтрів':
        await state.update_data(supply_second_filter=message.text)
        kbrd_filter = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Панельний G4'), KeyboardButton(text='Кишеньковий G4')],
                [KeyboardButton(text='M5'), KeyboardButton(text='F7')],
                [KeyboardButton(text='F8'), KeyboardButton(text='F9')],
            ], resize_keyboard=True
        )
        await message.answer('Виберіть фільтр першого ступеню витяжного повітря', reply_markup=kbrd_filter)
        await state.set_state(Addtinal_components.exhaust_first_filter)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(Addtinal_components.exhaust_second_filter)
async def handle_exhaust_second_filter(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text in ['Панельний G4', 'Кишеньковий G4', 'M5', 'F7', 'F8', 'F9']:
        await state.update_data(exhaust_second_filter=message.text)
        kbrd_automation = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Так')], [KeyboardButton(text='Ні')]
            ], resize_keyboard=True
        )
        await message.answer('Потрібна автоматика для установки?', reply_markup=kbrd_automation)
        await state.set_state(Addtinal_components.automation)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(Addtinal_components.automation)
async def handle_exhaust_second_filter(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text in ['Так', 'Ні']:
        await state.update_data(automation=message.text)
        kbrd_notes = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Немає приміток')]
            ], resize_keyboard=True
        )
        await message.answer('Якщо у Вас є примітки, запишіть їх або натисніть Немає приміток',
                             reply_markup=kbrd_notes)
        await state.set_state(Addtinal_components.notes)
    else:
        await message.answer('Виберіть з клавіатури')

@router.message(Addtinal_components.notes)
async def handle_notes(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    notes_text = message.text.strip()
    if not notes_text or notes_text.lower() == "немає приміток":
        notes_text = "немає"

    await state.update_data(notes=notes_text)
    data = await state.get_data()

    file_path = await generate_excel_file(data, message.from_user.id)
    await message.answer_document(FSInputFile(file_path), caption="Ось ваш заповнений файл ✅")
    kbrd_second_ahu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Так')], [KeyboardButton(text='Ні')]
        ], resize_keyboard=True
    )
    await message.answer('Потрібно заповнити опитувальний лист для іншої установки?', reply_markup=kbrd_second_ahu)
    await state.set_state(Addtinal_components.confirm_second_file)

@router.message(Addtinal_components.confirm_second_file)
async def handle_confirm_second_file(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    if message.text == 'Так':
        await state.update_data(confirm_second_file=message.text)
    elif message.text == 'Ні':
        await message.answer('Дякую! Якщо будуть ще проєкти — звертайтесь 🙂', reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        await message.answer('Виберіть з клавіатури')























