import requests
from bs4 import BeautifulSoup
import re

URL = "https://bulletin.case.edu/undergraduatestudies/majorsandminors/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

tr_tags = soup.findAll("tr")
tuples = []
for tr in tr_tags:
    column1 = tr.find("td", {"class": "column1"})
    column2 = tr.find("td", {"class": "column2"})
    column3 = tr.find("td", {"class": "column3"})
    if column3 is not None:
        string_column3 = str(column3.text)
        if string_column3.find("Major") != -1:
            major = "1"
        else:
            major = "0"
        if string_column3.find("Minor") != -1:
            minor = "1"
        else:
            minor = "0"
    if (column1 is not None) and (column2 is not None):
        string_column1 = str(column1.text)
        string_column2 = str(column2.text)
        if string_column2 != "---":
            tuples.append("(" + "\"" + string_column1 + " " + string_column2+ "\"" + "," + major + "," + minor +")")
        else:
            tuples.append("(" + "\"" + string_column1+ "\"" + "," + major + "," + minor +")")

f = open("majorMinor.sql", "w")
for tuple in tuples:
    f.write("insert into applicase_majorminor values " + tuple + ";\n")