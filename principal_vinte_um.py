import random
import math
from time import sleep

cartas_usuario = []
cartas_user_dividir = []
cartas_dealer = []

soma_final_dealer = 0
soma_final_usuario = 0
soma_final_user_dividir = 0

um_baralho = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"] * 4
baralho_p_jogo = um_baralho * 6
random.shuffle(baralho_p_jogo)
baralho_p_jogo.pop(0)

resultado_final = ""

quant_fichas_usuario = 50
fichas_apostadas = 0
fichas_obtidas = 0
dividiu_par = False
run_uma_vez = True


def printar_cartas(cartas_p_printar):
    if cartas_p_printar == cartas_usuario or cartas_p_printar == cartas_user_dividir:
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

    elif cartas_p_printar == cartas_user_dividir:
        print(f"({soma_final_user_dividir})")


def apostar_fichas():
    while True:

        print(f"Você tem {quant_fichas_usuario} fichas")
        input_aposta_fichas = input("Quanto quer apostar? : ")

        if input_aposta_fichas.isdigit():

            if int(input_aposta_fichas) > quant_fichas_usuario:
                print(f"\nVocê não tem {int(input_aposta_fichas)} fichas para apostar!\n")

            elif int(input_aposta_fichas) <= 0:
                print("\nDigite um numero vahlido!\n")

            elif int(input_aposta_fichas) == 1:
                print("\nA aposta minima é 2 fichas\n")

            else:
                return int(input_aposta_fichas)

        else:
            print("\nDigite apenas numeros!\n")


def logica_somar_cartas(cartas_p_somar):

    soma_final = 0

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


def dividir_par():
    print("\nJogo 2:\n")

    global soma_final_user_dividir

    while True:

        if dividiu_par and len(cartas_usuario) == cartas_usuario.count("A"):

            printar_cartas(cartas_user_dividir)
            cartas_user_dividir.append(baralho_p_jogo.pop(0))
            soma_final_user_dividir = logica_somar_cartas(cartas_user_dividir)
            printar_cartas(cartas_user_dividir)
            print()
            break

        soma_final_user_dividir = logica_somar_cartas(cartas_user_dividir)

        printar_cartas(cartas_user_dividir)
        print()

        if soma_final_user_dividir >= 21:
            print(f"Deu: {soma_final_user_dividir}")
            break

        while True:

            input_usuario_dividir = input("\n(1)-Carta (2)-Ficar : ")

            if input_usuario_dividir == "1" or input_usuario_dividir == "2":
                break

            else:
                print("\nDigite um dos valores abaixo!")

        print()

        if input_usuario_dividir == "1":
            cartas_user_dividir.append(baralho_p_jogo.pop(0))

        elif input_usuario_dividir == "2":
            printar_cartas(cartas_user_dividir)
            print()
            break


def dobrar_aposta():

    if fichas_apostadas * 2 > quant_fichas_usuario:
        print(f"Você não tem {fichas_apostadas} fichas sobrando para dobrar a aposta!\n")
        return fichas_apostadas, False
    else:
        cartas_usuario.append(baralho_p_jogo.pop(0))
        print()
        return fichas_apostadas * 2, True


def definir_mensagem_resultado(soma_final):
    if soma_final < 21 and soma_final_dealer < 21:
        print(f"\nResultado User: {soma_final}")
        print(f"Resultado Dealer: {soma_final_dealer}\n")

    elif soma_final > 21 or soma_final_dealer > 21:
        dealer_ou_user = "Voce" if soma_final > 21 else "Dealer"
        print(dealer_ou_user, "passou 21")

    if soma_final > 21:
        return "Dealer ganhou"

    elif soma_final_dealer > 21:
        return "User ganhou"

    else:
        if soma_final_dealer > soma_final or soma_final > 21:
            return "Dealer ganhou"

        elif soma_final_dealer < soma_final or soma_final_dealer > 21:
            return "User ganhou"

        elif soma_final_dealer == soma_final:
            return "Empate"


def calcular_fichas_obtidas(fichas_apostadas_parametro):
    guardar_fichas = 0

    if "Dealer" in resultado_final:
        return 0 - fichas_apostadas_parametro

    elif "User" in resultado_final:
        guardar_fichas += fichas_apostadas_parametro

        if len(cartas_usuario) == 2 and soma_final_usuario == 21 and not dividiu_par:
            print("\nBLACKJACK!\n")
            guardar_fichas += math.floor(fichas_apostadas_parametro * 1.5)

        return guardar_fichas

    elif "Empate" in resultado_final:
        return 0


print("Este eh um jogo de Blackjack!\n")
print("Voce recebeu 50 fichas")

# input("Pressione ENTER para começar")
print("-" * 30)
print()

