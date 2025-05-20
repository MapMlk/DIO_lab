menu = """
OPÇÕES
==========================
[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair
==========================
"""

LIMITE_SAQUE = 500  ## limite por saque
LIMITE_SAQUE_DIA = 3 ## limite de saques por dia
saldo = 0 ## armazena o saldo atual
saque_dia = 0 ## contador de saques já realizados no dia
extrato = "" ## string que armazena as movimentações 

def deposito(valor):    ## função de depósito
    global saldo, extrato   ##chama as variáveis globais
    if valor > 0:   ## verifica se o valor é positivo
        saldo += valor
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        extrato += f"Depósito: R$ {valor:.2f}\n"    ## adiciona a operação ao extrato
    else:
        print("Valor de depósito inválido.")

def saque(valor):   ## função de saque
    global saldo, saque_dia, extrato
    if valor > 0 and valor <= saldo:
        if saque_dia < LIMITE_SAQUE_DIA and valor <= LIMITE_SAQUE: ## checa se o há saques diarios disponiveis e se o valor do saque é menor que o limite
            saldo -= valor
            saque_dia += 1
            print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
            extrato += f"Saque: R$ {valor:.2f}\n"
        else:
            print("Limite de saques diários atingido ou valor do saque excede o limite.")
    else:
        print("Valor de saque inválido ou saldo insuficiente.")

def extrato_bancario(): ## função que exibe o extrato
    global saldo, extrato
    print(" EXTRATO ".center(26, "="))
    if extrato != "":  ## verifica se há movimentações então exibe o extrato
        print(extrato)
    else:   ## se não houver movimentações, exibe mensagem
        print("Nenhuma movimentação realizada.")
    
    print(f"Saldo atual: R$ {saldo:.2f}")
    print("=========================")

while True:
    print(menu)
    opcao = input("Escolha uma operação: ")

    if opcao == "1":
        valor = float(input("Informe o valor do depósito: "))
        deposito(valor)
    elif opcao == "2":
        valor = float(input("Informe o valor do saque: "))
        saque(valor)
    elif opcao == "3":
        extrato_bancario()
    elif opcao == "0":
       break
    else:
        print("Opção inválida. Tente novamente.")