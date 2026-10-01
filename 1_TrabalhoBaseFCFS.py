"""
Versão 1: Código-Base Comentado (FCFS)
Sistemas Operacionais - IFRS Campus Restinga - ADS 3N - 2026/2
Explicação detalhada do código-base e do algoritmo FCFS (First-Come, First-Served).
"""

import random

# Constante que define o teto máximo de tempo de simulação para evitar loops infinitos.
MAXIMO_TEMPO_EXECUCAO = 65535

# Número padrão de processos configurado na simulação.
n_processos = 3


def main():
    """
    Função principal que inicializa as estruturas de dados (listas paralelas),
    popula os processos, exibe o menu interativo e direciona para as escolhas do usuário.
    """
    # Criação das listas paralelas para armazenar os atributos de cada processo.
    # O uso de listas paralelas garante que o índice 'i' represente o mesmo processo em todas as listas.
    tempo_execucao = [0] * n_processos
    tempo_chegada = [0] * n_processos
    prioridade = [0] * n_processos
    tempo_espera = [0] * n_processos
    tempo_restante = [0] * n_processos

    # Popula os dados iniciais dos processos (via teclado ou de forma aleatória).
    popular_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

    # Imprime o estado inicial da lista de processos cadastrados.
    imprime_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

    # Loop principal do menu interativo do simulador.
    while True:
        alg = int(input(
            "Escolha o algoritmo?: [1=FCFS 2=SJF Preemptivo 3=SJF Nao Preemptivo  "
            "4=Prioridade Preemptivo 5=Prioridade Nao Preemptivo  6=Round_Robin  "
            "7=Imprime lista de processos 8=Popular processos novamente 9=Sair]: "))

        if alg == 1:  # FCFS (First-Come, First-Served)
            FCFS(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada)

        elif alg == 2:  # SJF PREEMPTIVO
            SJF(True, tempo_execucao, tempo_espera, tempo_restante, tempo_chegada)

        elif alg == 3:  # SJF NAO PREEMPTIVO
            SJF(False, tempo_execucao, tempo_espera, tempo_restante, tempo_chegada)

        elif alg == 4:  # PRIORIDADE PREEMPTIVO
            PRIORIDADE(True, tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

        elif alg == 5:  # PRIORIDADE NAO PREEMPTIVO
            PRIORIDADE(False, tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

        elif alg == 6:  # Round_Robin
            Round_Robin(tempo_execucao, tempo_espera, tempo_restante)

        elif alg == 7:  # IMPRIME CONTEUDO INICIAL DOS PROCESSOS
            imprime_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

        elif alg == 8:  # REATRIBUI VALORES INICIAIS SEM REINICIAR O PROGRAMA
            popular_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)
            imprime_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

        elif alg == 9:  # Encerra o programa
            break


def popular_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade):
    """
    Preenche os arrays de processos de forma manual (digitada) ou aleatória.
    O tempo restante inicial é igual ao tempo total de execução.
    """
    aleatorio = int(input("Sera aleatorio?:  "))

    for i in range(n_processos):
        if aleatorio == 1:
            tempo_execucao[i] = random.randint(1, 10)
            tempo_chegada[i] = random.randint(1, 10)
            prioridade[i] = random.randint(1, 15)
        else:
            tempo_execucao[i] = int(input("Digite o tempo de execucao do processo[" + str(i) + "]:  "))
            tempo_chegada[i] = int(input("Digite o tempo de chegada do processo[" + str(i) + "]:  "))
            prioridade[i] = int(input("Digite a prioridade do processo[" + str(i) + "]:  "))

        # No início, o tempo que falta rodar é igual ao tempo total de execução do processo.
        tempo_restante[i] = tempo_execucao[i]
        tempo_espera[i] = 0


def imprime_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade):
    """Exibe na tela os parâmetros atuais de cada processo da lista."""
    for i in range(n_processos):
        print("Processo[" + str(i) + "]: tempo_execucao=" + str(tempo_execucao[i]) +
              " tempo_restante=" + str(tempo_restante[i]) +
              " tempo_chegada=" + str(tempo_chegada[i]) +
              " prioridade =" + str(prioridade[i]))


def imprime_stats(espera):
    """Calcula e exibe o tempo de espera individual de cada processo e o tempo médio geral."""
    tempo_espera = list(espera)
    tempo_espera_total = 0.0

    for i in range(n_processos):
        print("Processo[" + str(i) + "]: tempo_espera=" + str(tempo_espera[i]))
        tempo_espera_total = tempo_espera_total + tempo_espera[i]

    print("Tempo medio de espera: " + str(tempo_espera_total / n_processos))


def FCFS(execucao, espera, restante, chegada):
    """
    Implementação do algoritmo FCFS (First-Come, First-Served).
    Executa os processos na ordem em que aparecem na lista (de 0 até n_processos - 1),
    sem interrupções (não preemptivo). Criamos cópias locais das listas para proteger 
    os dados originais e permitir comparações posteriores.
    """
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)

    processo_em_execucao = 0  # No FCFS puro, o primeiro processo a rodar é o índice 0.

    # Loop que simula o avanço do relógio do sistema (instante a instante).
    for i in range(1, MAXIMO_TEMPO_EXECUCAO):
        print("tempo[" + str(i) + "]: processo[" + str(processo_em_execucao) + "] restante=" +
              str(tempo_restante[processo_em_execucao]))

        # Identifica o exato momento em que o processo começa a ser atendido pela primeira vez
        # para registrar o seu tempo de espera acumulado até ali.
        if tempo_execucao[processo_em_execucao] == tempo_restante[processo_em_execucao]:
            tempo_espera[processo_em_execucao] = i - 1

        # Se o tempo restante do processo atual chega a 1, significa que ele conclui neste ciclo.
        if tempo_restante[processo_em_execucao] == 1:
            if processo_em_execucao == (n_processos - 1):
                break  # Todos os processos terminaram; encerra a simulação.
            else:
                processo_em_execucao = processo_em_execucao + 1  # Passa para o próximo processo da fila.
        else:
            # Caso contrário, decrementa o tempo restante de execução do processo atual.
            tempo_restante[processo_em_execucao] = tempo_restante[processo_em_execucao] - 1

    imprime_stats(tempo_espera)


def SJF(preemptivo, execucao, espera, restante, chegada):
    pass

def PRIORIDADE(preemptivo, execucao, espera, restante, chegada, prioridade):
    pass

def Round_Robin(execucao, espera, restante):
    pass

if __name__ == "__main__":
    main()