class File:
    #Definindo o arquivo no disco

    def __init__(self, arquivo, criador=None):
        self.nome = arquivo[0]
        self.bloco_inicio = int(arquivo[1])
        self.tamanho = int(arquivo[2])
        self.criador = criador

class FileOperation:

    #Nessa função inicial definimos as operações nos arquivos
    def __init__(self, operacao):
        self.PID = int(operacao[0])
        self.opcode = int(operacao[1])
        self.arquivo = operacao[2]
        if(self.opcode == 0):
            self.tamanho = int(operacao[3])
        else:
            self.tamanho = None

class FileManager:

    # Essa classe gerencia os arquivos e as operações dos processos
    
    qtd_blocos = 0
    qtd_segmentos = 0
    arquivos = []
    operacoes = []
    #Lista de blocos do disco
    disco = []
    #Saidas do gerenciador de arquivos
    log = []

    def inicia_disco(self):

        #E inicializado o disco com os arquivos que foram passados na entrada do arquivo
        
        self.disco = [0 for i in range(self.qtd_blocos)] 
        for arq in self.arquivos:
            self.disco[arq['bloco_inicio']:arq['bloco_inicio'] + arq['tamanho']] = arq['tamanho']*[arq['nome']]

    def cria_arquivo(self, nome, tamanho, criador):
        #função que cria um novo arquivo no disco
        
        offset = None
        disponiveis = 0

        if (next((arq for arq in self.arquivos if arq['nome'] == nome), None) is not None):
            self.log.append({
                "status": 'Falha',
                "mensagem": 'O processo {} nao criou o arquivo {} (Arquivo ja existe no disco)'.format(
                criador, nome
                )
            })
            return

        #localiza espaco disponivel com First Fit e armazena
        for i in range(self.qtd_blocos):
            bloco = self.disco[i]
            if(bloco == 0):
                disponiveis += 1
                # se o espaço disponivel for igual ao tamanho, irá ser criado o arquivo
                if(disponiveis == tamanho):
                    offset = i - disponiveis + 1
                    self.disco[offset:offset+disponiveis] = tamanho * [nome]
                    arquivo = File([nome, offset, tamanho], criador=criador)
                    self.arquivos.append(arquivo.__dict__)
                    self.log.append({
                        "status": 'Sucesso',
                        "mensagem": 'O processo {} criou o arquivo {} (blocos {})'.format(
                        criador, nome, range(offset,offset+disponiveis))
                    })
                    return
            else:
                disponiveis = 0
        self.log.append({
            "status": 'Falha',
            "mensagem": 'O processo {} nao criou o arquivo {} pelo motivo de nao ter espaco livre)'.format(
            criador, nome
            )
        })

    def deleta_arquivo(self, arquivo):
        #Remove o arquivo do disco

        self.disco[arquivo['bloco_inicio']:arquivo['bloco_inicio'] + arquivo['tamanho']] =  arquivo['tamanho']*[0]

    def opera_processo(self, processo):
        '''
        Executa todas as operacoes de um processo
        '''
        #Localiza as operacoes pertencentes ao processo
        ops = [op for op in self.operacoes if op['PID'] == processo['PID']]
        for op in ops:
            #Para a criação do arquivo
            if op['opcode'] == 0:
                self.cria_arquivo(op['arquivo'], op['tamanho'], processo['PID'])
            #Codigo para deletar o arquivo
            else:
                # Seleciona o arquivo pra ser deletado
                arquivo = next((arq for arq in self.arquivos if arq['nome'] == op['arquivo']), None)

                if arquivo is not None:
                    #Avalia permissoes
                    if (processo['prioridade'] == 0) or (arquivo['criador'] == None or processo['PID'] == arquivo['criador']):
                        self.deleta_arquivo(arquivo)
                        self.log.append({
                            "status": 'Sucesso',
                            "mensagem":'O processo {} deletou o arquivo {}'.format(
                            processo['PID'], arquivo['nome'])
                        })
                    else:
                        self.log.append({
                            "status": 'Falha',
                            "mensagem":'O processo {} nao pode deletar o arquivo {} pois o codigo da operacao esta errado'.format(
                            processo['PID'], arquivo['nome'])
                        })
                
                else:
                    self.log.append({
                        "status": 'Falha',
                        "mensagem":'O processo {} nao pode deletar o arquivo {} (Arquivo Inexistente)'.format(
                        processo['PID'], op['arquivo'])
                    })
                
            self.operacoes.remove(op)
