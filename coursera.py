import requests
import argparse
from lxml import etree
import random
from bs4 import BeautifulSoup
from openpyxl import Workbook


def parser_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-out', '--output',
        help='Path to result')
    return parser.parse_args()


def get_content(link):
    answer = requests.get(link)
    return answer.content


def get_random_courses_links(xml_content, number_courses):
    xml_tree = etree.fromstring(xml_content)
    courses_link = []
    for url_tag in xml_tree.getchildren():
        for loc_tag in url_tag.getchildren():
            courses_link.append(loc_tag.text)
    return random.sample(courses_link, number_courses)


def get_course_info(html_content, course_link):
    html_tree = BeautifulSoup(html_content, 'html.parser')
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
        work_sheet.append([
            course_info['name'],
            course_info['language'],
            course_info['start_date'],
            course_info['rating'],
            course_info['number_weeks'],
            course_info['course_link']
        ])
    return work_sheet


def set_columns_widths_by_content(work_sheet):
    for column in work_sheet.columns:
        max_width = 0
        column_name = column[0].column
        for cell in column:
            if cell.value:
                content_width = len(str(cell.value))
                max_width = max(content_width, max_width)
        work_sheet.column_dimensions[column_name].width = max_width + 2
    return work_sheet


if __name__ == '__main__':
    arguments = parser_arguments()
    output_file = arguments.output
    if not arguments.output:
        output_file = 'courses_info.xlsx'
    request_link = 'https://www.coursera.org/sitemap~www~courses.xml'
    number_courses = 20
    xml_content = get_content(request_link)
    courses_link = get_random_courses_links(xml_content, number_courses)
    courses_info = []
    for course_number, course_link in enumerate(courses_link, start=1):
        print('{}. {}'.format(course_number, course_link))
        html_content = get_content(course_link)
        course_info = get_course_info(html_content, course_link)
        courses_info.append(course_info)
    work_book = Workbook()
    work_sheet = work_book.active
    work_sheet = fill_work_sheet(courses_info, work_sheet)
    work_sheet = set_columns_widths_by_content(work_sheet)
    work_book.save(output_file)
