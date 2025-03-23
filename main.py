import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from texts import *
from classes import *
from settings import *

##########################################################################
# Все объявления


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=BOT_TOKEN)
# Диспетчер
dp = Dispatcher()

# Структура "Заказ"
order = Order()

# Структура с флагами для считывания деталей заказа
# Ключ - ID пользователя
# Значение - готовность принимать детали
struct_ready = {}

# Словарь, где ключ это сообщение в чате менеджеров,
# а значение, это ID пользователя, отправившего его + категория + подкатегория
struct_id = {}

# Словарь, где ключ это ID пользователя,
# а значение, это структура order, закреплённая за ним
struct_users = {}

##########################################################################
# Функции проверки ID


# Проверка на админа
def check_admin(id):
    if id in ID_ADMIN:
        return True
    return False


# Проверка на любого пользователя бота
# *все люди, у которых есть доступ к боту
def check_user(id):
    if id in ID_PEOPLE or id in ID_ADMIN:
        return True
    return False


# Проверка ID беседы (нужны беседы менеджеров)
# Беседы менеджеров, где бот - админ
def check_chat(id):
    if id in ID_CHAT:
        return True
    return False


# Проверка ID беседы (нужны личные сообщения)
# Личное общение с ботом
def check_solo(id_person, id_chat):
    if check_user(id_person) and not check_chat(id_chat):
        return True
    return False


##########################################################################
# Прочие функции


# Функция формирования сообщения о заказе
def create_message(structure):
    return f"""Новый заказ.
        Категория: {structure.get_category()}
        Подкатегория: {structure.get_sub_category()}
        Детали:"""


##########################################################################
# Служебные команды для разработчика


@dp.message(F.text.lower() == "id")
async def get_id(message: types.Message):
    if check_admin(str(message.from_user.id)) or check_chat(str(message.chat.id)):
        id_group = str(message.chat.id)
        id_user = str(message.from_user.id)
        await message.answer(f"ID группы: {id_group}\nID пользователя: {id_user}")


##########################################################################


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):
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


# Хэндлер на команду /finish
@dp.message(Command("finish"))
async def cmd_finish(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):
        struct_ready[str(message.from_user.id)] = False

        chat_id = None
        category = struct_users[str(message.from_user.id)].get_category()
        if category == K1:
            chat_id = CHAT_ID_1
        elif category == K2:
            chat_id = CHAT_ID_2
        elif category == K3:
            chat_id = CHAT_ID_3
        elif category == K4:
            chat_id = CHAT_ID_4
        elif category == K5:
            chat_id = CHAT_ID_5
        elif category == K6:
            chat_id = CHAT_ID_6
        else:
            await message.answer("Ошибка выбора категории. Попробуйте снова. (Учти что нет K7 и K8)")

        message_from_user = create_message(struct_users[str(message.from_user.id)])
        await bot.send_message(chat_id=chat_id, text=message_from_user)

        for msg in struct_id[str(message.from_user.id)]:
            await bot.send_message(chat_id=chat_id, text=msg)
        print(struct_id)
        print(struct_users)
        print(struct_ready)
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
        # Вывод сообщения и кнопок
        await message.answer(CREATE_ORDER)


# Хендлер команды "Создать заказ"
@dp.message(F.text.lower() == CREATE_ORDER_BUTTON.lower())
async def create_order(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):

        if str(message.from_user.id) not in struct_users:
            struct_users[str(message.from_user.id)] = Order()

        if str(message.from_user.id) not in struct_ready:
            struct_ready[str(message.from_user.id)] = False

        if str(message.from_user.id) not in struct_id:
            struct_id[str(message.from_user.id)] = []

        struct_users[str(message.from_user.id)].clean()

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
            input_field_placeholder=STAGE_ONE_BACKTEXT)
                             )


##########################################################################
# Категории


# Полиграфия 1
@dp.message(F.text.lower() == K1.lower())
async def polygraphy(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):
        struct_users[str(message.from_user.id)].set_category(K1)

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
            input_field_placeholder=STAGE_TWO_BACKTEXT)
                             )


# Широкоформат 2
@dp.message(F.text.lower() == K2.lower())
async def shirikoformat(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):
        struct_users[str(message.from_user.id)].set_category(K2)

        # Создание кнопок
        kb = [
            [types.KeyboardButton(text=K2P1)],
            [types.KeyboardButton(text=K2P2)],
            [types.KeyboardButton(text=K2P3)],
            [types.KeyboardButton(text=K2P4)]
        ]

        builder = ReplyKeyboardBuilder()
        for i in range(len(kb)):
            builder.add(kb[i][0])
        builder.adjust(3)  # Количество строк меняй тут
        await message.answer(SECOND_STEP, reply_markup=builder.as_markup(
            resize_keyboard=True,
            input_field_placeholder=STAGE_TWO_BACKTEXT)
                             )


