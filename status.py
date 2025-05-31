from aiogram.fsm.state import StatesGroup, State


class AHUform(StatesGroup):
    installation = State()
    frame = State()
    recycling = State()
    type_ahu = State()
    recuperation = State()
    type_glycol = State()
    percent_glycol = State()
    percent_recycling = State()
    temp_recycling = State()


class Airform(StatesGroup):
    winter_outside_temp = State()
    winter_outside_humidity = State()
    winter_internal1_temp = State()
    winter_internal2_temp = State()
    summer_outside_temp = State()
    summer_outside_humidity = State()
    summer_internal1_temp = State()
    summer_internal2_temp = State()
    winter_exhaust_temp = State()
    winter_exhaust_humidity = State()
    summer_exhaust_temp = State()
    summer_exhaust_humidity = State()
    confirm = State()

class Exchangerform(StatesGroup):
    heating1_type = State()
    heating1_param = State()
    heating1_percent_glycol = State()
    confirm_heating2 = State()
    heating2_type = State()
    heating2_param = State()
    heating2_percent_glycol = State()
    cooling1_type = State()
    cooling1_param = State()
    confirm_cooling2 = State()
    cooling1_glycol = State()
    cooling1_percent_glycol = State()
    cooling2_type = State()
    cooling2_param = State()
    cooling2_glycol = State()
    cooling2_percent_glycol = State()
    freon1 = State()
    freon2 = State()

class Param_airform(StatesGroup):
    supply_air = State()
    exhaust_air = State()
    supply_pressure = State()
    exhaust_pressure = State()

class Addtinal_components(StatesGroup):
    valve = State()
    supply_silence = State()
    exhaust_silence = State()
    supply_first_filter = State()
    confirm_supply_second_filter = State()
    exhaust_first_filter = State()
    supply_second_filter = State()
    exhaust_second_filter = State()
    confirm_exhaust_second_filter = State()
    automation = State()
    notes = State()
    confirm_second_file = State()




