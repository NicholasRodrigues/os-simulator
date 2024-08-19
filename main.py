class Processo:
    def __init__(self, pid, instrucoes):
        """
        Inicializa um novo processo.

        :param pid: Identificador único do processo.
        :param instrucoes: Lista de instruções que o processo deve executar.
        """
        self.pid = pid
        self.estado = 'pronto'  # Estado inicial do processo
        self.contador_programa = 0  # Aponta para a próxima instrução a ser executada
        self.registros = {}  # Simulação de registros do processo
        self.memoria_alocada = []  # Simulação de memória alocada para o processo
        self.instrucoes = instrucoes

    def __str__(self):
        """
        Retorna uma string representando o estado atual do processo.
        """
        return f"Processo[PID={self.pid}, Estado={self.estado}, PC={self.contador_programa}]"

    def obter_proxima_instrucao(self):
        """
        Obtém a próxima instrução a ser executada pelo processo.
        """
        if self.contador_programa < len(self.instrucoes):
            return self.instrucoes[self.contador_programa]
        return None


class GerenciadorProcessos:
    def __init__(self):
        """
        Inicializa o gerenciador de processos, responsável por criar e gerenciar processos.
        """
        self.processos = {}  # Dicionário que mapeia PIDs para processos
        self.pid_counter = 1  # Contador para gerar novos PIDs únicos

    def criar_processo(self, instrucoes):
        """
        Cria um novo processo.

        :param instrucoes: Lista de instruções que o processo deve executar.
        :return: O processo criado.
        """
        pid = self.pid_counter
        processo = Processo(pid, instrucoes)
        self.processos[pid] = processo
        self.pid_counter += 1
        print(f"Processo {pid} criado com sucesso!")
        return processo

    def terminar_processo(self, pid):
        """
        Termina o processo especificado.

        :param pid: Identificador do processo a ser terminado.
        """
        if pid in self.processos:
            self.processos[pid].estado = 'terminado'
            del self.processos[pid]
            print(f"Processo {pid} foi terminado e removido do gerenciador.")

    def obter_processo(self, pid):
        """
        Obtém o processo pelo seu PID.

        :param pid: Identificador do processo.
        :return: O processo correspondente ou None se não encontrado.
        """
        return self.processos.get(pid)

    def listar_processos(self):
        """
        Lista todos os processos gerenciados.

        :return: Lista de strings representando o estado de cada processo.
        """
        print("Listando todos os processos gerenciados...")
        return [str(processo) for processo in self.processos.values()]


class Escalonador:
    def __init__(self, politica='FIFO'):
        """
        Inicializa o escalonador de processos.

        :param politica: Política de escalonamento a ser utilizada ('FIFO', 'RoundRobin', 'SJF').
        """
        self.fila_prontos = []  # Fila de processos prontos para execução
        self.politica = politica

    def adicionar_processo(self, processo):
        """
        Adiciona um processo à fila de prontos.

        :param processo: O processo a ser adicionado.
        """
        self.fila_prontos.append(processo)
        print(f"Processo {processo.pid} adicionado à fila de prontos.")

    def selecionar_proximo_processo(self):
        """
        Seleciona o próximo processo a ser executado, baseado na política de escalonamento.

        :return: O próximo processo a ser executado ou None se não houver processos prontos.
        """
        if not self.fila_prontos:
            print("A fila de prontos está vazia, nenhum processo disponível para execução.")
            return None

        if self.politica == 'FIFO':
            print("Selecionando próximo processo com política FIFO...")
            return self.fila_prontos.pop(0)
        elif self.politica == 'RoundRobin':
            print("Selecionando próximo processo com política RoundRobin...")
            processo = self.fila_prontos.pop(0)
            self.fila_prontos.append(processo)
            return processo
        elif self.politica == 'SJF':
            print("Selecionando próximo processo com política SJF...")
            self.fila_prontos.sort(key=lambda p: len(p.instrucoes))
            return self.fila_prontos.pop(0)
        else:
            raise ValueError(f"Política de escalonamento {self.politica} desconhecida.")


class SimuladorExecucao:
    def __init__(self, escalonador):
        """
        Inicializa o simulador de execução de processos.

        :param escalonador: Instância do escalonador de processos.
        """
        self.escalonador = escalonador

    def executar_processo(self, processo):
        """
        Executa todas as instruções de um processo.

        :param processo: O processo a ser executado.
        """
        while processo.estado == 'executando' and processo.contador_programa < len(processo.instrucoes):
            instrucao = processo.obter_proxima_instrucao()
            if instrucao:
                self.executar_instrucao(processo, instrucao)
                processo.contador_programa += 1

        if processo.contador_programa >= len(processo.instrucoes):
            processo.estado = 'terminado'
            print(f"Processo {processo.pid} terminou a execução de todas as instruções.")

    def executar_instrucao(self, processo, instrucao):
        """
        Executa uma única instrução.

        :param processo: O processo executando a instrução.
        :param instrucao: A instrução a ser executada.
        """
        if instrucao == 'NOP':
            print(f"Processo {processo.pid}: NOP - Nenhuma operação realizada.")
        elif instrucao == 'END':
            processo.estado = 'terminado'
            print(f"Processo {processo.pid}: END - Processo finalizado.")
        else:
            print(f"Processo {processo.pid}: Executando instrução {instrucao}")

    def ciclo_de_execucao(self):
        """
        Executa o ciclo principal do simulador, alternando entre processos conforme a política do escalonador.
        """
        while True:
            processo = self.escalonador.selecionar_proximo_processo()
            if not processo:
                print("Nenhum processo para executar. Ciclo de execução encerrado.")
                break

            if processo.estado == 'pronto':
                print(f"Iniciando execução do processo {processo.pid}")
                processo.estado = 'executando'
                self.executar_processo(processo)
                print(f"Processo {processo.pid} terminou")


# Funções de teste
def teste_criar_processo():
    gerenciador = GerenciadorProcessos()
    processo = gerenciador.criar_processo(['NOP', 'END'])
    assert processo.pid == 1
    assert processo.estado == 'pronto'
    print("Teste criar_processo passou.\n")

def teste_escalonador_fifo():
    gerenciador = GerenciadorProcessos()
    escalonador = Escalonador(politica='FIFO')

    p1 = gerenciador.criar_processo(['NOP', 'END'])
    p2 = gerenciador.criar_processo(['END'])

    escalonador.adicionar_processo(p1)
    escalonador.adicionar_processo(p2)

    processo = escalonador.selecionar_proximo_processo()
    assert processo == p1
    processo = escalonador.selecionar_proximo_processo()
    assert processo == p2
    print("Teste escalonador_fifo passou.\n")

def teste_simulador_execucao():
    gerenciador = GerenciadorProcessos()
    escalonador = Escalonador(politica='FIFO')

    p1 = gerenciador.criar_processo(['NOP', 'END'])
    p2 = gerenciador.criar_processo(['NOP', 'NOP', 'END'])

    escalonador.adicionar_processo(p1)
    escalonador.adicionar_processo(p2)

    simulador = SimuladorExecucao(escalonador)
    simulador.ciclo_de_execucao()

    assert p1.estado == 'terminado'
    assert p2.estado == 'terminado'
    print("Teste simulador_execucao passou.\n")

# Execução da suíte de testes
def executar_suite_testes():
    print("Iniciando suíte de testes...\n")
    teste_criar_processo()
    teste_escalonador_fifo()
    teste_simulador_execucao()
    print("Todos os testes passaram com sucesso.\n")

executar_suite_testes()
