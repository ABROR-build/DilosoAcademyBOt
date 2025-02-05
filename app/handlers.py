from aiogram import F, Router
from aiogram import Bot, Dispatcher

from config import TOKEN
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from . import keyboard
from . import database

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()
bot = Bot(token=TOKEN)


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
    # Retrieve the collected data
    user_data = await state.get_data()
    fullname = user_data['fullname']
    age = user_data['age']
    telephone_number = user_data['telephone_number']
    username = message.from_user.username
    user_id = message.from_user.id

    # Insert the data into the database
    database.cursor.execute('''
            INSERT INTO users (fullname, username, user_id, age, telephone_number, is_confirmed, is_admin)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (fullname, username, user_id, age, telephone_number, False, False))

    database.database.commit()

    print(user_data)
    await state.clear()
    await message.answer("Ro'yxatdan o'tganingiz uchun rahmat!\n"
                         "agar kursga qiziqqan bo'lsangiz - 9860 6004 1828 0771\n"
                         "karta raqamiga 200 ming kurs to'lovini jo'natishingizni\n"
                         "va undan keyin to'lov chekini yuborishingizni\n"
                         "so'rab qolamiz")


# payment
@router.message(F.photo)
async def get_and_send_photo(message: Message):
    database.cursor.execute('SELECT * FROM users WHERE is_admin = 1')
    admin_users = database.cursor.fetchall()

    admins = {}
    admin_user_ids = []

    for user in admin_users:
        admins[user[0]] = {
            'fullname': user[1],
            'username': user[2],
            'user_id': user[3],
            'age': user[4],
            'telephone_number': user[5],
            'is_confirmed': user[6],
            'is_admin': user[7]
        }

    for individual_dict_key, individual_dict_value in admins.items():
        for column in individual_dict_value:
            if column == 'user_id':
                admin_user_ids.append(individual_dict_value[column])

    print(admin_user_ids)

    await message.answer('Adminlar tasdiqlashini kutishingizni soraymiz')

    photo_file_id = message.photo[-1].file_id
    for admin_id in admin_user_ids:
        await bot.send_photo(admin_id, photo_file_id)



