# coding=utf8
from selenium import webdriver
import requests
import time
import json
import re

class Helper():

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
            edicts = []
            last_links = 0
            for i in range(len(edicts_names)):
                if i == 0:
                    edict_infos_links = driver.find_elements_by_xpath('//div[contains(@class, "boxIndex")]/h2[contains(text(), "Editais")]/following-sibling::div[@id="barra-titulo-interno"]/p/a[following-sibling::strong[contains(., "%s")]]' % (edicts_names[1].text))
                    last_links = len(edict_infos_links)
                elif i == len(edicts_names) - 1:
                    edict_infos_links = driver.find_elements_by_xpath('//div[contains(@class, "boxIndex")]/h2[contains(text(), "Editais")]/following-sibling::div[@id="barra-titulo-interno"]/p/a[preceding-sibling::strong[contains(., "%s")]]' % (edicts_names[i].text))
                else:
                    edict_infos_links = driver.find_elements_by_xpath('//div[contains(@class, "boxIndex")]/h2[contains(text(), "Editais")]/following-sibling::div[@id="barra-titulo-interno"]/p/a[preceding-sibling::strong[contains(., "%s")] and following-sibling::strong[contains(., "%s")]]' % (edicts_names[i - 1].text, edicts_names[i + 1].text))
                    edict_infos_links = edict_infos_links[last_links:]
                    last_links = len(edict_infos_links)
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

    