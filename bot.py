# Установка UTF-8 кодировки
# -*- coding: utf-8 -*-

import time
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

# Настройка скрипт
token = "48a5ed426fc35638a2339b5103d3f1faf17201f0f59db08b5901c749d8919348c070f5da56f703fea6e0a" # API Key группы
admin_id = "150649447" # id администратора, которому будут пересланы сообщения с "Обратной связи"
# Настройка скрипта

# создания функций
def general_menu_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Информация об услугах', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Информация о командах', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Выключить бота', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('Обратная связь', color=VkKeyboardColor.NEGATIVE)
    return keyboard

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token).get_api()
# Работа с сообщениями
longpoll = VkLongPoll(vk_api.VkApi(token=token), wait=25)

# Бесконечный цикл
while True:
    print("Бот успешно запущен!")
    try:
        # Получение новых сообщений
        for event in longpoll.listen():
            # Если пришло новое сообщение
            if event.type == VkEventType.MESSAGE_NEW:
                # Если оно отправлено для меня
                if event.to_me:
                    if event.text.lower() == "выключить бота" or event.text.lower() == "/disable":
                        keyboard = VkKeyboard(one_time=False)
                        keyboard.add_button('Включить бота', color=VkKeyboardColor.PRIMARY)
                        vk.messages.send(user_id=event.user_id, v=5.89, message="Бот успешно выключен, для включения бота нажмите кнопку \"Включить бота\".", keyboard=keyboard.get_keyboard())
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW:
                                if event.to_me:
                                    if event.text.lower() == "включить бота" or event.text.lower() == "/enable":
                                        general_menu_keyboard()
                                        vk.messages.send(user_id=event.user_id, v=5.89, message="Бот успешно включен, выберите дальнейшие действия.", keyboard=keyboard.get_keyboard())
                                        break
                    elif event.text.lower() == "начать" or event.text.lower() == "/start":
                        general_menu_keyboard()
                        vk.messages.send(user_id=event.user_id, v=5.89, message="Привет, "+vk.users.get(user_ids=event.user_id)[0]['first_name']+"! Я бот, и если ты хочешь воспользоваться услугами данного паблика - я помогу тебе! Выбери дальнейшие действия.", keyboard=keyboard.get_keyboard()
                                        )
                    elif event.text.lower() == "информация об услугах" or event.text.lower() == "/info":
                        vk.messages.send(user_id=event.user_id, v=5.89, message='Ознакомиться с примерами работ или для заказа услуг тебе нужно перейти по этой ссылке - https://vk.com/market-181694592')
                    elif event.text.lower() == "обратная связь" or event.text.lower() == "/support":
                        keyboard = VkKeyboard(one_time=True)
                        keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
                        vk.messages.send(user_id=event.user_id, v=5.89, message="Если у тебя есть какие-либо вопросы, или ты хочешь воспользоваться услугами этого паблика - напиши сюда, администратор ответ на твое сообщение в ближайшее время.", keyboard=keyboard.get_keyboard())
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW:
                                if event.to_me:
                                    if event.text.lower() == "назад" or event.text.lower() == "начать" or event.text.lower() == "/start" or event.text.lower() == "информация об услугах" or event.text.lower() == "/info" or event.text.lower() == "обратная связь" or event.text.lower() == "/support" or event.text.lower() == "информация о командах" or event.text.lower() == "/help":
                                        general_menu_keyboard()
                                        vk.messages.send(user_id=event.user_id, v=5.89, message="Выберите дальнейшие действия.", keyboard=keyboard.get_keyboard())
                                        break
                                    else:
                                        general_menu_keyboard()
                                        vk.messages.send(user_id=admin_id, v=5.89, forward_messages=event.message_id)
                                        vk.messages.send(user_id=event.user_id, v=5.89, message="Администратор успешно получил ваше сообщение, ожидайте ответа в ближайшее время!", keyboard=keyboard.get_keyboard()
                                                        )
                                        break
                    elif event.text.lower() == "информация о командах" or event.text.lower() == "/help":
                        vk.messages.send(user_id=event.user_id, v=5.89, message='/info - информация об услугах\n/suppot - обратная связь\n/help - помощь по командам\n/disable - отключить бота\n/enable - включить бота')
                    else:
                        general_menu_keyboard()
                        vk.messages.send(user_id=event.user_id, v=5.89, message='К сожалению, я не знаю такой команды. Ознакомиться с полным списком моих команд ты можешь написав команду \"/help\".', keyboard=keyboard.get_keyboard())
    except Exception:
        time.sleep(1)
