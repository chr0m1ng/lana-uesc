# coding=utf8
from helpers.helper_uesc import Helper
from helpers.strings import ErrorStrings, GeneralStrings
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities    
# from importlib import reload
import sys
import os
import json

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
        self.driver, status = self.uesc_helper.IsUESCDown(self.driver)
        if status == False:
            self.driver, status = self.uesc_helper.GoToGraduationCoursesPage(self.driver)
            if status == True:
                self.driver, courses = self.uesc_helper.ListCoursesInGraduationCoursesPage(self.driver)
                if courses != {}:
                    response = 'Estes são os cursos de graduação da UESC:\n\n*Bacharelado*\n'
                    for bach in courses['bacharelado']:
                        response += '• [%s](%s)\n' % (bach['curso'], bach['site'])
                    response += '\n*Licenciatura*\n'
                    for lic in courses['licenciatura']:
                        response += '• [%s](%s)\n' % (lic['curso'], lic['site'])
                    response = response[:-1]
                    return {
                        'response' : response,
                        'type' : 'text',
                        'markdown' : True
                    }
                else:
                    return self.error_strings.GetGenericErrorMessage()
            else:
                return self.error_strings.GetGenericErrorMessage()
        else:
            return self.error_strings.GetUESCDownMessage()

    def UESC_Listar_Departamentos(self):
        self.driver, status = self.uesc_helper.IsUESCDown(self.driver)
        if status == False:
            self.driver, status = self.uesc_helper.GoToDepartmentsPage(self.driver)
            if status == True:
                self.driver, departments = self.uesc_helper.ListDepartmentsOnDepartmentsPage(self.driver)
                if departments != []:
                    response = 'Estes são os departamentos da UESC:\n'
                    for department in departments:
                        response += '• [%s](%s) - %s\n\n' % (department['sigla'], department['site'], department['departamento'])
                    response = response[:-2]
                    return {
                        'response' : response,
                        'type' : 'text',
                        'markdown' : True
                    }
                else:
                    return self.error_strings.GetGenericErrorMessage()
            else:
                return self.error_strings.GetGenericErrorMessage()
        else:
            return self.error_strings.GetUESCDownMessage()

    def UESC_Listar_Editais(self, params):
        return 'WiP'

    def UESC_Listar_Editais_Recentes(self):
        self.driver, status = self.uesc_helper.IsUESCDown(self.driver)
        if status == False:
            self.driver, edicts = self.uesc_helper.ListLastEdictsOnMainPage(self.driver)
            if edicts != []:
                response = 'Estes são os ultimos editais publicados no site da UESC:\n\n'
                for edict in edicts:
                    if len(edict['links']) > 0:
                        response += '*%s*\n' % (edict['titulo'])
                        for link in edict['links']:
                            response += '• [%s](%s)\n' % (link['titulo'], link['link']) 
                        response += '\n'
                response = response[:-2]
                return {
                    'response' : response,
                    'type' : 'text',
                    'markdown' : True
                }
            else:
                return self.error_strings.GetGenericErrorMessage()
        else:
            return self.error_strings.GetUESCDownMessage()

    def UESC_Listar_Editaisbens(self, params):
        return 'WiP'

    def UESC_Listar_Editaisbens_Recentes(self):
        return 'WiP'

    def UESC_Listar_Noticias(self, params):
        return 'WiP'

    def UESC_Listar_Noticias_Recentes(self):
        self.driver, status = self.uesc_helper.IsUESCDown(self.driver)
        if status == False:
            self.driver, news = self.uesc_helper.ListLastNewsOnMainPage(self.driver)
            if news != []:
                response = 'Estas são as ultimas noticias publicadas no site da UESC:\n'
                for n in news:
                    if len(n['links']) > 0:
                        response += '*%s*\n' % (n['titulo'])
                        for link in n['links']:
                            response += '• [%s](%s)\n' % (link['titulo'], link['link']) 
                        response += '\n'
                response = response[:-2]
                return {
                    'response' : response,
                    'type' : 'text',
                    'markdown' : True
                }
            else:
                return self.error_strings.GetGenericErrorMessage()
        else:
            return self.error_strings.GetUESCDownMessage()

    def UESC_Listar_Resultados(self, params):
        return 'WiP'

    def UESC_Listar_Resultados_Recentes(self):
        self.driver, status = self.uesc_helper.IsUESCDown(self.driver)
        if status == False:
            self.driver, results = self.uesc_helper.ListLastResultsOnMainPage(self.driver)
            if results != []:
                response = 'Estes são os ultimos resultados publicados no site da UESC:\n'
                for result in results:
                    if len(result['links']) > 0:
                        response += '*%s*\n' % (result['titulo'])
                        for link in result['links']:
                            response += '• [%s](%s)\n' % (link['titulo'], link['link']) 
                        response += '\n'
                response = response[:-2]
                return {
                    'response' : response,
                    'type' : 'text',
                    'markdown' : True
                }
            else:
                return self.error_strings.GetGenericErrorMessage()
        else:
            return self.error_strings.GetUESCDownMessage()


if __name__ == '__main__':
    bot_uesc = Bot()
    bot_uesc.driver, res = bot_uesc.uesc_helper.IsUESCDown(bot_uesc.driver)
    print (res)
    bot_uesc.driver, res = bot_uesc.uesc_helper.ListLastResultsOnMainPage(bot_uesc.driver)
    print (res)
    bot_uesc.__del__()