# Шелкография, ДТФ 3
@dp.message(F.text.lower() == K3.lower())
async def shelkographia_dtf(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):
        struct_users[str(message.from_user.id)].set_category(K3)

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
            input_field_placeholder=STAGE_TWO_BACKTEXT)
                             )


# Сувениры 4
@dp.message(F.text.lower() == K4.lower())
async def suvenirs(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):
        struct_users[str(message.from_user.id)].set_category(K4)

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
            input_field_placeholder=STAGE_TWO_BACKTEXT)
                             )


# Флаги, сублимация 5
@dp.message(F.text.lower() == K5.lower())
async def flags_sublimation(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):
        struct_users[str(message.from_user.id)].set_category(K5)

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
            input_field_placeholder=STAGE_TWO_BACKTEXT)
                             )


# Конструкции, монтажи 6
@dp.message(F.text.lower() == K6.lower())
async def constructions_montages(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):
        struct_users[str(message.from_user.id)].set_category(K6)

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
            input_field_placeholder=STAGE_TWO_BACKTEXT)
                             )


# Закупка 7
@dp.message(F.text.lower() == K7.lower())
async def zakupka(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):
        struct_users[str(message.from_user.id)].set_category(K7)

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
            input_field_placeholder=STAGE_TWO_BACKTEXT)
                             )


# Расчёт 8
@dp.message(F.text.lower() == K8.lower())
async def rasschet(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):
        struct_users[str(message.from_user.id)].set_category(K8)

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
            input_field_placeholder=STAGE_TWO_BACKTEXT)
                             )


##########################################################################
# Подкатегории


# Цифровая печать 1 1
@dp.message(F.text.lower() == K1P1.lower())
async def k1p1(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):

        struct_users[str(message.from_user.id)].set_sub_category(K1P1)
        await message.answer(K1P1_DETAILS, reply_markup=types.ReplyKeyboardRemove())
        struct_ready[str(message.from_user.id)] = True


# Офсет 1 2
@dp.message(F.text.lower() == K1P2.lower())
async def k1p2(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):

        struct_users[str(message.from_user.id)].set_sub_category(K1P2)
        await message.answer(K1P2_DETAILS, reply_markup=types.ReplyKeyboardRemove())
        struct_ready[str(message.from_user.id)] = True


# Баннеры 2 1
@dp.message(F.text.lower() == K2P1.lower())
async def k2p1(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):

        struct_users[str(message.from_user.id)].set_sub_category(K2P1)
        await message.answer(K2P1_DETAILS, reply_markup=types.ReplyKeyboardRemove())
        struct_ready[str(message.from_user.id)] = True


# Наклейки 2 2
@dp.message(F.text.lower() == K2P2.lower())
async def k2p2(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):

        struct_users[str(message.from_user.id)].set_sub_category(K2P2)
        await message.answer(K2P2_DETAILS, reply_markup=types.ReplyKeyboardRemove())
        struct_ready[str(message.from_user.id)] = True


# Таблички 2 3
@dp.message(F.text.lower() == K2P3.lower())
async def k2p3(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):

        struct_users[str(message.from_user.id)].set_sub_category(K2P3)
        await message.answer(K2P3_DETAILS, reply_markup=types.ReplyKeyboardRemove())
        struct_ready[str(message.from_user.id)] = True


# Стенды 2 4
@dp.message(F.text.lower() == K2P4.lower())
async def k2p4(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):

        struct_users[str(message.from_user.id)].set_sub_category(K2P4)
        await message.answer(K2P4_DETAILS, reply_markup=types.ReplyKeyboardRemove())
        struct_ready[str(message.from_user.id)] = True


# Шелкография 3 1
@dp.message(F.text.lower() == K3P1.lower())
async def k3p1(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):

        struct_users[str(message.from_user.id)].set_sub_category(K3P1)
        await message.answer(K3P1_DETAILS, reply_markup=types.ReplyKeyboardRemove())
        struct_ready[str(message.from_user.id)] = True


# ДТФ 3 2
@dp.message(F.text.lower() == K3P2.lower())
async def k3p2(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):

        struct_users[str(message.from_user.id)].set_sub_category(K3P2)
        await message.answer(K3P2_DETAILS, reply_markup=types.ReplyKeyboardRemove())
        struct_ready[str(message.from_user.id)] = True


# Термотрансфер 3 3
@dp.message(F.text.lower() == K3P3.lower())
async def k3p3(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):

        struct_users[str(message.from_user.id)].set_sub_category(K3P3)
        await message.answer(K3P3_DETAILS, reply_markup=types.ReplyKeyboardRemove())
        struct_ready[str(message.from_user.id)] = True


