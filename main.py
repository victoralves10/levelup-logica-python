import os
import re
import oracledb
import requests
import pandas as pd
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
    """Solicita ao usuário um CPF (11 dígitos), aceitando com ou sem formatação
    e retornando sempre no formato 000.000.000-00."""
    
    cpf = ""

    while not (cpf.isdigit() and len(cpf) == 11):
        entrada = input(_msg_input).strip()
        cpf = (
            entrada.replace(".", "")
                   .replace("-", "")
                   .replace(" ", "")
        )

        if not (cpf.isdigit() and len(cpf) == 11):
            print(f"{_msg_erro}\n")
            cpf = ""

    cpf_formatado = (
        f"{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"
    )

    return cpf_formatado


def obter_cnpj(_msg_input: str, _msg_erro: str) -> str:
    """Solicita ao usuário um CNPJ (14 dígitos), aceitando com ou sem formatação
    e retornando sempre no formato 00.000.000/0000-00."""
    
    cnpj = ""

    while not (cnpj.isdigit() and len(cnpj) == 14):
        entrada = input(_msg_input).strip()
        cnpj = (
            entrada.replace(".", "")
                   .replace("-", "")
                   .replace("/", "")
                   .replace(" ", "")
        )

        if not (cnpj.isdigit() and len(cnpj) == 14):
            print(f"{_msg_erro}\n")
            cnpj = ""

    cnpj_formatado = (
        f"{cnpj[0:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"
    )

    return cnpj_formatado

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
                    "pais": "BRA"
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
    return _endereco.get("pais", "BRA")


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
        print("INFORMAÇÕES DE ENDEREÇO\n")

        # ===== 1. CEP + consulta automática =====
        endereco = obter_endereco(
            "Digite o CEP (ex: 01310200): ",
            "CEP inválido! Digite um CEP com 8 números."
        )

        # ===== 2. País, Estado, Cidade, Bairro, Rua =====
        pais = obter_pais(endereco)
        estado = obter_estado(endereco)
        cidade = obter_cidade(endereco)
        bairro = obter_bairro(endereco)
        rua = obter_rua(endereco)

        imprimir_linha_separadora("=", 40)

        # ===== 3. Número =====
        numero = obter_int(
            "Número da residência: ",
            "Entrada inválida. Digite apenas números."
        )

        # ===== 5. Retorno final =====
        dados = {
            "cep": endereco["cep"],
            "pais": pais,
            "estado": estado,
            "cidade": cidade,
            "bairro": bairro,
            "rua": rua,
            "numero": numero
        }

        return (True, dados)

    except Exception as e:
        return (False, e)

def solicitar_dados_t_lvup_login() -> tuple[bool, any]:  # dict ou erro
    try:
        print("INFORMAÇÕES DE LOGIN\n")

        login = obter_texto("Digite o login (ex: seu.usuario): ","Entrada inválida. O campo não pode ficar vazio.")
        imprimir_linha_separadora("=", 40)

        senha = obter_texto("Digite a senha: ","Entrada inválida. O campo não pode ficar vazio.")

        dados = {
            "login": login,
            "senha": senha,
            "st_ativo": "S",
        }
        return (True, dados)

    except Exception as e:
        return (False, e)

def solicitar_dados_t_empresa() -> tuple[bool, any]:  # dict ou erro
    try:
        print("INFORMAÇÕES DA EMPRESA\n")

        nm_empresa = obter_texto("Nome da Empresa: ", "Entrada inválida. O campo não pode ficar vazio")
        imprimir_linha_separadora("=", 40)

        cnpj_empresa = obter_cnpj("CNPJ da Empresa (ex: 00.000.000/0000-00): ", "Entrada inválida. Digite um CNPJ com 14 números.")
        imprimir_linha_separadora("=", 40)

        email_empresa = obter_email("E-mail da Empresa: ","Formato de e-mail incorreto. Digite um e-mail válido da empresa.")

        dt_cadastro = datetime.now()

        dados = {
            "nm_empresa": nm_empresa,
            "cnpj_empresa": cnpj_empresa,
            "email_empresa": email_empresa,
            "dt_cadastro": dt_cadastro,
            "st_empresa": "A"
        }

        return (True, dados)

    except Exception as e:
        return (False, e)

