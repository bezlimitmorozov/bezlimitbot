import telebot
import requests

bot = telebot.TeleBot("5309006030:AAGFubzYnyAfYD4p9cadG5Y37Mq1DpMVQMc")


def get_code(phone):
    token = 'IJMcp2KDTiGU05YpYwvd2zWqcfiVJzfsyazLPppAfr-iB5GWkTIoW0tFZZ3UP4Tq'
    url = "https://api.bezlimit.ru/v1"
    headers = {'accept': 'application/json',
               'Api-Token': token,
               'authorization': 'Basic YXBpOldHZnpzQWlKYkxa'}
    params = {'phone': int(phone)}
    request_url = f"{url}/queue/sms"
    response = requests.get(request_url, headers=headers, params=params)
    print(response.content)
    raw_answer = response.json()
    for i in raw_answer['items']:
        raw_code = i['text']
        break

    if 'Проверочный код восстановления пароля ЛК Безлимит' in raw_code:
        answer = raw_code

    elif 'Проверочный код для регистрации в ЛК Безлимит' in raw_code:
        answer = raw_code

    elif 'Код подтверждения перевода' in raw_code:
        answer = raw_code

    elif 'Код подтверждения для добавления номера' in raw_code:
        answer = raw_code

    elif response.status_code == 500:
        answer = 'Возникла ошибка при попытке произвести запрос, попробуйте позже или обратитесь к разработчику.' \
                 'Но не к самому себе, Вы же тоже разработчик.' \
                 'К какому-нибудь другому разработчику.'

    else:
        answer = 'Кода подтверждения не поступало. По всем вопросам обращайтесь к @joanhoe1544.'

    return answer


def check_for_test_phone(number):
    phones_list = [9032417766, 9032526426, 9039944222, 9064442514, 9064442671, 9064603113, 9090691313, 9605554826,
                   9612229359, 9614828609, 9618885971, 9633243809, 9633244519, 9654513918, 9654514087, 9672999985,
                   9682220854, 9682221451, 9682223481, 9682224854, 9682224918, 9006471111, 9682227064, 9682228615,
                   9684118881, 9612224895, 9064447536, 9612227834, 9944412525, 9681110905, 9682225197]

    if number in phones_list:
        message = get_code(number)
    else:
        message = 'Номер должен относиться к списку тестовых номеров.'

    return message


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if "я сотрудник безлимит" in message.text.lower() and len(message.text) == 31:
        bot.send_message(message.from_user.id, "Выполняю запрос...")
        bot.send_message(message.from_user.id, check_for_test_phone(int(message.text.split()[3])))
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напишите кодовую фразу для доступа к функционалу.")
    else:
        bot.send_message(message.from_user.id, "Я Вас не понимаю. Напишите /help.")


bot.infinity_polling()
