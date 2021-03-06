# coding=utf8
from selenium import webdriver
from datetime import datetime
import requests
import time
import json
import re

class Helper():

    def MonthNumberToStringBR(self, month):
        months = ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        try:
            month_name = months[month]
            return month_name
        except:
            return 'Mes Inexistente'
            
    def IsUESCDown(self, driver):
        try:
            driver.get('http://www.uesc.br')
            driver.find_element_by_id('conteudo-index-esquerda')
        except Exception as exc:
            print (exc)
            return driver, True
        return driver, False

    def GoToGraduationCoursesPage(self, driver):
        try:
            driver.get('http://www.uesc.br/cursos/graduacao/')
            driver.find_element_by_id('conteudo-interno')
        except Exception as exc:
            print (exc)
            return driver, False
        return driver, True

    def ListCoursesInGraduationCoursesPage(self, driver):
        try:
            bach_courses = driver.find_elements_by_xpath('//div[@id="CollapsiblePanel1"]/div/ul/li/a')
            lic_courses = driver.find_elements_by_xpath('//div[@id="CollapsiblePanel1"]/div/div/ul/li/a')
            courses = {
                'bacharelado' : [],
                'licenciatura' : []
            }
            for bach in bach_courses:
                if bach.get_attribute('innerText').strip():
                    courses['bacharelado'].append({'curso' : bach.get_attribute('innerText'), 'site' : bach.get_attribute('href')})
            for lic in lic_courses:
                if lic.get_attribute('innerText') != ''.strip():
                    courses['licenciatura'].append({'curso' : lic.get_attribute('innerText'), 'site' : lic.get_attribute('href')})
        except Exception as exc:
            print (exc)
            return driver, {}
        return driver, courses

    def GoToDepartmentsPage(self, driver):
        try:
            driver.get('http://www.uesc.br/departamentos/')
            if driver.find_element_by_xpath('//div[@id="conteudo-interno"]/h2/strong').text == 'DEPARTAMENTOS':
                return driver, True
            else:
                return driver, False
        except Exception as exc:
            print (exc)
            return driver, False

    def ListDepartmentsOnDepartmentsPage(self, driver):
        try:
            departments_names = driver.find_elements_by_xpath('//div[@id="conteudo-interno"]/table/tbody/tr/td/strong[contains(text(), "Departamento")]')
            departments_siglas_links = driver.find_elements_by_xpath('//div[@id="conteudo-interno"]/table/tbody/tr/td/strong/a')
            departments = []
            for i in range(len(departments_names)):
                departments.append({
                    'departamento' : departments_names[i].get_attribute('innerText'),
                    'sigla' : departments_siglas_links[i].get_attribute('text'),
                    'site' : departments_siglas_links[i].get_attribute('href')
                })
        except Exception as exc:
            print (exc)
            return driver, []
        return driver, departments

    def ListLastEdictsOnMainPage(self, driver):
        try:
            edicts_names = driver.find_elements_by_xpath('//div[contains(@class, "boxIndex")]/h2[contains(text(), "Editais")]/following-sibling::div[@id="barra-titulo-interno"]/p/strong') 
            edicts_names = filter(lambda x: x.text.strip(), edicts_names)    
            edicts = []
            for i in range(len(edicts_names)):
                if i == 0:
                    edict_infos_links = driver.find_elements_by_xpath('//div[contains(@class, "boxIndex")]/h2[contains(text(), "Editais")]/following-sibling::div[@id="barra-titulo-interno"]/p/a[following-sibling::strong[contains(., "%s")]]' % (edicts_names[1].text))
                elif i == len(edicts_names) - 1:
                    edict_infos_links = driver.find_elements_by_xpath('//div[contains(@class, "boxIndex")]/h2[contains(text(), "Editais")]/following-sibling::div[@id="barra-titulo-interno"]/p/a[preceding-sibling::strong[contains(., "%s")]]' % (edicts_names[i].text))
                else:
                    edict_infos_links = driver.find_elements_by_xpath('//div[contains(@class, "boxIndex")]/h2[contains(text(), "Editais")]/following-sibling::div[@id="barra-titulo-interno"]/p/a[preceding-sibling::strong[contains(., "%s")] and following-sibling::strong[contains(., "%s")]]' % (edicts_names[i].text, edicts_names[i + 1].text))
                edicts.append({
                    'titulo' : edicts_names[i].text,
                    'links' : []
                })
                for eil in edict_infos_links:
                    edicts[i]['links'].append({
                        'titulo' : eil.text,
                        'link' : eil.get_attribute('href')
                    })
        except Exception as exc:
            print (exc)
            return driver, []
        return driver, edicts

    def ListLastNewsOnMainPage(self, driver):
        try:
            news_names = driver.find_elements_by_xpath('//div[contains(@class, "boxIndex")]/h2[contains(text(), "Notícias")]/following-sibling::div[@id="barra-titulo-interno"]/p/strong')
            news_names = filter(lambda x: x.text.strip(), news_names)    
            news = []
            for i in range(len(news_names)):
                if i == 0:
                    news_infos_links = driver.find_elements_by_xpath('//div[contains(@class, "boxIndex")]/h2[contains(text(), "Notícias")]/following-sibling::div[@id="barra-titulo-interno"]/p/a[following-sibling::strong[contains(., "%s")]]' % (news_names[1].text))
                elif i == len(news_names) - 1:
                    news_infos_links = driver.find_elements_by_xpath('//div[contains(@class, "boxIndex")]/h2[contains(text(), "Notícias")]/following-sibling::div[@id="barra-titulo-interno"]/p/a[preceding-sibling::strong[contains(., "%s")]]' % (news_names[i].text))
                else:
                    news_infos_links = driver.find_elements_by_xpath('//div[contains(@class, "boxIndex")]/h2[contains(text(), "Notícias")]/following-sibling::div[@id="barra-titulo-interno"]/p/a[preceding-sibling::strong[contains(., "%s")] and following-sibling::strong[contains(., "%s")]]' % (news_names[i].text, news_names[i + 1].text))
                news.append({
                    'titulo' : news_names[i].text,
                    'links' : []
                })

                for nil in news_infos_links:
                    news[i]['links'].append({
                        'titulo' : nil.text,
                        'link' : nil.get_attribute('href')
                    })
        except Exception as exc:
            print (exc)
            return driver, []
        return driver, news

    def ListLastResultsOnMainPage(self, driver):
        try:
            results_names = driver.find_elements_by_xpath('//div[contains(@class, "boxIndex")]/h2[contains(text(), "Resultados")]/following-sibling::div[@id="barra-titulo-interno"]/p/strong')
            results_names = filter(lambda x: x.text.strip(), results_names)    
            results = []
            for i in range(len(results_names)):
                if i == 0:
                    results_infos_links = driver.find_elements_by_xpath('//div[contains(@class, "boxIndex")]/h2[contains(text(), "Resultados")]/following-sibling::div[@id="barra-titulo-interno"]/p/a[following-sibling::strong[contains(., "%s")]]' % (results_names[1].text))
                elif i == len(results_names) - 1:
                    results_infos_links = driver.find_elements_by_xpath('//div[contains(@class, "boxIndex")]/h2[contains(text(), "Resultados")]/following-sibling::div[@id="barra-titulo-interno"]/p/a[preceding-sibling::strong[contains(., "%s")]]' % (results_names[i].text))
                else:
                    results_infos_links = driver.find_elements_by_xpath('//div[contains(@class, "boxIndex")]/h2[contains(text(), "Resultados")]/following-sibling::div[@id="barra-titulo-interno"]/p/a[preceding-sibling::strong[contains(., "%s")] and following-sibling::strong[contains(., "%s")]]' % (results_names[i].text, results_names[i + 1].text))
                results.append({
                    'titulo' : results_names[i].text,
                    'links' : []
                })

                for nil in results_infos_links:
                    results[i]['links'].append({
                        'titulo' : nil.text,
                        'link' : nil.get_attribute('href')
                    })
        except Exception as exc:
            print (exc)
            return driver, []
        return driver, results

    def GoToEditaisBensPage(self, driver):
        try:
            driver.get('http://www.uesc.br/proad/index.php?item=conteudo_publicacao.php')
            if driver.find_element_by_xpath('//div[@id="conteudo-interno"]/h2').text == 'PRÓ-REITORIA DE ADMINISTRAÇÃO E FINANÇAS - PROAD':
                return driver, True
            else:
                return driver, False
        except Exception as exc:
            print (exc)
            return driver, False

    def ListLastEditaisBensOnEditaisBensPage(self, driver):
        try:
            current_year = datetime.now().year
            nda_edicts = driver.find_elements_by_xpath('//div[@id="conteudo-interno"]/h3/following-sibling::div/div[contains(., "%s")]/following-sibling::div[@class="CollapsiblePanelContent"]/table[1]/tbody/tr/td[@bgcolor="#EAEAEA"]' % (current_year))
            edicts = []
            for i in range(0, len(nda_edicts), 3):
                edicts.append({
                    'numero' : nda_edicts[i].get_attribute('innerText'),
                    'link' : nda_edicts[i].find_element_by_xpath('./a').get_attribute('href'),
                    'descricao' : ' '.join(nda_edicts[i + 1].get_attribute('innerText').split()),
                    'abertura' : nda_edicts[i + 2].get_attribute('innerText')
                })
        except Exception as exc:
            print (exc)
            return driver, []
        return driver, edicts

    def GoToNewsPage(self, driver):
        try:
            driver.get('http://www.uesc.br/noticias/')
            if driver.find_element_by_xpath('//div[@id="conteudo-interno"]/h2').text == 'NOTÍCIAS':
                return driver, True
            else:
                return driver, False
        except Exception as exc:
            print (exc)
            return driver, False

    def ListNewsOfDateOnNewsPage(self, driver, date):
        try:
            date_obj = datetime.strptime(date, '%d/%m/%Y')
            month_name = self.MonthNumberToStringBR(date_obj.month)

            driver.find_element_by_xpath('//select[@id="mes_noticia"]/option[contains(., "%s")]' % (month_name)).click()
            driver.find_element_by_xpath('//select[@id="ano_noticia"]/option[contains(., "%s")]' % (date_obj.year)).click()
            driver.find_element_by_xpath('//input[@name="enviar"]').click()
            driver.get('http://www.uesc.br/noticias/index.php?&sortby=data_publicacao_noticia&sortdir=DESC&begin=0&rows=250')

            news_infos_links = driver.find_elements_by_xpath('//table[@id="tabela_noticias"]/tbody/tr[contains(@class, "content")]/td[@class="coluna_data_noticia" and contains(., "%s")]/following-sibling::td' % (date_obj.strftime('%d/%m')))
            news = []
            for nil in news_infos_links:
                news.append({
                    'titulo' : nil.text,
                    'link' : nil.find_element_by_xpath('./h4/a').get_attribute('href')
                })
        except Exception as exc:
            print (exc)
            return driver, [], False
        return driver, news, True

    def GoToEdictsPage(self, driver):
        try:
            driver.get('http://www.uesc.br/publicacoes/editais/')
            if driver.find_element_by_xpath('//div[@id="conteudo-interno"]/h2').text == 'EDITAIS':
                return driver, True
            else:
                return driver, False
        except Exception as exc:
            print (exc)
            return driver, False

    def ListEdictsOfDateOnEdictsPage(self, driver, date):
        try:
            date_obj = datetime.strptime(date, '%d/%m/%Y')
            month_name = self.MonthNumberToStringBR(date_obj.month)

            driver.find_element_by_xpath('//select[@id="mes_editais"]/option[contains(., "%s")]' % (month_name)).click()
            driver.find_element_by_xpath('//select[@id="ano_editais"]/option[contains(., "%s")]' % (date_obj.year)).click()
            driver.find_element_by_xpath('//input[@name="enviar"]').click()
            driver.get('http://www.uesc.br/publicacoes/editais/index.php?&sortby=numeracao_publicacao&sortdir=DESC&begin=0&rows=250')

            edicts_infos_links = driver.find_elements_by_xpath('//table[@id="tabela_Edital"]/tbody/tr[contains(@class, "content")]/td[@class="coluna_data_pub" and contains(., "%s")]/..' % (date_obj.strftime('%d/%m/%Y')))
            edicts = []
            for eil in edicts_infos_links:
                edicts.append({
                    'titulo' : eil.find_element_by_xpath('./td[@class="coluna_descricao_pub"]').text,
                    'link' : eil.find_element_by_xpath('./td/a').get_attribute('href')
                })
        except Exception as exc:
            print (exc)
            return driver, [], False
        return driver, edicts, True

    def ListEditaisBensOfDateOnEditaisBensPage(self, driver, date):
        try:
            date_obj = datetime.strptime(date, '%d/%m/%Y')
            month_name = self.MonthNumberToStringBR(date_obj.month).upper()
            try:
                driver.find_element_by_xpath('//div[contains(@class, "CollapsiblePanelTab") and contains(., "%s")]' % (date_obj.year)).click()
                nda_edicts = driver.find_elements_by_xpath('//div[contains(@class, "CollapsiblePanelTab") and contains(., "%s")]/following-sibling::div[contains(@class, "CollapsiblePanelContent")]/p[contains(., "%s")]/following-sibling::table[1]/tbody/tr/td[@bgcolor="#EAEAEA"]' % (date_obj.year, month_name))
            except:
                return driver, [], True
                
            edicts = []
            for i in range(0, len(nda_edicts), 3):
                edicts.append({
                    'numero' : nda_edicts[i].get_attribute('innerText'),
                    'link' : nda_edicts[i].find_element_by_xpath('./a').get_attribute('href'),
                    'descricao' : ' '.join(nda_edicts[i + 1].get_attribute('innerText').split()),
                    'abertura' : nda_edicts[i + 2].get_attribute('innerText')
                })
        except Exception as exc:
            print (exc)
            return driver, [], False
        return driver, edicts, True