# ==========================================================
#   BANCO DE DADOS
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

# ========= INSERT  =========
def insert_endereco(_conexao: oracledb.Connection, _dados_endereco: dict) -> tuple[bool, any]:
    """
    Insere um novo endereço na tabela T_ENDERECO.
    Retorna (True, id_endereco) ou (False, erro)
    """
    try:
        comando_sql = """
        INSERT INTO T_ENDERECO (
            cep, pais, estado, cidade, bairro, rua, numero
        ) VALUES (
            :cep, :pais, :estado, :cidade, :bairro, :rua, :numero
        )
        RETURNING id_endereco INTO :id_endereco
        """
        cur = _conexao.cursor()
        id_endereco = cur.var(int)
        cur.execute(comando_sql, {**_dados_endereco, "id_endereco": id_endereco})
        _conexao.commit()
        cur.close()
        return (True, id_endereco.getvalue()[0])
    except Exception as e:
        return (False, e)
"""CREATE TABLE T_ENDERECO(
id_endereco INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
cep VARCHAR2(10) NOT NULL,
pais VARCHAR2(3) NOT NULL,
estado VARCHAR2(2) NOT NULL,
cidade VARCHAR2(100) NOT NULL,
bairro VARCHAR2(100) NOT NULL,
rua VARCHAR2(150) NOT NULL,
numero INTEGER NOT NULL,
complemento VARCHAR2(150)
);
"""

#  ========= INSERT T_LVUP_LOGIN =========
def insert_lvup_login(_conexao: oracledb.Connection, _dados_login: dict) -> tuple[bool, any]:
    """
    Insere um novo login na tabela T_LVUP_LOGIN.
    Retorna (True, id_login) ou (False, erro)
    """
    try:
        comando_sql = """
        INSERT INTO T_LVUP_LOGIN (
            login, senha, st_ativo
        ) VALUES (
            :login, :senha, :st_ativo
        )
        RETURNING id_login INTO :id_login
        """
        cur = _conexao.cursor()
        id_login = cur.var(int)
        cur.execute(comando_sql, {**_dados_login, "id_login": id_login})
        _conexao.commit()
        cur.close()
        return (True, id_login.getvalue()[0])
    except Exception as e:
        return (False, e)
"""CREATE TABLE T_LVUP_LOGIN (
id_login INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
login VARCHAR2(100) NOT NULL,
senha VARCHAR2(100) NOT NULL,
st_ativo CHAR(1) NOT NULL,
id_empresa INTEGER,
id_instAcademica INTEGER,
id_pessoa INTEGER
);
"""

# ========= INSERT T_EMPRESA =========
def insert_empresa(_conexao: oracledb.Connection, _dados_empresa: dict, id_endereco: int, id_login: int) -> tuple[bool, any]:
    """
    Insere uma nova empresa na tabela T_EMPRESA.
    Retorna (True, id_empresa) ou (False, erro)
    """
    try:
        comando_sql = """
        INSERT INTO T_EMPRESA (
            nm_empresa, cnpj_empresa, email_empresa, dt_cadastro, st_empresa, id_endereco, id_login
        ) VALUES (
            :nm_empresa, :cnpj_empresa, :email_empresa, TO_DATE(:dt_cadastro, 'DD/MM/YY'), :st_empresa, :id_endereco, :id_login
        )
        RETURNING id_empresa INTO :id_empresa
        """
        cur = _conexao.cursor()
        id_empresa = cur.var(int)
        cur.execute(comando_sql, {**_dados_empresa, "id_endereco": id_endereco, "id_login": id_login, "id_empresa": id_empresa})
        _conexao.commit()
        cur.close()
        return (True, id_empresa.getvalue()[0])
    except Exception as e:
        return (False, e)
