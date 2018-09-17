# coding=utf8
from selenium import webdriver
import requests
import time
import json
import re

class Helper():

    def IsUESCDown(self, driver):
        try:
            driver.get('http://www.prograd.uesc.br/PortalSagres/Acesso.aspx')
            if driver.find_elements_by_class_name('label-padrao') == []:
                return driver, True
        except Exception as exc:
            print (exc)
            return driver, True
        return driver, False

    