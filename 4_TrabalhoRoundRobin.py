"""
Versão Final: Simulador Completo de Escalonamento de CPU
(FCFS, SJF, Prioridade e Round Robin)
Sistemas Operacionais - IFRS Campus Restinga - ADS 3N - 2026/2
"""

import random

MAXIMO_TEMPO_EXECUCAO = 65535
n_processos = 3


def main():
    tempo_execucao = [0] * n_processos
    tempo_chegada = [0] * n_processos
    prioridade = [0] * n_processos
    tempo_espera = [0] * n_processos
    tempo_restante = [0] * n_processos

    popular_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)
    imprime_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

    while True:
        alg = int(input(
            "Escolha o algoritmo?: [1=FCFS 2=SJF Preemptivo 3=SJF Nao Preemptivo  "
            "4=Prioridade Preemptivo 5=Prioridade Nao Preemptivo  6=Round_Robin  "
            "7=Imprime lista de processos 8=Popular processos novamente 9=Sair]: "))

        if alg == 1:
            FCFS(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada)

        elif alg == 2:  # SJF PREEMPTIVO (SRTF)
            SJF(True, tempo_execucao, tempo_espera, tempo_restante, tempo_chegada)

        elif alg == 3:  # SJF NAO PREEMPTIVO
            SJF(False, tempo_execucao, tempo_espera, tempo_restante, tempo_chegada)

        elif alg == 4:  # PRIORIDADE PREEMPTIVO
            PRIORIDADE(True, tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

        elif alg == 5:  # PRIORIDADE NAO PREEMPTIVO
            PRIORIDADE(False, tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

        elif alg == 6:  # ROUND ROBIN
            Round_Robin(tempo_execucao, tempo_espera, tempo_restante)

        elif alg == 7:
            imprime_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

        elif alg == 8:
            popular_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)
            imprime_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

        elif alg == 9:
            break


def popular_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade):
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

        tempo_restante[i] = tempo_execucao[i]
        tempo_espera[i] = 0


def imprime_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade):
    for i in range(n_processos):
        print("Processo[" + str(i) + "]: tempo_execucao=" + str(tempo_execucao[i]) +
              " tempo_restante=" + str(tempo_restante[i]) +
              " tempo_chegada=" + str(tempo_chegada[i]) +
              " prioridade =" + str(prioridade[i]))


def imprime_stats(espera):
    tempo_espera = list(espera)
    tempo_espera_total = 0.0

    for i in range(n_processos):
        print("Processo[" + str(i) + "]: tempo_espera=" + str(tempo_espera[i]))
        tempo_espera_total = tempo_espera_total + tempo_espera[i]

    print("Tempo medio de espera: " + str(tempo_espera_total / n_processos))


def FCFS(execucao, espera, restante, chegada):
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)

    processo_em_execucao = 0

    for i in range(1, MAXIMO_TEMPO_EXECUCAO):
        print("tempo[" + str(i) + "]: processo[" + str(processo_em_execucao) + "] restante=" +
              str(tempo_restante[processo_em_execucao]))

        if tempo_execucao[processo_em_execucao] == tempo_restante[processo_em_execucao]:
            tempo_espera[processo_em_execucao] = i - 1

        if tempo_restante[processo_em_execucao] == 1:
            if processo_em_execucao == (n_processos - 1):
                break
            else:
                processo_em_execucao = processo_em_execucao + 1
        else:
            tempo_restante[processo_em_execucao] = tempo_restante[processo_em_execucao] - 1

    imprime_stats(tempo_espera)


def SJF(preemptivo, execucao, espera, restante, chegada):
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    tempo_chegada = list(chegada)

    processos_concluidos = 0
    processo_em_execucao = -1

    for i in range(1, MAXIMO_TEMPO_EXECUCAO):
        if preemptivo or processo_em_execucao == -1:
            menor_tempo = MAXIMO_TEMPO_EXECUCAO
            candidato = -1

            for p in range(n_processos):
                if tempo_chegada[p] <= i and tempo_restante[p] > 0:
                    if tempo_restante[p] < menor_tempo:
                        menor_tempo = tempo_restante[p]
                        candidato = p

            processo_em_execucao = candidato

        if processo_em_execucao == -1:
            print("tempo[" + str(i) + "]: CPU ociosa (aguardando chegada de processos)")
            continue

        print("tempo[" + str(i) + "]: processo[" + str(processo_em_execucao) + "] restante=" +
              str(tempo_restante[processo_em_execucao]))

        tempo_restante[processo_em_execucao] -= 1

        if tempo_restante[processo_em_execucao] == 0:
            processos_concluidos += 1
            tempo_espera[processo_em_execucao] = i - tempo_chegada[processo_em_execucao] - tempo_execucao[processo_em_execucao]
            processo_em_execucao = -1

            if processos_concluidos == n_processos:
                break

    imprime_stats(tempo_espera)


