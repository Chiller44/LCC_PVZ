from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from common import send_start
from status import Contact_info, Airform

router = Router()

@router.message(F.text=='Почнемо')
async def start_name(message: Message, state: FSMContext):
    await message.answer("Будь ласка, введіть ім'я контактної особи", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Contact_info.contact_name)

@router.message(Contact_info.contact_name)
async def contact_name(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    name_contact = message.text
    await state.update_data(contact_name=name_contact)
    await message.answer('Введіть номер телефону контактної особи')
    await state.set_state(Contact_info.contact_phone)

@router.message(Contact_info.contact_phone)
async def contact_phone(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    phone_contact = message.text
    await state.update_data(contact_phone=phone_contact)
    await message.answer('Введіть назву організації контактної особи')
    await state.set_state(Contact_info.organization)

@router.message(Contact_info.organization)
async def organization(message: Message, state: FSMContext):
    if message.text == "/start":
        await send_start(message, state)
        return
    organization_contact = message.text
    await state.update_data(organization=organization_contact)
    await message.answer('Дякую за надану інформацію.')
    await message.answer('Почнемо з параметрів зовнішнього повітря.\n'
                         'Введіть зимову температуру зовнішнього повітря, °C')
    await state.set_state(Airform.winter_outside_temp)