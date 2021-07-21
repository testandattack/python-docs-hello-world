import datetime
from bs4 import BeautifulSoup
import requests
from bottle import run, post, request, response, get, route
from json import dumps
from datetime import datetime
from collections import OrderedDict
def parse():
    table_content = []
    values_21 = []
    values_20 = []
    values_19 = []
    url = 'https://www.tsa.gov/coronavirus/passenger-throughput'
    #url = 'https://www.transtats.bts.gov/Data_Elements.aspx?Data=5'
    NO_PROXY = {
        'no': 'pass',
    }
    page = requests.get(url,proxies=NO_PROXY,verify=False)
    soup = BeautifulSoup(page.content, "html.parser")
    rows = soup.find_all("table")[0].find("tbody").find_all("tr")
    todaysdate = datetime.now()
    #+ str(todaysdate.year)
    #.strftime('%d-%b'))
    cont = 0
    for row in rows:
        cells = row.find_all("td")
        value_21 = int(cells[1].get_text().strip().replace(",","")) if cells[1].get_text().strip() is not "" else 0
        value_20 = int(cells[2].get_text().strip().replace(",","")) if cells[2].get_text().strip() is not "" else 0
        value_19 = int(cells[3].get_text().strip().replace(",","")) if cells[3].get_text().strip() is not "" else 0
        json_object21 = {'name':cells[0].get_text().strip() [:-4]+ str(todaysdate.year), 'value': value_21}
        json_object20 = {'name':cells[0].get_text().strip() [:-4]+ str(todaysdate.year), 'value': value_20}
        json_object19 = {'name':cells[0].get_text().strip() [:-4]+ str(todaysdate.year), 'value' : value_19}
        values_21.append(json_object21)
        values_20.append(json_object20)
        values_19.append(json_object19)
    values_21 = sorted(values_21, key=lambda x: datetime.strptime(x['name'], '%m/%d/%Y'))
    values_20 = sorted(values_20, key=lambda x: datetime.strptime(x['name'], '%m/%d/%Y'))
    values_19 = sorted(values_19, key=lambda x: datetime.strptime(x['name'], '%m/%d/%Y'))
    for value in values_19:
        datetime.strptime(value['name'],'%m/%d/%Y').strftime('%b/%d')
    for value in values_20:
        datetime.strptime(value['name'],'%m/%d/%Y').strftime('%b/%d')
    for value in values_21:
        datetime.strptime(value['name'],'%m/%d/%Y').strftime('%b/%d')
    json_2021 = {'name':'2021', 'series': values_21}
    json_2020 = {'name':'2020', 'series': values_20}
    json_2019 = {'name':'2019', 'series': values_19}
    table_content.append(json_2021)
    table_content.append(json_2020)
    table_content.append(json_2019)
    return table_content
@route('/parser',method = 'GET')
def process():
    # set CORS headers
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    response.content_type = 'application/json'
    data = parse()
    return dumps(data)
run(host='localhost', port=8080, debug=True)