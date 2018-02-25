import requests
from lxml import etree
import random
from bs4 import BeautifulSoup
from openpyxl import Workbook


def get_courses_list(request_link):
    xml_content = requests.get(request_link).content
    xml_tree = etree.fromstring(xml_content)
    courses_link = []
    for url_tag in xml_tree.getchildren():
        for loc_tag in url_tag.getchildren():
            courses_link.append(loc_tag.text)
    return random.sample(courses_link, 20)


def get_course_info(course_link):
    html_page = requests.get(course_link).text
    html_tree = BeautifulSoup(html_page, 'html.parser')
    course_info = []
    course_info.append(html_tree.find('h1', class_='title display-3-text').getText())
    course_info.append(html_tree.find('div', class_='rc-Language').getText())
    course_info.append(html_tree.find('div', class_='startdate rc-StartDateString caption-text').getText())
    rating = html_tree.find('div', class_='ratings-text headline-2-text')
    if rating:
        course_info.append(rating.getText())
    else:
        course_info.append('None')
    course_info.append(len(html_tree.findAll('div', class_='week')))
    course_info.append(course_link)
    return course_info


def output_courses_info_to_xlsx(filepath, courses_info):
    wb = Workbook()
    ws = wb.active
    for course_info in courses_info:
        ws.append(course_info)
    wb.save(filepath)


if __name__ == '__main__':
    request_link = 'https://www.coursera.org/sitemap~www~courses.xml'
    courses_link = get_courses_list(request_link)
    courses_info = []
    for course_link in courses_link:
        print(course_link)
        courses_info.append(get_course_info(course_link))
    filepath = 'courses_info.xlsx'
    output_courses_info_to_xlsx(filepath, courses_info)
    