"""CREATE TABLE T_EMPRESA (
id_empresa INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
nm_empresa VARCHAR2(150) NOT NULL,
cnpj_empresa VARCHAR2(20) NOT NULL,
email_empresa VARCHAR2(100) NOT NULL,
dt_cadastro DATE NOT NULL, -- mudar isso para fazer automatico
st_empresa CHAR(1) NOT NULL,
id_endereco INTEGER REFERENCES T_ENDERECO (id_endereco),
id_login INTEGER NOT NULL REFERENCES T_LVUP_LOGIN (id_login)
);
"""

# ========= SELECT EMPRESA POR ID =========
def select_empresa_por_id(_conexao: oracledb.Connection, _id_empresa: int) -> tuple[bool, any]:
    """
    Recupera os dados de uma empresa específica pelo ID, incluindo informações de login e endereço.
    Retorna todas as colunas como lista de dicionários.
    """
    if not _id_empresa:
        return False, "Erro: é necessário informar o ID da empresa."

    try:
        query = """
        SELECT 
            e.id_empresa,
            e.nm_empresa,
            e.cnpj_empresa,
            e.email_empresa,
            e.dt_cadastro,
            e.st_empresa,
            l.login,
            l.st_ativo AS st_login,
            endr.cep,
            endr.pais,
            endr.estado,
            endr.cidade,
            endr.bairro,
            endr.rua,
            endr.numero,
            endr.complemento
        FROM T_EMPRESA e
        LEFT JOIN T_LVUP_LOGIN l ON e.id_login = l.id_login
        LEFT JOIN T_ENDERECO endr ON e.id_endereco = endr.id_endereco
        WHERE e.id_empresa = :id_empresa
        """

        cur = _conexao.cursor()
        cur.execute(query, {"id_empresa": _id_empresa})

        colunas_cursor = [c[0].lower() for c in cur.description]
        resultados = cur.fetchall()
        cur.close()

        if not resultados:
            return True, []  # Nenhum registro encontrado

        # Montar lista de dicionários
        lista_resultados = []
        for linha in resultados:
            registro = {}
            for i in range(len(colunas_cursor)):
                registro[colunas_cursor[i]] = linha[i]
            lista_resultados.append(registro)

        return True, lista_resultados

    except Exception as e:
        return False, str(e)

# ========= SELECT TODAS AS EMPRESAS COMPLETAS =========
def select_todas_empresas_completas(_conexao: oracledb.Connection) -> tuple[bool, any]:
    """
    Recupera todos os registros de empresas, incluindo informações de login e endereço.
    Retorna lista de dicionários, cada um representando uma empresa.
    """
    try:
        query = """
        SELECT 
            e.id_empresa,
            e.nm_empresa,
            e.cnpj_empresa,
            e.email_empresa,
            e.dt_cadastro,
            e.st_empresa,
            l.login,
            l.st_ativo AS st_login,
            endr.cep,
            endr.pais,
            endr.estado,
            endr.cidade,
            endr.bairro,
            endr.rua,
            endr.numero,
            endr.complemento
        FROM T_EMPRESA e
        LEFT JOIN T_LVUP_LOGIN l ON e.id_login = l.id_login
        LEFT JOIN T_ENDERECO endr ON e.id_endereco = endr.id_endereco
        ORDER BY e.id_empresa
        """

        cur = _conexao.cursor()
        cur.execute(query)

        colunas_cursor = [c[0].lower() for c in cur.description]
        resultados = cur.fetchall()
        cur.close()

        if not resultados:
            return True, []  # Nenhum registro encontrado

        lista_resultados = []
        for linha in resultados:
            registro = {}
            for i in range(len(colunas_cursor)):
                registro[colunas_cursor[i]] = linha[i]
            lista_resultados.append(registro)

        return True, lista_resultados

    except Exception as e:
        return False, str(e)

