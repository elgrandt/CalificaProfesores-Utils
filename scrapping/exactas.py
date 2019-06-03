from common import getPage
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import unicodedata
import json
import time

base = 'http://encuestas_finales.exactas.uba.ar/'
subjects = set()

def procesarPeriodos():
    url = 'http://encuestas_finales.exactas.uba.ar/periodos.html'
    page = getPage(url)
    for tr in page.select_one(".content").select("tr"):
        td = tr.select('td')[1]
        href = td.a.attrs["href"]
        processCuat(base+href)

def processCuat(url):
    cuatid = int(re.search(r'\d+', url).group())
    driver = webdriver.Chrome()
    driver.get(url)
    subjectsDiv = driver.find_element_by_id('list_mu%d' % cuatid)
    paginatorDivs = subjectsDiv.find_elements_by_class_name('head')
    if len(paginatorDivs) > 0:
        paginatorDiv = paginatorDivs[0]
        pagesCount = int(paginatorDiv.find_elements_by_tag_name('a')[-1].text)
        for pageNumber in range(pagesCount):
            changePageScript = 'lst("mu%d", %d)' % (cuatid, pageNumber)
            driver.execute_script(changePageScript)
            error = True
            while error:
                time.sleep(.001)
                try:
                    subjectsDiv = driver.find_element_by_id('list_mu%d' % cuatid)
                    subjectElements = subjectsDiv.find_elements_by_tag_name('li')
                    for subject in subjectElements:
                        unicodeSubjectName = subject.find_element_by_tag_name('a').text
                        subjectName = unicodedata.normalize('NFKD', unicodeSubjectName).encode('ascii','ignore')
                        subjects.add(subjectName)
                    error = False
                except:
                    pass
    else:
        for subject in subjectsDiv.find_elements_by_tag_name('li'):
            unicodeSubjectName = subject.find_element_by_tag_name('a').text
            subjectName = unicodedata.normalize('NFKD', unicodeSubjectName).encode('ascii','ignore')
            subjects.add(subjectName)
    driver.close()

if __name__ == '__main__':
    procesarPeriodos()
    file = open('materias.json', 'w+')
    file.write(json.dumps(list(subjects), sort_keys=True, indent=4, separators=(',', ': ')))