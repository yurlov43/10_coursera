import requests
from lxml import etree
import random
from bs4 import BeautifulSoup
from openpyxl import Workbook


def get_xml_tree(request_link):
    xml_content = requests.get(request_link).content
    return etree.fromstring(xml_content)


def get_random_courses_links(xml_tree, number_courses):
    courses_link = []
    for url_tag in xml_tree.getchildren():
        for loc_tag in url_tag.getchildren():
            courses_link.append(loc_tag.text)
    return random.sample(courses_link, number_courses)


def get_html_tree(course_link):
    html_page = requests.get(course_link)
    html_page.encoding = 'utf-8-sig'
    html_text = html_page.text
    return BeautifulSoup(html_text, 'html.parser')


def get_course_info(html_tree):
    course_info = dict(
        name=html_tree.find(
            'h1',
            class_='title display-3-text').getText(),
        language=html_tree.find(
            'div',
            class_='rc-Language').getText(),
        start_date=html_tree.find(
            'div',
            class_='startdate rc-StartDateString caption-text').getText(),
        rating=None,
        number_weeks=len(html_tree.findAll(
            'div',
            class_='week')),
        course_link=course_link)
    rating = html_tree.find(
        'div',
        class_='ratings-text headline-2-text')
    if rating:
        course_info['rating'] = rating.getText()
    return course_info


def fill_work_sheet(courses_info, work_sheet):
    for course_info in courses_info:
        work_sheet.append(list(course_info.values()))
    return work_sheet


def get_maximum_columns_widths(work_sheet):
    columns_widths = {}
    for row in work_sheet.rows:
        for cell in row:
            if cell.value and cell.column != 'E':
                column_width = columns_widths.get(cell.column, 0)
                width_of_text = len(cell.value)
                columns_widths[cell.column] = max(
                    column_width,
                    width_of_text)
    return columns_widths


def set_columns_widths_by_content(work_sheet, columns_widths):
    for column, width in columns_widths.items():
        work_sheet.column_dimensions[column].width = width
    return work_sheet


if __name__ == '__main__':
    request_link = 'https://www.coursera.org/sitemap~www~courses.xml'
    number_courses = 20
    xml_tree = get_xml_tree(request_link)
    courses_link = get_random_courses_links(xml_tree, number_courses)
    courses_info = []
    for course_number, course_link in enumerate(courses_link, start=1):
        print('{}. {}'.format(course_number, course_link))
        html_tree = get_html_tree(course_link)
        courses_info.append(get_course_info(html_tree))
    filepath = input('Enter the file name: ')
    if filepath:
        filepath = filepath + '.xlsx'
    else:
        filepath = 'courses_info.xlsx'
    work_book = Workbook()
    work_sheet = fill_work_sheet(courses_info, work_book.active)
    columns_widths = get_maximum_columns_widths(work_sheet)
    work_sheet = set_columns_widths_by_content(work_sheet, columns_widths)
    work_book.save(filepath)
