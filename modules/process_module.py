class Process:
    #Metodo construtor da classe process
    def __init__(self, process):
        self.tempo_init = process[0]
        self.prioridade = process[1]
        self.tempo_processador = process[2]
        self.blocos_memoria = process[3]
        self.numero_impressora = process[4]
        self.requisicao_scanner = process[5]
        self.requisicao_modem = process[6]
        self.numero_disco = process[7]
        self.offset = None
        self.PID = None
        self.execucoes = 0

class ProcessManager:
    fila_tempo_real = []
    fila_usuario = []
    prioridade_1 = []
    prioridade_2 = []
    prioridade_3 = []
    fila_principal = []
    em_execucao = {}
    ultimoPID = 0

    def escalona_processo_geral(self):
    
        #A seguir é realizado o escalonamento dos processos nas filas de usuario ou fila de tempo real

        if(not(self.fila_principal)):
            return False

        processo_topo = self.fila_principal[0]

        # distribui os processos ao longo das filas de usuario ou tempo real
        if ((processo_topo['prioridade'] == 0) and (len(self.fila_tempo_real) < 1000)):
            self.fila_principal.pop(0)
            self.fila_tempo_real.append(processo_topo)

        elif (len(self.fila_usuario) < 1000):
            # alocou para a fila de usuario
            # Para na função escalona_processo_usuario ser decidido em qual prioridade o processo vai ser rodado
            self.fila_principal.pop(0)
            self.fila_usuario.append(processo_topo)
        else:
            # Caso ele nao tenha conseguido alocar o processo nas filas
            return False
        return True

    def escalona_processo_usuario(self):

        # E realizado o escolanomento de processos de usuarios nas filas de prioridades

        if(not(self.fila_usuario)):
            return False

        processo_topo = self.fila_usuario[0]

        # aloca para a fila de prioridades
        if (processo_topo['prioridade'] == 1 and len(self.prioridade_1) < 1000):
            self.fila_usuario.pop(0)
            self.prioridade_1.append(processo_topo)
        elif (processo_topo['prioridade'] == 2 and len(self.prioridade_2) < 1000):
            self.fila_usuario.pop(0)
            self.prioridade_2.append(processo_topo)
        elif (processo_topo['prioridade'] == 3 and len(self.prioridade_3) < 1000):
            self.fila_usuario.pop(0)
            self.prioridade_3.append(processo_topo)
        else:
            return False

        return True
    def gera_pid(self):
        # Essa função gera um PID  e já calcula o próximo
   
        self.ultimoPID += 1
        return self.ultimoPID - 1
    def acabou(self):
        # Irá retornar se ainda tem um processo para ser realizado ou não
        
        return (not(self.fila_usuario) and not(self.fila_principal) and not(self.fila_tempo_real)
        and not(self.prioridade_1) and not(self.prioridade_2) and not(self.prioridade_3)
        and not(self.em_execucao))
