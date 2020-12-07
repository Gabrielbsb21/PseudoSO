#Constantes para o tamanho da memoria
#em Python não existe o tipo constante, mas temos uma conversão de colocar constantes em letra maiuscula
TAMANHO_TR = 64 #tamanho de tempo real
TAMANHO_USUARIO = 960 #tamanho dos processos de usuário

class MemoryManager:

    #Classe para o gerenciamento de memoria 
    #CAMPOS: memoria - lista de blocos da memoria

    
    # fazemos esse for para ser preenchido a variavel memoria com uma lista de 1024 espaços	
    memoria = [None for i in range(TAMANHO_TR + TAMANHO_USUARIO)]

    def salva (self, processo):
        ''' Armazena processo na memoria, retorna None se nao foi posssvel armazenar, ou retorna o
        offset caso contrario
        '''
        offset = None
        disponiveis = 0
        start = 0
        end = TAMANHO_TR+TAMANHO_USUARIO
        if processo['prioridade'] > 0:
            start = TAMANHO_TR
        else:
            end = TAMANHO_TR
        for i in range(start, end):
            bloco = self.memoria[i]
            if(bloco == None):
                disponiveis += 1
                if(disponiveis == processo['blocos_memoria']):
                    offset = i - disponiveis + 1
                    self.memoria[offset:offset+disponiveis] = processo['blocos_memoria'] * [processo['PID']]
                    break
            else:
                disponiveis = 0
        return offset

    def mata (self, processo):
        #função para remover o processo da memoria
        
        self.memoria[processo['offset']: processo['offset'] + processo['blocos_memoria']] =  processo['blocos_memoria']*[None]
