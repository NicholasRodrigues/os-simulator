# Documentação do Projeto: Máquina Virtual Simulada

## Sumário

1. [Introdução](#introdução)
2. [Arquitetura da VM](#arquitetura-da-vm)
   - [Visão Geral](#visão-geral)
   - [Componentes Principais](#componentes-principais)
3. [Descrição dos Componentes](#descrição-dos-componentes)
   - [Linguagem de Instruções](#linguagem-de-instruções)
   - [Interface de Linha de Comando (CLI)](#interface-de-linha-de-comando-cli)
   - [Gerenciador de Processos](#gerenciador-de-processos)
   - [Gerenciador de Memória](#gerenciador-de-memória)
   - [Gerenciador de E/S](#gerenciador-de-es)
   - [Escalonador de Processos](#escalonador-de-processos)
   - [Sistema de Arquivos Simples](#sistema-de-arquivos-simples)
   - [Simulador de Execução](#simulador-de-execução)
4. [Interação entre os Componentes](#interação-entre-os-componentes)
5. [Como Usar a VM](#como-usar-a-vm)
   - [Preparação do Ambiente](#preparação-do-ambiente)
   - [Execução da VM](#execução-da-vm)
   - [Comandos Disponíveis na CLI](#comandos-disponíveis-na-cli)
   - [Exemplos de Uso](#exemplos-de-uso)
6. [Considerações Finais](#considerações-finais)
7. [Anexos](#anexos)
   - [Estrutura dos Arquivos de Código](#estrutura-dos-arquivos-de-código)
   - [Instruções da Linguagem](#instruções-da-linguagem)
   - [Exemplo de Arquivo de Instruções](#exemplo-de-arquivo-de-instruções)

---

## Introdução

Este documento apresenta uma documentação detalhada do projeto de uma Máquina Virtual (VM) simulada, desenvolvida em Python. A VM foi projetada para simular a execução de processos em um sistema operacional de propósito específico, implementando componentes essenciais como gerenciamento de processos, memória, entrada/saída (E/S), escalonamento de processos, um sistema de arquivos simples, uma linguagem de instruções e uma interface de linha de comando (CLI).

O objetivo é fornecer uma visão abrangente da arquitetura da VM, detalhar cada componente implementado e orientar sobre como utilizar o sistema.

---

## Arquitetura da VM

### Visão Geral

A arquitetura da VM é modular e orientada a objetos, permitindo uma fácil manutenção e extensibilidade. Cada componente é responsável por uma funcionalidade específica, e a interação entre eles permite a simulação de um ambiente de sistema operacional completo.

### Componentes Principais

1. **Linguagem de Instruções**: Define as instruções que os processos podem executar.
2. **Interface de Linha de Comando (CLI)**: Permite a interação do usuário com a VM.
3. **Gerenciador de Processos**: Cria, gerencia e termina processos.
4. **Gerenciador de Memória**: Aloca e libera memória para processos.
5. **Gerenciador de E/S**: Simula dispositivos de entrada/saída e gerencia operações de E/S.
6. **Escalonador de Processos**: Decide qual processo será executado em determinado momento.
7. **Sistema de Arquivos Simples**: Fornece operações básicas de arquivos.
8. **Simulador de Execução**: Coordena a execução dos processos.

---

## Descrição dos Componentes

### Linguagem de Instruções

A linguagem de instruções permite que os processos realizem operações básicas necessárias para a execução dentro da VM. As instruções implementadas incluem:

- **Operações Aritméticas**:
  - `ADD R1 R2`: Soma o valor de `R2` ao registrador `R1`.
  - `SUB R1 R2`: Subtrai o valor de `R2` do registrador `R1`.
  - `MUL R1 R2`: Multiplica `R1` por `R2`.
  - `DIV R1 R2`: Divide `R1` por `R2`.

- **Controle de Fluxo**:
  - `JMP LABEL`: Salta para a instrução marcada com `LABEL`.
  - `JZ R1 LABEL`: Salta para `LABEL` se o registrador `R1` for zero.
  - `JNZ R1 LABEL`: Salta para `LABEL` se o registrador `R1` não for zero.

- **Operações de E/S**:
  - `READ R1`: Lê um valor do usuário e armazena no registrador `R1`.
  - `WRITE R1`: Escreve o valor do registrador `R1` na saída.

- **Manipulação de Memória**:
  - `LOAD R1 ENDEREÇO`: Carrega o valor do endereço de memória especificado no registrador `R1`.
  - `STORE R1 ENDEREÇO`: Armazena o valor do registrador `R1` no endereço de memória especificado.

- **Outras Instruções**:
  - `NOP`: Não realiza nenhuma operação.
  - `END`: Termina a execução do processo.

A sintaxe das instruções segue o padrão:

```
INSTRUÇÃO ARGUMENTO1 ARGUMENTO2 ...
```

### Interface de Linha de Comando (CLI)

A CLI permite que o usuário interaja com a VM por meio de comandos simples. Os comandos implementados incluem:

- **create_process \<arquivo\>**: Cria um novo processo a partir de um arquivo de instruções.
- **run_process**: Inicia a execução dos processos prontos.
- **list_processes**: Lista todos os processos gerenciados pela VM.
- **monitor_resources**: Exibe informações sobre o uso de recursos, como memória e processos bloqueados.
- **exit**: Encerra a VM.

A CLI é responsável por interpretar os comandos do usuário e acionar as funções correspondentes nos componentes da VM.

### Gerenciador de Processos

O Gerenciador de Processos é responsável por:

- **Criar Processos**: Inicializa um novo processo com um identificador único (PID), estado inicial e aloca memória necessária.
- **Gerenciar Estados**: Mantém o controle dos estados dos processos (pronto, executando, bloqueado, terminado).
- **Terminar Processos**: Libera recursos associados ao processo e remove-o do sistema.

Cada processo possui:

- **PID**: Identificador único.
- **Estado**: Estado atual do processo.
- **Contador de Programa (PC)**: Aponta para a próxima instrução a ser executada.
- **Registros**: Conjunto de registradores (e.g., `R0`, `R1`, `R2`, `R3`).
- **Memória Alocada**: Segmento de memória reservado para o processo.
- **Instruções**: Lista de instruções a serem executadas.

### Gerenciador de Memória

O Gerenciador de Memória implementa um esquema simples de segmentação para:

- **Alocar Memória**: Reserva segmentos de memória para novos processos.
- **Liberar Memória**: Libera segmentos quando processos terminam.
- **Gerenciar Espaço Livre**: Mantém uma tabela de alocações e espaços livres.

A memória é representada por uma lista ou array, e cada processo tem acesso apenas ao seu segmento alocado, garantindo isolamento entre processos.

### Gerenciador de E/S

O Gerenciador de E/S simula dispositivos de entrada/saída e gerencia operações de E/S dos processos. Suas funções incluem:

- **Gerenciar Filas de Dispositivos**: Mantém filas de requisições para cada dispositivo simulado (e.g., teclado, disco, rede).
- **Bloquear Processos**: Processos que solicitam E/S são bloqueados até que a operação seja concluída.
- **Processar Operações de E/S**: Simula o processamento de operações de E/S, liberando processos bloqueados.

### Escalonador de Processos

O Escalonador decide qual processo será executado com base em uma política de escalonamento. As políticas implementadas são:

- **FIFO (First-In, First-Out)**: Executa processos na ordem de chegada.
- **Round Robin**: Alterna entre processos, dando a cada um um tempo de execução fixo (quantum).
- **SJF (Shortest Job First)**: Prioriza processos com menor número de instruções.

O Escalonador interage com o Gerenciador de Processos e o Simulador de Execução para alternar entre processos.

### Sistema de Arquivos Simples

O Sistema de Arquivos permite operações básicas:

- **Criar Arquivo**: `CREATE_FILE "nome.txt"`
- **Escrever em Arquivo**: `WRITE_FILE "nome.txt" "conteúdo"`
- **Ler Arquivo**: `READ_FILE "nome.txt"`
- **Deletar Arquivo**: `DELETE_FILE "nome.txt"`

Os arquivos são armazenados em uma estrutura de dados, como um dicionário, que mapeia nomes de arquivos para seus conteúdos.

### Simulador de Execução

O Simulador de Execução coordena a execução dos processos, implementando o ciclo:

1. **Busca**: Obtém a próxima instrução do processo.
2. **Decodificação**: Interpreta a instrução e seus argumentos.
3. **Execução**: Realiza a operação especificada, interagindo com outros componentes conforme necessário.
4. **Atualização do Estado**: Atualiza o contador de programa e o estado do processo.

O Simulador de Execução também gerencia a alternância entre processos, conforme a política do Escalonador, e lida com situações como bloqueio devido a E/S.

---

## Interação entre os Componentes

- **CLI**: Recebe comandos do usuário e aciona os componentes apropriados.
- **Gerenciador de Processos**: Cria e termina processos, interagindo com o Gerenciador de Memória para alocar e liberar memória.
- **Escalonador**: Mantém a fila de processos prontos e decide a ordem de execução.
- **Simulador de Execução**: Executa as instruções dos processos e interage com o Gerenciador de E/S e o Sistema de Arquivos quando necessário.
- **Gerenciador de Memória**: Aloca memória para processos quando são criados e libera quando terminam.
- **Gerenciador de E/S**: Gerencia as operações de E/S solicitadas pelos processos, bloqueando-os até a conclusão da operação.
- **Sistema de Arquivos**: Fornece serviços de leitura e escrita de arquivos para os processos.

---

## Como Usar a VM

### Preparação do Ambiente

1. **Instale o Python 3**: Certifique-se de que o Python 3 está instalado no seu sistema.

2. **Arquivos Necessários**: Todos os arquivos de código devem estar no mesmo diretório:
   - `cli.py`
   - `GerenciadorProcessos.py`
   - `GerenciadorMemoria.py`
   - `GerenciadorIO.py`
   - `Escalonador.py`
   - `SimuladorExecucao.py`
   - `Processo.py`
   - `SistemaArquivos.py`

3. **Arquivos de Instruções**: Crie arquivos de texto contendo instruções para os processos. Veja um exemplo na seção [Exemplo de Arquivo de Instruções](#exemplo-de-arquivo-de-instruções).

### Execução da VM

Para iniciar a VM, execute o arquivo `cli.py`:

```bash
python cli.py
```

### Comandos Disponíveis na CLI

- **create_process \<arquivo\>**: Cria um novo processo a partir do arquivo especificado.
- **run_process**: Inicia a execução dos processos prontos.
- **list_processes**: Lista todos os processos gerenciados.
- **monitor_resources**: Exibe informações sobre o uso de recursos.
- **exit**: Encerra a VM.

### Exemplos de Uso

#### Criar e Executar um Processo

1. **Crie um arquivo de instruções**, por exemplo, `processo_exemplo.txt`:

   ```plaintext
   READ R1
   ADD R1 R1
   WRITE R1
   END
   ```

2. **Inicie a VM**:

   ```bash
   python cli.py
   ```

3. **Crie o processo**:

   ```bash
   VM> create_process processo_exemplo.txt
   ```

4. **Execute os processos**:

   ```bash
   VM> run_process
   ```

   - Durante a execução, o processo solicitará uma entrada do usuário, dobrará o valor e exibirá o resultado.

#### Listar Processos

```bash
VM> list_processes
```

- Exibe uma lista com os PIDs e estados dos processos gerenciados.

#### Monitorar Recursos

```bash
VM> monitor_resources
```

- Exibe informações sobre memória alocada e processos bloqueados.

#### Sair da VM

```bash
VM> exit
```

---

## Considerações Finais

O projeto implementa uma Máquina Virtual que simula aspectos essenciais de um sistema operacional, incluindo gerenciamento de processos, memória, E/S, escalonamento e sistema de arquivos. A arquitetura modular permite fácil manutenção e expansão. A VM suporta uma linguagem de instruções que permite operações básicas necessárias para a execução de processos em um ambiente simulado.

---

## Anexos

### Estrutura dos Arquivos de Código

- **cli.py**: Interface de linha de comando para interação com o usuário.
- **GerenciadorProcessos.py**: Gerencia criação, estados e término de processos.
- **GerenciadorMemoria.py**: Gerencia alocação e liberação de memória.
- **GerenciadorIO.py**: Simula dispositivos de E/S e gerencia operações.
- **Escalonador.py**: Implementa políticas de escalonamento de processos.
- **SimuladorExecucao.py**: Coordena a execução dos processos.
- **Processo.py**: Define a estrutura e comportamento de um processo.
- **SistemaArquivos.py**: Implementa operações básicas de arquivos.

### Instruções da Linguagem

#### Operações Aritméticas

- **ADD R1 R2**: Soma `R2` a `R1`.
- **SUB R1 R2**: Subtrai `R2` de `R1`.
- **MUL R1 R2**: Multiplica `R1` por `R2`.
- **DIV R1 R2**: Divide `R1` por `R2`.

#### Controle de Fluxo

- **JMP LABEL**: Salta para a instrução com o rótulo `LABEL`.
- **JZ R1 LABEL**: Salta para `LABEL` se `R1` for zero.
- **JNZ R1 LABEL**: Salta para `LABEL` se `R1` não for zero.

#### Operações de E/S

- **READ R1**: Lê um valor do usuário e armazena em `R1`.
- **WRITE R1**: Escreve o valor de `R1` na saída.

#### Manipulação de Memória

- **LOAD R1 ENDEREÇO**: Carrega o valor do endereço na memória em `R1`.
- **STORE R1 ENDEREÇO**: Armazena o valor de `R1` no endereço de memória.

#### Outras Instruções

- **NOP**: Não faz nada; passa para a próxima instrução.
- **END**: Termina a execução do processo.

### Exemplo de Arquivo de Instruções

**processo_exemplo.txt**

```plaintext
# Programa que lê um valor, dobra e escreve o resultado
READ R1
ADD R1 R1
WRITE R1
END
```

---

## Conclusão

Este documento forneceu uma visão detalhada da arquitetura e dos componentes da Máquina Virtual simulada. A implementação atende aos requisitos propostos, fornecendo um ambiente funcional que simula a execução de processos em um sistema operacional simplificado. Os componentes interagem de forma coesa para permitir a criação, gerenciamento e execução de processos, com suporte a operações de E/S, gerenciamento de memória, escalonamento e manipulação de arquivos.

A documentação visa facilitar a compreensão do sistema para futuros desenvolvedores ou usuários interessados em explorar ou expandir a funcionalidade da VM.

---
