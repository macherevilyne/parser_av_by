import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types
from config import token, user_id
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from parser import check_cars_update
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters.command import Command


logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    start_buttons = [
        [KeyboardButton(text='Все объявления')],
        [KeyboardButton(text='Новые объявления')],
        [KeyboardButton(text='Описание бота')],
        [KeyboardButton(text='Фильтр')]

    ]
    keyboard = ReplyKeyboardMarkup(keyboard=start_buttons,resize_keyboard=True)
    await message.answer('Лента объявлений', reply_markup=keyboard)

@dp.message(lambda message: message.text and "Описание" in message.text)
async def about_bot(message: types.Message):
    response_ = 'Бот делает выборку по заранее определенному фильтру машин, а так же можно указать свой фильтр для поиска'
    await message.answer(response_)


@dp.message(lambda message: message.text and "Все объявления по фильтру:год машины от 2014, стоимость машины"
                                             "до 4500$ " in message.text)
async def get_all_cars(message: types.Message):
    with open('pars_avby.json', 'r', encoding='utf-8') as file:
        cars_dict = json.load(file)
    print(cars_dict)
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


@dp.message(lambda message: message.text and "Фильтр"in message.text)
async def filer_car(message: types.Message):
    instruction_text = (
        "Инструкция по использованию фильтра:\n"
        "1. Выберите минимальный год выпуска автомобиля.\n"
        "2. Укажите максимальную цену в USD.\n"
        "3. Нажмите кнопку 'Применить фильтр', чтобы увидеть результаты.\n\n"
        "Пример команды:\n"
        "/filter year_min=2014 price_max=4500"
    )
    await message.answer(instruction_text)










@dp.message(lambda message: message.text and "Новые объявления" in message.text)
async def get_fresh_cars(message: types.Message):
    fresh_cars = check_cars_update()
    if len(fresh_cars) >= 1:
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

@dp.message(lambda message: message.text and "" in message.text)
async def get_fresh_cars(message: types.Message):
    fresh_cars = check_cars_update()
    if len(fresh_cars) >= 1:
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



async def news_car_every_hour():
    while True:
        fresh_cars = check_cars_update()
        if len(fresh_cars) >= 1:
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
        await asyncio.sleep(3600)

async def main():
    await asyncio.gather(
        dp.start_polling(bot),
        news_car_every_hour()
    )

if __name__ == "__main__":
    asyncio.run(main())