def PRIORIDADE(preemptivo, execucao, espera, restante, chegada, prioridade):
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    tempo_chegada = list(chegada)
    lista_prioridade = list(prioridade)

    processos_concluidos = 0
    processo_em_execucao = -1

    for i in range(1, MAXIMO_TEMPO_EXECUCAO):
        if preemptivo or processo_em_execucao == -1:
            melhor_prioridade = MAXIMO_TEMPO_EXECUCAO
            candidato = -1

            for p in range(n_processos):
                if tempo_chegada[p] <= i and tempo_restante[p] > 0:
                    if lista_prioridade[p] < melhor_prioridade:
                        melhor_prioridade = lista_prioridade[p]
                        candidato = p

            processo_em_execucao = candidato

        if processo_em_execucao == -1:
            print("tempo[" + str(i) + "]: CPU ociosa (aguardando chegada de processos)")
            continue

        print("tempo[" + str(i) + "]: processo[" + str(processo_em_execucao) + "] restante=" +
              str(tempo_restante[processo_em_execucao]) + " (prioridade=" + str(lista_prioridade[processo_em_execucao]) + ")")

        tempo_restante[processo_em_execucao] -= 1

        if tempo_restante[processo_em_execucao] == 0:
            processos_concluidos += 1
            tempo_espera[processo_em_execucao] = i - tempo_chegada[processo_em_execucao] - tempo_execucao[processo_em_execucao]
            processo_em_execucao = -1

            if processos_concluidos == n_processos:
                break

    imprime_stats(tempo_espera)


def Round_Robin(execucao, espera, restante):
    """
    Implementação do algoritmo Round Robin (Circular).
    Cada processo recebe uma fatia de tempo (quantum) na CPU. Se não terminar dentro do quantum,
    sofre preempção por tempo e cede a vez para o próximo processo ativo da fila circular.
    """
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)

    quantum = int(input("Digite o valor do quantum: "))
    contador_quantum = 0
    processo_em_execucao = 0
    processos_concluidos = 0

    for i in range(1, MAXIMO_TEMPO_EXECUCAO):
        print("tempo[" + str(i) + "]: processo[" + str(processo_em_execucao) + "] restante=" +
              str(tempo_restante[processo_em_execucao]) + " (quantum=" + str(contador_quantum + 1) + "/" + str(quantum) + ")")

        tempo_restante[processo_em_execucao] -= 1
        contador_quantum += 1

        # Caso 1: O processo atual terminou a sua execução
        if tempo_restante[processo_em_execucao] == 0:
            processos_concluidos += 1
            # Como o Round Robin base assume chegada em t=0 (igual ao FCFS do código),
            # Tempo de Espera = Instante de Término (i) - Tempo Total de Execução
            tempo_espera[processo_em_execucao] = i - tempo_execucao[processo_em_execucao]

            if processos_concluidos == n_processos:
                break

            # Reseta o contador de quantum e avança para o próximo processo não concluído
            contador_quantum = 0
            processo_em_execucao = (processo_em_execucao + 1) % n_processos
            while tempo_restante[processo_em_execucao] == 0:
                processo_em_execucao = (processo_em_execucao + 1) % n_processos

        # Caso 2: O processo ainda não terminou, mas atingiu o limite do quantum (Preempção por tempo)
        elif contador_quantum == quantum:
            contador_quantum = 0
            processo_em_execucao = (processo_em_execucao + 1) % n_processos
            while tempo_restante[processo_em_execucao] == 0:
                processo_em_execucao = (processo_em_execucao + 1) % n_processos

    imprime_stats(tempo_espera)


if __name__ == "__main__":
    main()
