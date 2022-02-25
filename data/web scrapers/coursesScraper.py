import requests
from bs4 import BeautifulSoup
import re

URL = "https://bulletin.case.edu/course-descriptions/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

a_tags = soup.findAll('a', href = re.compile("/course-descriptions/[a-z]{4}/$"), )
a_tags_href = set()
for a in a_tags:
    a_tags_href.add(a["href"][21:])

a_tags = soup.find_all(text=re.compile("^\([A-Z]{4}\)"))
dict = {}
dict["acct"] = "Accounting" # error in html, damn Case
for a in a_tags:
    dict[a[1:5].lower()] = a[7:]

a_tags_href = list(a_tags_href)
a_tags_href.sort()

subject_links = []
for href in a_tags_href:
    subject_links.append(URL + href)

f = open("courses.sql", "w")

for i in range(len(subject_links)):
    department = "\"" + dict[subject_links[i][46:50]] + "\""
    page = requests.get(subject_links[i])
    soup = BeautifulSoup(page.content, "html.parser")
    course_blocks = soup.find_all("div", {"class": "courseblock"})
    course_tuples = []
    for course_block in course_blocks:
        tuple_array = course_block.find('strong').text.strip().replace(" ", " ").split(".")
        code_value = "\"" + tuple_array[0].strip() + "\""
        name_value = "\"" + tuple_array[1].strip().replace('"', "")+ "\""
        credit_value = tuple_array[len(tuple_array) - 2].strip()[0]
        course_tuples.append("(" + code_value + "," + name_value + "," + department + "," + credit_value + ")")
    for title in course_tuples:
        f.write("insert into applicase_courses values " + title + ";\n")
f.close()