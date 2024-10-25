class SimuladorExecucao:
    def __init__(self, escalonador, gerenciador_io, sistema_arquivos, game_engine):
        """
        Inicializa o simulador de execução de processos.

        :param escalonador: Instância do escalonador de processos.
        :param gerenciador_io: Instância do gerenciador de E/S.
        :param sistema_arquivos: Instância do sistema de arquivos.
        :param game_engine: Instância do motor de jogo.
        """
        self.escalonador = escalonador
        self.gerenciador_io = gerenciador_io
        self.sistema_arquivos = sistema_arquivos
        self.game_engine = game_engine

    def executar_processo(self, processo):
        """
        Executa uma instrução de um processo.

        :param processo: O processo a ser executado.
        """
        instrucao = processo.obter_proxima_instrucao()
        if instrucao:
            self.executar_instrucao(processo, instrucao)
        else:
            processo.estado = 'terminado'
            print(f"Processo {processo.pid}: Nenhuma instrução restante.")

        if processo.contador_programa >= len(processo.instrucoes):
            processo.estado = 'terminado'
            print(f"Processo {processo.pid} terminou a execução de todas as instruções.")

    def executar_instrucao(self, processo, instrucao):
        """
        Executa uma única instrução.

        :param processo: O processo executando a instrução.
        :param instrucao: A instrução a ser executada.
        """
        tokens = instrucao.strip().split()
        if not tokens:
            processo.contador_programa += 1
            return

        command = tokens[0]
        args = tokens[1:]

        if command == 'NOP':
            print(f"Processo {processo.pid}: NOP - Nenhuma operação realizada.")
        elif command == 'END':
            processo.estado = 'terminado'
            print(f"Processo {processo.pid}: END - Processo finalizado.")
            return
        elif command == 'READ':
            reg = args[0]
            # Simular E/S bloqueante
            self.gerenciador_io.solicitar_io(processo.pid, 'teclado', {'registro': reg})
            processo.estado = 'bloqueado'
            print(f"Processo {processo.pid}: READ - Processo bloqueado aguardando E/S.")
            return
        elif command == 'WRITE':
            reg = args[0]
            # Simular E/S bloqueante
            self.gerenciador_io.solicitar_io(processo.pid, 'tela', {'registro': reg, 'valor': processo.registros[reg]})
            processo.estado = 'bloqueado'
            print(f"Processo {processo.pid}: WRITE - Processo bloqueado aguardando E/S.")
            return
        elif command == 'CREATE_CHARACTER':
            name, sprite_file, x, y = args
            x = int(x)
            y = int(y)
            self.game_engine.create_character(name, sprite_file, x, y)
        elif command == 'MOVE_CHARACTER':
            name, direction, distance = args
            distance = int(distance)
            self.game_engine.move_character(name, direction, distance)
        elif command == 'SET_CHARACTER_POSITION':
            name, x, y = args
            x = int(x)
            y = int(y)
            self.game_engine.set_character_position(name, x, y)
        # ... (Implementar outras instruções conforme necessário)
        else:
            print(f"Processo {processo.pid}: Instrução desconhecida '{command}'.")

        processo.contador_programa += 1

    def ciclo_de_execucao(self):
        """
        Executa o ciclo principal do simulador, alternando entre processos conforme a política do escalonador.
        """
        while True:
            # Processa operações de E/S
            self.gerenciador_io.processar_io()

            # Atualiza processos bloqueados
            for pid in list(self.gerenciador_io.processos_bloqueados.keys()):
                processo = self.escalonador.obter_processo(pid)
                if processo and processo.estado == 'bloqueado':
                    # Verifica se a E/S foi processada
                    if pid not in self.gerenciador_io.processos_bloqueados:
                        processo.estado = 'pronto'
                        print(f"Processo {pid}: E/S concluída, processo pronto.")

            processo = self.escalonador.selecionar_proximo_processo()
            if not processo:
                print("Nenhum processo para executar. Ciclo de execução encerrado.")
                break

            if processo.estado == 'pronto':
                print(f"Iniciando execução do processo {processo.pid}")
                processo.estado = 'executando'
                self.executar_processo(processo)
                if processo.estado == 'terminado':
                    self.escalonador.remover_processo(processo.pid)
                elif processo.estado == 'bloqueado':
                    # Retorna o processo à fila de prontos ou mantém bloqueado
                    print(f"Processo {processo.pid} está bloqueado e aguardando E/S.")
                else:
                    processo.estado = 'pronto'