while True:

    for i in range(2):
        cartas_dealer.append(baralho_p_jogo.pop(0))

        cartas_usuario.append(baralho_p_jogo.pop(0))

    # TODO: remover esse while depois. isso ta aqui pra testar dividir_par
    while len(set(cartas_usuario)) != 1:
        cartas_usuario.pop(0)
        cartas_usuario.append(baralho_p_jogo.pop(0))

    fichas_apostadas = apostar_fichas()

    print(f"\n\nCartas do dealer: {cartas_dealer[0]} | #\n")

    dealer_tem_Q_J_or_K = any(char in cartas_dealer for char in ["Q", "j", "K"])

    dealer_tem_21 = "A" in cartas_dealer and dealer_tem_Q_J_or_K

    while not dealer_tem_21:

        if dividiu_par and len(cartas_usuario) == cartas_usuario.count("A"):
            printar_cartas(cartas_usuario)
            cartas_usuario.append(baralho_p_jogo.pop(0))
            soma_final_usuario = logica_somar_cartas(cartas_usuario)
            printar_cartas(cartas_usuario)
            print()
            break

        soma_final_usuario = logica_somar_cartas(cartas_usuario)

        printar_cartas(cartas_usuario)
        print()

        if soma_final_usuario >= 21:
            print(f"Deu: {soma_final_usuario}")
            break

        inputs_permitidos = ["1", "2", "3", "4"] if not dividiu_par else ["1", "2"]
        msg_input_usuario = "\n(1)-Carta (2)-Ficar (3)-Dobrar : "

        if run_uma_vez and len(set(cartas_usuario)) == 1:
            msg_input_usuario = "\n(1)-Carta (2)-Ficar (3)-dobrar (4)-Dividir par : "

        elif dividiu_par:
            msg_input_usuario = "\n(1)-Carta (2)-Ficar : "

        while True:

            input_usuario = input(msg_input_usuario)

            if input_usuario in inputs_permitidos:

                run_uma_vez = False
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

        elif input_usuario == "3":
            fichas_apostadas, x = dobrar_aposta()
            if x:
                soma_final_usuario = logica_somar_cartas(cartas_usuario)
                printar_cartas(cartas_usuario)
                break

        elif input_usuario == "4":

            # TODO: tentar tirar esse if daqui
            if fichas_apostadas * 2 > quant_fichas_usuario:
                print(f"Voce nao tem {fichas_apostadas} fichas sobrando para dividir um par!\n")
            else:
                dividiu_par = True
                cartas_user_dividir.append(cartas_usuario.pop(0))
                print("Jogo 1:\n")

    if len(cartas_user_dividir) == 1:
        dividir_par()

    if soma_final_usuario <= 21 or dividiu_par and soma_final_user_dividir <= 21:

        print("\nDealer jogando:\n")

        while True:

            soma_final_dealer = logica_somar_cartas(cartas_dealer)

            printar_cartas(cartas_dealer)
            sleep(1.5)

            if soma_final_dealer >= 21:
                print(f"\ndeu: {soma_final_dealer}")
                break

            maior_17_maior_user = 17 <= soma_final_dealer >= soma_final_usuario
            maior_17_maior_user_dividir = 17 <= soma_final_dealer >= soma_final_user_dividir

            if dividiu_par:

                if soma_final_usuario > 21 and maior_17_maior_user_dividir:
                    break

                elif soma_final_user_dividir > 21 and maior_17_maior_user:
                    break

                elif maior_17_maior_user and maior_17_maior_user_dividir:
                    break

            elif maior_17_maior_user:
                break

            if soma_final_dealer < 17:
                # print("menor que 17")
                cartas_dealer.append(baralho_p_jogo.pop(0))

            elif dividiu_par:
                if 21 >= soma_final_usuario > soma_final_dealer:
                    cartas_dealer.append(baralho_p_jogo.pop(0))

                elif 21 >= soma_final_user_dividir > soma_final_dealer:
                    cartas_dealer.append(baralho_p_jogo.pop(0))

            elif soma_final_dealer < soma_final_usuario:
                # print("menos q usuario")
                cartas_dealer.append(baralho_p_jogo.pop(0))

    print("\n\nResultado(s):")

    # TODO: rever isso, pra mim nao ta bonito
    if len(cartas_user_dividir) >= 1:

        print("\nJogo 1:")
        resultado_final = definir_mensagem_resultado(soma_final_usuario)

        fichas_obtidas = calcular_fichas_obtidas(fichas_apostadas)

        quant_fichas_usuario += fichas_obtidas

        print(f"{resultado_final}  | {'+' if fichas_obtidas > 0 else ''}{fichas_obtidas} ficha(s)")
        print("¨" * 30)

        print("\nJogo 2:")
        resultado_final = definir_mensagem_resultado(soma_final_user_dividir)

        fichas_obtidas = calcular_fichas_obtidas(fichas_apostadas)

        quant_fichas_usuario += fichas_obtidas

        print(f"{resultado_final}  | {'+' if fichas_obtidas > 0 else ''}{fichas_obtidas} ficha(s)")

    else:
        resultado_final = definir_mensagem_resultado(soma_final_usuario)

        fichas_obtidas = calcular_fichas_obtidas(fichas_apostadas)

        quant_fichas_usuario += fichas_obtidas

        print(f"{resultado_final}  | {'+' if fichas_obtidas > 0 else ''}{fichas_obtidas} ficha(s)")

    print("¨" * 30)
    print()

    if quant_fichas_usuario <= 0:
        print("Suas fichas acabaram, Fim de jogo.")
        break

    if len(baralho_p_jogo) < 78:
        baralho_p_jogo = um_baralho * 6
        random.shuffle(baralho_p_jogo)
        baralho_p_jogo.pop(0)

    resultado_final = ""
    cartas_user_dividir, cartas_usuario, cartas_dealer = [], [], []
    soma_final_dealer, soma_final_usuario = 0, 0
    fichas_apostadas, fichas_obtidas = 0, 0
    run_uma_vez = True
    dividiu_par = False
