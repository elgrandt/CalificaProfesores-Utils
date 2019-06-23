
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import unicodedata
import json
import time
import numpy as np


base = 'https://sga.itba.edu.ar'
subjets = set()


class Professor:
    def __init__(self, nombre):
        self.nombre = nombre

    def __iter__(self):
        yield "Nombre", self.nombre


class Subject:
    def __init__(self, codigo, nombre, facultad):
        self.nombre = nombre.encode('utf-8')
        self.codigo = codigo.encode('utf-8')
        self.facultad = facultad.encode('utf-8')
        self.profesores = []

    def addProfesor(self, profesor):
        self.profesores.append(profesor)

    def __iter__(self):
        yield 'Codigo', self.codigo
        yield 'Nombre', self.nombre
        yield 'Facultad', self.facultad
        yield 'Profesores', [dict(prof) for prof in self.profesores]


# def testDict():
#     h1 = Subject("Matemática", "ITBA")
#     h1.addProfesor(Professor("Uria"))
#
#     print(dict(h1))


def getMateriasPage(driver):
    even_mat = np.array(
        driver
            .find_element_by_tag_name("tbody")
            .find_elements_by_class_name("even")
    )

    odd_mat = np.array(
        driver
            .find_element_by_tag_name("tbody")
            .find_elements_by_class_name("odd")
    )

    mat_list = np.concatenate((even_mat, odd_mat))

    return mat_list

def main():
    driver = webdriver.Chrome()
    driver.get(base)

    i = input("Press enter to begin")

    driver.find_element_by_id("id1").submit()

    i = input("Press enter to begin")

    driver.find_element_by_link_text('Académica').click()
    driver.find_element_by_link_text('Cursos').click()

    materias = []

    for number in range(1, 2):
        if number != 1:
            driver.find_element_by_link_text("%d" % number).click()

        mat_list = getMateriasPage(driver)
        for current in range(3):#len(mat_list)):
            time.sleep(.01)
            try:
                materia = Subject(
                    getMateriasPage(driver)[current].find_elements_by_tag_name("td")[0].text,
                    getMateriasPage(driver)[current].find_elements_by_tag_name("td")[1].text,
                    "ITBA"
                )

                getMateriasPage(driver)[current].find_elements_by_tag_name("td")[9]\
                .find_element_by_tag_name("span")\
                .find_element_by_tag_name("span").click()

                profList = driver \
                    .find_element_by_class_name("tab-panel") \
                    .find_elements_by_tag_name("ul")
                print(profList)

                for prof in profList:
                    ProfName = prof.find_element_by_class_name("fontSize14").text

                    materia.addProfesor(Professor(ProfName))

                materias.append(dict(materia))
            except:
                print("Error en ", number,"-", current)

            driver.back()

    file = open("materiasItba.json", "w+", encoding='utf8')
    file.write(json.dumps(materias))


    #
    # print("nombre = ",name)

    i = input("Press enter to begin")


if __name__ == '__main__':
    main()
