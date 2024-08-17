class Processo:
    def __init__(self, pid, instrucoes):
        """
        Inicializa um novo processo.

        :param pid: Identificador único do processo.
        :param instrucoes: Lista de instruções que o processo deve executar.
        """
        self.pid = pid
        self.estado = 'pronto'
        self.contador_programa = 0
        self.registros = {}
        self.memoria_alocada = []
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
        self.processos = {}
        self.pid_counter = 1

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
        return processo

    def terminar_processo(self, pid):
        """
        Termina o processo especificado.

        :param pid: Identificador do processo a ser terminado.
        """
        if pid in self.processos:
            self.processos[pid].estado = 'terminado'
            del self.processos[pid]

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
        return [str(processo) for processo in self.processos.values()]


class Escalonador:
    def __init__(self, politica='FIFO'):
        """
        Inicializa o escalonador de processos.

        :param politica: Política de escalonamento a ser utilizada ('FIFO', 'RoundRobin', 'SJF').
        """
        self.fila_prontos = []
        self.politica = politica

    def adicionar_processo(self, processo):
        """
        Adiciona um processo à fila de prontos.

        :param processo: O processo a ser adicionado.
        """
        self.fila_prontos.append(processo)

    def selecionar_proximo_processo(self):
        """
        Seleciona o próximo processo a ser executado, baseado na política de escalonamento.

        :return: O próximo processo a ser executado ou None se não houver processos prontos.
        """
        if not self.fila_prontos:
            return None

        if self.politica == 'FIFO':
            return self.fila_prontos.pop(0)
        elif self.politica == 'RoundRobin':
            processo = self.fila_prontos.pop(0)
            self.fila_prontos.append(processo)
            return processo
        elif self.politica == 'SJF':
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

    def executar_instrucao(self, processo, instrucao):
        """
        Executa uma única instrução.

        :param processo: O processo executando a instrução.
        :param instrucao: A instrução a ser executada.
        """
        if instrucao == 'NOP':
            pass  # Instrução de No Operation (não faz nada)
        elif instrucao == 'END':
            processo.estado = 'terminado'
        else:
            print(f"Executando {instrucao} no processo {processo.pid}")

    def ciclo_de_execucao(self):
        """
        Executa o ciclo principal do simulador, alternando entre processos conforme a política do escalonador.
        """
        while True:
            processo = self.escalonador.selecionar_proximo_processo()
            if not processo:
                print("Nenhum processo para executar.")
                break

            if processo.estado == 'pronto':
                print(f"Iniciando execução do processo {processo.pid}")
                processo.estado = 'executando'
                self.executar_processo(processo)
                print(f"Processo {processo.pid} terminou")


def teste_criar_processo():
    gerenciador = GerenciadorProcessos()
    processo = gerenciador.criar_processo(['NOP', 'END'])
    assert processo.pid == 1
    assert processo.estado == 'pronto'
    print("Teste criar_processo passou.")

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
    print("Teste escalonador_fifo passou.")

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
    print("Teste simulador_execucao passou.")

# Execução da suíte de testes
def executar_suite_testes():
    print("Iniciando suíte de testes...")
    teste_criar_processo()
    teste_escalonador_fifo()
    teste_simulador_execucao()
    print("Todos os testes passaram com sucesso.")

executar_suite_testes()

