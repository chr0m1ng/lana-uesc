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
            'response' : 'No Site da UESC eu posso realizar estes serviços:\n\n'
            '• Listas as noticias mais recentes\n'
            '• Listas as noticias de um dia especifico\n'
            '• Listar os resultados mais recentes\n'
            '• Listar os editais mais recentes\n'
            '• Listar os editais de um dia especifico\n'
            '• Listar editais de bens e serviços mais recentes, i.e. os editais de compra da UESC\n'
            '• Listar editais de bens e serviços de um mês especifico\n'
            '• Listar os cursos disponiveis na UESC junto ao site do colegiado de cada um\n'
            '• Listar os departamentos da universidade e os sites de cada\n',
            'type' : 'text'
        }
