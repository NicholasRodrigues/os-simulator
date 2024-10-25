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

    def remover_processo(self, pid):
        """
        Remove um processo da fila de prontos pelo seu PID.

        :param pid: Identificador do processo a ser removido.
        """
        self.fila_prontos = [p for p in self.fila_prontos if p.pid != pid]
        print(f"Processo {pid} removido da fila de prontos.")

    def obter_processo(self, pid):
        """
        Obtém um processo na fila de prontos pelo seu PID.

        :param pid: Identificador do processo.
        :return: O processo correspondente ou None se não encontrado.
        """
        for processo in self.fila_prontos:
            if processo.pid == pid:
                return processo
        return None
