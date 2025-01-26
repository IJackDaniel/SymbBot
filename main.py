import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from random import choice

from texts import *
from classes import *
from settings import *


##########################################################################


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=BOT_TOKEN)
# Диспетчер
dp = Dispatcher()
# Структура "Заказ"
order = Order()
# Флаг для считывания деталей заказа
ready = False


##########################################################################


def check_admin(id):
    if id == ID_ADMIN:
        return True
    return False


def check_user(id):
    if id in ID_PEOPLE:
        return True
    return False


##########################################################################
# Служебные команды для разработчика


@dp.message(F.text.lower() == "покажи заказ")
async def show_order(message: types.Message):
    if check_admin(str(message.from_user.id)):
        categ = order.get_category()
        sub_categ = order.get_sub_category()
        proper = order.get_properties()
        await message.answer(f"Категория: {categ}")
        await message.answer(f"Подкатегория: {sub_categ}")
        await message.answer(f"Свойства:\n{proper}")


@dp.message(F.text.lower() == "случайное заполнение")
async def rand_order(message: types.Message):
    if check_admin(str(message.from_user.id)):
        categ = choice([K1, K2, K3, K4, K5, K6, K7, K8])
        order.set_category(categ)

        sub_categ = choice([K1P1, K1P2,
                            K2P1, K2P2, K2P3, K2P4,
                            K3P1, K3P2, K3P3,
                            K4P1, K4P2, K4P3, K4P4,
                            K5P1, K5P2,
                            K6P1, K6P2, K6P3, K6P4,
                            K7P1, K7P2, K7P3, K7P4,
                            K8P1, K8P2, K8P3, K8P4, K8P5])
        order.set_sub_category(sub_categ)

        proper = choice(["БЛа бла бла бла бла",
                         "Ну вот, нужно ещё придумать много свойств",
                         "Так, пишу уже третью вариацию, и я определённо устал",
                         "На четвёртой точно всё"])
        order.set_properties(proper)
        await message.answer("Ок")


@dp.message(F.text.lower() == "очисть")
async def clean(message: types.Message):
    if check_admin(str(message.from_user.id)):
        order.clean()
        await message.answer("Ок")


@dp.message(F.text.lower() == "id")
async def get_id(message: types.Message):
    if check_admin(str(message.from_user.id)):
        id_group = str(message.chat.id)
        id_user = str(message.from_user.id)
        await message.answer(f"ID группы: {id_group}\nID пользователя: {id_user}")


##########################################################################


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Приветственное сообщение
    await message.answer(HELLO)

    # Создание кнопок
    kb = [
        [types.KeyboardButton(text=CREATE_ORDER_BUTTON)]
    ]

    # Параметры сетки с кнопками
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    # Вывод сообщения и кнопок
    await message.answer(CREATE_ORDER, reply_markup=keyboard)


# Хендлер команды "Создать заказ"
@dp.message(F.text.lower() == CREATE_ORDER_BUTTON.lower())
async def create_order(message: types.Message):
    if check_user(str(message.from_user.id)):
        order.clean()

        # Создание кнопок
        kb = [
            [types.KeyboardButton(text=K1)],
            [types.KeyboardButton(text=K2)],
            [types.KeyboardButton(text=K3)],
            [types.KeyboardButton(text=K4)],
            [types.KeyboardButton(text=K5)],
            [types.KeyboardButton(text=K6)],
            [types.KeyboardButton(text=K7)],
            [types.KeyboardButton(text=K8)]
        ]

        builder = ReplyKeyboardBuilder()
        for i in range(len(kb)):
            builder.add(kb[i][0])
        builder.adjust(3)  # Количество строк меняй тут
        await message.answer(FIRST_STEP, reply_markup=builder.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Категория")
                             )


##########################################################################


# Полиграфия 1
@dp.message(F.text.lower() == K1.lower())
async def polygraphy(message: types.Message):
    if check_user(str(message.from_user.id)):
        order.set_category(K1)

        # Создание кнопок
        kb = [
            [types.KeyboardButton(text=K1P1)],
            [types.KeyboardButton(text=K1P2)]
        ]

        builder = ReplyKeyboardBuilder()
        for i in range(len(kb)):
            builder.add(kb[i][0])
        builder.adjust(3)  # Количество строк меняй тут
        await message.answer(SECOND_STEP, reply_markup=builder.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Подкатегория")
                             )


# Широкоформат 2
@dp.message(F.text.lower() == K2.lower())
async def shirikoformat(message: types.Message):
    if check_user(str(message.from_user.id)):
        order.set_category(K2)

        # Создание кнопок
        kb = [
            [types.KeyboardButton(text=K2P1)],
            [types.KeyboardButton(text=K2P3)],
            [types.KeyboardButton(text=K2P3)],
            [types.KeyboardButton(text=K2P4)]
        ]

        builder = ReplyKeyboardBuilder()
        for i in range(len(kb)):
            builder.add(kb[i][0])
        builder.adjust(3)  # Количество строк меняй тут
        await message.answer(SECOND_STEP, reply_markup=builder.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Подкатегория")
                             )


