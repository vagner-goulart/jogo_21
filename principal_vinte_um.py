import random
import math
from time import sleep

cartas_usuario = []
cartas_dealer = []

soma_final_usuario = 0
soma_final_dealer = 0

um_baralho = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"] * 4
baralho_p_jogo = um_baralho * 6
random.shuffle(baralho_p_jogo)
baralho_p_jogo.pop(0)

resultado_final = ""

quant_fichas_usuario = 50
fichas_apostadas = 0
fichas_obtidas = 0


# TODO: colocar isso no final das funcoes
# def resetar_variaveis():
#     global cartas_usuario, cartas_dealer, resultado_final, fichas_obtidas, soma_final_dealer
#
#     cartas_usuario = []
#     cartas_dealer = []
#
#     resultado_final = ""
#     fichas_obtidas = 0
#
#     soma_final_dealer = 0


def printar_cartas(cartas_p_printar):
    if cartas_p_printar == cartas_usuario:
        print("Suas cartas: ", end="")
    elif cartas_p_printar == cartas_dealer:
        print("Cartas dealer: ", end="")

    for indice_carta, carta in enumerate(cartas_p_printar, start=1):

        if indice_carta == len(cartas_p_printar):
            print(carta, end="  - ")
        else:
            print(carta, "|", end=" ")

    if cartas_p_printar == cartas_usuario:
        print(f"({soma_final_usuario})")
    elif cartas_p_printar == cartas_dealer:
        print(f"({soma_final_dealer})")


def apostar_fichas():
    while True:

        print(f"Você tem {quant_fichas_usuario} fichas")
        input_aposta_fichas = input("Quanto quer apostar? : ")

        if input_aposta_fichas.isdigit():

            if int(input_aposta_fichas) > quant_fichas_usuario:
                print(f"\nVocê não tem {int(input_aposta_fichas)} fichas para apostar!\n")

            elif int(input_aposta_fichas) <= 0:
                print("\nDigite um numero vahlido!\n")

            else:
                return int(input_aposta_fichas)

        else:
            print("\nDigite apenas numeros!\n")


def logica_somar_cartas(cartas_p_somar, soma_final):
    for carta in cartas_p_somar:

        if carta == "J" or carta == "Q" or carta == "K":
            soma_final += 10

        if isinstance(carta, int):
            soma_final += carta

    for carta in cartas_p_somar:
        if carta == "A":

            if 1 + soma_final > 21:
                soma_final += 1
            else:
                if 11 + soma_final <= 21:
                    soma_final += 11
                elif 1 + soma_final <= 21:
                    soma_final += 1

    return soma_final


def definir_mensagem_resultado():
    if soma_final_usuario < 21 and soma_final_dealer < 21:
        print(f"\nResultado User: {soma_final_usuario}\n")
        print(f"Resultado Dealer: {soma_final_dealer}\n")

    elif soma_final_usuario > 21 or soma_final_dealer > 21:
        print("Passou 21")

    if soma_final_dealer > 21:
        print("teste1")
        return "User ganhou"

    elif soma_final_usuario > 21:
        return "Dealer ganhou"

    else:
        if soma_final_dealer > soma_final_usuario or soma_final_usuario > 21:
            return "Dealer ganhou"

        elif soma_final_dealer < soma_final_usuario or soma_final_dealer > 21:
            print("teste2")
            return "User ganhou"

        elif soma_final_dealer == soma_final_usuario:
            return "Empate"


def calcular_fichas_obtidas(fichas_apostadas_parametro):
    guardar_fichas = 0

    if "Dealer" in resultado_final:
        return 0 - fichas_apostadas_parametro

    elif "User" in resultado_final:
        guardar_fichas += fichas_apostadas_parametro

        if len(cartas_usuario) == 2 and soma_final_usuario == 21:
            print("\nBLACKJACK!\n")
            guardar_fichas += math.floor(fichas_apostadas_parametro * 1.5)

        return guardar_fichas

    elif "Empate" in resultado_final:
        return 0


print("Este eh um jogo de Blackjack!\n")
print("Voce recebeu 50 fichas")

input("Pressione ENTER para começar")
print("-" * 30)
print()

while True:

    for i in range(2):
        cartas_dealer.append(baralho_p_jogo.pop(0))

        cartas_usuario.append(baralho_p_jogo.pop(0))

    fichas_apostadas = apostar_fichas()

    print(f"\n\nCartas do dealer: {cartas_dealer[0]} | #\n")

    while True:
        soma_final_usuario = 0

        # if cartas_usuario.count("A") == 1 and cartas_usuario[-1] == "A":

        dealer_tem_Q_J_or_K = "K" in cartas_dealer or "Q" in cartas_dealer or "J" in cartas_dealer

        if "A" in cartas_dealer and dealer_tem_Q_J_or_K:
            break

        soma_final_usuario = logica_somar_cartas(cartas_usuario, soma_final_usuario)

        printar_cartas(cartas_usuario)
        print()

        if soma_final_usuario >= 21:
            print(f"Deu: {soma_final_usuario}")
            break

        while True:

            # input_usuario = input("\nEscolha: (1)-Pedir carta (2)-Ficar (3)-Dobrar : ")
            input_usuario = input("\nEscolha: (1)-Pedir carta (2)-Ficar : ")

            if input_usuario == "1" or input_usuario == "2":
                break

            else:
                print("\nDigite um dos valores abaixo!")

        print()

        if input_usuario == "1":
            cartas_usuario.append(baralho_p_jogo.pop(0))

        elif input_usuario == "2":
            printar_cartas(cartas_usuario)
            print()
            break

    if soma_final_usuario <= 21:

        print("\nDealer jogando:\n")

        while True:

            soma_final_dealer = 0

            soma_final_dealer = logica_somar_cartas(cartas_dealer, soma_final_dealer)

            printar_cartas(cartas_dealer)
            sleep(1.5)

            if soma_final_dealer >= 21:
                print(f"\ndeu: {soma_final_dealer}\n")
                break

            if soma_final_dealer > 17 and soma_final_dealer >= soma_final_usuario:
                break

            if soma_final_dealer <= 17:
                # print("menor que 17")
                cartas_dealer.append(baralho_p_jogo.pop(0))

            elif soma_final_dealer < soma_final_usuario:
                # print("menos q usuario")
                cartas_dealer.append(baralho_p_jogo.pop(0))

    resultado_final = definir_mensagem_resultado()

    fichas_obtidas = calcular_fichas_obtidas(fichas_apostadas)

    quant_fichas_usuario += fichas_obtidas

    print(f"{resultado_final}  | {'+' if fichas_obtidas > 0 else ''}{fichas_obtidas} ficha(s)")

    if len(baralho_p_jogo) < 78:
        baralho_p_jogo = um_baralho * 6
        random.shuffle(baralho_p_jogo)
        baralho_p_jogo.pop(0)

    # resetar_variaveis()

    cartas_usuario = []
    cartas_dealer = []
    resultado_final = ""
    fichas_obtidas = 0
    soma_final_dealer = 0
    fichas_apostadas = 0

    print("¨" * 30)
    print()

    if quant_fichas_usuario <= 0:
        print("Suas fichas acabaram, Fim de jogo.")
        break
