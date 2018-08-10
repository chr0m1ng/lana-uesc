# coding=utf8
from helper_sagres import Helper
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities    
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

DESIREDCAPS = DesiredCapabilities.CHROME
DESIREDCAPS ['loggingPrefs'] = { 'browser':'ALL' }
OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument('headless')

class Bot():
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=OPTIONS, desired_capabilities=DESIREDCAPS)
        self.sagres_helper = Helper()

    def Sagres(self):
        return 'ABOUT'

    def Sagres_Calcular_CRAA(self, params):
        return 'ok'

    def Sagres_Horarios_Corrente(self, params):
        return 'ok'

    def Sagres_Listar_Disciplinas(self, params):
        self.driver, status = self.sagres_helper.IsSagresDown(self.driver)
        if status == False:
            self.driver, status = self.sagres_helper.Login(self.driver, params['sagres_username'], params['sagres_password'])
            if status == True:
                self.driver, status = self.sagres_helper.IsAluno(self.driver)
                if status == True:
                    self.driver, status = self.sagres_helper.GoToTabPortalDoAluno(self.driver)
                    if status == True:
                        self.driver, courses = self.sagres_helper.ListCoursesOnTabPortalDoAluno(self.driver)
                        if courses != []:
                            response = ''
                            for course in courses:
                                response += '• %s\nMédia: %s\nFaltas: %s\n\n' % (course['disciplina'], course['media'], course['faltas'])
                            response = response[:-2]
                            return {
                                'response' : response,
                                'type' : 'text'
                            }
                        else:
                            return self.sagres_helper.GetGenericErrorMessage()
                    else:
                        return self.sagres_helper.GetGenericErrorMessage()
                else:
                    return self.sagres_helper.GetNotAllowedMessage(params['sagres_username'], params['sagres_password'], 'aluno')
            else:
                return self.sagres_helper.GetLoginErrorMessage(params['sagres_username'], params['sagres_password'])
        else:
            return self.sagres_helper.GetSagresDownMessage()

    def Sagres_Listar_Disciplinas_Corrente(self, params):
        self.driver, status = self.sagres_helper.IsSagresDown(self.driver)
        if status == False:
            self.driver, status = self.sagres_helper.Login(self.driver, params['sagres_username'], params['sagres_password'])
            if status == True:
                self.driver, status = self.sagres_helper.IsAluno(self.driver)
                if status == True:
                    self.driver, status = self.sagres_helper.GoToPageDisciplinasCorrente(self.driver)
                    if status == True:
                        self.driver, courses = self.sagres_helper.ListCoursesOnPageDisciplinasCorrente(self.driver)
                        if courses != []:
                            response = ''
                            for course in courses:
                                if len(course['media']) == 6: #Tem escrito 'media:' sem nota
                                    media = 'Não divulgada'
                                else:
                                    media = course['media'][7:]
                                response += '• %s\nMédia: %s\nFaltas: %s\n\n' % (course['disciplina'], media, course['faltas'])
                            response = response[:-2]
                            return {
                                'response' : response,
                                'type' : 'text'
                            }
                        else:
                            return self.sagres_helper.GetGenericErrorMessage()
                    else:
                        return self.sagres_helper.GetGenericErrorMessage()
                else:
                    return self.sagres_helper.GetNotAllowedMessage(params['sagres_username'], params['sagres_password'], 'aluno')
            else:
                return self.sagres_helper.GetLoginErrorMessage(params['sagres_username'], params['sagres_password'])
        else:
            return self.sagres_helper.GetSagresDownMessage()

    def Sagres_Listar_Faltas(self, params):
        return self.Sagres_Listar_Disciplinas(params)

    def Sagres_Listar_Faltas_Disciplina(self, params):
        return 'ok'

    def Sagres_Listar_Notas(self, params):
        return self.Sagres_Listar_Disciplinas(params)

    def Sagres_Listar_Notas_Disciplina(self, params):
        self.driver, status = self.sagres_helper.IsSagresDown(self.driver)
        if status == False:
            self.driver, status = self.sagres_helper.Login(self.driver, params['sagres_username'], params['sagres_password'])
            if status == True:
                self.driver, status = self.sagres_helper.IsAluno(self.driver)
                if status == True:
                    self.driver, status = self.sagres_helper.GoToTabPortalDoAluno(self.driver)
                    if status == True:
                        self.driver, exams, err = self.sagres_helper.ListCourseCredits(self.driver, params['codigo_disciplina'])
                        if err == False and type(exams) == type([]) and exams != []:
                            response = '%s\n' % (exams[0]['curso'])
                            for exam in exams:
                                response += '• (%s) %s: %s\n' % (exam['tipo'], exam['credito'], exam['nota'])
                            response = response[:-1]
                            return {
                                'response' : response,
                                'type' : 'text'
                            }
                        elif err == True:
                            return self.sagres_helper.GetNoSuchCourseErrorMessage(params['codigo_disciplina'])
                        else:
                            return self.sagres_helper.GetNoCreditsYetForCourseErrorMessage(params['codigo_disciplina'])
                    else:
                        return self.sagres_helper.GetGenericErrorMessage()
                else:
                    return self.sagres_helper.GetNotAllowedMessage(params['sagres_username'], params['sagres_password'], 'aluno')
            else:
                return self.sagres_helper.GetLoginErrorMessage(params['sagres_username'], params['sagres_password'])
        else:
            return self.sagres_helper.GetSagresDownMessage()

# if __name__ == '__main__':
#     bot = Bot()
#     bot.driver, res = bot.sagres_helper.Login(bot.driver, 'grsantos13', '201420374')
#     print (res)
#     bot.driver, res = bot.sagres_helper.GoToTabPortalDoAluno(bot.driver)
#     print (res)
#     bot.driver, res = bot.sagres_helper.ListCourseCredits(bot.driver, 'cet098')
#     print (res)
#     bot.driver.quit()
