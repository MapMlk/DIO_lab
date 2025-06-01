menu = """
OPÇÕES
==========================
[1] Depositar
[2] Sacar
[3] Extrato
[4] Novo Usuário
[5] Nova Conta
[0] Sair
==========================
"""

LIMITE_SAQUE = 500  ## limite por saque
LIMITE_SAQUE_DIA = 3 ## limite de saques por dia
AGENCIA = "0001"  ## número da agência
saldo = 0 ## armazena o saldo atual
saque_dia = 0 ## contador de saques já realizados no dia
extrato = "" ## string que armazena as movimentações 
usuarios = {}  ## dicionário que armazena os usuários
contas_ativas = {}  ## dicionário que armazena as contas ativas

def pause():
    input("Pressione Enter para continuar...")  

def deposito(valor):    ## função de depósito
    global saldo, extrato   ##chama as variáveis globais
    if valor > 0:   ## verifica se o valor é positivo
        saldo += valor
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        extrato += f"Depósito: R$ {valor:.2f}\n"    ## adiciona a operação ao extrato
        pause()
    else:
        print("Valor de depósito inválido.")
        pause()

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
            pause()
    else:
        print("Valor de saque inválido ou saldo insuficiente.")
        pause()

def extrato_bancario(): ## função que exibe o extrato
    global saldo, extrato
    print(" EXTRATO ".center(26, "="))
    if extrato != "":  ## verifica se há movimentações então exibe o extrato
        print(extrato)
    else:   ## se não houver movimentações, exibe mensagem
        print("Nenhuma movimentação realizada.")
    
    print(f"Saldo atual: R$ {saldo:.2f}")
    print("=========================")
    pause()

def criar_usuario():  ## função que cria um novo usuário
    nome = input("Informe o nome do usuário: ")
    while True:
        cpf = input("Informe o CPF do usuário (somente números): ")
        if not cpf.isdigit() or len(cpf) != 11:
            print("CPF inválido. Certifique-se de que contém 11 números.")
            pause() 
            continue
        if cpf in [user["cpf"] for user in usuarios.values()]:
            print("CPF já cadastrado. Informe um CPF único.")
            pause()
            continue
        break
    data_nascimento = input("Informe a data de nascimento (DD/MM/AAAA): ")
    usuarios[cpf] = {
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento
    }
    print(f"Usuário {nome} criado com sucesso!")
    pause()

def criar_conta(cpf):  ## função que cria uma nova conta
    numero_conta = f"{AGENCIA}-{len(contas_ativas) + 1:06d}"  ## gera um número de conta único
    contas_ativas[numero_conta] = {
        "cpf": cpf,
        "saldo": 0,
        "numero_saques": 0,
        "extrato": ""
    }
    print(f"Conta criada com sucesso! Número da conta: {numero_conta}")
    pause()

def main():
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
        elif opcao == "4":
            criar_usuario()
        elif opcao == "5":
            cpf = input("Informe o CPF do usuário: ")
            if cpf in usuarios:
                criar_conta(cpf)
            else:
                print("Usuário não encontrado. Crie um usuário primeiro.")
        elif opcao == "0":
            print("Saindo do sistema.")
            break
        else:
            print("Opção inválida. Tente novamente.")

main()