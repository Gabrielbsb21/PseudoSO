class Logger:
    '''
        Criamos essa classe para administrar a saída do programa
        Dessa forma o código fica mais organizado
    '''

    # Ultimo processo a ser executado
    last_exec = None

    def dispatch(self, process):
        # A seguir é imprimido na tela as informações do processo a ser despachado

        if(self.last_exec != -1 and self.last_exec != None):
            print('\tP{} INTERRUPTED'.format(self.last_exec))
        self.last_exec = -1
        print('dispatcher =>')
        print('\tPID:\t\t {}'.format(process['PID']))
        # print(f'\tPID:\t\t {process['PID']}')
        print('\toffset:\t\t {}'.format(process['offset']))
        print('\tblocks:\t\t {}'.format(process['blocos_memoria']))
        print('\tpriority:\t {}'.format(process['prioridade']))
        print('\ttime:\t\t {}'.format(process['tempo_processador']))
        print('\tprinters:\t {}'.format(bool(process['numero_impressora'])))
        print('\tscanner:\t {}'.format(bool(process['requisicao_scanner'])))
        print('\tmodem:\t\t {}'.format(bool(process['requisicao_modem'])))
        print('\tdrives:\t\t {}'.format(bool(process['numero_disco'])))

    def executa(self, process):
        '''
        Mostra informacoes da execucao do processo
        STARTED quando o processo eh executado pela primeira vez
        INTERRUPTED quando o processo deixa de ser executado antes de terminar
        RESUMED quando um processo interrompido retorna sua execucao
        return SIGINT quando um processo finaliza sua execucao
        '''
        if(self.last_exec != process['PID']):
            if(self.last_exec != -1):  # is not -1
                print('\tP{} INTERRUPTED'.format(self.last_exec))
            print('processo {} =>'.format(process['PID']))
            if(process['execucoes'] == 1):
                print('\tP{} STARTED'.format(process['PID']))
            else:
                print('\tP{} RESUMED'.format(process['PID']))
        print('\tP{} instruction {}'.format(
            process['PID'], process['execucoes']))
        self.last_exec = process['PID']
        if(process['tempo_processador'] == 0):
            print('\tP{} return SIGINT'.format(process['PID']))
            self.last_exec = -1

    def disco(self, fs):
        '''
        Mostra as informacoes das operacoes e estado final do sistema de arquivos
        '''
        print('Sistema de Arquivos =>')
        i = 1
        for l in fs.log:
            print('\tOperacao {} => {}'.format(i, l['status']))
            print('\t\t{}'.format(l['mensagem']))
            i += 1
        for op in fs.operacoes:
            print('\tOperacao {} => Falha'.format(i))
            print('\t\tO processo {} nao existe'.format(op['PID']))
            i += 1
        print('\tMapa de Ocupacao de Disco:')
        print('\t\t{}'.format(fs.disco))
