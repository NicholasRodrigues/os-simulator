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
            else:
                processo.estado = 'terminado'
                print(f"Processo {processo.pid}: Nenhuma instrução restante.")
                break

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
        elif command == 'ADD':
            reg1, reg2 = args
            processo.registros[reg1] += processo.registros[reg2]
            print(f"Processo {processo.pid}: ADD - {reg1} = {processo.registros[reg1]}")
        elif command == 'SUB':
            reg1, reg2 = args
            processo.registros[reg1] -= processo.registros[reg2]
            print(f"Processo {processo.pid}: SUB - {reg1} = {processo.registros[reg1]}")
        elif command == 'MUL':
            reg1, reg2 = args
            processo.registros[reg1] *= processo.registros[reg2]
            print(f"Processo {processo.pid}: MUL - {reg1} = {processo.registros[reg1]}")
        elif command == 'DIV':
            reg1, reg2 = args
            if processo.registros[reg2] == 0:
                print(f"Processo {processo.pid}: DIV - Erro: Divisão por zero.")
                processo.estado = 'terminado'
                return
            processo.registros[reg1] //= processo.registros[reg2]
            print(f"Processo {processo.pid}: DIV - {reg1} = {processo.registros[reg1]}")
        elif command == 'JMP':
            label = args[0]
            if label in processo.labels:
                processo.contador_programa = processo.labels[label]
                print(f"Processo {processo.pid}: JMP para label {label}")
                return  # Retorna para evitar incrementar PC
            else:
                print(f"Processo {processo.pid}: JMP - Label {label} não encontrado.")
        elif command == 'JZ':
            reg, label = args
            if processo.registros[reg] == 0:
                if label in processo.labels:
                    processo.contador_programa = processo.labels[label]
                    print(f"Processo {processo.pid}: JZ - {reg} é zero, pulando para {label}")
                    return
                else:
                    print(f"Processo {processo.pid}: JZ - Label {label} não encontrado.")
            else:
                print(f"Processo {processo.pid}: JZ - {reg} não é zero, continuando.")
        elif command == 'JNZ':
            reg, label = args
            if processo.registros[reg] != 0:
                if label in processo.labels:
                    processo.contador_programa = processo.labels[label]
                    print(f"Processo {processo.pid}: JNZ - {reg} não é zero, pulando para {label}")
                    return
                else:
                    print(f"Processo {processo.pid}: JNZ - Label {label} não encontrado.")
            else:
                print(f"Processo {processo.pid}: JNZ - {reg} é zero, continuando.")
        elif command == 'READ':
            reg = args[0]
            try:
                valor = int(input(f"Processo {processo.pid}: READ - Digite um valor para {reg}: "))
                processo.registros[reg] = valor
                print(f"Processo {processo.pid}: READ - {reg} = {valor}")
            except ValueError:
                print(f"Processo {processo.pid}: READ - Entrada inválida. Definindo {reg} como 0.")
                processo.registros[reg] = 0
        elif command == 'WRITE':
            reg = args[0]
            print(f"Processo {processo.pid}: WRITE - {reg} = {processo.registros[reg]}")
        elif command == 'LOAD':
            reg, addr = args
            try:
                addr = int(addr)
                valor = processo.memoria_alocada.get(addr, 0)
                processo.registros[reg] = valor
                print(f"Processo {processo.pid}: LOAD - {reg} = {valor} de endereço {addr}")
            except ValueError:
                print(f"Processo {processo.pid}: LOAD - Endereço inválido '{addr}'.")
        elif command == 'STORE':
            reg, addr = args
            try:
                addr = int(addr)
                valor = processo.registros[reg]
                processo.memoria_alocada[addr] = valor
                print(f"Processo {processo.pid}: STORE - {valor} de {reg} armazenado em endereço {addr}")
            except ValueError:
                print(f"Processo {processo.pid}: STORE - Endereço inválido '{addr}'.")
        else:
            print(f"Processo {processo.pid}: Instrução desconhecida '{command}'.")

        processo.contador_programa += 1

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
                if processo.estado == 'terminado':
                    self.escalonador.remover_processo(processo.pid)
                else:
                    processo.estado = 'pronto'