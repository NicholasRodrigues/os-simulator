from Processo import Processo
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
        else:
            print(f"Processo {pid} não encontrado.")

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