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
subjects = []
profesores = []


def procesarPeriodos():
    url = 'http://encuestas_finales.exactas.uba.ar/periodos.html'
    page = getPage(url)
    for tr in page.select_one(".content").select("tr"):
        td = tr.select('td')[1]
        href = td.a.attrs["href"]
        processCuat(base+href)

def processCuat(url):
    driver = webdriver.Chrome()
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
                    for i in range(len(subjectElements)):
                        subjectsDiv = driver.find_element_by_id('list_mu%d' % cuatid)
                        subjectElements = subjectsDiv.find_elements_by_tag_name('li')
                        subject = subjectElements[i]
                        unicodeSubjectName = subject.find_element_by_tag_name('a').text
                        subjectName = unicodedata.normalize('NFKD', unicodeSubjectName).encode('ascii','ignore').decode('ascii')
                        subject.find_element_by_tag_name('a').click()
                        subjectProfessors = getSubjectProfessors(driver)
                        driver.back()
                        subjects.append({"Name": subjectName, "Professors": subjectProfessors})
                    error = False
                except:
                    pass
    else:
        for i in range(len(subjectsDiv.find_elements_by_tag_name('li'))):
            subjectsDiv = driver.find_element_by_id('list_mu%d' % cuatid)
            subject = subjectsDiv.find_elements_by_tag_name('li')[i]
            unicodeSubjectName = subject.find_element_by_tag_name('a').text
            subjectName = unicodedata.normalize('NFKD', unicodeSubjectName).encode('ascii','ignore').decode('ascii')
            subject.find_element_by_tag_name('a').click()
            subjectProfessors = getSubjectProfessors(driver)
            driver.back()
            subjects.append({"Name": subjectName, "Professors": subjectProfessors})
    driver.close()

def getSubjectProfessors(driver):
    subjectProfessors = set()
    for turno in driver.find_elements_by_tag_name('tr'):
        container = turno.find_elements_by_css_selector('td.rg')
        if container:
            container = container[0]
        else:
            continue
        divs = container.find_elements_by_tag_name('div')
        for profesor in divs:
            try:
                professorName = profesor.find_element_by_tag_name('a').text
            except:
                continue
            if professorName in profesores:
                id = profesores.index(professorName)
            else:
                profesores.append(professorName)
                id = len(profesores) - 1
            subjectProfessors.add(id)
    return list(subjectProfessors)

if __name__ == '__main__':
    procesarPeriodos()
    file = open('materias.json', 'w+')
    file.write(json.dumps(list(subjects), sort_keys=True, indent=4, separators=(',', ': ')))
    file.close()
    file = open('profesores.json', 'w+')
    file.write(json.dumps(list(profesores), sort_keys=True, indent=4, separators=(',', ': ')))
    file.close()