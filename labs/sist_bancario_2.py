menu = """
==========================
[1] Depositar
[2] Sacar
[3] Extrato
[4] Novo Usuário
[5] Nova Conta
[6] Listar Contas
[0] Sair
==========================
"""

import re

LIMITE_SAQUE = 500  ## limite por saque
LIMITE_SAQUE_DIA = 3 ## limite de saques por dia
AGENCIA = "0001"  ## número da agência
usuarios = {}  ## dicionário que armazena os usuários
contas_ativas = {}  ## dicionário que armazena as contas ativas

def pause():
    input("Pressione Enter para continuar...")

def cpf_valido(cpf):
    if re.match(r"^\d{11}$", cpf):
        return cpf
    if re.match(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf):
        return re.sub(r"\D", "", cpf)
    return None

def nome_valido(nome):
    return bool(re.match(r"^[\w\sÀ-ÿ]+$", nome))

def nascimento_valido(nascimento):
    return bool(re.match(r"^\d{2}/\d{2}/\d{4}$", nascimento))

def conta_valida(numero_conta, senha):
    conta = contas_ativas.get(numero_conta)
    if conta and conta["senha"] == senha:
        return True
    print("Conta ou senha inválida.")
    return False

def criar_usuario(cpf, nome, nascimento):  ## função que cria um usuário
    cpf_limpo = cpf_valido(cpf)
    if not cpf_limpo:
        print("CPF inválido. Deve conter 11 dígitos.")
        pause()
        return False
    if not nome_valido(nome):
        print("Nome inválido. Deve conter apenas letras e espaços.")
        pause()
        return False
    if not nascimento_valido(nascimento):
        print("Data de nascimento inválida. Deve estar no formato DD/MM/AAAA.")
        pause()
        return False
    usuarios[cpf_limpo] = {"nome": nome, "nascimento": nascimento}  ## armazena o usuário no dicionário
    print(f"Usuário {nome} criado com sucesso.")
    pause()

def criar_conta(cpf):  ## função que cria uma conta
    cpf_limpo = cpf_valido(cpf)  ## valida e limpa o CPF
    if not cpf_limpo:
        print("CPF inválido. Deve conter 11 dígitos.")
        pause()
        return False
    usuario = usuarios.get(cpf_limpo)  ## busca o usuário pelo CPF limpo
    if usuario is None:  ## verifica se o CPF está cadastrado
        print("Usuário não encontrado. Crie um usuário primeiro.")
        pause()
        return False
    usuario = usuario["nome"]  ## acessa o campo "nome" do usuário
    conta_numero = f"{AGENCIA}{len(contas_ativas) + 1}"  ## gera o número da conta
    senha = input("Digite uma senha para a conta: ")
    contas_ativas[conta_numero] = {"senha": senha, "cpf":cpf,"usuario": usuario, "saldo": 0,"numero_saques": 0, "extrato": ""}
    print(f"Conta criada com sucesso para {usuario}. Número da conta: {conta_numero}")
    pause()

def listar_contas(cpf):  ## função que lista as contas de um usuário
    contas_usuario = [conta for conta in contas_ativas.values() if conta["cpf"] == cpf]
    if not contas_usuario:
        print("Nenhuma conta encontrada para este usuário.")
        pause()
        return False
    print("Contas do usuário:")
    for conta in contas_usuario:
        print(f"Conta: {conta['usuario']} - Número: {conta['numero']}")
    pause()
    return True

def depositar(numero_conta, senha, valor):  ## função que deposita um valor na conta
    if numero_conta not in contas_ativas:
        print("Conta não encontrada.")
        pause()
        return False
    conta = contas_ativas.get(numero_conta)
    if not conta_valida(numero_conta, senha):
        pause()
        return False
    if valor <= 0:
        print("Valor de depósito deve ser positivo.")
        pause()
        return False
    conta["saldo"] += valor
    conta["extrato"] += f"Depósito: R$ {valor:.2f}\n"
    print(f"Depósito de R$ {valor:.2f} realizado com sucesso na conta {numero_conta}.")
    pause()
    return True

def sacar(numero_conta, senha, valor):  ## função que saca um valor da conta
    conta = contas_ativas.get(numero_conta)
    if not conta_valida(numero_conta, senha):
        pause()
        return False
    if valor <= 0:
        print("Valor de saque deve ser positivo.")
        pause()
        return False
    if valor > LIMITE_SAQUE:
        print(f"Valor do saque excede o limite de R$ {LIMITE_SAQUE:.2f}.")
        pause()
        return False
    if conta["numero_saques"] >= LIMITE_SAQUE_DIA:
        print("Limite de saques diários atingido.")
        pause()
        return False
    if valor > conta["saldo"]:
        print("Saldo insuficiente para saque.")
        pause()
        return False
    conta["saldo"] -= valor
    conta["numero_saques"] += 1
    conta["extrato"] += f"Saque: R$ {valor:.2f}\n"
    print(f"Saque de R$ {valor:.2f} realizado com sucesso na conta {numero_conta}.")
    pause()
    return True

def extrato_bancario(numero_conta, senha):  ## função que exibe o extrato da conta
    conta = contas_ativas.get(numero_conta)
    if not conta_valida(numero_conta, senha):
        pause()
        return False
    print(" EXTRATO ".center(26, "="))
    if conta["extrato"]:
        print(conta["extrato"])
    else:
        print("Nenhuma movimentação realizada.")
    print(f"Saldo atual: R$ {conta['saldo']:.2f}")
    print("=========================")
    pause()
    return True

while True:
    print(menu)
    opcao = input("Escolha uma operação: ")

    if opcao == "1":
        numero_conta = input("Informe o número da conta: ")
        senha = input("Informe a senha da conta: ")
        valor = float(input("Informe o valor do depósito: "))
        depositar(numero_conta, senha, valor)
    elif opcao == "2":
        numero_conta = input("Informe o número da conta: ")
        senha = input("Informe a senha da conta: ")
        valor = float(input("Informe o valor do saque: "))
        sacar(numero_conta, senha, valor)
    elif opcao == "3":
        numero_conta = input("Informe o número da conta: ")
        senha = input("Informe a senha da conta: ")
        extrato_bancario(numero_conta, senha)
    elif opcao == "4":
        cpf = input("Informe o CPF do usuário: ")
        cpf = cpf_valido(cpf)
        nome = input("Informe o nome do usuário: ")
        nascimento = input("Informe a data de nascimento (DD/MM/AAAA): ")
        criar_usuario(cpf, nome, nascimento)

    elif opcao == "5":
        cpf = input("Informe o CPF do usuário: ")
        criar_conta(cpf)
    elif opcao == "6":
        cpf = input("Informe o CPF do usuário: ")
        listar_contas(cpf)
    elif opcao == "0":
       break
    else:
       print("Opção inválida. Tente novamente.")