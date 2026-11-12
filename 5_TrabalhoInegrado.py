"""
Versão Final: Simulador Completo de Escalonamento de CPU
(FCFS, SJF, Prioridade e Round Robin)
Sistemas Operacionais - IFRS Campus Restinga - ADS 3N - 2026/2
"""

import random  # Biblioteca para gerar números aleatórios (usada para criar processos automaticamente)

MAXIMO_TEMPO_EXECUCAO = 65535  # Limite máximo de tempo para simular o relógio da CPU
n_processos = 3  # Quantidade padrão de processos criados


def main():
    # Cria listas preenchidas com zeros para guardar os dados dos processos
    tempo_execucao = [0] * n_processos
    tempo_chegada = [0] * n_processos
    prioridade = [0] * n_processos
    tempo_espera = [0] * n_processos
    tempo_restante = [0] * n_processos

    # Preenche os dados iniciais dos processos e os exibe na tela
    popular_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)
    imprime_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

    # Loop infinito que exibe o menu principal para o usuário escolher o que fazer
    while True:
        alg = int(input(
            "Escolha o algoritmo?: [1=FCFS 2=SJF Preemptivo 3=SJF Nao Preemptivo  "
            "4=Prioridade Preemptivo 5=Prioridade Nao Preemptivo  6=Round_Robin  "
            "7=Imprime lista de processos 8=Popular processos novamente 9=Sair]: "))

        # Executa o algoritmo escolhido pelo usuário com base no número digitado
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
            break  # Sai do loop e encerra o programa


def popular_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade):
    # Pergunta se o usuário quer gerar valores aleatórios ou digitar manualmente
    aleatorio = int(input("Sera aleatorio?:  "))

    for i in range(n_processos):
        if aleatorio == 1:
            # Gera valores automáticos de 1 a 10
            tempo_execucao[i] = random.randint(1, 10)
            tempo_chegada[i] = random.randint(1, 10)
            prioridade[i] = random.randint(1, 15)
        else:
            # Pede para o usuário digitar os valores de cada processo
            tempo_execucao[i] = int(input("Digite o tempo de execucao do processo[" + str(i) + "]:  "))
            tempo_chegada[i] = int(input("Digite o tempo de chegada do processo[" + str(i) + "]:  "))
            prioridade[i] = int(input("Digite a prioridade do processo[" + str(i) + "]:  "))

        tempo_restante[i] = tempo_execucao[i]  # O tempo restante começa igual ao de execução
        tempo_espera[i] = 0


def imprime_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade):
    # Mostra na tela os dados atuais de todos os processos
    for i in range(n_processos):
        print("Processo[" + str(i) + "]: tempo_execucao=" + str(tempo_execucao[i]) +
              " tempo_restante=" + str(tempo_restante[i]) +
              " tempo_chegada=" + str(tempo_chegada[i]) +
              " prioridade =" + str(prioridade[i]))


def imprime_stats(espera):
    # Mostra o tempo de espera de cada processo e calcula a média geral
    tempo_espera = list(espera)
    tempo_espera_total = 0.0

    for i in range(n_processos):
        print("Processo[" + str(i) + "]: tempo_espera=" + str(tempo_espera[i]))
        tempo_espera_total = tempo_espera_total + tempo_espera[i]

    print("Tempo medio de espera: " + str(tempo_espera_total / n_processos))


def FCFS(execucao, espera, restante, chegada):
    # FCFS (First-Come, First-Served): O primeiro que chega é o primeiro a ser executado
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)

    processo_em_execucao = 0

    # Simula o relógio da CPU passo a passo
    for i in range(1, MAXIMO_TEMPO_EXECUCAO):
        print("tempo[" + str(i) + "]: processo[" + str(processo_em_execucao) + "] restante=" +
              str(tempo_restante[processo_em_execucao]))

        if tempo_execucao[processo_em_execucao] == tempo_restante[processo_em_execucao]:
            tempo_espera[processo_em_execucao] = i - 1

        # Se o processo atual acabou, passa para o próximo; senão, reduz 1 segundo do tempo restante
        if tempo_restante[processo_em_execucao] == 1:
            if processo_em_execucao == (n_processos - 1):
                break
            else:
                processo_em_execucao = processo_em_execucao + 1
        else:
            tempo_restante[processo_em_execucao] = tempo_restante[processo_em_execucao] - 1

    imprime_stats(tempo_espera)


