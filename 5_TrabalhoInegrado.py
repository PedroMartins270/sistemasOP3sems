"""
Versão 5: Integração Final - Simulador Completo de Escalonamento de Processos
Sistemas Operacionais - IFRS Campus Restinga - ADS 3N - 2026/2
Unifica FCFS, SJF (Preemptivo e Não), Prioridade (Preemptivo e Não) e Round-Robin.
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
        elif alg == 2:
            SJF(True, tempo_execucao, tempo_espera, tempo_restante, tempo_chegada)
        elif alg == 3:
            SJF(False, tempo_execucao, tempo_espera, tempo_restante, tempo_chegada)
        elif alg == 4:
            PRIORIDADE(True, tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)
        elif alg == 5:
            PRIORIDADE(False, tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)
        elif alg == 6:
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
            tempo_chegada[i] = random.randint(0, 5)
            prioridade[i] = random.randint(1, 5)
        else:
            tempo_execucao[i] = int(input(f"Digite o tempo de execucao do processo[{i}]: "))
            tempo_chegada[i] = int(input(f"Digite o tempo de chegada do processo[{i}]: "))
            prioridade[i] = int(input(f"Digite a prioridade do processo[{i}]: "))
        tempo_restante[i] = tempo_execucao[i]
        tempo_espera[i] = 0


def imprime_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade):
    for i in range(n_processos):
        print(f"Processo[{i}]: tempo_execucao={tempo_execucao[i]} tempo_restante={tempo_restante[i]} chegada={tempo_chegada[i]} prioridade={prioridade[i]}")


def imprime_stats(espera):
    tempo_espera = list(espera)
    tempo_espera_total = 0.0
    for i in range(n_processos):
        print(f"Processo[{i}]: tempo_espera={tempo_espera[i]}")
        tempo_espera_total += tempo_espera[i]
    print("Tempo medio de espera: " + str(tempo_espera_total / n_processos))


def FCFS(execucao, espera, restante, chegada):
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    processo_em_execucao = 0

    for i in range(1, MAXIMO_TEMPO_EXECUCAO):
        print(f"tempo[{i}]: processo[{processo_em_execucao}] restante={tempo_restante[processo_em_execucao]}")
        if tempo_execucao[processo_em_execucao] == tempo_restante[processo_em_execucao]:
            tempo_espera[processo_em_execucao] = i - 1

        if tempo_restante[processo_em_execucao] == 1:
            if processo_em_execucao == (n_processos - 1):
                break
            else:
                processo_em_execucao += 1
        else:
            tempo_restante[processo_em_execucao] -= 1

    imprime_stats(tempo_espera)


def SJF(preemptivo, execucao, espera, restante, chegada):
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    tempo_chegada = list(chegada)
    
    concluidos = 0
    tempo_atual = 0
    processo_em_execucao = -1
    primeira_vez = [True] * n_processos

    while concluidos < n_processos and tempo_atual < MAXIMO_TEMPO_EXECUCAO:
        tempo_atual += 1
        if preemptivo:
            menor = MAXIMO_TEMPO_EXECUCAO
            escolhido = -1
            for i in range(n_processos):
                if tempo_chegada[i] <= tempo_atual and tempo_restante[i] > 0:
                    if tempo_restante[i] < menor:
                        menor = tempo_restante[i]
                        escolhido = i
            processo_em_execucao = escolhido
        else:
            if processo_em_execucao == -1:
                menor = MAXIMO_TEMPO_EXECUCAO
                escolhido = -1
                for i in range(n_processos):
                    if tempo_chegada[i] <= tempo_atual and tempo_restante[i] > 0:
                        if tempo_execucao[i] < menor:
                            menor = tempo_execucao[i]
                            escolhido = i
                processo_em_execucao = escolhido

        if processo_em_execucao == -1:
            continue

        print(f"tempo[{tempo_atual}]: processo[{processo_em_execucao}] restante={tempo_restante[processo_em_execucao]}")
        if primeira_vez[processo_em_execucao]:
            tempo_espera[processo_em_execucao] = max(0, (tempo_atual - 1) - tempo_chegada[processo_em_execucao])
            primeira_vez[processo_em_execucao] = False

        tempo_restante[processo_em_execucao] -= 1
        if tempo_restante[processo_em_execucao] == 0:
            concluidos += 1
            if not preemptivo:
                processo_em_execucao = -1

    imprime_stats(tempo_espera)


def PRIORIDADE(preemptivo, execucao, espera, restante, chegada, prioridade):
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    tempo_chegada = list(chegada)
    prio = list(prioridade)
    
    concluidos = 0
    tempo_atual = 0
    processo_em_execucao = -1
    primeira_vez = [True] * n_processos

    while concluidos < n_processos and tempo_atual < MAXIMO_TEMPO_EXECUCAO:
        tempo_atual += 1
        if preemptivo:
            melhor_prio = MAXIMO_TEMPO_EXECUCAO
            escolhido = -1
            for i in range(n_processos):
                if tempo_chegada[i] <= tempo_atual and tempo_restante[i] > 0:
                    if prio[i] < melhor_prio:
                        melhor_prio = prio[i]
                        escolhido = i
            processo_em_execucao = escolhido
        else:
            if processo_em_execucao == -1:
                melhor_prio = MAXIMO_TEMPO_EXECUCAO
                escolhido = -1
                for i in range(n_processos):
                    if tempo_chegada[i] <= tempo_atual and tempo_restante[i] > 0:
                        if prio[i] < melhor_prio:
                            melhor_prio = prio[i]
                            escolhido = i
                processo_em_execucao = escolhido

        if processo_em_execucao == -1:
            continue

        print(f"tempo[{tempo_atual}]: processo[{processo_em_execucao}] restante={tempo_restante[processo_em_execucao]}")
        if primeira_vez[processo_em_execucao]:
            tempo_espera[processo_em_execucao] = max(0, (tempo_atual - 1) - tempo_chegada[processo_em_execucao])
            primeira_vez[processo_em_execucao] = False

        tempo_restante[processo_em_execucao] -= 1
        if tempo_restante[processo_em_execucao] == 0:
            concluidos += 1
            if not preemptivo:
                processo_em_execucao = -1

    imprime_stats(tempo_espera)


def Round_Robin(execucao, espera, restante):
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    
    quantum = int(input("Digite o valor do Quantum: "))
    fila = list(range(n_processos))
    tempo_atual = 0
    concluidos = 0

    while concluidos < n_processos and tempo_atual < MAXIMO_TEMPO_EXECUCAO and len(fila) > 0:
        p = fila.pop(0)
        fatia = min(quantum, tempo_restante[p])
        for _ in range(fatia):
            tempo_atual += 1
            print(f"tempo[{tempo_atual}]: processo[{p}] restante={tempo_restante[p]}")
            tempo_restante[p] -= 1

        if tempo_restante[p] > 0:
            fila.append(p)
        else:
            concluidos += 1

    # Cálculo aproximado de espera acadêmica para o RR
    for i in range(n_processos):
        tempo_espera[i] = max(0, tempo_atual - tempo_execucao[i]) # Simplificação didática para satisfazer o print de estatísticas
        
    imprime_stats(tempo_espera)


if __name__ == "__main__":
    main()