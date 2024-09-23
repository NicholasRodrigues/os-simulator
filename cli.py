from GerenciadorProcessos import GerenciadorProcessos
from Escalonador import Escalonador
from SimuladorExecucao import SimuladorExecucao
def cli():
    gerenciador = GerenciadorProcessos()
    escalonador = Escalonador(politica='FIFO')  # Você pode mudar a política aqui
    simulador = SimuladorExecucao(escalonador)

    while True:
        command = input("VM> ").strip()
        if not command:
            continue
        tokens = command.split()
        cmd = tokens[0]
        args = tokens[1:]

        if cmd == 'create_process':
            if not args:
                print("Uso: create_process caminho_do_arquivo")
                continue
            arquivo = args[0]
            try:
                with open(arquivo, 'r') as f:
                    instrucoes = [line.strip() for line in f if line.strip()]
                processo = gerenciador.criar_processo(instrucoes)
                escalonador.adicionar_processo(processo)
            except FileNotFoundError:
                print(f"Arquivo {arquivo} não encontrado.")
            except Exception as e:
                print(f"Erro ao criar processo: {e}")
        elif cmd == 'run_process':
            try:
                simulador.ciclo_de_execucao()
            except AttributeError as e:
                print(f"Erro: {e}. Verifique se 'ciclo_de_execucao' está implementado corretamente.")
            except Exception as e:
                print(f"Erro durante a execução dos processos: {e}")
        elif cmd == 'list_processes':
            processos = gerenciador.listar_processos()
            for p in processos:
                print(p)
        elif cmd == 'monitor_resources':
            # Simulação simples de monitoramento
            print("Monitoramento de Recursos não implementado.")
        elif cmd == 'exit':
            print("Encerrando VM.")
            break
        else:
            print(f"Comando '{cmd}' não reconhecido.")
            
if __name__ == "__main__":
    cli()