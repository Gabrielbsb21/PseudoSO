class IOManager:
    # Classe que define a gerencia de Entrada e Saída
    
    scanner = [None] #1 scanner
    printer = [None, None] # 2 impressoras
    modem = [None] # 1 modem
    sata = [None, None] #2 satas

    def aloca(self, processo):

        #Essa função irá realizar a analise para ver se os recursos estão disponiveis e alocar se eles estiverem


        free = True
        if processo['requisicao_modem'] > 0 and self.modem[0] is not None:
            free = False
        elif processo['requisicao_scanner'] > 0 and self.scanner[0] is not None:
            free = False
        elif processo['numero_impressora'] > 0 and self.printer[processo['numero_impressora'] - 1] is not None:
            free = False
        elif processo['numero_disco'] > 0 and self.sata[processo['numero_disco'] - 1] is not None:
            free = False
        if free:
            if processo['requisicao_modem'] > 0:
                self.modem[0] = processo['PID']
            if processo['requisicao_scanner'] > 0:
                self.scanner[0] = processo['PID']
            if processo['numero_impressora'] > 0:
                self.printer[processo['numero_impressora'] - 1] = processo['PID']
            if processo['numero_disco'] > 0:
                self.printer[processo['numero_disco'] - 1] = processo['PID']
            return True
        else:
            return False
    def libera(self, processo):

        #Libera todos os recursos que estão sendo utilizados pelo processo

        if self.modem[0] == processo['PID']:
            self.modem[0] = None
        if self.scanner[0] == processo['PID']:
            self.scanner[0] = None
        if  processo['PID'] in self.printer:
            self.printer[processo['numero_impressora'] - 1] = None
        if  processo['PID'] in self.sata:
            self.sata[processo['numero_disco'] - 1] = None
