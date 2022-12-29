import argparse
import collections
import datetime
from dotenv import load_dotenv
import os
import pandas

from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


def define_date():
    now = datetime.date.today()
    winery_age = now.year - foundation_date
    return winery_age


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


if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser(description='Сайт винодельни',)
    parser.add_argument('file_path',
                        nargs='?',
                        default=os.environ['file_path'],
                        help='Введите путь до файла с таблицей')

    file_path = parser.parse_args().file_path
    foundation_date = 1920

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template.html')

    rendered_page = template.render(
        time_passed=write_years(define_date()),
        wine_table=get_inf_wine_file(file_path),)


    with open('index.html', 'w', encoding="utf8") as file:
         file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()