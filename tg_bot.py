import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types, Router

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import TOKEN, user_id
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from parser import check_cars_update, get_parser_av_filters
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters.command import Command


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()
form_router = Router()

class Form(StatesGroup):
    get_min_year = State()
    get_max_price = State()


@dp.message(Command("start" ))
async def start(message: types.Message):
    start_buttons = [
        [KeyboardButton(text='Описание бота')],
        [KeyboardButton(text='Все объявления')],
        [KeyboardButton(text='Новые объявления')],
        [KeyboardButton(text='Фильтр')]

    ]
    keyboard = ReplyKeyboardMarkup(keyboard=start_buttons,resize_keyboard=True)
    logging.info(f"Бот запущен: {message.text}")
    await message.answer('Лента объявлений', reply_markup=keyboard)


@dp.message(lambda message: message.text and "Описание" in message.text)
async def about_bot(message: types.Message):
    response_ = 'Бот делает выборку машин по заранее определенному фильтру,' \
                'год машины от 2014г и стоимость авто до 4500 $, а так же можно указать свой фильтр для поиска'
    await message.answer(response_)


@dp.message(lambda message: message.text and "Все объявления" in message.text, state="*")
async def get_all_cars(message: types.Message, state: FSMContext):
    await state.clear()
    with open('pars_avby.json', 'r', encoding='utf-8') as file:
        cars_dict = json.load(file)
    print(cars_dict)
    response_ = 'Бот делает выборку машин по заранее определенному фильтру,' \
                'год машины от 2014г и стоимость авто до 4500 $'
    await message.answer(response_)
    for k, v in cars_dict.items():
        car_url = v.get("car_url", "URL не указан")
        car_about_title = v.get("car_about_title", "Название не указано")
        car_params = v.get("car_params", "Параметры не указаны")
        car_price_by = v.get("car_price_by", "Цена в BY не указана")
        car_price_usd = v.get("car_price_usd", "Цена в USD не указана")
        car_info = v.get("car_info", "Информация не указана")

        cars_message = (
            f'<b>URL:</b> {hlink(car_about_title, car_url)}\n'
            f'<b>Название:</b> {hunderline(car_about_title)}\n'
            f'<b>Параметры:</b> {hcode(car_params)}\n'
            f'<b>Цена (BY):</b> {hbold(car_price_by)}\n'
            f'<b>Цена (USD):</b> {hbold(car_price_usd)}\n'
            f'<b>Информация:</b> {hcode(car_info)}\n'
        )

        await message.answer(cars_message, parse_mode=ParseMode.HTML)
        await asyncio.sleep(1)  # Задержка между отправкой сообщений, чтобы избежать лимитов


@dp.message(lambda message: message.text and "Фильтр"in message.text, state="*")
async def filer_car(message: types.Message,  state: FSMContext):
    await state.clear()
    instruction_text = (
        "Инструкция по использованию фильтра:\n"
        "1. Выберите минимальный год выпуска автомобиля.\n"
        "2. Укажите максимальную цену в USD.\n"
    )
    await message.answer(instruction_text)
    await asyncio.sleep(3)
    try:

        await message.answer("Введите минимальный год выпуска:")
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число для года выпуска.")
    await state.set_state(Form.get_min_year)


# Обработчик для получения минимального года выпуска
@dp.message(Form.get_min_year)
async def get_min_year(message: types.Message, state: FSMContext):
    try:
        min_year = int(message.text)
        if 1900 <= min_year <= 2100:
            await state.update_data(min_year=min_year)
            await message.answer("Введите максимальную цену в USD:")
            await state.set_state(Form.get_max_price)  # Переход к следующему состоянию
        else:
            await message.answer("Пожалуйста, введите четырехзначное число для года выпуска (например, 2023).")
    except ValueError:
        logging.error(f"Ошибка преобразования года выпуска: {message.text}")
        await message.answer("Пожалуйста, введите корректное число для года выпуска.")


