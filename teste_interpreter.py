from GerenciadorProcessos import GerenciadorProcessos
from Escalonador import Escalonador
from SimuladorExecucao import SimuladorExecucao

def teste_interpreter():
    gerenciador = GerenciadorProcessos()
    escalonador = Escalonador(politica='FIFO')
    instrucoes = [
        'READ R1',
        'LOAD R2 0',
        'ADD R1 R2',
        'STORE R1 0',
        'WRITE R1',
        'JNZ R1 loop',
        'END',
        'loop: SUB R1 R3',
        'JMP 2',
    ]
    p1 = gerenciador.criar_processo(instrucoes)
    escalonador.adicionar_processo(p1)
    simulador = SimuladorExecucao(escalonador)
    simulador.ciclo_de_execucao()
    print("Teste interpreter passou.\n")
    
if __name__ == "__main__":
    teste_interpreter()