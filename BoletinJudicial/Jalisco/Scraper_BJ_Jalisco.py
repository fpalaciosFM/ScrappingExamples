from traceback import print_exc
from datetime import datetime
from requests import Session
from pprint import pprint
from bs4 import BeautifulSoup

dict_juzgados = {
	'C01': 'JUZGADO PRIMERO DE LO CIVIL',
	'C02': 'JUZGADO SEGUNDO DE LO CIVIL',
	'C03': 'JUZGADO TERCERO DE LO CIVIL',
	'C04': 'JUZGADO CUARTO DE LO CIVIL',
	'C05': 'JUZGADO QUINTO DE LO CIVIL',
	'C06': 'JUZGADO SEXTO DE LO CIVIL',
	'C07': 'JUZGADO SEPTIMO DE LO CIVIL',
	'C08': 'JUZGADO OCTAVO DE LO CIVIL',
	'C09': 'JUZGADO NOVENO DE LO CIVIL',
	'C10': 'JUZGADO DECIMO DE LO CIVIL',
	'C11': 'JUZGADO DECIMO PRIMERO DE LO CIVIL',
	'C12': 'JUZGADO DECIMO SEGUNDO DE LO CIVIL',
	'C13': 'JUZGADO DECIMO TERCERO DE LO CIVIL',
	'F01': 'JUZGADO PRIMERO DE LO FAMILIAR',
	'F02': 'JUZGADO SEGUNDO DE LO FAMILIAR',
	'F03': 'JUZGADO TERCERO DE LO FAMILIAR',
	'F04': 'JUZGADO CUARTO DE LO FAMILIAR',
	'F05': 'JUZGADO QUINTO DE LO FAMILIAR',
	'F06': 'JUZGADO SEXTO DE LO FAMILIAR',
	'F07': 'JUZGADO SEPTIMO DE LO FAMILIAR',
	'F08': 'JUZGADO OCTAVO DE LO FAMILIAR',
	'F09': 'JUZGADO NOVENO DE LO FAMILIAR',
	'F10': 'JUZGADO DECIMO DE LO FAMILIAR',
	'F12': 'JUZGADO DECIMO SEGUNDO DE LO FAMILIAR',
	'F13': 'JUZGADO DECIMO TERCERO DE LO FAMILIAR',
	'M01': 'JUZGADO PRIMERO DE LO MERCANTIL',
	'M02': 'JUZGADO SEGUNDO DE LO MERCANTIL',
	'M03': 'JUZGADO TERCERO DE LO MERCANTIL',
	'M04': 'JUZGADO CUARTO DE LO MERCANTIL',
	'M05': 'JUZGADO QUINTO DE LO MERCANTIL',
	'M06': 'JUZGADO SEXTO DE LO MERCANTIL',
	'M07': 'JUZGADO SEPTIMO DE LO MERCANTIL',
	'M08': 'JUZGADO OCTAVO DE LO MERCANTIL',
	'M09': 'JUZGADO NOVENO DE LO MERCANTIL',
	'M10': 'JUZGADO DECIMO DE LO MERCANTIL',
	'OM01': 'JUZGADO PRIMERO ESPECIALIZADO EN MATERIA ORAL MERCANTIL',
	'OM02': 'JUZGADO SEGUNDO ESPECIALIZADO EN MATERIA ORAL MERCANTIL',
	'OM03': 'JUZGADO TERCERO ESPECIALIZADO EN MATERIA ORAL MERCANTIL',
	'OM04': 'JUZGADO CUARTO ESPECIALIZADO EN MATERIA ORAL MERCANTIL',
	'OM05': 'JUZGADO QUINTO ESPECIALIZADO EN MATERIA ORAL MERCANTIL',
	'OM06': 'JUZGADO SEXTO ESPECIALIZADO EN MATERIA ORAL MERCANTIL',
	'OM07': 'JUZGADO SEPTIMO ESPECIALIZADO EN MATERIA ORAL MERCANTIL',
	'OM08': 'JUZGADO OCTAVO ESPECIALIZADO EN MATERIA ORAL MERCANTIL',
	'OM09': 'JUZGADO NOVENO ESPECIALIZADO EN MATERIA ORAL MERCANTIL',
	'XF1': 'JUZGADO DECIMO PRIMERO ESPECIALIZADO DE LO FAMILIAR'
}

class ScraperBoletinJalisco():
	def __init__(self, id_juzgado, nombre_juzgado, fecha):
		self.id_juzgado = id_juzgado
		self.nombre_juzgado = nombre_juzgado
		self.fecha = fecha
		self.session = Session()

		self.intentos_max = 3
		self.timeout = 10

	def print_status(self, type_alert, message):
		print(f'[{type_alert}] -- id_juzgado:{self.id_juzgado}, nombre_juzgado:{self.nombre_juzgado}, fecha:{self.fecha}::\t\t {message}')

	def request_get_juzgados(self):
		self.print_status('R', 'scrap_juzgados')
		url = 'http://cjj.judicaturajalisco.net/Boletin.php'
		r_juzgados = None

		for intento in range(self.intentos_max):
			try:
				r_juzgados = self.session.get(url, timeout=self.timeout)
				if r_juzgados and r_juzgados.status_code == 200:
					break
			except:
				print_exc()
				self.print_status('E', '')

		return r_juzgados

	def scrap_juzgados(self):
		self.print_status('X', 'scrap_juzgados')
		dict_juzgados = None

		r_juzgados = self.request_get_juzgados()
		if not r_juzgados or r_juzgados.status_code != 200:
			return 'f', 'f'

		soup_juzgados = BeautifulSoup(r_juzgados.content, 'html.parser')
		soup_juzgados_select = soup_juzgados.find('option', class_='campos')
		soup_juzgados_options = soup_juzgados_select.find_all('option')

		dict_juzgados = { option.get('value') : option.getText().strip() for option in soup_juzgados_options }

		return dict_juzgados, 'ok'

if __name__ == '__main__':
	print('[X] -- Scraper_BJ_Jalisco Main')
	scraper = ScraperBoletinJalisco('a', 'b', 'c')
	pprint( scraper.scrap_juzgados() )
