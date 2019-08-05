import requests
import json
from bs4 import BeautifulSoup
from json import JSONEncoder
import numpy as np


subjects = dict()
professors = dict()


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def getPage(url):
    return BeautifulSoup(requests.get(url).content, 'html.parser')


def generateJson(object):
    return json.dumps(
        object,
        cls=MyEncoder,
        sort_keys=True,
        indent=4,
        separators=(',', ': '),
        ensure_ascii=False
    )


def cargarData():
    file = open("materias.json", "r")
    
    subjects = json.loads(file.read())
    file.close()

    file = open("profesores.json", "r")
    professors = json.loads(file.read())
    file.close()


def guardarData(filename = "materias.json"):
    file = open(filename, "w+")
    file.write(generateJson(subjects))
    file.close()

    file = open("profesores.json", "w+")
    file.write(generateJson(professors))
    file.close()


class Professor:
    def __init__(self, nombre):
        self.profName = ''.join(nombre.split(","))
        self.facultades = []

    def __iter__(self):
        yield "facultades", self.facultades
        yield "materias", self.materias

    def __eq__(self, other):
        return self.profName == other.profName

    def __hash__(self):
        return hash(str(self))


class Subject:
    def __init__(self, nombre, facultad, facultadName, facultadId):
        self.Facultad = facultad
        self.FacultadName = facultadName
        self.facultadId = facultadId

        self.name = nombre
        self.prof = []
        self.timestamp = 0

    def addProfesor(self, name):
        name = ''.join(name.split(","))

        if not name in professors:
            professors[name] = Professor(name)
            professors[name].facultades.append(self.FacultadName)

        self.prof.append(professors[name].profName)

    def __iter__(self):
        yield 'Facultad', self.Facultad
        yield 'FacultadName', self.FacultadName
        yield 'ShownName', self.name
        yield 'prof', self.prof

