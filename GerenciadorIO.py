# GerenciadorIO.py

from collections import deque


class GerenciadorIO:
    def __init__(self):
        """
        Inicializa o gerenciador de E/S com filas para cada dispositivo simulado.
        """
        self.dispositivos = {
            'disco': deque(),
            'teclado': deque(),
            'tela': deque(),
            'rede': deque()
        }
        self.processos_bloqueados = {}

    def solicitar_io(self, pid, dispositivo, dados):
        """
        Solicita uma operação de E/S para um dispositivo.

        :param pid: Identificador do processo solicitante.
        :param dispositivo: Nome do dispositivo ('disco', 'teclado', 'tela', 'rede').
        :param dados: Dados relacionados à operação de E/S.
        """
        if dispositivo in self.dispositivos:
            self.dispositivos[dispositivo].append((pid, dados))
            print(f"Gerenciador de E/S: Processo {pid} solicitou E/S no dispositivo {dispositivo}.")
            self.processos_bloqueados[pid] = dispositivo
        else:
            print(f"Gerenciador de E/S: Dispositivo {dispositivo} não reconhecido.")

    def processar_io(self):
        """
        Processa uma operação de E/S em cada dispositivo.
        """
        for dispositivo, fila in self.dispositivos.items():
            if fila:
                pid, dados = fila.popleft()
                print(f"Gerenciador de E/S: Processando E/S para o processo {pid} no dispositivo {dispositivo}.")
                # Simulação do processamento da E/S
                # Após o processamento, remove o processo dos bloqueados
                if pid in self.processos_bloqueados:
                    del self.processos_bloqueados[pid]
