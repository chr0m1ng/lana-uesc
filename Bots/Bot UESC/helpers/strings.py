# coding=utf8

class ErrorStrings():
    def GetNoEdictsErrorMessage(self, date):
        return {
            'response' : 'Não foi possivel encontrar editais no dia %s no site da UESC' % (date),
            'type' : 'text'
        }
    
    def GetNoNewsErrorMessage(self, date):
        return {
            'response' : 'Nenhuma noticia do dia %s foi encontrada no site da UESC' % (date),
            'type' : 'text'
        }
    
    def GetGenericErrorMessage(self):
        return {
            'response' : 'Erro interno ao tentar acessar recurso da UESC',
            'type' : 'text'
        }

    def GetUESCDownMessage(self):
        return {
            'response' : 'O site da UESC está fora do ar',
            'type' : 'text'
        }

    def GetNoEditaisBensErrorMessage(self, month_year):
        return {
            'response' : 'Não foi possivel encontrar editais de bens e serviços em %s no site da UESC' % (month_year),
            'type' : 'text'
        }

class GeneralStrings():
    def GetAboutUESCMessage(self):
        return {
            'response' : 'WiP',
            'type' : 'text'
        }
