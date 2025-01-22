from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import re
from crud_functions import *

api = '7269628965:AAH2Et-1chdUtKhxHctaTdXkBxEhCuYwjpo'
bot = Bot(token=api)
dp = Dispatcher(bot, storage = MemoryStorage())
#Клавиатуры-------------------------------------------------------------------------------------------------------------
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_calculate = KeyboardButton(text= 'Рассчитать')
button_info = KeyboardButton(text= 'Информация')
button_shop = KeyboardButton(text = 'Купить')
button_register = KeyboardButton(text= 'Регистрация')
kb.add(button_calculate,button_info)
kb.add(button_shop)
kb.add(button_register)
#Для расчёта калорий----------------------------------------------------------------------------------------------------
in_kb = InlineKeyboardMarkup()
button_rkn = InlineKeyboardButton(text= 'Рассчитать норму калорий', callback_data= 'calories')
button_fc = InlineKeyboardButton(text= 'Формула расчёта', callback_data= 'formulas')
in_kb.row(button_rkn,button_fc)

f_c = InlineKeyboardMarkup()
but_men = InlineKeyboardButton(text= 'мужчин', callback_data= 'men')
but_women = InlineKeyboardButton(text= 'женщин', callback_data= 'women')
f_c.row(but_men, but_women)

@dp.message_handler(text= 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup= in_kb)

@dp.callback_query_handler(text= 'calories')
async def formulas_choice(call):
    await call.message.answer('Рассчитать для:', reply_markup= f_c)
    await call.answer()

#Для покупок------------------------------------------------------------------------------------------------------------
in_shop = InlineKeyboardMarkup()
but_1 = InlineKeyboardButton(text = 'Продукт1', callback_data= 'product_baying')
but_2 = InlineKeyboardButton(text = 'Продукт2', callback_data= 'product_baying')
but_3 = InlineKeyboardButton(text = 'Продукт3', callback_data= 'product_baying')
but_4 = InlineKeyboardButton(text = 'Продукт4', callback_data= 'product_baying')
in_shop.row(but_1, but_2, but_3, but_4)

users = get_all_products()

@dp.message_handler(text= 'Купить')
async def get_buying_list(message):

    with open('photo/ph1.jpg','rb') as img:
        await message.answer_photo(img,
            caption= f'Название: {users[0][0]} | Описание: {users[0][1]} | {users[0][2]}')

    with open('photo/ph2.jpg','rb') as img:
        await message.answer_photo(img,
            caption= f'Название: {users[1][0]} | Описание: {users[1][1]} | {users[1][2]}')

    with open('photo/ph3.jpg','rb') as img:
        await message.answer_photo(img,
            caption= f'Название: {users[2][0]} | Описание: {users[2][1]} | {users[2][2]}')

    with open('photo/ph4.jpg','rb') as img:
        await message.answer_photo(img,
            caption= f'Название: {users[3][0]} | Описание: {users[3][1]} | {users[3][2]}')

    await message.answer('Выберите продукт для покупки:', reply_markup= in_shop)

@dp.callback_query_handler(text= 'product_baying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
#-----------------------------------------------------------------------------------------------------------------------

#Формулы расчета калорий------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text= 'formulas')
async def get_formulas(call):
    await call.message.answer(
        '• Формула Миффлина-Сан Жеора для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5\n'
        '• Формула Миффлина-Сан Жеора для женщин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) - 161')
    await call.answer()
#Для женщин-------------------------------------------------------------------------------------------------------------
class UserStateW(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text= 'women')
async def set_age_w(call):
    print('Введите свой возраст:')
    await call.message.answer('Введите свой возраст:')
    await UserStateW.age.set()
    await call.answer()

@dp.message_handler(state= UserStateW.age)
async def set_group_w(message, state):
    await state.update_data(age = message.text)
    data = await state.get_data()

    print('Введите свой рост:')
    await message.answer('Введите свой рост:')
    await UserStateW.growth.set()

@dp.message_handler(state= UserStateW.growth)
async def set_weight_w(message, state):
    await state.update_data(growth= message.text)
    data = await state.get_data()
    print('Введите свой вес:')
    await message.answer('Введите свой вес:')
    await UserStateW.weight.set()

@dp.message_handler(state= UserStateW.weight)
async def send_calories_w(message, state):
    try:
        await state.update_data(weight=message.text)
        data = await state.get_data()
        cal = 10*int(data['weight']) + 6.25*int(data['growth']) - 5*int(data['age']) - 161
        await message.answer(f'{message.from_user.first_name} ваше необходимое количество ккал: {cal}')
    except ValueError:
        await message.answer('Данные не верны.\n'
         'Нажмите "Рассчитать" и введите данные снова.')

    await state.finish()

#Для Мужчин-------------------------------------------------------------------------------------------------------------
class UserStateM(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text= 'men')
async def set_age_m(call):
    print('Введите свой возраст:')
    await call.message.answer('Введите свой возраст:')
    await UserStateM.age.set()
    await call.answer()

@dp.message_handler(state= UserStateM.age)
async def set_group_m(message, state):
    await state.update_data(age = message.text)
    data = await state.get_data()
    print('Введите свой рост:')
    await message.answer('Введите свой рост:')
    await UserStateM.growth.set()

@dp.message_handler(state= UserStateM.growth)
async def set_weight_m(message, state):
    await state.update_data(growth= message.text)
    data = await state.get_data()
    print('Введите свой вес:')
    await message.answer('Введите свой вес:')
    await UserStateM.weight.set()

@dp.message_handler(state= UserStateM.weight)
async def send_calories_m(message, state):
    try:
        await state.update_data(weight=message.text)
        data = await state.get_data()
        cal = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
        await message.answer(f'{message.from_user.first_name} ваше необходимое количество ккал: {cal}')
    except ValueError:
        await message.answer('Данные не верны.\n'
                             'Нажмите "Рассчитать" и введите данные снова.')

    await state.finish()
#-----------------------------------------------------------------------------------------------------------------------

#Регистрация------------------------------------------------------------------------------------------------------------
class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000

@dp.message_handler(text= 'Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит): ')
    await RegistrationState.username.set()

@dp.message_handler(state= RegistrationState.username)
async def set_username(message, state):

    if re.search(r'[^a-zA-Z]', message.text):
        await message.answer('Только латинский алфавит!')
        await RegistrationState.username.set()
    elif is_included(message.text) == True:
        await RegistrationState.username.set()
        await message.answer('Пользователь существует, введите другое имя')
    else:
        await state.update_data(username=message.text)
        data = await state.get_data()
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()




@dp.message_handler(state= RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    data = await state.get_data()
    if '@' not in data['email']:
        await message.answer('Неверная почта. Введите заново')
        await RegistrationState.email.set()
    else:
        await message.answer('Введите свой возраст')
        await RegistrationState.age.set()


@dp.message_handler(state= RegistrationState.age)
async def set_age(message,state):
    await state.update_data(age= message.text)
    data= await state.get_data()
    if data['age'] != int:
        await message.answer('Неверные данные. Введите заново')
        await RegistrationState.age.set()
    username = data['username']
    email = data['email']
    age = data['age']

    add_user(username, email, age)
    await message.answer('Регистрaция прошла успешно!')
    await state.finish()




#-----------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands= 'start')
async def start(message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup= kb)

@dp.message_handler()
async def all_massage(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
