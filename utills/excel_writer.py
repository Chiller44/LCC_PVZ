from datetime import datetime
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
import openpyxl
from openpyxl.reader.excel import load_workbook


async def generate_excel_file(data: dict, user_id: int):
    installation = data.get('installation')
    frame = data.get('frame')
    recycling = data.get('recycling')
    type_ahu = data.get('type_ahu')
    recuperation = data.get('recuperation')
    type_glycol = data.get('type_glycol')
    percent_glycol = data.get('percent_glycol')
    percent_recycling = data.get('percent_recycling')
    temp_recycling = data.get('temp_recycling')
    winter_outside_temp = data.get('winter_outside_temp')
    winter_outside_humidity = data.get('winter_outside_humidity')
    summer_outside_temp = data.get('summer_outside_temp')
    summer_outside_humidity = data.get('summer_outside_humidity')
    winter_exhaust_temp = data.get('winter_exhaust_temp')
    winter_exhaust_humidity = data.get('winter_exhaust_humidity')
    summer_exhaust_temp = data.get('summer_exhaust_temp')
    summer_exhaust_humidity = data.get('summer_exhaust_humidity')
    winter_internal1_temp = data.get('winter_internal1_temp')
    winter_internal2_temp = data.get('winter_internal2_temp')
    summer_internal1_temp = data.get('summer_internal1_temp')
    summer_internal2_temp = data.get('summer_internal2_temp')
    supply_air = data.get('supply_air')
    exhaust_air = data.get('exhaust_air')
    supply_pressure = data.get('supply_pressure')
    exhaust_pressure = data.get('exhaust_pressure')
    valve = data.get('valve')
    supply_silence = data.get('supply_silence')
    exhaust_silence = data.get('exhaust_silence')
    supply_first_filter = data.get('supply_first_filter')
    exhaust_first_filter = data.get('exhaust_first_filter')
    supply_second_filter = data.get('supply_second_filter')
    exhaust_second_filter = data.get('exhaust_second_filter')
    confirm_supply_second_filter = data.get('confirm_supply_second_filter')
    confirm_exhaust_second_filter = data.get('confirm_exhaust_second_filter')
    automation = data.get('automation')
    heating1_type = data.get('heating1_type')
    heating2_type = data.get('heating2_type')
    heating1_param = data.get('heating1_param')
    heating2_param = data.get('heating2_param')
    heating1_percent_glycol = data.get('heating1_percent_glycol')
    heating2_percent_glycol = data.get('heating2_percent_glycol')
    cooling1_type = data.get('cooling1_type')
    cooling2_type = data.get('cooling2_type')
    confirm_heating2 = data.get('confirm_heating2')
    confirm_cooling2 = data.get('confirm_cooling2')
    cooling1_param = data.get('cooling1_param')
    cooling2_param = data.get('cooling2_param')
    cooling1_glycol = data.get('cooling1_glycol')
    cooling2_glycol = data.get('cooling2_glycol')
    cooling1_percent_glycol = data.get('cooling1_percent_glycol')
    cooling2_percent_glycol = data.get('cooling2_percent_glycol')
    freon1 = data.get('freon1')
    freon2 = data.get('freon2')
    notes = data.get('notes')

    wb = openpyxl.load_workbook("templates/ahu_template.xlsx")
    ws = wb.active

    ws['A16'] = '+' if installation == 'Внутрішня' else None
    ws['A17'] = '+' if installation == 'Наружна' else None

    ws['E16'] = '+' if frame == 'На рамі' else None
    ws['E17'] = '+' if frame == 'Без рами' else None

    ws['A49'] = '+' if recycling == 'Так' else None

    ws['I16'] = '+' if type_ahu == 'Припливна' else None
    ws['I17'] = '+' if type_ahu == 'Витяжна' else None
    ws['I18'] = '+' if type_ahu == 'Припливно-витяжна' else None

    ws['A51'] = '+' if recuperation == 'Гліколевий' else None
    ws['A53'] = '+' if recuperation == 'Пластинчатий' else None
    ws['A55'] = '+' if recuperation == 'Роторний' else None
    ws['A57'] = '+' if recuperation == 'Без нагрівача' else None

    ws['F51'] = type_glycol
    ws['K51'] = percent_glycol

    ws['F49'] = percent_recycling
    ws['K49'] = temp_recycling

    ws['F60'] = winter_outside_temp
    ws['H60'] = winter_outside_humidity
    ws['K60'] = summer_outside_temp
    ws['M60'] = summer_outside_humidity
    ws['F61'] = winter_exhaust_temp
    ws['H61'] = winter_exhaust_humidity
    ws['K61'] = summer_exhaust_temp
    ws['M61'] = summer_exhaust_humidity

    ws['F31'] = winter_internal1_temp
    ws['F35'] = winter_internal2_temp
    ws['F39'] = summer_internal1_temp
    ws['F44'] = summer_internal2_temp

    ws['G22'] = supply_air if type_ahu in ['Припливна', 'Припливно-витяжна'] else None
    ws['K22'] = exhaust_air if type_ahu in ['Витяжна', 'Припливно-витяжна'] else None
    ws['G23'] = supply_pressure if type_ahu in ['Припливна', 'Припливно-витяжна'] else None
    ws['K23'] = exhaust_pressure if type_ahu in ['Витяжна', 'Припливно-витяжна'] else None

    ws['G25'] = '+' if valve == 'Так' else None
    ws['I25'] = '+' if valve == 'Ні' else None
    ws['G64'] = supply_silence if (supply_silence in ['910', '1090', '1390', '1600']
                                   and type_ahu in ['Припливна', 'Припливно-витяжна']) else None
    ws['N64'] = exhaust_silence if (supply_silence in ['910', '1090', '1390', '1600']
                                   and type_ahu in ['Витяжна', 'Припливно-витяжна']) else None
    ws['G28'] = supply_first_filter if (supply_first_filter in ['Панельний G4', 'Кишеньковий G4', 'M5', 'F7', 'F8', 'F9']
                                    and type_ahu in ['Припливна', 'Припливно-витяжна']) else None
    ws['M28'] = exhaust_first_filter if (exhaust_first_filter in ['Панельний G4', 'Кишеньковий G4', 'M5', 'F7', 'F8', 'F9']
                                    and type_ahu in ['Витяжна', 'Припливно-витяжна']) else None
    ws['G29'] = supply_second_filter if (confirm_supply_second_filter == 'Так' and
                supply_second_filter in ['Панельний G4', 'Кишеньковий G4', 'M5', 'F7', 'F8', 'F9']
                and type_ahu in ['Припливна', 'Припливно-витяжна']) else None
    ws['M29'] = exhaust_second_filter if (confirm_exhaust_second_filter == 'Так' and
                                          exhaust_second_filter in ['Панельний G4', 'Кишеньковий G4', 'M5', 'F7', 'F8',
                                                                   'F9']
                                          and type_ahu in ['Витяжна', 'Припливно-витяжна']) else None

    ws['E67'] = '+' if automation == 'Так' else None
    ws['E68'] = '+' if automation == 'Ні' else None

    ws['N31'] = '+' if heating1_type == 'Водяний' and type_ahu in ['Припливна', 'Припливно-витяжна'] else None
    ws['N32'] = '+' if heating1_type == 'Електричний' and type_ahu in ['Припливна', 'Припливно-витяжна'] else None
    ws['N35'] = '+' if (heating2_type == 'Водяний' and type_ahu in ['Припливна', 'Припливно-витяжна']
                        and confirm_heating2 == 'Так') else None
    ws['N36'] = '+' if (heating2_type == 'Електричний' and type_ahu in ['Припливна', 'Припливно-витяжна']
                        and confirm_heating2 == 'Так') else None

    ws['F32'] = heating1_param if (heating1_type == 'Водяний'
                                   and type_ahu in ['Припливна', 'Припливно-витяжна']) else None
    ws['F36'] = heating2_param if (heating2_type == 'Водяний'
                                   and confirm_heating2 == 'Так'
                                   and type_ahu in ['Припливна','Припливно-витяжна']) else None
    ws['F33'] = heating1_percent_glycol if (heating1_type == 'Водяний'
                                            and type_ahu in ['Припливна','Припливно-витяжна']) else None
    ws['F37'] = heating2_percent_glycol if (heating2_type == 'Водяний' and confirm_heating2 == 'Так'
                                            and type_ahu in ['Припливна', 'Припливно-витяжна']) else None

    ws['N39'] = '+' if cooling1_type == 'Водяний' and type_ahu in ['Припливна', 'Припливно-витяжна'] else None
    ws['N40'] = '+' if cooling1_type == 'Фреоновий' and type_ahu in ['Припливна', 'Припливно-витяжна'] else None
    ws['N44'] = '+' if (cooling2_type == 'Водяний' and type_ahu in ['Припливна', 'Припливно-витяжна']
                        and confirm_cooling2 == 'Так') else None
    ws['N45'] = '+' if (cooling2_type == 'Фреоновий' and type_ahu in ['Припливна', 'Припливно-витяжна']
                        and confirm_cooling2 == 'Так') else None

    ws['F40'] = cooling1_param if cooling1_type == 'Водяний' and type_ahu in ['Припливна',
                                                                              'Припливно-витяжна'] else None
    ws['F45'] = cooling2_param if (cooling2_type == 'Водяний'
                                   and type_ahu in ['Припливна', 'Припливно-витяжна']
                                   and confirm_cooling2 == 'Так') else None

    if cooling1_type == 'Водяний' and type_ahu in ['Припливна', 'Припливно-витяжна']:
        ws['F42'] = cooling1_glycol
    elif cooling1_type == 'Фреоновий' and type_ahu in ['Припливна', 'Припливно-витяжна']:
        ws['F42'] = freon1

    if cooling2_type == 'Водяний' and type_ahu in ['Припливна', 'Припливно-витяжна'] and confirm_cooling2 == 'Так':
        ws['F47'] = cooling2_glycol
    elif cooling2_type == 'Фреоновий' and type_ahu in ['Припливна', 'Припливно-витяжна'] and confirm_cooling2 == 'Так':
        ws['F47'] = freon2

    ws['F41'] = cooling1_percent_glycol if (cooling1_type == 'Водяний'
                                    and type_ahu in ['Припливна', 'Припливно-витяжна']) else None
    ws['F46'] = cooling2_percent_glycol if (cooling2_type == 'Водяний'
                                            and type_ahu in ['Припливна', 'Припливно-витяжна']
                                            and confirm_cooling2 == 'Так') else None

    ws['D73'] = notes

    timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    filename = f"output/{user_id}_{timestamp}_filled.xlsx"
    wb.save(filename)

    return filename

















