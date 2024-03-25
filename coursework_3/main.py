from coursework_3.utils import (sorts_by_date, exclude_null_elements, load_json_file,
                                selects_list_of_five_operations, formats_transaction_information_from,
                                converts_str_to_date)


def main():
    lst = selects_list_of_five_operations(
        sorts_by_date(converts_str_to_date(exclude_null_elements(load_json_file('operations.json'))))
    )
    print(*[formats_transaction_information_from(x) for x in lst], sep='\n\n')


main()
