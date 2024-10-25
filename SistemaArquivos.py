# SistemaArquivos.py

class SistemaArquivos:
    def __init__(self):
        """
        Inicializa o sistema de arquivos simples.
        """
        self.arquivos = {}  # Dicionário que mapeia nomes de arquivos para conteúdo

    def criar_arquivo(self, nome):
        """
        Cria um arquivo vazio.

        :param nome: Nome do arquivo.
        """
        if nome in self.arquivos:
            print(f"Sistema de Arquivos: Arquivo '{nome}' já existe.")
        else:
            self.arquivos[nome] = ''
            print(f"Sistema de Arquivos: Arquivo '{nome}' criado.")

    def escrever_arquivo(self, nome, conteudo):
        """
        Escreve conteúdo em um arquivo.

        :param nome: Nome do arquivo.
        :param conteudo: Conteúdo a ser escrito.
        """
        if nome in self.arquivos:
            self.arquivos[nome] = conteudo
            print(f"Sistema de Arquivos: Conteúdo escrito em '{nome}'.")
        else:
            print(f"Sistema de Arquivos: Arquivo '{nome}' não encontrado.")

    def ler_arquivo(self, nome):
        """
        Lê o conteúdo de um arquivo.

        :param nome: Nome do arquivo.
        :return: Conteúdo do arquivo ou None se não encontrado.
        """
        if nome in self.arquivos:
            print(f"Sistema de Arquivos: Lendo conteúdo de '{nome}'.")
            return self.arquivos[nome]
        else:
            print(f"Sistema de Arquivos: Arquivo '{nome}' não encontrado.")
            return None

    def deletar_arquivo(self, nome):
        """
        Deleta um arquivo.

        :param nome: Nome do arquivo.
        """
        if nome in self.arquivos:
            del self.arquivos[nome]
            print(f"Sistema de Arquivos: Arquivo '{nome}' deletado.")
        else:
            print(f"Sistema de Arquivos: Arquivo '{nome}' não encontrado.")
