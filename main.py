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