# ========= SELECT PARA PREVIEW =========
def select_para_preview(_conexao: oracledb.Connection) -> tuple[bool, any]:
    """
    Recupera apenas o ID e o nome de todas as empresas.
    Retorna uma lista de dicionários com as colunas: id_empresa e nm_empresa.
    """
    try:
        query = "SELECT id_empresa, nm_empresa FROM T_EMPRESA ORDER BY id_empresa"

        cur = _conexao.cursor()
        cur.execute(query)

        colunas_cursor = [c[0].lower() for c in cur.description]
        resultados = cur.fetchall()
        cur.close()

        if not resultados:
            return True, []  # Nenhum registro encontrado

        # Montar lista de dicionários
        lista_resultados = []
        for linha in resultados:
            registro = {}
            for i in range(len(colunas_cursor)):
                registro[colunas_cursor[i]] = linha[i]
            lista_resultados.append(registro)

        return True, lista_resultados

    except Exception as e:
        return False, str(e)

# ========= IMPRIMIR LISTA COMO TABELA =========
def imprimir_lista_como_tabela(lista_resultados: list[dict]) -> None:
    """
    Recebe uma lista de dicionários e imprime em formato de tabela organizada usando pandas.
    """
    if not lista_resultados:
        print("Nenhum registro encontrado.")
        return

    df = pd.DataFrame(lista_resultados)
    print(df.to_string(index=False))

# ========= IMPRIMIR LISTA NORMAL =========
def imprimir_lista_simples(lista_resultados: list[dict]) -> None:
    if not lista_resultados:
        print("Nenhum registro encontrado.")
        return

    print("index | Dados")

    contador = 1  # contador global de campos
    for item in lista_resultados:
        for chave, valor in item.items():
            print(f"{contador} - {chave}: {valor}")
            contador += 1

