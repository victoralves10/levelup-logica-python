import os
import re
import oracledb
import requests
from datetime import datetime, date
os.system("cls" if os.name == "nt" else "clear")

# ==========================================================
#   SUBALGORITMOS
# ==========================================================

# ==========================================================
#   EXIBIÇÃO
# ==========================================================

def limpar_terminal() -> None:
    """Limpa a tela do terminal, compatível com Windows e Linux."""
    os.system("cls" if os.name == "nt" else "clear")

def exibir_titulo_centralizado(_texto: str, _largura_caracteres: int) -> None:
    """Mostra um título centralizado com linhas decorativas acima e abaixo."""
    print("=-" * (_largura_caracteres // 2))
    print(_texto.center(_largura_caracteres))
    print("=-" * (_largura_caracteres // 2), "\n")

def imprimir_linha_separadora(simbolo: str, quantidade: int) -> None:
    """Mostra uma linha formada pela repetição de um símbolo."""
    print()
    print(simbolo * quantidade)
    print()

# ==========================================================
#   VALIDAÇÃO DE DADOS (TIPOS BÁSICOS)
# ==========================================================

def obter_int(_msg_input: str, _msg_erro: str) -> int:
    """Obtém um número inteiro digitado pelo usuário, exibindo uma mensagem de erro personalizada."""
    entrada_int = None
    while entrada_int is None:
        try:
            entrada_int = int(input(_msg_input).strip())
        except ValueError:
            print(f"{_msg_erro}\n") # Exemplo: Entrada inválida. Por favor, digite um número inteiro.
            entrada_int = None
    return entrada_int

def obter_float(_msg_input: str, _msg_erro: str) -> float:
    """Obtém um número float digitado pelo usuário, exibindo uma mensagem de erro personalizada."""
    entrada_float = None
    while entrada_float is None:
        try:
            valor = float(input(_msg_input).strip().replace(',', '.'))  # aceita vírgula ou ponto
            entrada_float = float(valor)
        except ValueError:
            print(f"{_msg_erro}\n")  # Exemplo: "Entrada inválida. Por favor, digite um número decimal."
            entrada_float = None
    return entrada_float

def obter_texto(_msg_input: str, _msg_erro: str) -> str:
    """Obtém um texto digitado pelo usuário, garantindo que não esteja vazio e exibindo uma mensagem de erro personalizada."""
    entrada_texto = ""
    
    while not entrada_texto:
        entrada_texto = input(_msg_input).strip()
        if not entrada_texto:
            print(f"{_msg_erro}\n") # Entrada inválida. O campo não pode ficar vazio.
    
    return entrada_texto

def obter_data(_msg_input: str, _msg_erro: str) -> str:
    """Obtém uma data digitada pelo usuário (formato DD/MM/AAAA), exibindo uma mensagem de erro personalizada."""
    data = None
    while data is None:
        data_str = input(_msg_input).strip()
        if not data_str:
            print(f"{_msg_erro}\n")
            continue
        try:
            data = datetime.strptime(data_str, "%d/%m/%Y")
        except ValueError:
            print(f"{_msg_erro}\n")  # Exemplo: "Data inválida. Use o formato DD/MM/AAAA."
            data = None
    return data.strftime("%d/%m/%Y")

def obter_data_hora(_msg_input: str, _msg_erro: str) -> str:
    """Obtém uma data e hora digitada pelo usuário no formato 'dd/mm/aaaa hh:mm',
    exibindo uma mensagem de erro personalizada."""
    
    data = None

    while data is None:
        data_str = input(_msg_input).strip()
        
        if not data_str:
            print(f"{_msg_erro}\n")

        else:
            try:
                data = datetime.strptime(data_str, "%d/%m/%Y %H:%M")
            except ValueError:
                print(f"{_msg_erro}\n") # Formato inválido! Use dd/mm/aaaa hh:mm, por exemplo: 15/11/2025 14:30.
                data = None

    return data.strftime("%d/%m/%Y %H:%M")

def obter_sim_nao(_msg_input: str, _msg_erro: str) -> bool:
    """Pergunta ao usuário uma questão de Sim/Não e retorna True para 'S' ou False para 'N',
    aceitando também 'sim' e 'não', com mensagem personalizável."""
    
    entrada_sim_nao = ""
    resultado = False

    while entrada_sim_nao not in ["S", "N"]:
        entrada_sim_nao = input(_msg_input).strip().upper()

        if not entrada_sim_nao:
            print(f"{_msg_erro}\n")
            entrada_sim_nao = ""

        else:
            if entrada_sim_nao[0] == "S":
                resultado = True
                entrada_sim_nao = "S"

            elif entrada_sim_nao[0] == "N":
                resultado = False
                entrada_sim_nao = "N"

            else:
                print(f"{_msg_erro}\n")
                entrada_sim_nao = ""

    return resultado

def obter_int_intervalado(_msg_input: str, _msg_erro: str, _min: int, _max: int) -> int:
    """Solicita ao usuário um número inteiro entre os valores mínimos e máximos informados, com mensagem personalizável."""

    entrada_valida = False
    entrada_numero = None

    while not entrada_valida:
        try:
            entrada_numero = int(input(_msg_input).strip())

            if _min <= entrada_numero <= _max:
                entrada_valida = True

            else:
                print(f"{_msg_erro} Digite entre {_min} e {_max}.\n")  # Entrada inválida.

        except ValueError:
            print(f"{_msg_erro} Digite entre {_min} e {_max}.\n")

    return entrada_numero

def obter_opcao_dict(_msg_input: str, _msg_erro: str, _opcoes_dict: dict) -> str:
    """Exibe um dicionário numerado de opções e solicita ao usuário que escolha um número válido."""

    minimo = min(_opcoes_dict.keys())
    maximo = max(_opcoes_dict.keys())

    escolha = obter_int_intervalado(_msg_input, _msg_erro, minimo, maximo)

    return _opcoes_dict[escolha]

def obter_multiplas_opcoes_dict(_msg_input: str, _msg_erro: str, _opcoes_dict: dict) -> tuple[str, list]:
    """Solicita ao usuário uma ou mais opções numéricas (separadas por vírgula) com base em um dicionário numerado.
    Aceita também 'A' para selecionar todas as opções.
    Retorna uma tupla contendo: (string_formatada, lista_de_valores)."""

    valores_str = ""
    valores_lista = []
    entrada_valida = False

    while not entrada_valida:
        entrada = input(_msg_input).strip().upper()

        if not entrada:
            print(f"{_msg_erro}\n")
            continue

        if entrada == "A":
            valores_lista = []
            for chave in _opcoes_dict:
                valores_lista.append(_opcoes_dict[chave])
            valores_str = ", ".join(valores_lista)
            entrada_valida = True
            continue

        try:
            numeros = []
            partes = entrada.split(",")
            for parte in partes:
                parte = parte.strip()
                if parte:
                    numeros.append(int(parte))

            if not numeros:
                print(f"{_msg_erro}\n")
                continue

            todos_validos = True
            for n in numeros:
                if n not in _opcoes_dict:
                    todos_validos = False
                    break

            if todos_validos:
                valores_lista = []
                for n in numeros:
                    valores_lista.append(_opcoes_dict[n])

                valores_str = ", ".join(valores_lista)
                entrada_valida = True
            else:
                print(f"{_msg_erro}\n")

        except ValueError:
            print(f"{_msg_erro}\n")

    return valores_str, valores_lista

# ==========================================================
#   VALIDAÇÃO DE DADOS ESPECÍFICO
# ==========================================================

def obter_email(_msg_input: str, _msg_erro: str) -> str:
    """Solicita um e-mail válido usando regex, exibindo mensagem de erro personalizada."""
    email = ""
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    
    while not re.match(padrao, email):
        email = input(_msg_input).strip()
        if not re.match(padrao, email):
            print(f"{_msg_erro}\n")
            email = ""
    return email

def obter_m_f(_msg_input: str, _msg_erro: str) -> str:
    """Pergunta ao usuário o sexo ('M' ou 'F'), aceitando também palavras completas ('Masculino', 'Feminino'),
    e exibindo uma mensagem de erro personalizada em caso de entrada inválida."""
    
    entrada_mf = ""

    while entrada_mf not in ["M", "F"]:
        entrada_mf = input(_msg_input).strip().upper()

        if not entrada_mf:
            print(f"{_msg_erro}\n") 
            entrada_mf = ""

        else:
            if entrada_mf[0] == "M":
                entrada_mf = "M"

            elif entrada_mf[0] == "F":
                entrada_mf = "F"

            else:
                print(f"{_msg_erro}\n") # Entrada inválida. Digite 'M' para Masculino ou 'F' para Feminino.
                entrada_mf = ""

    return entrada_mf

def obter_cpf(_msg_input: str, _msg_erro: str) -> str:
    """Solicita ao usuário um CPF no formato numérico (11 dígitos), aceitando também formatos com pontos e traço,
    exibindo uma mensagem de erro personalizada em caso de entrada inválida.
    Exemplo aceito: 555.555.555-20 ou 55555555520."""
    
    cpf = ""

    while not (cpf.isdigit() and len(cpf) == 11):
        entrada = input(_msg_input).strip()
        cpf = entrada.replace(".", "").replace("-", "").replace(" ", "")
        
        if not (cpf.isdigit() and len(cpf) == 11):
            print(f"{_msg_erro}\n") # Entrada inválida. Digite um CPF com 11 números.
            cpf = ""

    return cpf

def obter_rg(_msg_input: str, _msg_erro: str) -> str:
    """Solicita ao usuário um número de RG (somente números, 9 dígitos), 
    aceitando também formatos com pontos e traços, e exibindo uma mensagem de erro personalizada.
    Exemplo aceito: 12.345.678-9 ou 123456789."""
    
    rg = ""

    while not (rg.isdigit() and len(rg) == 9):
        entrada = input(_msg_input).strip()
        rg = entrada.replace(".", "").replace("-", "").replace(" ", "")

        if not (rg.isdigit() and len(rg) == 9):
            print(f"{_msg_erro}\n")
            rg = "" # Entrada inválida. Digite um RG com 9 números.

    return rg

def obter_endereco(_msg_input: str, _msg_erro: str) -> dict:
    """Consulta a API ViaCEP com o CEP informado e retorna o endereço completo.
    Aceita CEP com ou sem traço, exibe mensagem de erro personalizada.
    API pública: https://viacep.com.br
    """
    
    endereco = None

    while endereco is None:
        cep = input(_msg_input).strip().replace("-", "").replace(".", "").replace(" ", "")

        if not (cep.isdigit() and len(cep) == 8):
            print(f"{_msg_erro}\n")
            continue

        try:
            response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
            data = response.json()

            if "erro" in data:
                print(f"{_msg_erro}\n") # CEP inválido ou não encontrado. Tente novamente.
                endereco = None
            else:
                endereco = {
                    "cep": data.get("cep", ""),
                    "logradouro": data.get("logradouro", ""),
                    "bairro": data.get("bairro", ""),
                    "cidade": data.get("localidade", ""),
                    "estado": data.get("uf", ""),
                    "pais": "Brasil"
                }

        except Exception:
            print(f"{_msg_erro}\n")
            endereco = None

    return endereco

def obter_cep(_endereco: dict) -> str:
    """Retorna o CEP do endereço obtido pela função obter_endereco()."""
    return _endereco.get("cep", "")

def obter_rua(_endereco: dict) -> str:
    """Retorna o logradouro do endereço obtido pela função obter_endereco()."""
    return _endereco.get("logradouro", "")

def obter_bairro(_endereco: dict) -> str:
    """Retorna o bairro do endereço obtido pela função obter_endereco()."""
    return _endereco.get("bairro", "")

def obter_cidade(_endereco: dict) -> str:
    """Retorna a cidade do endereço obtido pela função obter_endereco()."""
    return _endereco.get("cidade", "")

def obter_estado(_endereco: dict) -> str:
    """Retorna o estado do endereço obtido pela função obter_endereco()."""
    return _endereco.get("estado", "")

def obter_pais(_endereco: dict) -> str:
    """Retorna o país associado ao endereço obtido pela função obter_endereco()."""
    return _endereco.get("pais", "Brasil")


# ==========================================================
#   SOLICITAÇÃO DE DADOS T_ENDERECO
# ==========================================================

def solicitar_dados_endereco() -> tuple[bool, any]:  # dict ou erro
    """
    Solicita e retorna todos os dados da tabela T_ENDERECO.
    
    Retorno:
        (True, dict)  -> quando os dados são obtidos com sucesso
        (False, erro) -> quando ocorre alguma exceção
    """
    try:
        print("INFORMAÇÕES DE ENDEREÇO")

        # ===== 1. CEP + consulta automática =====
        endereco = obter_endereco(
            "Digite o CEP (ex: 01310200): ",
            "CEP inválido! Digite um CEP com 8 números."
        )

        imprimir_linha_separadora("=", 40)

        # ===== 2. País, Estado, Cidade, Bairro, Rua =====
        pais = obter_pais(endereco)
        estado = obter_estado(endereco)
        cidade = obter_cidade(endereco)
        bairro = obter_bairro(endereco)
        rua = obter_rua(endereco)

        # ===== 3. Número =====
        numero = obter_int(
            "Número da residência: ",
            "Entrada inválida. Digite apenas números."
        )

        # ===== 4. Complemento (máx 150 caracteres, pode ser vazio) =====
        imprimir_linha_separadora("=", 40)
        complemento = input("Complemento (máx 150 caracteres, pode ser vazio): ")
        while len(complemento) > 150:
            print("\nO complemento deve ter no máximo 150 caracteres.\n")
            complemento = complemento = input("Complemento (máx 150 caracteres, pode ser vazio): ")

        # ===== 5. Retorno final =====
        dados = {
            "cep": endereco["cep"],
            "pais": pais,
            "estado": estado,
            "cidade": cidade,
            "bairro": bairro,
            "rua": rua,
            "numero": numero,
            "complemento": complemento
        }

        return (True, dados)

    except Exception as e:
        return (False, e)

# ==========================================================
#   CONEXÃO BANCO DE DADOS
# ==========================================================

# ========= CONEXÃO BANCO DE DADOS =========
def conectar_oracledb(_user: str, _password: str, _dsn: str) -> tuple[bool, any]:
    """Tenta conectar ao Oracle e retorna (True, conexão) ou (False, erro)."""
    retorno = None

    try:
        conexao_bd = oracledb.connect(
            user = _user,
            password = _password,
            dsn = _dsn
        )
    
        retorno = (True, conexao_bd) 

    except Exception as e:
        
        retorno = (False, e)
    
    return retorno

# ========================================
#   CONEXÃO COM O BANCO DE DADOS ORACLE
# ========================================

'''
user = "rm561833"
password = "070406"
dsn = "oracle.fiap.com.br:1521/ORCL"

ok, conn = conectar_oracledb(user, password, dsn)

if ok:
    limpar_terminal()
    exibir_titulo_centralizado("CONECTADO AO BANCO DE DADOS COM SUCESSO", 60)
    print("\nConexão estabelecida com sucesso com o servidor Oracle da FIAP.")
    input("\nAperte ENTER para acessar o sistema...")
else:
    limpar_terminal()
    exibir_titulo_centralizado("ERRO AO CONECTAR AO BANCO DE DADOS", 60)
    print(f"\nDetalhes do erro:\n{conn}\n")
    input("Aperte ENTER para encerrar o programa...")
''' 

ok = True

# ========================================
#   MENU PRINCIPAL
# ========================================

while ok:
    limpar_terminal()
    exibir_titulo_centralizado("LEVEL UP - PORTAL DE EMPRESAS E DEMANDAS", 60)

    print("LEVEL UP — conectamos as demandas das empresas ao futuro.")
    print("Cadastre sua necessidade e identificaremos as áreas mais requisitadas,")
    print("impulsionando eventos de qualificação e novas oportunidades no mercado.\n")

    print("1 - Cadastrar nova empresa")
    print("2 - Consultar empresas cadastradas")
    print("3 - Atualizar informações de uma empresa")
    print("4 - Remover cadastro de empresa")
    print("5 - Limpar todos os registros de empresas")
    print("6 - Exportar registros para JSON")
    print("0 - Sair do sistema")

    escolha_menu_principal = obter_int_intervalado("Escolha: ", "Entrada inválida.", 0, 6)

    match escolha_menu_principal:

        case 0:
            limpar_terminal()
            print("\nPrograma encerrado. Até logo!\n")
            ok = False

        case 1:
            limpar_terminal()
            exibir_titulo_centralizado("CADASTRAR NOVA EMPRESA", 60)

            print("\nAntes de continuar, precisamos solicitar algumas informações da empresa.\n")

            deseja_continuar = obter_sim_nao(
                "Deseja informar os dados para continuar? (S/N): ",
                "Entrada inválida! Digite 'S' para Sim ou 'N' para Não."
            )

            if not deseja_continuar:
                limpar_terminal()
                print("\nCadastro cancelado pelo usuário.\n")
                input("\nAperte ENTER para voltar ao menu principal...")
                continue  # volta ao menu

            # --- Solicitar endereço ---
            limpar_terminal()
            exibir_titulo_centralizado("CADASTRAR NOVA EMPRESA", 60)

            sucesso, retorno = solicitar_dados_endereco()

            if not sucesso:
                print("\nOcorreu um erro ao solicitar o endereço:")
                print(retorno)
                input("\nAperte ENTER para voltar ao menu principal...")
                continue  # volta ao menu

            print("\nEndereço registrado com sucesso!")
            print("Dados:", retorno)

            input("\nAperte ENTER para voltar ao menu principal...")
            continue

        case 2:
            limpar_terminal()
            exibir_titulo_centralizado("CONSULTAR EMPRESAS CADASTRADAS", 60)
            print("\nFunção em manutenção. Em breve disponível!\n")
            input("\nAperte ENTER para voltar ao menu principal...")

        case 3:
            limpar_terminal()
            exibir_titulo_centralizado("ATUALIZAR INFORMAÇÕES DE EMPRESA", 60)
            print("\nFunção em manutenção. Em breve disponível!\n")
            input("\nAperte ENTER para voltar ao menu principal...")

        case 4:
            limpar_terminal()
            exibir_titulo_centralizado("REMOVER CADASTRO DE EMPRESA", 60)
            print("\nFunção em manutenção. Em breve disponível!\n")
            input("\nAperte ENTER para voltar ao menu principal...")

        case 5:
            limpar_terminal()
            exibir_titulo_centralizado("LIMPAR TODOS OS REGISTROS", 60)
            print("\nFunção em manutenção. Em breve disponível!\n")
            input("\nAperte ENTER para voltar ao menu principal...")

        case 6:
            limpar_terminal()
            exibir_titulo_centralizado("EXPORTAR REGISTROS PARA JSON", 60)
            print("\nFunção em manutenção. Em breve disponível!\n")
            input("\nAperte ENTER para voltar ao menu principal...")