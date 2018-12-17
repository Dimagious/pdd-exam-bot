import gspread
from oauth2client.service_account import ServiceAccountCredentials
import config
import logging
import messages

logging.basicConfig(format=messages.LOGGING, level=logging.INFO)
logger = logging.getLogger(__name__)


def get_ticket_data(ticket_number):
    """
    Метод все данные билета
    :param ticket_number: номер номер билета
    :return: данные билета
    """
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(credentials)
    return client.open(config.DOC_NAME).get_worksheet(ticket_number)


def get_question(ticket_number, question_number):
    """
    Метод возвращает вопрос билета по заданному номеру
    :param ticket_number: номер билета
    :param question_number: номер вопроса в билете
    :return: вопрос
    """
    ticket = get_ticket_data(ticket_number)
    all_questions = ticket.range(config.QUESTIONS)
    question = all_questions[question_number].value
    return question


def get_write_answer(ticket_number, question_number):
    """
    Метод возвращает вариант правильного ответа на вопрос по заданному номеру вопроса
    :param ticket_number: номер билета
    :param question_number: номер вопроса в билете
    :return: ответ
    """
    ticket = get_ticket_data(ticket_number)
    all_write_answers = ticket.range(config.ANSWERS)
    write_answer = all_write_answers[question_number].value
    return write_answer


def get_comment(ticket_number, question_number):
    """
    Метод возвращает комментарий ответа по заданному номеру вопроса
    :param ticket_number: номер билета
    :param question_number: номер вопроса в билете
    :return: комментарий
    """
    ticket = get_ticket_data(ticket_number)
    all_comments = ticket.range(config.COMMENTS)
    comment = all_comments[question_number].value
    return comment


def get_picture(ticket_number, question_number):
    """
    Метод возвращает картинку к вопросу (если она есть) по заданному номеру вопроса
    :param ticket_number: номер билета
    :param question_number: номер вопроса в билете
    :return: картинка
    """
    ticket = get_ticket_data(ticket_number)
    all_pictures = ticket.range(config.PICTURES)
    picture = all_pictures[question_number].value
    return picture


def get_number_of_choices(ticket_number, question_number):
    """
    Метод возвращает вариантов ответов на вопрос по заданному номеру вопроса
    :param ticket_number: номер билета
    :param question_number: номер вопроса в билете
    :return: количество вариантов ответов
    """
    ticket = get_ticket_data(ticket_number)
    all_choices = ticket.range(config.CHOICES)
    number_of_choices = all_choices[question_number].value
    return number_of_choices

