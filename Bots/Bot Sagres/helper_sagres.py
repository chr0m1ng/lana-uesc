# coding=utf8
from selenium import webdriver

class Helper():
    def IsSagresDown(self, driver):
        try:
            driver.get('http://www.prograd.uesc.br/PortalSagres/Acesso.aspx')
            if driver.find_elements_by_class_name('label-padrao') == []:
                return driver, True
        except:
            return driver, True
        return driver, False

    def GetSagresDownMessage(self):
        return {
            'response' : 'O Portal Sagres está fora do ar',
            'type' : 'text'
        }

    def Login(self, driver, user, password):
        try:
            driver.get('http://www.prograd.uesc.br/PortalSagres/Acesso.aspx')
            input_login = driver.find_elements_by_class_name('input-login') #Campo login [0] Campo senha [1]
            input_login[0].send_keys(user)
            input_login[1].send_keys(password)
            driver.find_element_by_id('ctl00_PageContent_LoginPanel_LoginButton').click() #Clica para entrar
            try: #Testa se conseguiu fazer o login verificando se existe o nome no canto superior esquerdo
                driver.find_element_by_class_name('usuario-nome').text
            except:
                return driver, False
        except:
            return driver, False
        return driver, True

    def GetLoginErrorMessage(self, user, password):
        return {
                    'response' : 'O usuario ou a senha do Portal Sagres passados estão incorretos',
                    'type' : 'text',
                    'inputError' : True,
                    'inputs' : [
                        {'param': 'sagres_username', 'value' : user},
                        {'param': 'sagres_password', 'value' : password}
                    ]
                }

    def IsAluno(self, driver):
        try:
            driver.find_element_by_xpath("//span[@oldtitle='Minhas Turmas']")
        except:
            return driver, False
        return driver, True

    def GetNotAllowedMessage(self, user, password, shoudlBe):
        return {
            'response' : 'Esta funcionalidade só é permitido para %s' % (shoudlBe),
            'type' : 'text',
            'inputError' : True,
            'inputs' : [
                {'param': 'sagres_username', 'value' : user},
                {'param': 'sagres_password', 'value' : password}
            ]
        }

    def GoToTabPortalDoAluno(self, driver):
        try:
            driver.get('http://www.prograd.uesc.br/PortalSagres/Modules/Diario/Aluno/Default.aspx')
            driver.find_element_by_class_name('controle-menu-txt') #Troca de pagina e tenta achar botão 'menu' do canto esquerdo que so aparece em portal do aluno
        except:
            return driver, False
        return driver, True

    def GoToPageDisciplinasCorrente(self, driver):
        try:
            driver.get('http://www.prograd.uesc.br/PortalSagres/Modules/Diario/Aluno/Relatorio/Boletim.aspx')
            if driver.find_element_by_id('ctl00_PageTitle').text == 'Notas e faltas':
                return driver, True
            else:
                return driver, False
        except:
            return driver, False

    def GetGenericErrorMessage(self):
        return {
            'response' : 'Erro interno ao tentar acessar recurso do sagres',
            'type' : 'text'
        }
    
    def ListCoursesOnPageDisciplinasCorrente(self, driver):
        try:
            titulos = driver.find_elements_by_class_name('boletim-item-titulo')
            medias = driver.find_elements_by_xpath("//a[@class='boletim-botao']/span[contains(text(), 'Média:')]")
            faltas = driver.find_elements_by_class_name('cabecalho_numero_faltas')
            courses = []
            for i in range(len(titulos)):
                courses.append({'disciplina' : titulos[i].text, 'media' : medias[i].text, 'faltas' : faltas[i].text})
        except:
            return driver, []
        return driver, courses
            