@dp.message(Form.get_max_price)
async def get_max_price(message: types.Message, state: FSMContext):
    try:
        logging.debug(f"Получен ввод для максимальной цены: {message.text}")
        max_price = int(message.text)
        if max_price <= 0:
            await message.answer("Пожалуйста, введите корректное число для максимальной цены.")
            return

        user_data = await state.get_data()
        min_year = user_data['min_year']
        logging.debug(f"Фильтры: год выпуска - {min_year}, максимальная цена - {max_price}")
        parser_response = get_parser_av_filters(min_year, max_price)

        if not parser_response:
            await message.answer("Не найдено объявлений, соответствующих указанным параметрам.")
            return

        # with open('pars_avby_filter.json', 'r', encoding='utf-8') as file:
        #     cars_dict = json.load(file)



        response_finished = len(parser_response)
        await message.answer(f'Всего найдено объявлений: {response_finished}')

        for k, v in parser_response.items():
            car_url = v.get("car_url", "URL не указан")
            car_about_title = v.get("car_about_title", "Название не указано")
            car_params = v.get("car_params", "Параметры не указаны")
            car_price_by = v.get("car_price_by", "Цена в BY не указана")
            car_price_usd = v.get("car_price_usd", "Цена в USD не указана")
            car_info = v.get("car_info", "Информация не указана")

            cars_message = (
                f'<b>URL:</b> {hlink(car_about_title, car_url)}\n'
                f'<b>Название:</b> {hunderline(car_about_title)}\n'
                f'<b>Параметры:</b> {hcode(car_params)}\n'
                f'<b>Цена (BY):</b> {hbold(car_price_by)}\n'
                f'<b>Цена (USD):</b> {hbold(car_price_usd)}\n'
                f'<b>Информация:</b> {hcode(car_info)}\n'
            )
            await message.answer(cars_message, parse_mode=ParseMode.HTML)
            await asyncio.sleep(1)


        await state.clear()  # Завершение состояния после обработки

    except ValueError:
        logging.error(f"Ошибка преобразования цены: {message.text}")
        await message.answer("Пожалуйста, введите корректное число для цены.")


@dp.message(lambda message: message.text and "Новые объявления" in message.text, state="*")
async def get_fresh_cars(message: types.Message, state: FSMContext):
    await state.clear()
    fresh_cars = check_cars_update()
    if len(fresh_cars) >= 1:
        await bot.send_message(user_id, f'Найдено новых объявлений: {len(fresh_cars)}')
        for k, v in fresh_cars.items():
            car_url = v.get("car_url", "URL не указан")
            car_about_title = v.get("car_about_title", "Название не указано")
            car_params = v.get("car_params", "Параметры не указаны")
            car_price_by = v.get("car_price_by", "Цена в BY не указана")
            car_price_usd = v.get("car_price_usd", "Цена в USD не указана")
            car_info = v.get("car_info", "Информация не указана")

            cars_message = (
                f'<b>URL:</b> {hlink(car_about_title, car_url)}\n'
                f'<b>Название:</b> {hunderline(car_about_title)}\n'
                f'<b>Параметры:</b> {hcode(car_params)}\n'
                f'<b>Цена (BY):</b> {hbold(car_price_by)}\n'
                f'<b>Цена (USD):</b> {hbold(car_price_usd)}\n'
                f'<b>Информация:</b> {hcode(car_info)}\n'
            )
            await message.answer(cars_message, parse_mode=ParseMode.HTML)
            await asyncio.sleep(1)  # Задержка между отправкой сообщений, чтобы избежать лимитов

    else:
        await message.answer('Пока нет свежий объявлений')


async def check_update_cars():
    while True:
        fresh_cars = check_cars_update()

        if len(fresh_cars) >= 1:
            await bot.send_message(user_id, f'Найдено новых объявлений: {len(fresh_cars)}')

            for k, v in fresh_cars.items():
                car_url = v.get("car_url", "URL не указан")
                car_about_title = v.get("car_about_title", "Название не указано")
                car_params = v.get("car_params", "Параметры не указаны")
                car_price_by = v.get("car_price_by", "Цена в BY не указана")
                car_price_usd = v.get("car_price_usd", "Цена в USD не указана")
                car_info = v.get("car_info", "Информация не указана")

                cars_message = (
                    f'<b>URL:</b> {hlink(car_about_title, car_url)}\n'
                    f'<b>Название:</b> {hunderline(car_about_title)}\n'
                    f'<b>Параметры:</b> {hcode(car_params)}\n'
                    f'<b>Цена (BY):</b> {hbold(car_price_by)}\n'
                    f'<b>Цена (USD):</b> {hbold(car_price_usd)}\n'
                    f'<b>Информация:</b> {hcode(car_info)}\n'
                )
                await bot.send_message(user_id,cars_message, parse_mode=ParseMode.HTML, disable_notification=True)
                await asyncio.sleep(1)  # Задержка между отправкой сообщений, чтобы избежать лимитов
        else:
            await bot.send_message(user_id, 'Пока нет свежий объявлений', disable_notification=True)
        await asyncio.sleep(600)


@dp.message()
async def unknow_message(message:types.Message):
    await message.answer("Извините, я не понимаю эту команду. Пожалуйста, выберите одну из опций на клавиатуре.")


async def main():
    await asyncio.gather(
        dp.start_polling(bot),
        check_update_cars()
    )

if __name__ == "__main__":
    asyncio.run(main())