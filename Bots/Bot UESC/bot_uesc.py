# coding=utf8
from helpers.helper_uesc import Helper
from helpers.strings import ErrorStrings, GeneralStrings
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities    
# from importlib import reload
import sys
import os

reload(sys)
sys.setdefaultencoding("utf-8")


DESIREDCAPS = DesiredCapabilities.CHROME
DESIREDCAPS ['loggingPrefs'] = { 'browser':'ALL' }
OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument('--headless')
OPTIONS.add_argument('--no-sandbox')

class Bot():
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=OPTIONS, desired_capabilities=DESIREDCAPS)
        self.uesc_helper = Helper()
        self.error_strings = ErrorStrings()
        self.general_strings = GeneralStrings()

    def __del__(self):
        self.driver.quit()

    def UESC(self):
        return self.general_strings.GetAboutUESCMessage()

    def UESC_Listar_Cursos(self):
        return 'WiP'

    def UESC_Listar_Departamentos(self):
        return 'WiP'

    def UESC_Listar_Editais(self, params):
        return 'WiP'

    def UESC_Listar_Editais_Recentes(self):
        return 'WiP'

    def UESC_Listar_Editaisbens(self, params):
        return 'WiP'

    def UESC_Listar_Editaisbens_Recentes(self):
        return 'WiP'

    def UESC_Listar_Noticias(self, params):
        return 'WiP'

    def UESC_Listar_Noticias_Recentes(self):
        return 'WiP'

    def UESC_Listar_Resultados(self, params):
        return 'WiP'

    def UESC_Listar_Resultados_Recentes(self):
        return 'WiP'