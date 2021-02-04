from modules import process_module as pm
from modules import file_module as fm
from modules import io_module as iom
from modules import memory_module as mm
from modules import program_exit_module as pem
import sys
import operator
'''
Acima ocorre as importações dos arquivos que vão ser disparados no arquivo main.py
'''


def main():
    print('\tBem-vindo ao PSEUDO-SO 2021')

    # Nessa parte estamos inicializando os modulos

    manager = pm.ProcessManager()
    memory = mm.MemoryManager()
    io = iom.IOManager()
    filesystem = fm.FileManager()
    logger = pem.Logger()

    # Se tiver dois argumentos de linha, vai utiliza, senão vai para o comando else

    if len(sys.argv) > 2:
        procFile = sys.argv[1]
        arqFile = sys.argv[2]
    '''    
    else:
        procFile = 'processes.txt'
        arqFile = 'files.txt'
    '''
    
    # Nessa parte o programa abre o arquivo de processo e realiza a leitura do mesmo
    with open(procFile, 'r') as f:
        procs = [[int(x) for x in line.split(',')] for line in f]
        processes = [pm.Process(x).__dict__ for x in procs]

    # Nesse outro with realizamos a leitura do arquivo files.txt e é realizado a leitura da qtd de blocos e segmentos
    with open(arqFile, 'r') as f:
        temp = f.read().splitlines()
        filesystem.qtd_blocos = int(temp[0])
        filesystem.qtd_segmentos = int(temp[1])
        filesystem.arquivos = [fm.File(temp[i].replace(' ', '').split(',')).__dict__
                               for i in range(2, filesystem.qtd_segmentos+2)]
       
        filesystem.operacoes = [fm.FileOperation(temp[i].replace(' ', '').split(',')).__dict__
                                for i in range(filesystem.qtd_segmentos+2, len(temp))]
                                
    #Aqui inicializamos o discos com os arquivos de entrada, chamando a funcao inicia_disco
    filesystem.inicia_disco()
    # Aqui realizamos a ordernação dos processos pela ordem de chegada, a função sorted do Python nós ajuda nessa parte
    manager.fila_principal = list(
        sorted(processes, key=operator.itemgetter('tempo_init')))
    # Como o quantum e um, o tratamento e apenas um iterador t
    t = 0
    while(True):
        # Se ocorrer de algum processo não ter sido processado, vai entrar nesse while
        while(manager.fila_principal):
            # E escalonado os processos do tempo de chegada igual a t
            if(manager.fila_principal[0]['tempo_init'] == t):
                manager.escalona_processo_geral()
            else:
                break
        # Nessa parte realizamos o escalonamento de processos da fila de usuario para as filas de prioridades
        while(manager.escalona_processo_usuario()):
            pass

        #Se nao tiver nada executando, passa para esse if, se tiver, vai estar executando na fila de tempo real
        if(not(manager.em_execucao)):
            # Executa tempo real se tiver
            for novo_processo in manager.fila_tempo_real:
                # Se tiver espaço, vai ser realizado uma tentativa de salvar na memória
                novo_processo['PID'] = manager.gera_pid()
                offset = memory.salva(novo_processo)
                # Aqui colocamos em execução
                if(offset is not None):
                    manager.em_execucao = manager.fila_tempo_real.pop(
                        manager.fila_tempo_real.index(novo_processo))
                    manager.em_execucao['offset'] = offset
                    logger.dispatch(manager.em_execucao)
                    break
                # Colocamos esse else para não atribuir um PID se não for possível salvar na memória
                else:
                    novo_processo['PID'] = None
                    manager.ultimoPID -= 1
            # Se nao tiver tempo real, irá ser despachado para os processos de usuario
            else:
                # E realizado a procura de algum processo que tenha a prioridade 1, para o mesmo ser executado
                for novo_processo in manager.prioridade_1:
                    # Se o processo ainda não estiver na memória, consequentemente o mesmo nunca foi executado 
                    if novo_processo['offset'] is None:
                        # Aqui vamos verificar se é possível ser alocado no IO
                        novo_processo['PID'] = manager.gera_pid()
                        if(io.aloca(novo_processo)):
                            offset = memory.salva(novo_processo)
                            novo_processo['offset'] = offset
                            #se o offeset não for none, a função dispactch dispara um novo processo
                            if offset is not None:
                                logger.dispatch(novo_processo)
                    offset = novo_processo['offset']
                    # Nessa parte vai ser carregado para a cpu, se o processo puder ser executado
                    if(offset is not None):
                        manager.em_execucao = manager.prioridade_1.pop(
                            manager.prioridade_1.index(novo_processo))
                        break
                    else:
                        novo_processo['PID'] = None
                        manager.ultimoPID -= 1

                # Se nao pode atribuir processos de prioridade ele vai cair nesse else
                else:
                    for novo_processo in manager.prioridade_2:
                        # Se o processo não estiver alocado na memoria
                        if novo_processo['offset'] is None:
                            # Verifica se o processo pode ser alocado em IO
                            novo_processo['PID'] = manager.gera_pid()
                            if(io.aloca(novo_processo)):
                                offset = memory.salva(novo_processo)
                                novo_processo['offset'] = offset
                                if offset is not None:
                                    logger.dispatch(novo_processo)
                        offset = novo_processo['offset']
                        # Se o processo puder ser executado, carrega para a CPU
                        if(offset is not None):
                            manager.em_execucao = manager.prioridade_2.pop(
                                manager.prioridade_2.index(novo_processo))
                            break
                        else:
                            novo_processo['PID'] = None
                            manager.ultimoPID -= 1

                    # Se nao pode atribuir processos de prioridade 1 ou 2 (e porque tem uma falta de processos ou recursos(memoria e io))
                    else:
                        for novo_processo in manager.prioridade_3:
                            # Se processo ainda nao esta na memoria
                            if novo_processo['offset'] is None:
                                # Verifica se o processo pode ser alocado em IO
                                novo_processo['PID'] = manager.gera_pid()
                                if(io.aloca(novo_processo)):
                                    offset = memory.salva(novo_processo)
                                    novo_processo['offset'] = offset
                                    if offset is not None:
                                        logger.dispatch(novo_processo)
                            offset = novo_processo['offset']
                            # Se o processo puder ser executado, carrega o mesmo para a CPU
                            if(offset is not None):
                                manager.em_execucao = manager.prioridade_3.pop(
                                    manager.prioridade_3.index(novo_processo))
                                break
                            else:
                                novo_processo['PID'] = None
                                manager.ultimoPID -= 1
            if(manager.acabou()):
                # Aqui criamos uma condição de saída do programa => Nao tem nenhum processo em nenhuma fila
                # E se todos os processos já chegaram também
                break
        # A seguir uma condicional para execução do processo
        if(manager.em_execucao):
            # Os comandos a seguir são para decrementar o tempo restante e aumentar o numero de instruções rodadas
            manager.em_execucao['tempo_processador'] -= 1
            manager.em_execucao['execucoes'] += 1
            # Aqui realizamos a evocação da função em_execução para mostrar a saída
            logger.executa(manager.em_execucao)
            '''
                Feito a execução, e realizado a remoção do processo da memória e libera os recursos
                se tiver acabado o tempo
            '''

            if manager.em_execucao['tempo_processador'] == 0:
                filesystem.opera_processo(manager.em_execucao)
                io.libera(manager.em_execucao)
                memory.mata(manager.em_execucao)
                manager.em_execucao = {}
            # Como o quantum eh um, processos de usuario sao retirados da CPU em toda iteracao
            elif manager.em_execucao['prioridade'] > 0:
                if manager.em_execucao['prioridade'] == 1:
                    manager.prioridade_1.append(manager.em_execucao)
                elif manager.em_execucao['prioridade'] == 2:
                    manager.prioridade_2.append(manager.em_execucao)
                elif manager.em_execucao['prioridade'] == 3:
                    manager.prioridade_3.append(manager.em_execucao)
                manager.em_execucao = {}
        # Nessa parte apenas fazemos um incremento na unidade de tempo
        t += 1

    # Aqui chamamos o arquivo responsavel por mostrar a saída do sistema de arquivos
    logger.disco(filesystem)


if __name__ == '__main__':
    main()
