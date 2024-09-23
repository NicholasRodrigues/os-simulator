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
        self.registros = {'R0': 0, 'R1': 0, 'R2': 0, 'R3': 0}  # Registros do processo
        self.memoria_alocada = {}  # Memória alocada para o processo
        self.instrucoes = instrucoes
        self.labels = self._process_labels()  # Mapeamento de labels para índices de instrução

    def _process_labels(self):
        """
        Processa labels nas instruções e cria um mapeamento de labels para índices.
        """
        labels = {}
        novas_instrucoes = []
        for idx, instrucao in enumerate(self.instrucoes):
            if ':' in instrucao:
                label, instrucao_sem_label = instrucao.split(':', 1)
                labels[label.strip()] = len(novas_instrucoes)
                instrucao = instrucao_sem_label.strip()
                if instrucao:
                    novas_instrucoes.append(instrucao)
            else:
                novas_instrucoes.append(instrucao)
        self.instrucoes = novas_instrucoes
        return labels

    def __str__(self):
        return f"Processo[PID={self.pid}, Estado={self.estado}, PC={self.contador_programa}]"

    def obter_proxima_instrucao(self):
        if self.contador_programa < len(self.instrucoes):
            return self.instrucoes[self.contador_programa]
        return None