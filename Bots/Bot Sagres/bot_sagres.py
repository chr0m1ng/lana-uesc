# coding=utf8
from helpers.helper_sagres import Helper
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

    def __del__(self):
        self.driver.quit()

    def Sagres(self):
        return 'ABOUT'

    def Sagres_Calcular_CRAA(self, params):
        self.driver, status = self.sagres_helper.IsSagresDown(self.driver)
        if status == False:
            self.driver, status = self.sagres_helper.Login(self.driver, params['sagres_username'], params['sagres_password'])
            if status == True:
                self.driver, status = self.sagres_helper.IsAluno(self.driver)
                if status == True:
                    self.driver, craa = self.sagres_helper.CalculateCRAA(self.driver)
                    if craa != '':
                        return {
                            'response' : 'Aqui está, seu CRAA é %s' % (craa),
                            'type' : 'text'
                        }
                    else:
                        return self.sagres_helper.GetGenericErrorMessage()
                else:
                    return self.sagres_helper.GetNotAllowedMessage(params['sagres_username'], params['sagres_password'], 'aluno')
            else:
                return self.sagres_helper.GetLoginErrorMessage(params['sagres_username'], params['sagres_password'])
        else:
            return self.sagres_helper.GetSagresDownMessage()

    def Sagres_Horarios_Corrente(self, params):
        self.driver, status = self.sagres_helper.IsSagresDown(self.driver)
        if status == False:
            self.driver, status = self.sagres_helper.Login(self.driver, params['sagres_username'], params['sagres_password'])
            if status == True:
                self.driver, schedule_url = self.sagres_helper.GetSemesterSchedule(self.driver)
                if schedule_url != '':
                    return {
                        'response' : schedule_url,
                        'type' : 'image'
                    }
                else:
                    return self.sagres_helper.GetGenericErrorMessage()
            else:
                return self.sagres_helper.GetLoginErrorMessage(params['sagres_username'], params['sagres_password'])
        else:
            return self.sagres_helper.GetSagresDownMessage()

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
        self.driver, status = self.sagres_helper.IsSagresDown(self.driver)
        if status == False:
            self.driver, status = self.sagres_helper.Login(self.driver, params['sagres_username'], params['sagres_password'])
            if status == True:
                self.driver, status = self.sagres_helper.IsAluno(self.driver)
                if status == True:
                    self.driver, status = self.sagres_helper.GoToTabPortalDoAluno(self.driver)
                    print(status)
                    if status == True:
                        self.driver, courses = self.sagres_helper.ListFaultsOnTabPortalDoAluno(self.driver)
                        if courses != []:
                            response = ''
                            for course in courses:
                                response += '• %s\nTotal de Faltas: %s faltas\nLimite de Faltas: %s faltas\n\n' % (course['disciplina'], course['faltas'], course['limite_faltas'])
                            response = response[:-2]
                            return {
                                'response' : response,
                                'type' : 'text'
                            }
                        else:
                            print(courses)
                            return self.sagres_helper.GetGenericErrorMessage()
                    else:
                        return self.sagres_helper.GetGenericErrorMessage()
                else:
                    return self.sagres_helper.GetNotAllowedMessage(params['sagres_username'], params['sagres_password'], 'aluno')
            else:
                return self.sagres_helper.GetLoginErrorMessage(params['sagres_username'], params['sagres_password'])
        else:
            return self.sagres_helper.GetSagresDownMessage()

    def Sagres_Listar_Faltas_Disciplina(self, params):
        self.driver, status = self.sagres_helper.IsSagresDown(self.driver)
        if status == False:
            self.driver, status = self.sagres_helper.Login(self.driver, params['sagres_username'], params['sagres_password'])
            if status == True:
                self.driver, status = self.sagres_helper.IsAluno(self.driver)
                if status == True:
                    self.driver, status = self.sagres_helper.GoToTabPortalDoAluno(self.driver)
                    if status == True:
                        self.driver, faults, err = self.sagres_helper.ListCourseFaults(self.driver, params['codigo_disciplina'])
                        if err == False and type(faults) == type({}) and faults != {}:
                            response = '%s\n• %s' % (faults['curso'], faults['faltas_e_limite'])
                            return {
                                'response' : response,
                                'type' : 'text'
                            }
                        elif err == True:
                            return self.sagres_helper.GetNoSuchCourseErrorMessage(params['codigo_disciplina'])
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

    def Sagres_Listar_Notas(self, params):
        self.driver, status = self.sagres_helper.IsSagresDown(self.driver)
        if status == False:
            self.driver, status = self.sagres_helper.Login(self.driver, params['sagres_username'], params['sagres_password'])
            if status == True:
                self.driver, status = self.sagres_helper.IsAluno(self.driver)
                if status == True:
                    self.driver, status = self.sagres_helper.GoToTabPortalDoAluno(self.driver)
                    if status == True:
                        self.driver, courses = self.sagres_helper.ListAvgOnTabPortalDoAluno(self.driver)
                        if courses != []:
                            response = ''
                            for course in courses:
                                response += '• %s\nMédia: %s\n\n' % (course['disciplina'], course['media'])
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

    def Sagres_Listar_Turmas(self, params):
        return 'OK'

    def Sagres_Listar_Alunos_Turmas(self, params):
        return 'OK'
        
# if __name__ == '__main__':
#     bot = Bot()
#     bot.driver, res = bot.sagres_helper.IsSagresDown(bot.driver)
#     print (res)
#     bot.driver, res = bot.sagres_helper.Login(bot.driver, 'grsantos13', '201420374')
#     print (res)
#     bot.driver, res = bot.sagres_helper.GetSemesterSchedule(bot.driver)
#     print (res)
#     bot.driver.quit()
