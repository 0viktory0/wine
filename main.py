from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

import datetime
import pandas
import collections


file_path = 'wine3.xlsx'

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml']))
template = env.get_template('template.html')


def define_data():
    now = datetime.date.today()
    time_data = now.year - 1920
    return time_data


def write_years(num):
    year_string = 'лет'

    if str(num)[-2:-1] != '1':
        if str(num)[-1] == '1':
            year_string = 'год'
        if str(num)[-1] == '2' or str(num)[-1] == '3' or str(num)[-1] == '4':
            year_string = 'года'
    return f'{num} {year_string}'


def get_inf_wine_file(file_path):
    excel_data_df = pandas.read_excel(file_path, na_filter=False)
    wines = excel_data_df.to_dict(orient='records')
    wine_card = collections.defaultdict(list)
    for wine in wines:
        value = wine['Категория']
        wine_card[value].append(wine)
    return wine_card


rendered_page = template.render(
    time=write_years(define_data()),
    wine_table=get_inf_wine_file(file_path),)


with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()


if __name__ == '__main__':
    main()