# Шелкография, ДТФ 3
@dp.message(F.text.lower() == K3.lower())
async def shelkographia_dtf(message: types.Message):
    if check_user(str(message.from_user.id)):
        order.set_category(K3)

        # Создание кнопок
        kb = [
            [types.KeyboardButton(text=K3P1)],
            [types.KeyboardButton(text=K3P2)],
            [types.KeyboardButton(text=K3P3)]
        ]

        builder = ReplyKeyboardBuilder()
        for i in range(len(kb)):
            builder.add(kb[i][0])
        builder.adjust(3)  # Количество строк меняй тут
        await message.answer(SECOND_STEP, reply_markup=builder.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Подкатегория")
                             )


# Сувениры 4
@dp.message(F.text.lower() == K4.lower())
async def suvenirs(message: types.Message):
    if check_user(str(message.from_user.id)):
        order.set_category(K4)

        # Создание кнопок
        kb = [
            [types.KeyboardButton(text=K4P1)],
            [types.KeyboardButton(text=K4P2)],
            [types.KeyboardButton(text=K4P3)],
            [types.KeyboardButton(text=K4P4)]
        ]

        builder = ReplyKeyboardBuilder()
        for i in range(len(kb)):
            builder.add(kb[i][0])
        builder.adjust(3)  # Количество строк меняй тут
        await message.answer(SECOND_STEP, reply_markup=builder.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Подкатегория")
                             )


# Флаги, сублимация 5
@dp.message(F.text.lower() == K5.lower())
async def flags_sublimation(message: types.Message):
    if check_user(str(message.from_user.id)):
        order.set_category(K5)

        # Создание кнопок
        kb = [
            [types.KeyboardButton(text=K5P1)],
            [types.KeyboardButton(text=K5P2)]
        ]

        builder = ReplyKeyboardBuilder()
        for i in range(len(kb)):
            builder.add(kb[i][0])
        builder.adjust(3)  # Количество строк меняй тут
        await message.answer(SECOND_STEP, reply_markup=builder.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Подкатегория")
                             )


# Конструкции, монтажи 6
@dp.message(F.text.lower() == K6.lower())
async def constructions_montages(message: types.Message):
    if check_user(str(message.from_user.id)):
        order.set_category(K6)

        # Создание кнопок
        kb = [
            [types.KeyboardButton(text=K6P1)],
            [types.KeyboardButton(text=K6P2)],
            [types.KeyboardButton(text=K6P3)],
            [types.KeyboardButton(text=K6P4)]
        ]

        builder = ReplyKeyboardBuilder()
        for i in range(len(kb)):
            builder.add(kb[i][0])
        builder.adjust(3)  # Количество строк меняй тут
        await message.answer(SECOND_STEP, reply_markup=builder.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Подкатегория")
                             )


# Закупка 7
@dp.message(F.text.lower() == K7.lower())
async def zakupka(message: types.Message):
    if check_user(str(message.from_user.id)):
        order.set_category(K7)

        # Создание кнопок
        kb = [
            [types.KeyboardButton(text=K7P1)],
            [types.KeyboardButton(text=K7P2)],
            [types.KeyboardButton(text=K7P3)],
            [types.KeyboardButton(text=K7P4)]
        ]

        builder = ReplyKeyboardBuilder()
        for i in range(len(kb)):
            builder.add(kb[i][0])
        builder.adjust(3)  # Количество строк меняй тут
        await message.answer(SECOND_STEP, reply_markup=builder.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Подкатегория")
                             )


# Расчёт 8
@dp.message(F.text.lower() == K8.lower())
async def rasschet(message: types.Message):
    if check_user(str(message.from_user.id)):
        order.set_category(K8)

        # Создание кнопок
        kb = [
            [types.KeyboardButton(text=K8P1)],
            [types.KeyboardButton(text=K8P2)],
            [types.KeyboardButton(text=K8P3)],
            [types.KeyboardButton(text=K8P4)],
            [types.KeyboardButton(text=K8P5)]
        ]

        builder = ReplyKeyboardBuilder()
        for i in range(len(kb)):
            builder.add(kb[i][0])
        builder.adjust(3)  # Количество строк меняй тут
        await message.answer(SECOND_STEP, reply_markup=builder.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Подкатегория")
                             )


##########################################################################
# Свойства


# Цифровая печать 1 1
@dp.message(F.text.lower() == K1P1.lower())
async def k1p1(message: types.Message):
    if check_user(str(message.from_user.id)):
        global ready

        order.set_sub_category(K1P1)
        await message.answer(K1P1_DETAILS, reply_markup=types.ReplyKeyboardRemove())
        ready = True


##########################################################################


# Получение деталей заказа
@dp.message()
async def details(message: types.Message):
    global ready
    if ready and check_user(str(message.from_user.id)):
        ready = False

        order.set_properties(message.text)

        message_from_user = f"""Новый заказ.
        Категория {order.get_category()}
        Подкатегория {order.get_sub_category()}
        Детали:
        {order.get_properties()}"""

        await bot.send_message(chat_id=CHAT_ID_1, text=message_from_user)

        ### Повторное создание кнопки "создать заказ"
        # Создание кнопок
        kb = [
            [types.KeyboardButton(text=CREATE_ORDER_BUTTON)]
        ]

        # Параметры сетки с кнопками
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True
        )
        # Вывод сообщения и кнопок
        await message.answer(SEND, reply_markup=keyboard)


##########################################################################


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
