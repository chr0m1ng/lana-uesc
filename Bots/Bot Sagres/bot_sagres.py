# coding=utf8
from helper_sagres import Helper
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument('headless')

class Bot():
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=OPTIONS)
        self.sagres_helper = Helper()

    def Sagres(self):
        return 'ABOUT'

    def Sagres_Calcular_CRAA(self, params):
        return 'ok'

    def Sagres_Horarios_Corrente(self, params):
        return 'ok'

    def Sagres_Listar_Disciplinas(self, params):
        return 'ok'

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
                                    media = 'Média não disponivel'
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
        return 'ok'

    def Sagres_Listar_Faltas_Disciplina(self, params):
        return 'ok'

    def Sagres_Listar_Notas(self, params):
        return 'ok'

    def Sagres_Listar_Notas_Disciplina(self, params):
        return 'ok'

# if __name__ == '__main__':
#     bot = Bot()
#     bot.driver, res = bot.sagres_helper.Login(bot.driver, 'grsantos13', '201420374')
#     print (res)
#     bot.driver, res = bot.sagres_helper.GoToPageDisciplinasCorrente(bot.driver)
#     bot.driver, res = bot.sagres_helper.ListCoursesOnPageDisciplinasCorrente(bot.driver)
#     bot.driver.quit()