# ========= UPDATE POR ID =========
def atualizar_dados_empresa_por_id(_conexao: oracledb.Connection, _index: int, id_empresa: int) -> tuple[bool, any]:
    """
    Atualiza os dados de uma empresa pelo ID e pelo índice de campo escolhido.
    index = 1..16 conforme os campos:
    1 - ID (não editável)
    2 - Nome da empresa
    3 - CNPJ
    4 - E-mail
    5 - Data de cadastro
    6 - Status da empresa
    7 - Login
    8 - Status do login
    9 - CEP
    10 - País
    11 - Estado
    12 - Cidade
    13 - Bairro
    14 - Rua
    15 - Número
    16 - Complemento

    Retorno:
        (True, dados_atualizados) ou (False, erro)
    """
    try:
        # Recupera os dados atuais da empresa
        ok, dados_empresa = select_empresa_por_id(_conexao, id_empresa)
        if not ok or not dados_empresa:
            return False, "Empresa não encontrada ou erro ao consultar."
        dados_empresa = dados_empresa[0]  # pega o primeiro registro (único ID)

        # Garantir que id_login e id_endereco estejam presentes
        cur = _conexao.cursor()
        if "id_login" not in dados_empresa or not dados_empresa.get("id_login"):
            cur.execute(
                "SELECT id_login FROM T_LVUP_LOGIN WHERE login = :login",
                {"login": dados_empresa.get("login")}
            )
            row = cur.fetchone()
            dados_empresa["id_login"] = row[0] if row else None

        if "id_endereco" not in dados_empresa or not dados_empresa.get("id_endereco"):
            # Supõe que T_EMPRESA tem a coluna id_endereco
            dados_empresa["id_endereco"] = dados_empresa.get("id_endereco")

        cur.close()

        # Atualiza o campo escolhido
        match _index:
            case 1:
                return False, "Não é possível atualizar o ID."
            case 2:
                dados_empresa["nm_empresa"] = obter_texto("Nome da Empresa: ", "Entrada inválida. O campo não pode ficar vazio")
            case 3:
                dados_empresa["cnpj_empresa"] = obter_cnpj("CNPJ da Empresa (ex: 00.000.000/0000-00): ", "Entrada inválida. Digite um CNPJ com 14 números.")
            case 4:
                dados_empresa["email_empresa"] = obter_email("E-mail da Empresa: ","Formato de e-mail incorreto. Digite um e-mail válido.")
            case 5:
                dados_empresa["dt_cadastro"] = datetime.now()
            case 6:
                dados_empresa["st_empresa"] = "A" if obter_sim_nao("Empresa está ativa (S/N)? ", "Erro!") else "I"
            case 7:
                dados_empresa["login"] = obter_texto("Digite o login (ex: seu.usuario): ","Entrada inválida. O campo não pode ficar vazio")
            case 8:
                dados_empresa["st_login"] = "S" if obter_sim_nao("Login está ativo (S/N)? ", "Erro!") else "N"
            case 9:
                endereco = obter_endereco("Digite o CEP (ex: 01310200): ", "CEP inválido!")
                dados_empresa["cep"] = endereco["cep"]
            case 10:
                dados_empresa["pais"] = obter_texto("País (ex: BRA): ", "Entrada inválida. O campo não pode ficar vazio")
            case 11:
                dados_empresa["estado"] = obter_texto("Estado (ex: SP): ", "Entrada inválida. O campo não pode ficar vazio")
            case 12:
                dados_empresa["cidade"] = obter_texto("Cidade: ", "Entrada inválida. O campo não pode ficar vazio")
            case 13:
                dados_empresa["bairro"] = obter_texto("Bairro: ", "Entrada inválida. O campo não pode ficar vazio")
            case 14:
                dados_empresa["rua"] = obter_texto("Rua: ", "Entrada inválida. O campo não pode ficar vazio")
            case 15:
                dados_empresa["numero"] = obter_int("Número: ", "Entrada inválida. Digite apenas números.")
            case 16:
                dados_empresa["complemento"] = obter_texto("Complemento: ", "Entrada inválida. O campo não pode ficar vazio")
            case _:
                return False, "Campo inválido!"

        # Atualização no banco de dados
        cur = _conexao.cursor()

        # Atualiza apenas o campo escolhido na T_EMPRESA
        campos_empresa_map = {2: "nm_empresa", 3: "cnpj_empresa", 4: "email_empresa", 5: "dt_cadastro", 6: "st_empresa"}
        if _index in campos_empresa_map:
            campo_sql = campos_empresa_map[_index]
            sql = f"UPDATE T_EMPRESA SET {campo_sql} = :valor WHERE id_empresa = :id_empresa"
            cur.execute(sql, {"valor": dados_empresa[campo_sql], "id_empresa": id_empresa})

        # Atualiza login
        campos_login_map = {7: "login", 8: "st_login"}
        if _index in campos_login_map:
            campo_sql = campos_login_map[_index]
            sql_login = f"UPDATE T_LVUP_LOGIN SET {campo_sql if campo_sql != 'st_login' else 'st_ativo'} = :valor WHERE id_login = :id_login"
            cur.execute(sql_login, {"valor": dados_empresa[campo_sql], "id_login": dados_empresa["id_login"]})

        # Atualiza endereço
        campos_end_map = {9: "cep", 10: "pais", 11: "estado", 12: "cidade", 13: "bairro", 14: "rua", 15: "numero", 16: "complemento"}
        if _index in campos_end_map:
            campo_sql = campos_end_map[_index]
            sql_end = f"UPDATE T_ENDERECO SET {campo_sql} = :valor WHERE id_endereco = :id_endereco"
            cur.execute(sql_end, {"valor": dados_empresa[campo_sql], "id_endereco": dados_empresa["id_endereco"]})

        _conexao.commit()
        cur.close()

        return True, dados_empresa

    except Exception as e:
        return False, str(e)

# ========================================
#   CONEXÃO COM O BANCO DE DADOS ORACLE
# ========================================

user = "rm561713"
password = "290107"
dsn = "oracle.fiap.com.br:1521/ORCL"

ok, conn = conectar_oracledb(user, password, dsn)

if ok:
    limpar_terminal()
    exibir_titulo_centralizado("✅ CONECTADO AO BANCO DE DADOS COM SUCESSO", 60)
    print("Conexão estabelecida com sucesso com o servidor Oracle da FIAP.")
    input("\nAperte ENTER para acessar o sistema...")
