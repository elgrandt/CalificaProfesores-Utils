from common import getPage
import re

base = 'http://encuestas_finales.exactas.uba.ar/'

def procesarPeriodos():
    url = 'http://encuestas_finales.exactas.uba.ar/periodos.html'
    page = getPage(url)
    for tr in page.select_one(".content").select("tr"):
        td = tr.select('td')[1]
        href = td.a.attrs["href"]
        processCuat(base+href)

def processCuat(url):
    cuatid = int(re.search(r'\d+', url).group())
    if cuatid != 1563: return
    for mat_page in range(10):
        page = getPage('%s#l_mu%s_%s' % (url, cuatid, mat_page))
        lst = page.select_one('#list_mu%s' % cuatid)
        materias = lst.select('li')
        print materias

if __name__ == '__main__':
    procesarPeriodos()