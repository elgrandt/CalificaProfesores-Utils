
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import unicodedata
import json
import time
from common import *
import numpy as np


base = 'https://sga.itba.edu.ar'


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

    form = driver.find_element_by_id('id1')
    nameInput = form.find_element_by_css_selector('input[name=user]')
    passwordInput = form.find_element_by_css_selector('input[name=password]')
    nameInput.send_keys(input("Ingrese el usuario: "))
    passwordInput.send_keys(input("Ingrese la password: "))

    form.submit()

    driver.find_element_by_link_text('Académica').click()
    driver.find_element_by_link_text('Cursos').click()

    for number in range(1, 2):
        if number != 1:
            driver.find_element_by_link_text("%d" % number).click()

        mat_list = getMateriasPage(driver)
        for current in range(3):#len(mat_list)):
            time.sleep(.01)
            try:
                codigo = getMateriasPage(driver)[current].find_elements_by_tag_name("td")[0].text
                materia = Subject(
                    getMateriasPage(driver)[current].find_elements_by_tag_name("td")[1].text + "-" + codigo,
                    "Instituto Tecnológico de Buenos Aires",
                    "itba"
                )

                getMateriasPage(driver)[current].find_elements_by_tag_name("td")[9]\
                .find_element_by_tag_name("span")\
                .find_element_by_tag_name("span").click()

                profList = driver \
                    .find_element_by_class_name("tab-panel") \
                    .find_elements_by_tag_name("ul")

                for prof in profList:
                    ProfName = prof.find_element_by_class_name("fontSize14").text

                    materia.addProfesor(ProfName)

                subjects.append(dict(materia))
            except Exception as e:
                print(e)
                print("Error en ", number,"-", current)

            driver.back()


if __name__ == '__main__':
    cargarData()
    main()
    guardarData()
