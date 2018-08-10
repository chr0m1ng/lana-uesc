# coding=utf8
from selenium import webdriver
import time


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

    def ListCoursesOnTabPortalDoAluno(self, driver):
        try:
            titulos = driver.find_elements_by_xpath('//a[contains(@class, "webpart-aluno-nome")]')
            medias = driver.find_elements_by_xpath('//div[contains(@class, "webpart-aluno-links")]/div/a[contains(text(), "Média:")]/strong/span')
            faltas = driver.find_elements_by_xpath("//div[contains(@class, 'webpart-aluno-links')]/div/a[contains(., 'faltas')]/strong/span")
            courses = []
            for i in range(len(titulos)):
                courses.append({'disciplina' : titulos[i].text, 'media' : medias[i].text, 'faltas' : faltas[i].text})
        except:
            return driver, []
        return driver, courses

    # def ListDisciplineCredits(self, driver, code):
    #     try:
    #         mediaXpath = '//a[contains(@class, "webpart-aluno-nome") and contains(text(), "%s")]/../../div[contains(@class, "webpart-aluno-links")]/div/a[contains(text(), "Média:")]' % (code.upper())
    #         mediaId = driver.find_element_by_xpath(mediaXpath).get_attribute('id')
    #         driver.execute_script('document.getElementById("%s").click()' % (mediaId))
    #         while self.IsPageLoaded(driver) == False:
    #             print('carregando')
    #         tableXpath = '//div[contains(@class, "boletim-expandido")]/div/div/table/..'
    #         tableId = driver.find_elements_by_xpath(tableXpath)[0].get_attribute('id')
    #         driver.execute_script('var script = document.createElement("script");script.type = "text/javascript";script.src = "http://html2canvas.hertzen.com/dist/html2canvas.js";document.head.appendChild(script);')
    #         time.sleep(5)
    #         driver.execute_script('html2canvas(document.getElementById("%s")).then(canvas => console.log(canvas.toDataURL()));' % (tableId))
    #         time.sleep(5)
    #         print(driver.get_log('browser'))
    #     except Exception as exc:
    #         print(exc)
    #         return driver, []
    #     return driver, []

    # def IsPageLoaded(self, driver):
    #     print("Checking if {} page is loaded.".format(driver.current_url))
    #     page_state = driver.execute_script('return document.readyState;')
    #     return page_state == 'complete'

    def ListCourseCredits(self, driver, code):
        try:
            code = code.upper()
            course = driver.find_element_by_xpath('//a[contains(@class, "webpart-aluno-nome") and contains(text(), "%s")]' % (code)).text
            mediaXpath = '//a[contains(@class, "webpart-aluno-nome") and contains(text(), "%s")]/../../div[contains(@class, "webpart-aluno-links")]/div/a[contains(text(), "Média:")]' % (code.upper())
            mediaId = driver.find_element_by_xpath(mediaXpath).get_attribute('id')
            driver.execute_script('document.getElementById("%s").click()' % (mediaId))
            titulos = driver.find_elements_by_xpath('//div[contains(@class, "boletim-expandido")]/div/div/table/tbody/tr/td[@class="ident"]/span')
            creditos = driver.find_elements_by_xpath('//div[contains(@class, "boletim-expandido")]/div/div/table/tbody/tr/td[@class="txt-center"]/span')
            notas = []
            for i in range(len(titulos)):
                tipo = titulos[i].find_elements_by_xpath('../../preceding-sibling::tr/th')
                if len(tipo) == 1:
                    j = 0
                else:
                    j = 1
                notas.append({'curso' : course, 'tipo' : tipo[j].text, 'credito' : titulos[i].text, 'nota' : creditos[i].text})
        except:
            return driver, '', True
        return driver, notas, False

    def GetNoSuchCourseErrorMessage(self, code):
        return {
            'response' : 'Não foi possivel encontrar a disciplina %s dentre as já cursadas' % (code),
            'type' : 'text'
        }
    
    def GetNoCreditsYetForCourseErrorMessage(self, code):
        return {
            'response' : 'Ainda não existem notas cadastradas para a disciplina %s' % (code),
            'type' : 'text'
        }