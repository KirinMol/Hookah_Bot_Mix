import telebot
import settings
from telebot import types
from two_m import TwoMix
from three_m import ThreeMix
bot = telebot.TeleBot(settings.API_KEY)


class BotHandler:
    """Класс для обработки колбэков и подгрузки данных по миксам и чашам"""
    def __init__(self):
        self.user_mixes = ""
        self.ask_quest = False


    def handle_call(self, call):
        """Обработка колбэка по количеству вкусов в миксе"""
        if call.data == "да":
            marcup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(text="Два", callback_data="два")
            btn2 = types.InlineKeyboardButton(text="Три", callback_data="три")
            marcup.row(btn1, btn2)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Отлично! Сколько вкусов добавить в микс?", reply_markup=marcup)

        if call.data in ["два", "три"]:
            marcup = types.InlineKeyboardMarkup()
            marcup.add(types.InlineKeyboardButton(text="Кислый", callback_data="кислый"))
            marcup.add(types.InlineKeyboardButton(text="Сладкий", callback_data="сладкий"))
            marcup.add(types.InlineKeyboardButton(text="Выпечка", callback_data="выпечка"))
            marcup.add()
            self.user_mixes = call.data
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Отлично! Выбери категорию вкуса.", reply_markup=marcup)

        elif call.data in ["кислый", "сладкий", "выпечка"]:
            # Под каждый вкус отображается соответствующая картинка
            sweet = open('picture/sweet_fruit.png', 'rb')
            acid = open('picture/acid_mix.png', 'rb')
            bakery = open('picture/candy_mix.png', 'rb')

            if call.data == "кислый":
                photo = acid
            elif call.data == "сладкий":
                photo = sweet
            elif call.data == "выпечка":
                photo = bakery


            if self.user_mixes == "два":
                mix = TwoMix()
                result = mix.question_for_flavor(call.data)
                bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id, text=f"{result}")
                bot.send_photo(call.message.chat.id, photo)
                bot.send_message(call.message.chat.id, "Помочь с забивкой микса?")
                self.ask_quest = True
            elif self.user_mixes == "три":
                mix = ThreeMix()
                result = mix.question_for_flavor(call.data)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f"{result}")
                bot.send_photo(call.message.chat.id, photo)
                bot.send_message(call.message.chat.id, "Помочь с забивкой микса?")
                self.ask_quest = True

        elif call.data == "нет":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=f"Хорошо, в другой раз!")
            # self.reset_flag()


    def handle_new_mix(self, message): #добавил новое
        """Повторить блок функции handle_call если прилетел 'хочу микс' колбэк"""
        self.user_mixes = ""

        marcup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Два", callback_data="два")
        btn2 = types.InlineKeyboardButton("Три", callback_data="три")
        marcup.row(btn1, btn2)
        bot.send_message(message.chat.id, "Ок! Сколько вкусов добавить в микс?", reply_markup=marcup)
        self.reset_flag()

    def reset_flag(self):
        """Сброс флага, который реагирует на команды (да, нет, хочу микс)"""
        self.ask_quest = False


BotHandler()