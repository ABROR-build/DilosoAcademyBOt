from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from . import keyboard
from . import database


from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()


# greeting
@router.message(CommandStart())
async def command_start(message: Message):
    content_url = 'https://t.me/solo_build/322'
    await message.answer_video(
        video=content_url,
        caption=f'Assalomu alyekum {message.from_user.first_name}\n'
                f"Bu kosmetologiya kursimiz kursmiz haqida ma'lumot quyidagicha:\n"
                f"Kursimiz 1 oyga mo'ljallangan bo'lib u kosmetologlarning\n"
                f"saloyihatini oshirishga qaratilgan\n"
                f"Agar taklifimiz sizni qiziqtirsa ro'yxatdan o'tish tugmasini bosing",
        reply_markup=keyboard.register_keyboard
    )


# registration
class Registration(StatesGroup):
    full_name = State()
    age = State()
    telephone_number = State()


@router.callback_query(lambda c: c.data == 'registration')
async def start_register(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Registration.full_name)
    await callback_query.message.answer("To'liq ism va familiyangizni kiriting")


@router.message(Registration.full_name)
async def registering_full_name(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await state.set_state(Registration.age)
    await message.answer("Ajoyib endi yoshingizni kiriting")


@router.message(Registration.age)
async def registering_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Registration.telephone_number)
    await message.answer('''Oxirgi qadam endi telefon raqamingizni "+998906667799" ko'rinishida kiriting''')


@router.message(Registration.telephone_number)
async def registering_telephone_number(message: Message, state: FSMContext):
    await state.update_data(telephone_number=message.text)
    data = await state.get_data()
    print(data)
    # Retrieve the collected data
    user_data = await state.get_data()
    fullname = user_data['fullname']
    age = user_data['age']
    telephone_number = user_data['telephone_number']


    # Insert the data into the database
    database.cursor.execute('''
            INSERT INTO users (fullname, age, telephone_number, is_confirmed, is_admin)
            VALUES (?, ?, ?, ?, ?)
        ''', (fullname, age, telephone_number, False, False))

    database.database.commit()

    await message.answer('Registration completed!')

