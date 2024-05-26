import requests
from bs4 import BeautifulSoup
import json

def get_parser_av():
    url = 'https://cars.av.by/filter?year[min]=2014&price_usd[max]=4500'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    # Инициализируем счетчик
    count = 0
    cars_dict = {}
    while True:

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        print(response)

        # Находим контейнер с объявлениями
        listing_items_container = soup.find('div', class_='listing__items')
        # print(listing_items_container, 'listing')

        if listing_items_container is None:
            print("None listing")
            print("Unable to find the 'listing-items' element.")
            print("Response content:")
            print(response.content)  # Печать полученного HTML-контента для отладки
            return []
        car_elements = listing_items_container.find_all('div', class_='listing-item')
        # print(car_elements, 'car_elem')

        # Выводим информацию об объявлениях
        for car in car_elements:
            count += 1
            car_about_title = car.find('h3', class_='listing-item__title').text.strip()
            car_url = f"https://cars.av.by{car.find('h3', class_='listing-item__title').find('a')['href']}"
            cars_id = car_url.split('/')[-1]
            cars_id = cars_id[::]
            # print(cars_id, 'cars_id')
            car_params = car.find('div', class_='listing-item__params').text.strip()
            car_price_by = car.find('div', class_='listing-item__price').text.strip()
            car_price_usd =car.find('div', class_='listing-item__priceusd').text.strip()
            car_info = car.find('div', class_='listing-item__location').text.strip()
            # print(f'{car_url} | '
            #       f'{car_about_title} | '
            #       f'{car_params} |'
            #       f' {car_price_by} | '
            #       f' {car_price_usd} | '
            #       f' {car_info}')

            cars_dict[cars_id] = {'car_url': car_url,
                                      'car_about_title':car_about_title,
                                  'car_params':car_params,
                                  'car_price_by':car_price_by,
                                  'car_price_usd': car_price_usd,
                                  'car_info':car_info
            }
            # print(cars_dict, 'cars_dict')
        print("Количество объектов:", len(cars_dict))
        # Проверяем наличие кнопки "Показать ещё"
        next_button = soup.find('a', class_='button--default', string='Показать ещё')
        if next_button:
            url = 'https://cars.av.by' + next_button['href']
        else:
            break  # Выходим из цикла, если кнопки "Показать ещё" больше нет
        print(f'Спарсировано объявлений: {count}')


    with open ('pars_avby.json', 'w', encoding='utf-8') as file:
        json.dump(cars_dict, file, indent=4, ensure_ascii=False)

get_parser_av()



def check_cars_update():
    fresh_cars = {}
    with open('pars_avby.json', 'r', encoding='utf-8') as file:
        cars_dict = json.load(file)
        # print(cars_dict, 'cars_dict')

    url = 'https://cars.av.by/filter?year[min]=2014&price_usd[max]=4500'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    # Находим контейнер с объявлениями
    listing_items_container = soup.find('div', class_='listing__items')
    if listing_items_container is None:
        print("None listing")
        print("Unable to find the 'listing-items' element.")
        print("Response content:")
        print(response.content)  # Печать полученного HTML-контента для отладки
        return []
    car_elements = listing_items_container.find_all('div', class_='listing-item')

    for car in car_elements:
        car_url = f"https://cars.av.by{car.find('h3', class_='listing-item__title').find('a')['href']}"
        cars_id = car_url.split('/')[-1]
        cars_id = cars_id[::]
        if cars_id in cars_dict:
            continue
        else:
            car_url = f"https://cars.av.by{car.find('h3', class_='listing-item__title').find('a')['href']}"
            car_about_title = car.find('h3', class_='listing-item__title').text.strip()
            car_params = car.find('div', class_='listing-item__params').text.strip()
            car_price_by = car.find('div', class_='listing-item__price').text.strip()
            car_price_usd = car.find('div', class_='listing-item__priceusd').text.strip()
            car_info = car.find('div', class_='listing-item__location').text.strip()
            cars_dict[cars_id] = {'car_url': car_url,
                'car_about_title': car_about_title,
                                  'car_params': car_params,
                                  'car_price_by': car_price_by,
                                  'car_price_usd': car_price_usd,
                                  'car_info': car_info
                                  }
            fresh_cars[cars_id] = {'car_url': car_url,
                'car_about_title': car_about_title,
                                  'car_params': car_params,
                                  'car_price_by': car_price_by,
                                  'car_price_usd': car_price_usd,
                                  'car_info': car_info
                                  }
    with open ('pars_avby.json', 'w', encoding='utf-8') as file:
        json.dump(cars_dict, file, indent=4, ensure_ascii=False)

    return fresh_cars
print(check_cars_update())


def get_parser_av_filters():
    url = 'https://cars.av.by/filter'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    # Инициализируем счетчик
    count = 0
    cars_dict = {}
    while True:

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        print(response)

        # Находим контейнер с объявлениями
        listing_items_container = soup.find('div', class_='listing__items')
        # print(listing_items_container, 'listing')

        if listing_items_container is None:
            print("None listing")
            print("Unable to find the 'listing-items' element.")
            print("Response content:")
            print(response.content)  # Печать полученного HTML-контента для отладки
            return []
        car_elements = listing_items_container.find_all('div', class_='listing-item')
        # print(car_elements, 'car_elem')

        # Выводим информацию об объявлениях
        for car in car_elements:
            count += 1
            car_about_title = car.find('h3', class_='listing-item__title').text.strip()
            car_url = f"https://cars.av.by{car.find('h3', class_='listing-item__title').find('a')['href']}"
            cars_id = car_url.split('/')[-1]
            cars_id = cars_id[::]
            # print(cars_id, 'cars_id')
            car_params = car.find('div', class_='listing-item__params').text.strip()
            car_price_by = car.find('div', class_='listing-item__price').text.strip()
            car_price_usd =car.find('div', class_='listing-item__priceusd').text.strip()
            car_info = car.find('div', class_='listing-item__location').text.strip()
            # print(f'{car_url} | '
            #       f'{car_about_title} | '
            #       f'{car_params} |'
            #       f' {car_price_by} | '
            #       f' {car_price_usd} | '
            #       f' {car_info}')

            cars_dict[cars_id] = {'car_url': car_url,
                                      'car_about_title':car_about_title,
                                  'car_params':car_params,
                                  'car_price_by':car_price_by,
                                  'car_price_usd': car_price_usd,
                                  'car_info':car_info
            }
            # print(cars_dict, 'cars_dict')
        print("Количество объектов:", len(cars_dict))
        # Проверяем наличие кнопки "Показать ещё"
        next_button = soup.find('a', class_='button--default', string='Показать ещё')
        if next_button:
            url = 'https://cars.av.by' + next_button['href']
        else:
            break  # Выходим из цикла, если кнопки "Показать ещё" больше нет
        print(f'Спарсировано объявлений: {count}')


    with open ('pars_avby.json', 'w', encoding='utf-8') as file:
        json.dump(cars_dict, file, indent=4, ensure_ascii=False)

get_parser_av()