# УФ-печать 4 1
@dp.message(F.text.lower() == K4P1.lower())
async def k4p1(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):

        struct_users[str(message.from_user.id)].set_sub_category(K4P1)
        await message.answer(K4P1_DETAILS, reply_markup=types.ReplyKeyboardRemove())
        struct_ready[str(message.from_user.id)] = True


# Гравировка 4 2
@dp.message(F.text.lower() == K4P2.lower())
async def k4p2(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):

        struct_users[str(message.from_user.id)].set_sub_category(K4P2)
        await message.answer(K4P2_DETAILS, reply_markup=types.ReplyKeyboardRemove())
        struct_ready[str(message.from_user.id)] = True


# Тиснение 4 3
@dp.message(F.text.lower() == K4P3.lower())
async def k4p3(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):

        struct_users[str(message.from_user.id)].set_sub_category(K4P3)
        await message.answer(K4P3_DETAILS, reply_markup=types.ReplyKeyboardRemove())
        struct_ready[str(message.from_user.id)] = True


# Сублимация 4 4
@dp.message(F.text.lower() == K4P4.lower())
async def k4p4(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):

        struct_users[str(message.from_user.id)].set_sub_category(K4P4)
        await message.answer(K4P4_DETAILS, reply_markup=types.ReplyKeyboardRemove())
        struct_ready[str(message.from_user.id)] = True


# Флаги 5 1
@dp.message(F.text.lower() == K5P1.lower())
async def k5p1(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):

        struct_users[str(message.from_user.id)].set_sub_category(K5P1)
        await message.answer(K5P1_DETAILS, reply_markup=types.ReplyKeyboardRemove())
        struct_ready[str(message.from_user.id)] = True


# Пошив текстиля 5 2
@dp.message(F.text.lower() == K5P2.lower())
async def k5p2(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):

        struct_users[str(message.from_user.id)].set_sub_category(K5P2)
        await message.answer(K5P2_DETAILS, reply_markup=types.ReplyKeyboardRemove())
        struct_ready[str(message.from_user.id)] = True


# Джокер 6 1
@dp.message(F.text.lower() == K6P1.lower())
async def k6p1(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):

        struct_users[str(message.from_user.id)].set_sub_category(K6P1)
        await message.answer(K6P1_DETAILS, reply_markup=types.ReplyKeyboardRemove())
        struct_ready[str(message.from_user.id)] = True


# Брус 6 2
@dp.message(F.text.lower() == K6P2.lower())
async def k6p2(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):

        struct_users[str(message.from_user.id)].set_sub_category(K6P2)
        await message.answer(K6P2_DETAILS, reply_markup=types.ReplyKeyboardRemove())
        struct_ready[str(message.from_user.id)] = True


# Монтаж 6 3
@dp.message(F.text.lower() == K6P3.lower())
async def k6p3(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):

        struct_users[str(message.from_user.id)].set_sub_category(K6P3)
        await message.answer(K6P3_DETAILS, reply_markup=types.ReplyKeyboardRemove())
        struct_ready[str(message.from_user.id)] = True


# Виндеры 6 4
@dp.message(F.text.lower() == K6P4.lower())
async def k6p4(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):

        struct_users[str(message.from_user.id)].set_sub_category(K6P4)
        await message.answer(K6P4_DETAILS, reply_markup=types.ReplyKeyboardRemove())
        struct_ready[str(message.from_user.id)] = True


##########################################################################
# Получение деталей заказа
@dp.message()
async def details(message: types.Message):
    if check_solo(str(message.from_user.id), str(message.chat.id)):
        try:
            if struct_ready[str(message.from_user.id)]:
                # struct_ready[str(message.from_user.id)] = False

                struct_users[str(message.from_user.id)].set_properties(message.text)

                # message_from_user = create_message(struct_users[str(message.from_user.id)])

                # await bot.send_message(chat_id=chat_id, text=message_from_user)
                struct_id[str(message.from_user.id)].append(message.text)
        except KeyError:
            pass
    # Обсуждение в чате менеджеров
    if check_chat(str(message.chat.id)):
        if message.reply_to_message:
            print(0)
            if str(message.reply_to_message.from_user.id) == ID_BOT:
                print(1)
                try:
                    recipient = None
                    for key, data in struct_id.items():
                        if message.reply_to_message.text in data:
                            recipient = key
                    print(recipient)
                    if recipient is None:
                        await message.reply(ALREADY)
                    else:
                        answer = message.text
                        await bot.send_message(chat_id=recipient, text=answer)

                        del struct_id[recipient]
                except KeyError:
                    await message.reply(ALREADY)


##########################################################################


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
