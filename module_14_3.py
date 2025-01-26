from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = types.KeyboardButton(text='Рассчитать')
button_2 = types.KeyboardButton(text='Информация')
button_3 = types.KeyboardButton(text='Купить')  # Добавляем кнопку "Купить"
kb.add(button_1, button_2, button_3)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    print('Привет! Я бот, помогающий твоему здоровью.')
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def set_age(message: types.Message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(text='Информация')
async def inform(message: types.Message):
    await message.answer('Здесь будет информация о здоровье.')


@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    products = [
        {'name': 'Product1', 'description': 'Описание 1', 'price': 100, 'image': 'files/1.jpg'},
        {'name': 'Product2', 'description': 'Описание 2', 'price': 200, 'image': 'files/2.jpg'},
        {'name': 'Product3', 'description': 'Описание 3', 'price': 300, 'image': 'files/3.jpg'},
        {'name': 'Product4', 'description': 'Описание 4', 'price': 400, 'image': 'files/4.jpg'},
    ]

    for product in products:
        await message.answer(
            f'Название: {product['name']} | Описание: {product['description']} | Цена: {product['price']}₽'
        )
        await message.answer_photo(photo=open(product['image'], 'rb'))

    inline_kb = types.InlineKeyboardMarkup(row_width=len(products))
    buttons = []
    for product in products:
        button = types.InlineKeyboardButton(text=product['name'], callback_data='product_buying')
        buttons.append(button)
    inline_kb.add(*buttons)

    await message.answer('Выберите продукт для покупки:', reply_markup=inline_kb)


@dp.callback_query_handler(lambda call: call.data == 'product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer('Вы успешно приобрели продукт!')


@dp.message_handler(state=UserState.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def process_growth(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def process_weight(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)

    user_data = await state.get_data()
    age = int(user_data['age'])
    growth = int(user_data['growth'])
    weight = int(user_data['weight'])

    calories = 10 * weight + 6.25 * growth - 5 * age + 5

    await message.answer(f'Ваша норма калорий: {calories:.2f} ккал')
    await state.finish()


@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



