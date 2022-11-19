from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from rembg import remove
from PIL import Image
from pathlib import Path
from random import randint
import requests

API_TOKEN = '5620818004:AAE3M4nIw6VWk2oRetohzUuRcXhBQG-PFC8'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply('Я умею вырезать объект из фотографии и рассказывать шутки.')


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply('Для того чтобы я рассказал шутку, напиши <шутка>.\n Для того чтобы я вырезал объект из фотографии, пришли фотографию.')


def weatherday(city):
    appid = "e173e2835b248384d08be500b4e16f26"
    res = requests.get("http://api.openweathermap.org/data/2.5/weather", params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()
    try:
        return f'Прогноз погоды на день:\n\nГород: {city}\nПогодные условия: {data["weather"][0]["description"]}\nCкорость ветра: {data["wind"]["speed"]} м/с\nВидимость: {data["visibility"] / 100}%\nТемпература: {data["main"]["temp"]}\nМинимальная температура: {data["main"]["temp_min"]}\nМаксимальная температура: {data["main"]["temp_max"]}'
    except:
        return 0


def log_writer(nm, ms, id):
    log = open('log.txt', 'a+', encoding='utf-8')
    log.write(f"{datetime.now()}\n{nm}\n{ms}\n{id}\n{'-'*40}\n")
    log.close


@dp.message_handler(commands=['day'])
async def main(message: types.Message):
    global weather_id
    log_writer(message.chat.full_name, message.text, message.chat.id)
    id = message.chat.id
    text = message.text.lower().split()
    print(message.text, message.chat.id)
    city = text[1]
    if weatherday(city) == 0:
        await message.reply("Я не смог найти ваш город, пожалуйста проверьте корректность города.")
    else:
        await message.reply(weatherday(city))


def remove_bg():
    list_of_extensions = ['*.jpg', '*.png']
    all_files = []

    for ext in list_of_extensions:
        all_files.extend(Path('C:\\Users\\User\\Desktop\\piton\\BblPEZATEJlb\\input_imgs').glob(ext))

    for index, item in enumerate(all_files):
        input_path = Path(item)
        file_name = input_path.stem

        output_path = f'C:\\Users\\User\\Desktop\\piton\\BblPEZATEJlb\\output_imgs\{file_name}_output.png'

        input_img = Image.open(input_path)
        output_img = remove(input_img)
        output_img.save(output_path)

        print(f'Completed: {index + 1}/{len(all_files)}')

with open("MyApp\Lab7\phra1se.txt",encoding='utf-8') as file:
    phrases=[i.strip() for i in file.readlines()]
    

@dp.message_handler(content_types=['text'])
async def send_sad_phrase(ms: types.Message):
    if ms.text == 'шутка':
        await ms.answer(phrases[randint(0,len(phrases)-1)])
    elif ms.text == 'МТУСИ':
        await ms.answer('Вот наш сайт -> https://mtuci.ru/')
        

@dp.message_handler(content_types=['photo'])
async def main123(message: types.Message):
    await message.photo[-1].download('BblPEZATEJlb\input_imgs\image.png')
    t = str(datetime.now())
    for m in [':', '.', ' ']: t = t.replace(m, '_')
    await message.photo[-1].download(f'BblPEZATEJlb\LOG\{t}_{message.chat.full_name}.png')
    remove_bg()
    photo = open('BblPEZATEJlb\output_imgs\\image_output.png',mode='rb')
    await bot.send_photo(photo=photo, chat_id=message.chat.id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

