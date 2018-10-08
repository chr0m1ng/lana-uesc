# coding=utf8
from helpers.helper_uesc import Helper
from helpers.strings import ErrorStrings, GeneralStrings
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities    
from datetime import datetime
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
        self.driver, status = self.uesc_helper.IsUESCDown(self.driver)
        if status == False:
            self.driver, status = self.uesc_helper.GoToEdictsPage(self.driver)
            if status == True:
                self.driver, edicts, status = self.uesc_helper.ListEdictsOfDateOnEdictsPage(self.driver, params['date'])
                if status == True and edicts != []:
                    if len(edicts) == 1:
                        response = 'Este foi o edital publicado no site da UESC no dia %s:\n' % (params['date'])
                    else:    
                        response = 'Estes foram os editais publicados no site da UESC no dia %s:\n' % (params['date'])
                    for e in edicts:
                        response += '• [%s](%s)\n\n' % (e['titulo'], e['link'])
                    response = response[:-2]
                    return {
                        'response' : response,
                        'type' : 'text',
                        'markdown' : True
                    }
                elif status == True and edicts == []:
                    response = 'Nenhum edital do dia %s foi encontrado no site da UESC' % (params['date'])
                    return self.error_strings.GetNoEdictsErrorMessage(params['date'])
                else:
                    return self.error_strings.GetGenericErrorMessage()
            else:
                return self.error_strings.GetGenericErrorMessage()
        else:
            return self.error_strings.GetUESCDownMessage()

    def UESC_Listar_Editais_Recentes(self):
        self.driver, status = self.uesc_helper.IsUESCDown(self.driver)
        if status == False:
            self.driver, edicts = self.uesc_helper.ListLastEdictsOnMainPage(self.driver)
            if edicts != []:
                response = 'Estes foram os ultimos editais publicados no site da UESC:\n\n'
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
        self.driver, status = self.uesc_helper.IsUESCDown(self.driver)
        if status == False:
            self.driver, status = self.uesc_helper.GoToEditaisBensPage(self.driver)
            if status == True:
                self.driver, edicts, status = self.uesc_helper.ListEditaisBensOfDateOnEditaisBensPage(self.driver, params['date'])
                if status == True and edicts != []:
                    date_obj = datetime.strptime(params['date'], '%d/%m/%Y')
                    month_name = self.uesc_helper.MonthNumberToStringBR(date_obj.month).lower()
                    year = date_obj.year
                    response = 'Estes foram os editais de bens e serviços publicados no site da UESC no mês de %s em %s:\n\n*NÚMERO* - *DESCRIÇÃO* - *ABERTURA DO CERTAME*\n' % (month_name, year)
                    for edict in edicts:
                        response += '• [%s](%s) - %s - %s\n\n' % (edict['numero'], edict['link'], edict['descricao'], edict['abertura'])
                    response = response[:-2]
                    return {
                        'response' : response,
                        'type' : 'text',
                        'markdown' : True
                    }
                elif status == True and edicts == []:
                    date_obj = datetime.strptime(params['date'], '%d/%m/%Y')
                    return self.error_strings.GetNoEditaisBensErrorMessage(date_obj.strftime('%m/%Y'))
                else:
                    return self.error_strings.GetGenericErrorMessage()
            else:
                return self.error_strings.GetGenericErrorMessage()
        else:
            return self.error_strings.GetUESCDownMessage()

    def UESC_Listar_Editaisbens_Recentes(self):
        self.driver, status = self.uesc_helper.IsUESCDown(self.driver)
        if status == False:
            self.driver, status = self.uesc_helper.GoToEditaisBensPage(self.driver)
            if status == True:
                self.driver, edicts = self.uesc_helper.ListLastEditaisBensOnEditaisBensPage(self.driver)
                if edicts != []:
                    response = 'Estes foram os ultimos editais de bens e serviços publicados no site da UESC:\n\n*NÚMERO* - *DESCRIÇÃO* - *ABERTURA DO CERTAME*\n'
                    for edict in edicts:
                        response += '• [%s](%s) - %s - %s\n\n' % (edict['numero'], edict['link'], edict['descricao'], edict['abertura'])
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

    def UESC_Listar_Noticias(self, params):
        self.driver, status = self.uesc_helper.IsUESCDown(self.driver)
        if status == False:
            self.driver, status = self.uesc_helper.GoToNewsPage(self.driver)
            if status == True:
                self.driver, news, status = self.uesc_helper.ListNewsOfDateOnNewsPage(self.driver, params['date'])
                if status == True and news != []:
                    if len(news) == 1:
                        response = 'Esta foi a noticia publicada no site da UESC no dia %s:\n' % (params['date'])
                    else:    
                        response = 'Estas foram as noticias publicadas no site da UESC no dia %s:\n' % (params['date'])
                    for n in news:
                        response += '• [%s](%s)\n\n' % (n['titulo'], n['link'])
                    response = response[:-2]
                    return {
                        'response' : response,
                        'type' : 'text',
                        'markdown' : True
                    }
                elif status == True and news == []:
                    return self.error_strings.GetNoNewsErrorMessage(params['date'])
                else:
                    return self.error_strings.GetGenericErrorMessage()
            else:
                return self.error_strings.GetGenericErrorMessage()
        else:
            return self.error_strings.GetUESCDownMessage()

    def UESC_Listar_Noticias_Recentes(self):
        self.driver, status = self.uesc_helper.IsUESCDown(self.driver)
        if status == False:
            self.driver, news = self.uesc_helper.ListLastNewsOnMainPage(self.driver)
            if news != []:
                response = 'Estas foram as ultimas noticias publicadas no site da UESC:\n'
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