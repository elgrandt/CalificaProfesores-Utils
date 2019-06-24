import requests
import json
from bs4 import BeautifulSoup
from json import JSONEncoder

subjects = []
professors = {}

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def getPage(url):
    return BeautifulSoup(requests.get(url).content, 'html.parser')

def generateJson(object):
    return json.dumps(object, cls=MyEncoder, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

def cargarData():
    file = open("materias.json", "r")
    subjects = json.loads(file.read())
    file.close()

    file = open("profesores.json", "r")
    professors = json.loads(file.read())
    file.close()

def guardarData():
    file = open("materias.json", "w+")
    file.write(generateJson(subjects))
    file.close()

    file = open("profesores.json", "w+")
    file.write(generateJson(professors))
    file.close()

class Professor:
    def __init__(self, id, nombre):
        self.id = id
        self.create = True
        self.erase = False
        self.facultades = {}
        self.materias = {}
        self.profName = nombre
        self.timestamp = 0

    def __iter__(self):
        yield "id", self.id
        yield "create", self.create
        yield "erase", self.erase
        yield "facultades", self.facultades
        yield "materias", self.materias
        yield "profName", self.profName
        yield "timestamp", self.timestamp

class Subject:
    def __init__(self, nombre, facultad, facultadName):
        self.Facultad = facultad
        self.FacultadName = facultadName
        self.ShownName = nombre
        self.prof = {}

    def addProfesor(self, profesor):
        if not profesor in professors:
            professors[profesor] = Professor(len(professors), profesor)
        self.prof[professors[profesor].id] = profesor

    def __iter__(self):
        yield 'Facultad', self.Facultad
        yield 'FacultadName', self.FacultadName
        yield 'ShownName', self.ShownName
        yield 'prof', self.prof