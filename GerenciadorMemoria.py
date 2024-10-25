# GerenciadorMemoria.py

class GerenciadorMemoria:
    def __init__(self, tamanho_total=1024):
        """
        Inicializa o gerenciador de memória.

        :param tamanho_total: O tamanho total da memória disponível.
        """
        self.tamanho_total = tamanho_total
        self.memoria = [None] * tamanho_total  # Representa a memória física
        self.alocacoes = {}  # Mapeia PIDs para segmentos de memória alocados

    def alocar_memoria(self, pid, tamanho):
        """
        Aloca um segmento de memória para um processo.

        :param pid: Identificador do processo.
        :param tamanho: Tamanho da memória a ser alocada.
        :return: Lista de endereços alocados ou None se não houver memória suficiente.
        """
        segmentos_livres = self._encontrar_segmentos_livres(tamanho)
        if segmentos_livres is None:
            print(f"Gerenciador de Memória: Memória insuficiente para o processo {pid}.")
            return None
        else:
            for endereco in segmentos_livres:
                self.memoria[endereco] = pid
            self.alocacoes[pid] = segmentos_livres
            print(f"Gerenciador de Memória: Memória alocada para o processo {pid}.")
            return segmentos_livres

    def liberar_memoria(self, pid):
        """
        Libera a memória alocada para um processo.

        :param pid: Identificador do processo.
        """
        if pid in self.alocacoes:
            for endereco in self.alocacoes[pid]:
                self.memoria[endereco] = None
            del self.alocacoes[pid]
            print(f"Gerenciador de Memória: Memória liberada para o processo {pid}.")

    def _encontrar_segmentos_livres(self, tamanho):
        """
        Encontra segmentos livres contíguos de memória para alocação.

        :param tamanho: Tamanho do segmento necessário.
        :return: Lista de endereços livres ou None se não houver espaço.
        """
        contador = 0
        inicio = 0
        for i in range(self.tamanho_total):
            if self.memoria[i] is None:
                if contador == 0:
                    inicio = i
                contador += 1
                if contador == tamanho:
                    return list(range(inicio, inicio + tamanho))
            else:
                contador = 0
        return None
