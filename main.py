import telebot
from telebot import types

from choice_flavor import BotHandler
from hookah_bowl import HookahBowl
import settings


bot = telebot.TeleBot(settings.API_KEY)

bot_handler = BotHandler()

@bot.message_handler(commands=['start'])
def main(message):
    photo = open('picture/hookah_start.png', 'rb')
    marcup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Да", callback_data="да")
    btn2 = types.InlineKeyboardButton(text="Нет", callback_data="нет")
    marcup.row(btn1, btn2)
    bot.send_photo(message.chat.id, photo)
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! "
                                      f"Создать тебе интересный микс?", reply_markup=marcup)
    # bot_handler.ask_quest = True


@bot.message_handler(commands=['info'])
def all_command(message):
    bot.send_message(message.chat.id, f"/start - начало работы\n/help - помощь в работе с ботом\n")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f"1. Бота можно вызвать командой 'Создай микс'.\n"
                                      f"2. С помощью команды 'Больше инфо' можно узнать информацию "
                                      f"о способах забивки и чашах.\n"
                                      f"3. Для микса необходимо выбрать количество вкусов.\n"
                                      "4. Что бы бот подсказал как забить чашу, выбери тип чаши.\n"
                                      "5. Бот реагирует только на определенные команды, его конкретная цель помочь"
                                      " собрать микс, не забывай об этом!\n")


@bot.message_handler(content_types=["text"])
def get_hookah_bowl(message):
    """Условия для обработки некоторых месаджей от юзера"""
    if message.text.lower() == "да":
        # Отрабатывает если был вопрос про забивку и флаг ask_quest тру
        if bot_handler.ask_quest:
            marcup = types.InlineKeyboardMarkup()
            marcup.add(types.InlineKeyboardButton(text="Фанел",callback_data="фанел"))
            marcup.add(types.InlineKeyboardButton(text="Турка",callback_data="турка"))
            marcup.add(types.InlineKeyboardButton(text="Evil",callback_data="evil"))
            marcup.add(types.InlineKeyboardButton("Подробнее",
                                                  url='https://hookahhouse.ru/company/news/sposoby_zabivki_tabaka_v_chashu_kalyana_instruktsiya/'))
            bot.send_message(message.chat.id, "Отлично! Выбери тип чаши.\n"
                                              "Чтобы узнать больше о чашах и забивке выбери 'Подробнее'.", reply_markup=marcup)
            bot_handler.reset_flag()

    elif message.text.lower() == "нет":
        # Реагирует на флаг, если он тру, то отвечаем и блокируем флаг в фолс
        if bot_handler.ask_quest:
            bot.send_message(message.chat.id, "Ок! Давай потом.😉")
            bot_handler.reset_flag()
    elif message.text.lower() == "привет":
        bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}!🙂")

    elif message.text.lower() == "создай микс":
        # Включаем флаг и используем функцию handle_new_mix, блок выполняется и переводит флаг в фолс
        bot_handler.ask_quest = True
        bot_handler.handle_new_mix(message)

    elif message.text.lower() == "хочу микс":
        # После вопроса про еще один микс, выполняем функцию handle_new_mix
        if bot_handler.ask_quest:
            bot_handler.handle_new_mix(message)

    elif message.text.lower() == "больше инфо":
        marcup = types.InlineKeyboardMarkup()
        marcup.add(types.InlineKeyboardButton("Перейти на сайт",
                                              url='https://hookahhouse.ru/company/news/sposoby_zabivki_tabaka_v_chashu_kalyana_instruktsiya/'))
        bot.send_message(message.chat.id, "Ок, вот!", reply_markup=marcup)

    elif message.text.lower():
        bot.send_message(message.chat.id, f"Простите, я не понимаю ваш запрос: '{message.text}'.")


@bot.callback_query_handler(func=lambda call: True)
def callback_message(call):
    """Обработка колбэков с миксом и чашей"""

    # Отрабатывает если был выбрана чаша в функции get_hookah_bowl
    if call.data in ["фанел", "турка", "evil"]:
        chasha = HookahBowl()
        result = chasha.choice_bowl(call.data)
        bowl_name = call.data
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f"Для чаши '{bowl_name.title()}', {result}")
        bot.send_message(call.message.chat.id, "Создать еще один микс? Напиши 'Хочу микс'") #добавил новое
        bot_handler.ask_quest = True

    # Во всех других ситуациях создаем микс с помощью handle_call из класса BotHandler
    else:
        bot_handler.handle_call(call)


bot.polling(none_stop=True)

# Хочу добавить вывод на сайт с описанием забивки чаш
# Доработать логику обработки сообщений пользователя
# Проверить условие "хочу микс"
# Изменить команды и добавить описание в бота
# Добавить картинку микса кальяна, когда выдает результат - сделан
# Когда создан микс выводить кнопку "Хочу еще микс"
# После того как выводится вопрос о забивке, вывести инсрукцию по забивке
# Рассмотреть возможность добавления кнопки больше инфо в блок с чашами


