import telebot
import requests

bot = telebot.TeleBot("5309006030:AAGFubzYnyAfYD4p9cadG5Y37Mq1DpMVQMc", parse_mode=None)


def get_code(phone):
    token = 'Z1RseVcn9twtKLY84eYQf57Pw8ENZ1yks436TJHXaC2dJhcRZLJ2mGsgRBpTuFp7'
    url = "https://api.bezlimit.ru/v1"
    headers = {'accept': 'application/json',
               'Api-Token': token}
    params = {'phone': int(phone)}
    request_url = f"{url}/queue/sms"
    response = requests.get(request_url, headers=headers, params=params)
    raw_answer = str(response.json())[0:147]

    if 'Проверочный код восстановления пароля ЛК Безлимит' in raw_answer:
        raw_answer = raw_answer[0:118]
        answer = raw_answer.split("'text': '")[1]

    elif 'Проверочный код для регистрации в ЛК Безлимит' in raw_answer:
        raw_answer = raw_answer[0:114]
        answer = raw_answer.split("'text': '")[1]

    elif 'Код подтверждения перевода' in raw_answer:
        raw_answer = raw_answer
        answer = raw_answer.split("'text': '")[1]

    elif 'Код подтверждения для добавления номера' in raw_answer:
        raw_answer = raw_answer[0:121]
        answer = raw_answer.split("'text': '")[1]

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
                   9684118881, 9612224895, 9064447536, 9612227834, 9944412525, 9681110905]

    if number in phones_list:
        message = get_code(number)
    else:
        message = 'Э!\n Номер должен относиться к списку тестовых номеров...\n' \
                  'Не шалите так больше.' \
                  'Или напишите Ивану Морозову.'

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
