import os
import json

from datetime import datetime


def load_json_file(name):
    """
    читает json-данные из файла
    """
    path_file = os.path.join(os.path.abspath("../data"), name)
    with open(path_file, encoding="utf-8") as json_file:
        return json.load(json_file)


def exclude_null_elements(operations: list):
    """исключает нулевые элементы списка"""
    oper_new = []
    for operation in operations:
        if operation:
            oper_new.append(operation)
    return oper_new


def converts_str_to_date(operations):
    """заменяет значения по ключу 'date', преобразуя строку в <class 'datetime.datetime'> """
    for oper in operations:
        oper['date'] = datetime.strptime(oper['date'], '%Y-%m-%dT%H:%M:%S.%f')
    return operations


def sorts_by_date(operations: list):
    """сортирует список по дате в порядке убывания"""
    def sort_key(o):
        return o['date']
    operations.sort(key=sort_key, reverse=True)
    return operations


def formats_the_transfer_date(date_transfer):
    """переводит дату в формат ДД.ММ.ГГГГ"""
    return date_transfer.strftime('%d.%m.%Y')


def performs_account_masking(n: str):
    """маскирует номер карты и счета"""
    space = n.rfind(' ')
    if n and space != -1:
        if 'Счет' in n:
            number_str = n[:space] + " ****" + n[-4:]
        else:
            number_str = n[:space] + n[space:space+5] + " " + n[space+5:space+7] + "** **** " + n[-4:]
        return number_str
    return ''


def formats_transaction_information_from(o: dict):
    """форматирует информацию об операции"""
    return f"""{formats_the_transfer_date(o['date'])} {o['description']}\n""" + \
        f"""{performs_account_masking(o.get('from', ''))}-> {performs_account_masking(o['to'])}\n""" + \
        f"""{o['operationAmount']['amount']} {o['operationAmount']['currency']['name']}"""


def selects_list_of_five_operations(operations: list):
    """возвращает список из 5 последних операций EXECUTED"""
    i = 0
    opers_executed = []
    for operation in operations:
        if operation['state'] == 'EXECUTED':
            i += 1
            opers_executed.append(operation)
            if i == 5:
                break
    return opers_executed