def SJF(preemptivo, execucao, espera, restante, chegada):
    # SJF (Shortest Job First): Executa primeiro o processo que tem o MENOR tempo de execução
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    tempo_chegada = list(chegada)

    processos_concluidos = 0
    processo_em_execucao = -1

    for i in range(1, MAXIMO_TEMPO_EXECUCAO):
        # Escolhe o processo com o menor tempo restante que já tenha chegado
        if preemptivo or processo_em_execucao == -1:
            menor_tempo = MAXIMO_TEMPO_EXECUCAO
            candidato = -1

            for p in range(n_processos):
                if tempo_chegada[p] <= i and tempo_restante[p] > 0:
                    if tempo_restante[p] < menor_tempo:
                        menor_tempo = tempo_restante[p]
                        candidato = p

            processo_em_execucao = candidato

        # Se nenhum processo chegou ainda, a CPU fica ociosa
        if processo_em_execucao == -1:
            print("tempo[" + str(i) + "]: CPU ociosa (aguardando chegada de processos)")
            continue

        print("tempo[" + str(i) + "]: processo[" + str(processo_em_execucao) + "] restante=" +
              str(tempo_restante[processo_em_execucao]))

        tempo_restante[processo_em_execucao] -= 1

        # Se o processo terminou, calcula o tempo de espera e verifica se todos terminaram
        if tempo_restante[processo_em_execucao] == 0:
            processos_concluidos += 1
            tempo_espera[processo_em_execucao] = i - tempo_chegada[processo_em_execucao] - tempo_execucao[processo_em_execucao]
            processo_em_execucao = -1

            if processos_concluidos == n_processos:
                break

    imprime_stats(tempo_espera)


def PRIORIDADE(preemptivo, execucao, espera, restante, chegada, prioridade):
    # Executa os processos com base na prioridade (geralmente menor número = maior prioridade)
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    tempo_chegada = list(chegada)
    lista_prioridade = list(prioridade)

    processos_concluidos = 0
    processo_em_execucao = -1

    for i in range(1, MAXIMO_TEMPO_EXECUCAO):
        # Busca o processo com a melhor prioridade entre os que já chegaram
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

    quantum = int(input("Digite o valor do quantum: "))  # Tempo máximo que cada processo fica na CPU por vez
    contador_quantum = 0
    processo_em_execucao = 0
    processos_concluidos = 0

    for i in range(1, MAXIMO_TEMPO_EXECUCAO):
        print("tempo[" + str(i) + "]: processo[" + str(processo_em_execucao) + "] restante=" +
              str(tempo_restante[processo_em_execucao]) + " (quantum=" + str(contador_quantum + 1) + "/" + str(quantum) + ")")

        tempo_restante[processo_em_execucao] -= 1
        contador_quantum += 1

        # Caso 1: O processo atual terminou a sua execução antes ou durante o quantum
        if tempo_restante[processo_em_execucao] == 0:
            processos_concluidos += 1
            tempo_espera[processo_em_execucao] = i - tempo_execucao[processo_em_execucao]

            if processos_concluidos == n_processos:
                break

            # Reseta o contador e passa a vez para o próximo processo que ainda não terminou
            contador_quantum = 0
            processo_em_execucao = (processo_em_execucao + 1) % n_processos
            while tempo_restante[processo_em_execucao] == 0:
                processo_em_execucao = (processo_em_execucao + 1) % n_processos

        # Caso 2: O processo estourou o tempo do quantum, então ele pausa e vai para o final da fila
        elif contador_quantum == quantum:
            contador_quantum = 0
            processo_em_execucao = (processo_em_execucao + 1) % n_processos
            while tempo_restante[processo_em_execucao] == 0:
                processo_em_execucao = (processo_em_execucao + 1) % n_processos

    imprime_stats(tempo_espera)


if __name__ == "__main__":
    main()
