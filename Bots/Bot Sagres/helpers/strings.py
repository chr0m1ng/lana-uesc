# coding=utf8

class ErrorStrings():
    def GetNoSuchCourseErrorMessage(self, code):
        return {
            'response' : 'Não foi possivel encontrar a disciplina %s dentre as já cursadas' % (code),
            'type' : 'text'
        }
    
    def GetNoSuchClassErrorMessage(self, code):
        return {
            'response' : 'Não foi possivel encontrar a turmma %s dentre as atuais' % (code),
            'type' : 'text'
        }

    def GetNoCreditsYetForCourseErrorMessage(self, code):
        return {
            'response' : 'Ainda não existem notas cadastradas para a disciplina %s' % (code),
            'type' : 'text'
        }
    
    def GetGenericErrorMessage(self):
        return {
            'response' : 'Erro interno ao tentar acessar recurso do sagres',
            'type' : 'text'
        }

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

    def GetSagresDownMessage(self):
        return {
            'response' : 'O Portal Sagres está fora do ar',
            'type' : 'text'
        }

class GeneralStrings():
    def GetAboutSagresMessage(self):
        return {
            'response' : 'No Portal Sagres eu posso realizar estes serviços:\n\n'
            '- Para Alunos:\n'
            ' • Calcular o CRAA\n'
            ' • Montar o horário do semestre\n'
            ' • Listar todas as disciplinas já cursadas\n'
            ' • Listar as disciplinas do semestre atual\n'
            ' • Listar a quantidade de faltas em todas as disciplinas já cursadas\n'
            ' • Listar a quantidade de faltas de uma disciplina especifica\n'
            ' • Listar as médias de todas as disciplinas já cursadas\n'
            ' • Listar as notas de uma disciplina especifica\n\n'
            '- Para Professores:\n'
            ' • Montar o horário do semestre\n'
            ' • Listar as turmas do semestre\n'
            ' • Informar a quantidade de alunos matriculados em uma disciplina especifica',
            'type' : 'text'
        }