else:
    limpar_terminal()
    exibir_titulo_centralizado("❌ ERRO AO CONECTAR AO BANCO DE DADOS", 60)
    print(f"Detalhes do erro:\n{conn}\n")
    input("Aperte ENTER para encerrar o programa...")

# ok = True

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

        case 0: # 0 - Sair do sistema
            limpar_terminal()
            print("\nPrograma encerrado. Até logo!\n")
            ok = False

        case 1: # 1 - Cadastrar nova empresa
            limpar_terminal()
            exibir_titulo_centralizado("CADASTRAR NOVA EMPRESA — LOGIN", 60)

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
            
            limpar_terminal()
            exibir_titulo_centralizado("CADASTRAR NOVA EMPRESA — LOGIN", 60)
            # ---------------------------
            # 1. SOLICITAR LOGIN
            # ---------------------------
            sucesso_login, dados_login = solicitar_dados_t_lvup_login()
            if not sucesso_login:
                print("\nErro ao coletar dados de login:")
                print(dados_login)
                input("\nAperte ENTER para voltar ao menu principal...")
                continue


            # ---------------------------
            # 2. SOLICITAR ENDEREÇO
            # ---------------------------
            limpar_terminal()
            exibir_titulo_centralizado("CADASTRAR NOVA EMPRESA — ENDEREÇO", 60)

            sucesso_end, dados_endereco = solicitar_dados_endereco()
            if not sucesso_end:
                print("\nErro ao coletar dados de endereço:")
                print(dados_endereco)
                input("\nAperte ENTER para voltar ao menu principal...")
                continue


            # ---------------------------
            # 3. SOLICITAR DADOS DA EMPRESA
            # ---------------------------
            limpar_terminal()
            exibir_titulo_centralizado("CADASTRAR NOVA EMPRESA — DADOS DA EMPRESA", 60)

            sucesso_emp, dados_empresa = solicitar_dados_t_empresa()
            if not sucesso_emp:
                print("\nErro ao coletar dados da empresa:")
                print(dados_empresa)
                input("\nAperte ENTER para voltar ao menu principal...")
                continue

            # ---------------------------
            # 4. INSERIR TUDO NO BANCO DE DADOS
            # ---------------------------
            limpar_terminal()
            exibir_titulo_centralizado("PROCESSANDO CADASTRO...", 60)

            # INSERE LOGIN
            ok_login, id_login = insert_lvup_login(conn, dados_login)
            if not ok_login:
                print("Erro ao inserir login no banco:")
                print(id_login)
                input("\nAperte ENTER para voltar ao menu principal...")
                continue

            # INSERE ENDEREÇO
            ok_end_bd, id_endereco = insert_endereco(conn, dados_endereco)
            if not ok_end_bd:
                print("Erro ao inserir endereço no banco:")
                print(id_endereco)
                input("\nAperte ENTER para voltar ao menu principal...")
                continue

            # INSERE EMPRESA
            ok_emp_bd, id_empresa = insert_empresa(conn, dados_empresa, id_endereco, id_login)
            if not ok_emp_bd:
                print("Erro ao inserir empresa no banco:")
                print(id_empresa)
                input("\nAperte ENTER para voltar ao menu principal...")
                continue

            # SUCESSO FINAL
            print("\nCadastro concluído com sucesso!")
            input("\nAperte ENTER para voltar ao menu principal...")

        case 2: # 2 - Consultar empresas cadastradas
            limpar_terminal()
            exibir_titulo_centralizado("CONSULTAR EMPRESAS CADASTRADAS", 60)

            deseja_continuar = obter_sim_nao(
                "Deseja fazer uma pesquisa? (S/N): ",
                "Entrada inválida! Digite 'S' para Sim ou 'N' para Não."
            )

            limpar_terminal()
            exibir_titulo_centralizado("CONSULTAR EMPRESAS CADASTRADAS", 60)

            if not deseja_continuar:
                limpar_terminal()
                print("Pesquisa cancelado pelo usuário.\n")
                input("\nAperte ENTER para voltar ao menu principal...")
                continue  # volta ao menu

            # Pergunta se deseja consultar uma empresa específica ou todas
            opcao_consulta = obter_sim_nao(
                "Deseja consultar uma empresa específica pelo ID? (S/N): ",
                "Entrada inválida! Digite S para Sim ou N para Não."
            )

            if opcao_consulta:  # Consulta por ID
                # Mostra preview de todas as empresas (ID e Nome) antes de digitar
                ok_preview, preview_empresas = select_para_preview(conn)
                if ok_preview and preview_empresas:
                    print("\nPreview das empresas cadastradas (ID e Nome):")
                    imprimir_lista_como_tabela(preview_empresas)
                else:
                    print("\nNenhuma empresa encontrada para preview.")

                # Solicita o ID após o preview
                id_empresa = obter_int(
                    "\nDigite o ID da empresa que deseja consultar: ",
                    "Entrada inválida! Digite apenas números."
                )
                ok_sel, resultado = select_empresa_por_id(conn, id_empresa)

            else:  # Consulta todas as empresas completas
                ok_sel, resultado = select_todas_empresas_completas(conn)

            if not ok_sel:
                print("\nErro ao consultar o banco de dados:")
                print(resultado)
            else:
                limpar_terminal()
                exibir_titulo_centralizado("CONSULTAR EMPRESAS CADASTRADAS", 60)
                imprimir_lista_como_tabela(resultado)

            input("\nAperte ENTER para voltar ao menu principal...")

        case 3:  # 3 - Atualizar informações de uma empresa
            limpar_terminal()
            exibir_titulo_centralizado("ATUALIZAR INFORMAÇÕES DE EMPRESA", 60)

            deseja_continuar = obter_sim_nao(
                "Deseja atualizar os dados? (S/N): ",
                "Entrada inválida! Digite 'S' para Sim ou 'N' para Não."
            )

            if not deseja_continuar:
                limpar_terminal()
                print("Atualização cancelada pelo usuário.\n")
                input("\nAperte ENTER para voltar ao menu principal...")
                continue  # volta ao menu

            # Preview das empresas
            ok_preview, preview_empresas = select_para_preview(conn)
            if ok_preview and preview_empresas:
                print("\nPreview das empresas cadastradas (ID e Nome):")
                imprimir_lista_como_tabela(preview_empresas)
            else:
                print("\nNenhuma empresa encontrada para preview.")

            # Solicita o ID da empresa
            id_empresa = obter_int(
                "\nDigite o ID da empresa que deseja atualizar: ",
                "Entrada inválida! Digite apenas números."
            )

            ok_sel, resultado = select_empresa_por_id(conn, id_empresa)
            if not ok_sel or not resultado:
                print("\nErro ao consultar o banco de dados ou empresa não encontrada:")
                print(resultado)
                input("\nAperte ENTER para voltar ao menu principal...")
                continue

            # Mostra os dados atuais
            limpar_terminal()
            exibir_titulo_centralizado("DADOS ATUAIS DA EMPRESA", 60)
            imprimir_lista_simples(resultado)

            campo_escolhido = obter_int_intervalado(
                "\nDigite o número do campo a atualizar: ",
                "Entrada inválida! Digite um número válido.",
                0, 16
            )

            if campo_escolhido == 0:
                print("\nAtualização cancelada pelo usuário.")
                input("\nAperte ENTER para voltar ao menu principal...")
                continue

            # Chama a função de atualização
            ok_atual, resultado_atual = atualizar_dados_empresa_por_id(conn, campo_escolhido, id_empresa)
            if ok_atual:
                limpar_terminal()
                print("\nDados atualizados com sucesso!")
                imprimir_lista_simples([resultado_atual])
            else:
                limpar_terminal()
                print("\nErro ao atualizar os dados:")
                print(resultado_atual)

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