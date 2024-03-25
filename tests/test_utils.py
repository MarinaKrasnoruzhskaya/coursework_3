import pytest


from coursework_3 import utils


@pytest.fixture
def examp():
    return [
        {'id': 509645757, 'state': 'EXECUTED', 'date': '2019-10-30T01:49:52.939296'},
        {'id': 863064926, 'state': 'EXECUTED', 'date': '2019-12-08T22:46:21.935582'},
        {'id': 560813069, 'state': 'CANCELED', 'date': '2019-12-03T04:27:03.427014'},
    ]


@pytest.fixture
def examp_2():
    return {
        'id': 441945886,
        'state': 'EXECUTED',
        'date': '2019-08-26T10:50:58.294041',
        'operationAmount': {'amount': '31957.58', 'currency': {'name': 'руб.', 'code': 'RUB'}},
        'description': 'Перевод организации',
        'from': 'Maestro 1596837868705199',
        'to': 'Счет 64686473678894779589'
    }


def test_load_json():

    assert utils.load_json_file("example.json") == [{"one": "two", "key": "value"}]


def test_exclude_null_elements():
    assert utils.exclude_null_elements([{}, {"one": "two", "key": "value"}]) == [{"one": "two", "key": "value"}]
    assert utils.exclude_null_elements([{}, {}]) == []


def test_sorts_by_date(examp):
    assert utils.sorts_by_date(examp) == [
        {'id': 863064926, 'state': 'EXECUTED', 'date': '2019-12-08T22:46:21.935582'},
        {'id': 560813069, 'state': 'CANCELED', 'date': '2019-12-03T04:27:03.427014'},
        {'id': 509645757, 'state': 'EXECUTED', 'date': '2019-10-30T01:49:52.939296'}
    ]


def test_formats_the_transfer_date():
    assert utils.formats_the_transfer_date('2019-12-08T22:46:21.935582') == '08.12.2019'


def test_formats_the_transfer_data_error():
    with pytest.raises(ValueError):
        utils.formats_the_transfer_date('')


def test_performs_account_masking():
    assert utils.performs_account_masking('Счет 90424923579946435907') == 'Счет ****5907'


def test_performs_account_masking_card():
    assert utils.performs_account_masking('Visa Classic 2842878893689012') == 'Visa Classic 2842 87** **** 9012'


def test_performs_account_masking_null():
    assert utils.performs_account_masking('') == ''


def test_performs_account_masking_non_format():
    assert utils.performs_account_masking('Счет90424923579946435907') == ''


def test_formats_transaction_information_from(examp_2):
    assert utils.formats_transaction_information_from(examp_2) == "26.08.2019 Перевод организации\n" + \
           "Maestro 1596 83** **** 5199-> Счет ****9589\n" + \
           "31957.58 руб."


def test_formats_transaction_information_from_error():
    with pytest.raises(KeyError):
        utils.formats_transaction_information_from({})


def test_selects_list_of_five_operations(examp):
    assert len(utils.selects_list_of_five_operations(examp)) == 2


def test_selects_list_of_five_operations_break():
    assert len(utils.selects_list_of_five_operations([
        {'state': 'CANCELED'}, {'state': 'EXECUTED'}, {'state': 'EXECUTED'}, {'state': 'EXECUTED'},
        {'state': 'EXECUTED'}, {'state': 'EXECUTED'}, {'state': 'EXECUTED'}, {'state': 'CANCELED'},
    ])) == 5
