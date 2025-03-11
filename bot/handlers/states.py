from aiogram.filters.state import State, StatesGroup

class Form(StatesGroup):
    get_admin_tg_id = State()
    get_admin_full_name = State()
    send_message = State()
    choose_language = State()
    edit_language = State()
    get_token_file = State()
    get_branch_name_en = State()  # Ingliz tilidagi nom
    get_branch_name_ru = State()  # Rus tilidagi nom
    get_branch_address = State()  # Manzil
    get_branch_phone = State()
    get_branch_instagram_choice = State()
    get_branch_instagram_link = State()
    get_branch_hours = State()
    get_branch_location = State()