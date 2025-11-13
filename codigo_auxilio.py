# ==========================================================
#   INSTRUÇÕES PARA EXECUTAR O PROGRAMA
# ==========================================================
# 1  -   Execute o comando SQL abaixo no 'Oracle SQL Developer' para criar as tabelas necessárias.
# 2  -   Instale as bibliotecas exigidas no terminal:
#         pip install oracledb
#         pip install tabulate
#         pip install requests
#         pip install pandas

# COMANDO SQL PARA ORACLE:

"""
-- Tabela de Pacientes
CREATE TABLE T_PACIENTE (
    ID_PACIENTE        NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    NM_COMPLETO        VARCHAR2(150) NOT NULL,
    DT_NASCIMENTO      DATE NOT NULL,
    SEXO               CHAR(1) NOT NULL,
    CPF                VARCHAR2(11),
    RG                 VARCHAR2(9),
    ESTADO_CIVIL       VARCHAR2(20),
    BRASILEIRO         CHAR(1),  -- S/N
    CEP                VARCHAR2(8),
    RUA                VARCHAR2(100),
    BAIRRO             VARCHAR2(50),
    CIDADE             VARCHAR2(50),
    ESTADO             CHAR(2),
    NUMERO_ENDERECO    NUMBER,
    CELULAR            VARCHAR2(11),
    EMAIL              VARCHAR2(100),
    CONVENIO           CHAR(1),   -- S/N

    -- Campos de consulta
    DT_HORA_CONSULTA   TIMESTAMP,
    TIPO_CONSULTA      VARCHAR2(20),
    ESPECIALIDADE      VARCHAR2(50),
    STATUS_CONSULTA    VARCHAR2(20),

    -- Controle de registro
    DT_CADASTRO        DATE DEFAULT SYSDATE,
    DT_ULTIMA_ATUALIZACAO TIMESTAMP DEFAULT SYSTIMESTAMP
);

-- Trigger para atualizar automaticamente DT_ULTIMA_ATUALIZACAO
CREATE OR REPLACE TRIGGER trg_t_paciente_atualizacao
BEFORE UPDATE ON T_PACIENTE
FOR EACH ROW
BEGIN
    :NEW.DT_ULTIMA_ATUALIZACAO := SYSTIMESTAMP;
END;
"""

# Este programa utiliza a API pública do ViaCEP para consultar informações de endereços
# a partir do CEP informado pelo usuário.
# A API retorna dados como: Logradouro, Bairro, Cidade, Estado e outros dados relacionados ao CEP.

# Após isso, o código estará pronto para ser executado.

# Execute o programa pelo arquivo principal: main.py
# (no terminal: python main.py)

# --- Bibliotecas padrão ---
import os
import re
import json
from datetime import datetime, date

# --- Pacotes externos ---
import oracledb
import requests
import pandas as pd
from tabulate import tabulate

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
#   VALIDAÇÃO DE DADOS PARA CADASTRO (PACIENTE)
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
                    "estado": data.get("uf", "")
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

# ==========================================================
#   SOLICITAÇÃO DE DADOS T_PACIENTE
# ==========================================================

def solicitar_dados_paciente() -> tuple[bool, dict]:
    """Solicita e retorna todos os dados do paciente e da consulta.
       Retorna uma tupla: (sucesso: bool, dados: dict)
    """
    try:
        # ========= DADOS DO PACIENTE =========
        nome_completo = obter_texto("Nome do paciente: ", "Nome inválido!")
        imprimir_linha_separadora("=-", 20)

        data_nascimento = obter_data("Data de nascimento (dd/mm/aaaa): ", "Data inválida!")
        imprimir_linha_separadora("=-", 20)

        sexo = obter_m_f("Sexo [M/F]: ", "Entrada inválida! Digite M ou F.")
        imprimir_linha_separadora("=-", 20)

        cpf = obter_cpf("CPF (somente números, ex: 12345678901): ", "CPF inválido!")
        imprimir_linha_separadora("=-", 20)

        rg = obter_rg("RG (somente números, ex: 123456789): ", "RG inválido!")
        imprimir_linha_separadora("=-", 20)

        estado_civil_dict = {1: "Solteiro", 2: "Casado", 3: "Divorciado", 4: "Viuvo"}
        estado_civil = obter_opcao_dict("""Estado civil
1 - Solteiro
2 - Casado
3 - Divorciado
4 - Viuvo
Escolha: """, "Opção inválida!", estado_civil_dict)
        imprimir_linha_separadora("=-", 20)

        brasileiro = obter_sim_nao("É brasileiro? [S/N]: ", "Entrada inválida!")
        imprimir_linha_separadora("=-", 20)

        endereco = obter_endereco("CEP (ex: 01310200): ", "CEP inválido!")
        imprimir_linha_separadora("=-", 20)

        numero_endereco = obter_int("Número da residência (ex: 123): ", "Número inválido!")
        imprimir_linha_separadora("=-", 20)

        celular = obter_texto("Celular (DDD + número — ex: 11987654321): ", "Número inválido!")
        imprimir_linha_separadora("=-", 20)

        email = obter_email("Informe o e-mail (exemplo: exemplo@email.com)\nE-mail: ", "E-mail inválido!")
        imprimir_linha_separadora("=-", 20)

        convenio = obter_sim_nao("Possui convênio/plano de saúde? [S/N]: ", "Entrada inválida!")
        imprimir_linha_separadora("=-", 20)

        # ========= DADOS DA CONSULTA =========
        data_hora_consulta = obter_data_hora("Digite a data e hora da consulta (ex: 25/10/2025 14:30): ", "Data e hora inválida!")
        imprimir_linha_separadora("=-", 20)

        tipo_consulta_dict = {1: "Retorno", 2: "Emergencia", 3: "Rotina", 4: "Exame", 5: "Geral"}
        tipo_consulta = obter_opcao_dict("""Tipo de consulta
1 - Retorno
2 - Emergencia
3 - Rotina
4 - Exame
5 - Geral
Escolha: """, "Opção inválida!", tipo_consulta_dict)
        imprimir_linha_separadora("=-", 20)

        especialidade_dict = {
            1: "Cardiologia",
            2: "Neurologia",
            3: "Ortopedia",
            4: "Dermatologia",
            5: "Pediatria",
            6: "Oftalmologia",
            7: "Clínico Geral"
        }
        especialidade = obter_opcao_dict("""Especialidade
1 - Cardiologia
2 - Neurologia
3 - Ortopedia
4 - Dermatologia
5 - Pediatria
6 - Oftalmologia
7 - Clínico Geral
Escolha: """, "Opção inválida!", especialidade_dict)
        imprimir_linha_separadora("=-", 20)

        status_consulta_dict = {1: "Realizada", 2: "Cancelada", 3: "Absenteísmo"}
        status_consulta = obter_opcao_dict("""Status da consulta
1 - Realizada
2 - Cancelada
3 - Absenteísmo
Escolha: """, "Opção inválida!", status_consulta_dict)

        # ========= RETORNO =========
        dados = {
            "nome_completo": nome_completo,
            "data_nascimento": data_nascimento,
            "sexo": sexo,
            "cpf": cpf[:11],
            "rg": rg[:9],
            "estado_civil": estado_civil[:20],
            "brasileiro": "S" if brasileiro else "N",
            "cep": obter_cep(endereco).replace("-", ""),
            "rua": obter_rua(endereco)[:100],
            "bairro": obter_bairro(endereco)[:50],
            "cidade": obter_cidade(endereco)[:50],
            "estado": obter_estado(endereco)[:2],
            "numero_endereco": numero_endereco,
            "celular": celular[:11],
            "email": email[:100],
            "convenio": "S" if convenio else "N",
            "data_hora_consulta": data_hora_consulta,
            "tipo_consulta": tipo_consulta[:20],
            "especialidade": especialidade[:50],
            "status_consulta": status_consulta[:20]
        }

        retorno = True, dados

    except Exception as e:
        print(f"Erro ao solicitar dados: {e}")
        retorno = False, {}

    return retorno

# ==========================================================
#   FORMATAÇÃO DE VALORES
# ==========================================================
def formatar_valor(valor, largura_max: int = 20) -> str:
    """
    Formata um valor para exibição, convertendo datas em strings legíveis
    e quebrando textos longos em múltiplas linhas com largura máxima.
    Retorna uma string pronta para exibição em tabelas"""
    if valor is None:
        return ""
    elif isinstance(valor, datetime):
        if valor.time() == datetime.min.time():
            return valor.strftime("%d/%m/%Y")
        else:
            return valor.strftime("%d/%m/%Y %H:%M")
    elif isinstance(valor, date):
        return valor.strftime("%d/%m/%Y")
    else:
        texto = str(valor)
        linhas = []
        for i in range(0, len(texto), largura_max):
            linhas.append(texto[i:i+largura_max])
        return "\n".join(linhas)

# ==========================================================
#   IMPRESSÃO DE RESULTADOS ORACLE
# ==========================================================

def imprimir_resultado_tabulate_oracle(resultado_cursor, largura_max: int = 20) -> tuple[bool, str]:
    """
    Converte resultados de consulta Oracle em uma tabela formatada usando Tabulate,
    aplicando quebra de linhas em textos longos e formatação de datas.
    Retorna uma tupla com sucesso e a string da tabela pronta para exibição.
    """
    try:
        # Se não houver resultados
        if not resultado_cursor:
            return False, "Nenhum registro encontrado."

        if hasattr(resultado_cursor, "description"):
            headers = []
            for col in resultado_cursor.description:
                headers.append(col[0])
            dados = resultado_cursor.fetchall()
        else:
            dados = resultado_cursor
            headers = []
            if len(dados) > 0 and isinstance(dados[0], dict):
                for key in dados[0].keys():
                    headers.append(key)
            else:
                for i in range(len(dados[0])):
                    headers.append(f"Col{i+1}")

        df = pd.DataFrame(dados, columns=headers)

        # Formatar valores
        for coluna in df.columns:
            df[coluna] = df[coluna].apply(lambda x: formatar_valor(x, largura_max))

        tabela = tabulate(
            df.to_dict(orient="records"),
            headers="keys",
            tablefmt="fancy_grid",
            numalign="right",
            stralign="left"
        )

        return True, tabela

    except Exception as e:
        return False, f"Erro ao imprimir resultado: {e}"

def imprimir_resultado_vertical_oracle(dados: list[dict]) -> None:
    """
    Exibe os dados de um registro Oracle em formato vertical, mostrando
    cada campo e seu valor. Mostra mensagem se não houver registros.
    """
    if not dados:
        print("Nenhum registro encontrado.")
        return

    registro = dados[0]
    df = pd.DataFrame(list(registro.items()), columns=["Campo", "Valor"])
    
    print(df.to_string(index=False))

# ==========================================================
#   CRUD BANCO DE DADOS
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

# ========= FUNÇÃO PARA VERIFICAR SE TABELA TEM DADOS =========
def verifica_tabela(_conexao: oracledb.Connection, nome_tabela: str) -> bool:
    """Verifica se a tabela possui registros e retorna True ou False."""
    try:
        cur = _conexao.cursor()
        cur.execute(f"SELECT 1 FROM {nome_tabela} WHERE ROWNUM = 1")
        resultado = cur.fetchone()
        return bool(resultado)
    except Exception as e:
        print(f"Erro ao verificar tabela {nome_tabela}: {e}")
        return False
    finally:
        cur.close()

# ========= INSERT PACIENTE =========
def insert_paciente(_conexao: oracledb.Connection, _dados_paciente: dict) -> tuple[bool, any]:
    """
    Insere um novo paciente na tabela T_PACIENTE do banco Oracle usando os dados fornecidos.
    Converte datas e horários para os formatos adequados e realiza commit da transação.
    Retorna uma tupla indicando sucesso e, em caso de erro, o objeto de exceção.
    """
    try:
        comando_sql = """
        INSERT INTO T_PACIENTE (
            NM_COMPLETO, DT_NASCIMENTO, SEXO, CPF, RG, ESTADO_CIVIL, BRASILEIRO,
            CEP, RUA, BAIRRO, CIDADE, ESTADO, NUMERO_ENDERECO, CELULAR, EMAIL, CONVENIO,
            DT_HORA_CONSULTA, TIPO_CONSULTA, ESPECIALIDADE, STATUS_CONSULTA
        )
        VALUES (
            :nome_completo, TO_DATE(:data_nascimento, 'DD/MM/YYYY'), :sexo, :cpf, :rg, :estado_civil, :brasileiro,
            :cep, :rua, :bairro, :cidade, :estado, :numero_endereco, :celular, :email, :convenio,
            TO_TIMESTAMP(:data_hora_consulta, 'DD/MM/YYYY HH24:MI'), :tipo_consulta, :especialidade, :status_consulta
        )
        """
        cur = _conexao.cursor()
        cur.execute(comando_sql, _dados_paciente)
        _conexao.commit()
        cur.close()

        return (True, None)

    except Exception as e:
        return (False, e)

# ========= SELECT PACIENTE =========
def select_paciente(_conexao: oracledb.Connection, _campos: str) -> tuple[bool, any]:
    """
    Retorna registros da tabela T_PACIENTE como lista de dicionários.
    Recebe uma string com os campos para SELECT (ex: id_paciente, nm_completo).
    """
    try:
        query = f"SELECT {_campos} FROM T_PACIENTE"

        with _conexao.cursor() as cur:
            cur.execute(query)

            colunas_cursor = []
            for c in cur.description:
                colunas_cursor.append(c[0].lower())

            resultados = cur.fetchall()
            df = pd.DataFrame(resultados, columns=colunas_cursor)


        return True, df.to_dict(orient="records")

    except Exception as e:
        return False, e

# ========= SELECT PACIENTE POR ID =========
def select_paciente_por_id(_conexao: oracledb.Connection, campos: str, _id_paciente: int) -> tuple[bool, any]:
    """
    Recupera os dados de um paciente específico pelo ID a partir da tabela T_PACIENTE.
    Retorna apenas os campos especificados e converte o resultado em lista de dicionários.
    Retorna uma tupla com sucesso (True/False) e os dados ou mensagem de erro.
    """

    if not _id_paciente:
        return False, "Erro: é necessário informar o ID do paciente."

    try:
        query = f"SELECT {campos} FROM T_PACIENTE WHERE id_paciente = :id_paciente"

        cur = _conexao.cursor()
        cur.execute(query, {"id_paciente": _id_paciente})

        colunas_cursor = []
        for c in cur.description:
            colunas_cursor.append(c[0].lower())

        resultados = cur.fetchall()

        cur.close()

        if not resultados:
            return True, []  

        df = pd.DataFrame(resultados, columns=colunas_cursor)
        return True, df.to_dict(orient="records")

    except Exception as e:
        return False, str(e)

# ========= SELECT PACIENTE POR TEXTO =========
def buscar_paciente_por_texto(_conexao: oracledb.Connection, _campo_where: str, _texto: str, _colunas_exibir: str) -> list[dict]:
    """
    Busca pacientes na tabela T_PACIENTE filtrando por texto em um campo específico.
    Retorna apenas as colunas selecionadas e converte os resultados em lista de dicionários.
    Campos inválidos ou erros de execução retornam uma lista vazia.
    """

    campos_validos = ["NM_COMPLETO", "ESTADO_CIVIL", "RUA", "BAIRRO", "CIDADE", "EMAIL", "TIPO_CONSULTA",
    "ESPECIALIDADE", "STATUS_CONSULTA"]

    if _campo_where.upper() not in campos_validos:
        print("\nErro: campo inválido para busca textual.\n")
        return []

    if not _colunas_exibir.strip():
        print("\nErro: nenhuma coluna selecionada para exibição.\n")
        return []

    comando_sql = f"""
        SELECT {_colunas_exibir}
        FROM T_PACIENTE
        WHERE UPPER({_campo_where}) LIKE :texto
    """

    try:
        cur = _conexao.cursor()
        cur.execute(comando_sql, {"texto": f"%{_texto.upper()}%"})
        resultados = cur.fetchall()

        colunas = [col[0].upper() for col in cur.description]

        lista_pacientes = [dict(zip(colunas, linha)) for linha in resultados]

        return lista_pacientes

    except Exception as e:
        print(f"\nErro ao executar consulta SQL: {e}\n")
        return []

    finally:
        cur.close()

# ========= SELECT PACIENTE POR NÚMERO =========
def buscar_paciente_por_numero(_conexao: oracledb.Connection, _campo: str, _operador: str, _valor: int, _colunas_exibir: str) -> list[dict]:
    """
    Busca pacientes na tabela T_PACIENTE filtrando por valor numérico em um campo específico.
    Retorna apenas as colunas selecionadas como lista de dicionários.
    Erros de execução resultam em uma lista vazia.
    """

    comando_sql = f"SELECT {_colunas_exibir} FROM T_PACIENTE WHERE {_campo} {_operador} :valor"
    cur = _conexao.cursor()

    try:
        cur.execute(comando_sql, {"valor": _valor})
        resultados = cur.fetchall()
        nomes_colunas = [col[0].upper() for col in cur.description]

        lista_pacientes = [dict(zip(nomes_colunas, linha)) for linha in resultados]

        return lista_pacientes

    except Exception as e:
        print(f"\nErro ao executar consulta SQL: {e}\n")
        return []

    finally:
        cur.close()

# ========= UPDATE PACIENTE POR ID =========
def atualizar_coluna_paciente(conn, id_paciente, coluna):
    """
    Atualiza uma coluna específica de um paciente.
    A função pergunta o valor correto dependendo da coluna usando match-case.
    Retorna (True, None) se sucesso, ou (False, erro) se falha.
    """
    try:
        coluna_upper = coluna.upper()
        
        match coluna_upper:
            # DADOS DO PACIENTE
            case "NM_COMPLETO":
                valor = obter_texto("\nNome do paciente: ", "Nome inválido!")
            case "DATA_NASCIMENTO":
                valor = obter_data("\nData de nascimento (dd/mm/aaaa): ", "Data inválida!")
            case "SEXO":
                valor = obter_m_f("\nSexo [M/F]: ", "Entrada inválida! Digite M ou F.")
            case "CPF":
                valor = obter_cpf("\nCPF (somente números, ex: 12345678901): ", "CPF inválido!")
            case "RG":
                valor = obter_rg("\nRG (somente números, ex: 123456789): ", "RG inválido!")
            case "ESTADO_CIVIL":
                estado_civil_dict = {1: "Solteiro", 2: "Casado", 3: "Divorciado", 4: "Viuvo"}
                valor = obter_opcao_dict("""\nEstado civil
1 - Solteiro
2 - Casado
3 - Divorciado
4 - Viuvo
Escolha: """, "Opção inválida!", estado_civil_dict)
            case "BRASILEIRO" | "CONVENIO":
                valor = obter_sim_nao(f"\n{coluna.replace('_', ' ').capitalize()}? [S/N]: ", "Entrada inválida!")
            case "ENDERECO":
                valor = obter_endereco("\nCEP (ex: 01310200): ", "CEP inválido!")
            case "NUMERO_ENDERECO":
                valor = obter_int("\nNúmero da residência (ex: 123): ", "Número inválido!")
            case "CELULAR":
                valor = obter_texto("\nCelular (DDD + número — ex: 11987654321): ", "Número inválido!")
            case "EMAIL":
                valor = obter_email("\nInforme o e-mail (exemplo: exemplo@email.com)\nE-mail: ", "E-mail inválido!")
            
            # DADOS DA CONSULTA
            case "DATA_HORA_CONSULTA":
                valor = obter_data_hora("\nDigite a data e hora da consulta (ex: 25/10/2025 14:30): ", "Data e hora inválida!")
            case "TIPO_CONSULTA":
                tipo_consulta_dict = {1: "Retorno", 2: "Emergencia", 3: "Rotina", 4: "Exame", 5: "Geral"}
                valor = obter_opcao_dict("""\nTipo de consulta
1 - Retorno
2 - Emergencia
3 - Rotina
4 - Exame
5 - Geral
Escolha: """, "Opção inválida!", tipo_consulta_dict)
            case "ESPECIALIDADE":
                especialidade_dict = {
                    1: "Cardiologia", 2: "Neurologia", 3: "Ortopedia",
                    4: "Dermatologia", 5: "Pediatria", 6: "Oftalmologia",
                    7: "Clínico Geral"
                }
                valor = obter_opcao_dict("""\nEspecialidade
1 - Cardiologia
2 - Neurologia
3 - Ortopedia
4 - Dermatologia
5 - Pediatria
6 - Oftalmologia
7 - Clínico Geral
Escolha: """, "Opção inválida!", especialidade_dict)
            case "STATUS_CONSULTA":
                status_consulta_dict = {1: "Realizada", 2: "Cancelada", 3: "Absenteísmo"}
                valor = obter_opcao_dict("""Status da consulta
1 - Realizada
2 - Cancelada
3 - Absenteísmo
Escolha: """, "Opção inválida!", status_consulta_dict)
            
            case _:
                return (False, f"Coluna '{coluna}' não reconhecida!")

        comando_sql = f"UPDATE T_PACIENTE SET {coluna_upper} = :valor WHERE ID_PACIENTE = :id_paciente"
        dados_paciente = {"valor": valor, "id_paciente": id_paciente}

        cur = conn.cursor()
        cur.execute(comando_sql, dados_paciente)
        conn.commit()
        cur.close()

        return (True, None)

    except Exception as e:
        return (False, e)

# ========= DELETE PACIENTE POR ID =========
def deletar_paciente(_conexao: oracledb.Connection, _id_paciente: int) -> tuple[bool, any]:
    """Remove paciente pelo ID e retorna status da operação."""
    try:
        comando_sql = "DELETE FROM T_PACIENTE WHERE ID_PACIENTE = :id"
        cur = _conexao.cursor()
        cur.execute(comando_sql, {"id": _id_paciente})

        if cur.rowcount == 0:
            _conexao.rollback()
            cur.close()
            return (False, "Nenhum paciente encontrado com este ID para remover.")

        _conexao.commit()
        cur.close()
        return (True, None)
    except Exception as e:
        return (False, e)

# ========= DELETE TODOS PACIENTE =========
def limpar_todos_pacientes(_conexao: oracledb.Connection) -> tuple[bool, any]:
    """Apaga todos os pacientes do banco e retorna status da operação."""
    try:
        comando_sql = "DELETE FROM T_PACIENTE"
        cur = _conexao.cursor()
        cur.execute(comando_sql)
        
        _conexao.commit()
        cur.close()
        
        return (True, None)

    except Exception as e:
        return (False, e)

# ==========================================================
#   EXPORTAR PACIENTES PARA JSON
# ==========================================================

# ========= EXPORTAR PACIENTES PARA JSON =========
def exportar_para_json(_dados: list[dict], _nome_arquivo: str = "pacientes.json") -> tuple[bool, any]:
    try:
        if not _dados:
            return (False, "Nenhum dado recebido para exportar.")

        for item in _dados:
            for chave, valor in item.items():
                if isinstance(valor, datetime):
                    item[chave] = valor.strftime("%d/%m/%Y %H:%M")
                elif isinstance(valor, date):
                    item[chave] = valor.strftime("%d/%m/%Y")

        # Salva os dados em um arquivo JSON
        with open(_nome_arquivo, "w", encoding="utf-8") as arquivo_json:
            json.dump(_dados, arquivo_json, ensure_ascii=False, indent=4)

        return (True, None)

    except Exception as e:
        return (False, e)

campos_msg = """SELECIONE OS CAMPOS QUE DESEJA VISUALIZAR:

=== DADOS PESSOAIS ===        === ENDEREÇO ===           === CONTATO / CONVÊNIO ===
1  - ID DO PACIENTE           9  - CEP                  15 - CELULAR
2  - NOME COMPLETO            10 - RUA                  16 - EMAIL
3  - DATA DE NASCIMENTO       11 - NÚMERO DO ENDEREÇO   17 - CONVÊNIO (S/N)
4  - SEXO                     12 - BAIRRO
5  - CPF                      13 - CIDADE
6  - RG                       14 - ESTADO
7  - ESTADO CIVIL
8  - BRASILEIRO (S/N)

=== CONSULTA MÉDICA ===        === CONTROLE DE REGISTRO ===
18 - DATA E HORA DA CONSULTA   22 - DATA DE CADASTRO
19 - TIPO DE CONSULTA          23 - DATA DA ÚLTIMA ATUALIZAÇÃO
20 - ESPECIALIDADE
21 - STATUS DA CONSULTA

- Digite os números dos campos separados por vírgula (por exemplo: 1,2,5,21,22,23)
- Para selecionar todos os campos, digite: A

DIGITE SUA ESCOLHA: """

campos_dict = {
    1: "ID_PACIENTE",       2: "NM_COMPLETO",       3: "DT_NASCIMENTO",
    4: "SEXO",              5: "CPF",               6: "RG",
    7: "ESTADO_CIVIL",      8: "BRASILEIRO",        9: "CEP",
    10: "RUA",              11: "NUMERO_ENDERECO",  12: "BAIRRO",
    13: "CIDADE",           14: "ESTADO",           15: "CELULAR",
    16: "EMAIL",            17: "CONVENIO",         18: "DT_HORA_CONSULTA",
    19: "TIPO_CONSULTA",    20: "ESPECIALIDADE",    21: "STATUS_CONSULTA",
    22: "DT_CADASTRO",      23: "DT_ULTIMA_ATUALIZACAO"
}

# ==========================================================
#   PROGRAMA PRINCIPAL
# ==========================================================

try:
    user = "rm561833"
    password = "070406"
    dsn = "oracle.fiap.com.br:1521/ORCL"
    ok, conn = conectar_oracledb(user, password, dsn)
    conectado = bool(conn)
except Exception as e:
    conectado = False

while conectado:
    limpar_terminal()
    exibir_titulo_centralizado("AXCESS TECH - SISTEMA DE GERENCIAMENTO DE PACIENTE", 60)
    print("1 - REGISTRAR PACIENTE")
    print("2 - CONSULTAR REGISTROS")
    print("3 - ATUALIZAR REGISTROS")
    print("4 - REMOVER REGISTRO")
    print("5 - LIMPAR TODOS OS REGISTROS")
    print("6 - EXPORTAÇÃO PARA JSON")
    print("0 - SAIR")
    print("")

    escolha_menu = obter_int_intervalado("Escolha: ", "Entrada inválida.", 0, 6)

    match escolha_menu:

        case 0:  # SAIR
            limpar_terminal()
            print("\nPrograma encerrado. Até logo!\n")
            conectado = False

        case 1:  # REGISTRAR PACIENTE
            limpar_terminal()
            exibir_titulo_centralizado("MENU REGISTRO PACIENTE", 60)
            sucesso_dados, dados_registro = solicitar_dados_paciente()

            if sucesso_dados:
                sucesso, erro = insert_paciente(conn, dados_registro)
                if sucesso:
                    limpar_terminal()
                    print("\nPaciente registrado com sucesso!")
                else:
                    limpar_terminal()
                    print("\nErro ao registrar paciente!")
                    print(erro)
            else:
                limpar_terminal()
                print("\nErro ao coletar os dados do paciente!")

            input("\nAperte ENTER para voltar ao menu principal...")

        case 2:  # CONSULTAR REGISTROS
            resultado = verifica_tabela(conn, "T_PACIENTE")
            if resultado:
                escolha_submenu = -1
                while escolha_submenu != 0:
                    limpar_terminal()
                    exibir_titulo_centralizado("MENU CONSULTA PACIENTE", 60)
                    print("DESEJA FAZER SUA CONSULTA POR:")
                    print("1 - TODOS OS PACIENTES")
                    print("2 - POR ID DO PACIENTE")
                    print("3 - PESQUISA DE TEXTO")
                    print("4 - PESQUISA NUMÉRICA")
                    print("0 - VOLTAR\n")

                    escolha_submenu = obter_int_intervalado("Escolha: ", "Entrada inválida.", 0, 5)

                    match escolha_submenu:
                        case 0:  # VOLTAR
                            break

                        case 1:  # TODOS OS PACIENTES
                            limpar_terminal()
                            exibir_titulo_centralizado("CONSULTA - TODOS OS PACIENTES", 60)
                            texto, lista = obter_multiplas_opcoes_dict(
                                campos_msg,
                                "Erro! Escolha os campos separando os números por ',' .",
                                campos_dict
                            )

                            sucesso, busca = select_paciente(conn, texto)
                            if sucesso:
                                sucesso, tabela = imprimir_resultado_tabulate_oracle(busca)
                                if sucesso:
                                    limpar_terminal()
                                    exibir_titulo_centralizado("CONSULTA - TODOS OS PACIENTES", 60)
                                    print(tabela)
                                else:
                                    limpar_terminal()
                                    print("\nErro ao formatar os resultados:")
                                    print(tabela)
                            else:
                                limpar_terminal()
                                print("\nErro ao consultar pacientes no banco de dados:")
                                print(busca)

                            deseja_exportar = obter_sim_nao(
                                "\nDeseja exportar essa consulta para um arquivo JSON? (S/N): ",
                                "Entrada inválida! Digite 'S' para Sim ou 'N' para Não."
                            )

                            if deseja_exportar:
                                nome_arquivo = input(
                                    "\nDigite o nome do arquivo (ex: pacientes.json): "
                                ).strip()

                                if not nome_arquivo:
                                    nome_arquivo = "pacientes.json"
                                elif not nome_arquivo.lower().endswith(".json"):
                                    nome_arquivo += ".json"

                                sucesso_export, erro_export = exportar_para_json(busca, nome_arquivo)
                                if sucesso_export:
                                    print(f"\nConsulta exportada com sucesso para '{nome_arquivo}'!")
                                else:
                                    print(f"\nErro ao exportar para JSON: {erro_export}")

                            input("\nAperte ENTER para voltar ao menu de consulta...")

                        case 2:  # POR ID DO PACIENTE
                            limpar_terminal()
                            exibir_titulo_centralizado("CONSULTA - PACIENTE POR ID", 60)

                            sucesso_select, resultados_preview = select_paciente(
                                conn, "ID_PACIENTE, NM_COMPLETO, TIPO_CONSULTA, STATUS_CONSULTA"
                            )

                            if sucesso_select:
                                sucesso_preview, tabela_preview = imprimir_resultado_tabulate_oracle(resultados_preview)
                            else:
                                sucesso_preview = False
                                tabela_preview = f"Erro ao consultar pacientes: {resultados_preview}"

                            if sucesso_preview:
                                resp = True
                                while resp:
                                    limpar_terminal()
                                    exibir_titulo_centralizado("CONSULTA - PACIENTE POR ID", 60)
                                    print(tabela_preview)

                                    resp = obter_sim_nao("Deseja pesquisar consulta por ID? (S/N): ", "Erro. Digite S ou N.")
                                    if resp:
                                        _id_paciente = obter_int("\nDigite o ID do paciente: ", "ID inválido. Digite um número inteiro.")
                                        
                                        limpar_terminal()
                                        exibir_titulo_centralizado("CONSULTA - PACIENTE POR ID", 60)
                                        
                                        texto, lista = obter_multiplas_opcoes_dict(
                                            campos_msg,
                                            "Erro! Escolha os campos separando os números por ',' .",
                                            campos_dict
                                        )
                                        
                                        try:
                                            sucesso_select_id, resultados = select_paciente_por_id(conn, texto, _id_paciente)

                                            if not resultados:
                                                limpar_terminal()
                                                print(f"\nNenhum paciente encontrado com ID {_id_paciente}.")
                                            else:
                                                sucesso, tabela = imprimir_resultado_tabulate_oracle(resultados)
                                                if sucesso:
                                                    limpar_terminal()
                                                    exibir_titulo_centralizado(f"PACIENTE - ID {_id_paciente}", 60)
                                                    print(tabela)

                                                    deseja_exportar = obter_sim_nao(
                                                        "\nDeseja exportar esta consulta para um arquivo JSON? (S/N): ",
                                                        "Entrada inválida! Digite 'S' para Sim ou 'N' para Não."
                                                    )

                                                    if deseja_exportar:
                                                        nome_arquivo = input(
                                                            "\nDigite o nome do arquivo (ex: paciente.json): "
                                                        ).strip()

                                                        if not nome_arquivo:
                                                            nome_arquivo = f"paciente_{_id_paciente}.json"
                                                        elif not nome_arquivo.lower().endswith(".json"):
                                                            nome_arquivo += ".json"

                                                        sucesso_export, erro_export = exportar_para_json(resultados, nome_arquivo)
                                                        if sucesso_export:
                                                            print(f"\nConsulta exportada com sucesso para '{nome_arquivo}'!")
                                                        else:
                                                            print(f"\nErro ao exportar para JSON: {erro_export}")

                                                else:
                                                    limpar_terminal()
                                                    print("\nErro ao formatar os resultados:")
                                                    print(tabela)

                                        except Exception as e:
                                            limpar_terminal()
                                            print("\nErro ao consultar paciente no banco de dados:")
                                            print(e)

                                        input("\nAperte ENTER para continuar...")
                                    else:
                                        break
                            else:
                                limpar_terminal()
                                print(f"\nNão foi possível exibir o preview dos pacientes.\n{tabela_preview}")
                                input("\nAperte ENTER para voltar ao menu principal...")

                        case 3:  # PESQUISA DE TEXTO
                            limpar_terminal()
                            exibir_titulo_centralizado("PESQUISA DE TEXTO - PACIENTES", 60)

                            sucesso_select, resultados_preview = select_paciente(
                                conn, "ID_PACIENTE, NM_COMPLETO, TIPO_CONSULTA, STATUS_CONSULTA"
                            )

                            if sucesso_select:
                                sucesso_preview, tabela_preview = imprimir_resultado_tabulate_oracle(resultados_preview)
                            else:
                                sucesso_preview = False
                                tabela_preview = f"Erro ao consultar pacientes: {resultados_preview}"

                            if sucesso_preview:
                                resp = True
                                while resp:
                                    limpar_terminal()
                                    exibir_titulo_centralizado("PESQUISA DE TEXTO - PACIENTES", 60)
                                    print(tabela_preview)

                                    resp = obter_sim_nao("Deseja pesquisar paciente por texto? (S/N): ", "Erro. Digite S ou N.")
                                    print("")
                                    if resp:
                                        campo_busca_dict = {
                                            1: "NM_COMPLETO",
                                            2: "ESTADO_CIVIL",
                                            3: "RUA",
                                            4: "BAIRRO",
                                            5: "CIDADE",
                                            6: "EMAIL",
                                            7: "TIPO_CONSULTA",
                                            8: "ESPECIALIDADE",
                                            9: "STATUS_CONSULTA"
                                        }

                                        campo_busca = obter_opcao_dict(
"""Escolha o campo para pesquisar por texto:
1 - Nome
2 - Estado Civil
3 - Rua
4 - Bairro
5 - Cidade
6 - E-mail
7 - Tipo de Consulta
8 - Especialidade
9 - Status da Consulta
Escolha: """,
                                            "Opção inválida!",
                                            campo_busca_dict
                                        )

                                        texto_pesquisa = obter_texto("\nDigite o texto a ser pesquisado: ", "Entrada inválida!")

                                        limpar_terminal()
                                        exibir_titulo_centralizado("PESQUISA DE TEXTO - PACIENTES", 60)
                                        texto_colunas, lista_colunas = obter_multiplas_opcoes_dict(
                                            campos_msg,
                                            "Erro! Escolha os campos separando os números por ',' .",
                                            campos_dict
                                        )

                                        resultados = buscar_paciente_por_texto(conn, campo_busca, texto_pesquisa, texto_colunas)

                                        if not resultados:
                                            limpar_terminal()
                                            print(f"\nNenhum paciente encontrado com '{texto_pesquisa}' no campo {campo_busca}.")
                                        else:
                                            sucesso, tabela = imprimir_resultado_tabulate_oracle(resultados)
                                            if sucesso:
                                                limpar_terminal()
                                                exibir_titulo_centralizado(f"RESULTADOS DA PESQUISA - {campo_busca}", 60)
                                                print(tabela)

                                                deseja_exportar = obter_sim_nao(
                                                    "\nDeseja exportar o resultado desta pesquisa para um arquivo JSON? (S/N): ",
                                                    "Entrada inválida! Digite 'S' para Sim ou 'N' para Não."
                                                )

                                                if deseja_exportar:
                                                    nome_arquivo = input(
                                                        "\nDigite o nome do arquivo (ex: pesquisa_pacientes.json): "
                                                    ).strip()

                                                    if not nome_arquivo:
                                                        nome_arquivo = f"pesquisa_{campo_busca.lower()}_{texto_pesquisa.lower().replace(' ', '_')}.json"
                                                    elif not nome_arquivo.lower().endswith(".json"):
                                                        nome_arquivo += ".json"

                                                    sucesso_export, erro_export = exportar_para_json(resultados, nome_arquivo)
                                                    if sucesso_export:
                                                        print(f"\nPesquisa exportada com sucesso para '{nome_arquivo}'!")
                                                    else:
                                                        print(f"\nErro ao exportar para JSON: {erro_export}")

                                            else:
                                                limpar_terminal()
                                                print("\nErro ao formatar os resultados:")
                                                print(tabela)

                                        input("\nAperte ENTER para continuar...")
                                    else:
                                        break
                            else:
                                limpar_terminal()
                                print(f"\nNão foi possível exibir o preview dos pacientes.\n{tabela_preview}")
                                input("\nAperte ENTER para voltar ao menu principal...")


                        case 4:  # PESQUISA NUMÉRICA
                            limpar_terminal()
                            exibir_titulo_centralizado("PESQUISA NUMÉRICA - PACIENTES", 60)

                            sucesso_select, resultados_preview = select_paciente(
                                conn, "ID_PACIENTE, NM_COMPLETO, TIPO_CONSULTA, STATUS_CONSULTA"
                            )

                            if sucesso_select:
                                sucesso_preview, tabela_preview = imprimir_resultado_tabulate_oracle(resultados_preview)
                            else:
                                sucesso_preview = False
                                tabela_preview = f"Erro ao consultar pacientes: {resultados_preview}"

                            if sucesso_preview:
                                resp = True
                                while resp:
                                    limpar_terminal()
                                    exibir_titulo_centralizado("PESQUISA NUMÉRICA - PACIENTES", 60)
                                    print(tabela_preview)

                                    resp = obter_sim_nao("Deseja pesquisar paciente por valor numérico? (S/N): ", "Erro. Digite S ou N.")
                                    if not resp:
                                        break

                                    campo_busca_dict = {
                                        1: "ID_PACIENTE",
                                        2: "NUMERO_ENDERECO"
                                    }

                                    print()
                                    campo_busca = obter_opcao_dict(
"""Escolha o campo numérico para pesquisar:
1 - ID_PACIENTE
2 - NUMERO_ENDERECO
Escolha: """,
                                        "Opção inválida!",
                                        campo_busca_dict
                                    )

                                    valor = obter_int("\nDigite o valor para pesquisa: ", "Entrada inválida. Digite um número inteiro.")

                                    print()
                                    operador = obter_opcao_dict(
                """Escolha o operador para pesquisa:
1 - Igual (=)
2 - Maior (>)
3 - Menor (<)
4 - Maior ou igual (>=)
5 - Menor ou igual (<=)
6 - Diferente (<>)
Escolha: """,
                                        "Opção inválida!",
                                        {1: "=", 2: ">", 3: "<", 4: ">=", 5: "<=", 6: "<>"}
                                    )

                                    limpar_terminal()
                                    exibir_titulo_centralizado("PESQUISA NUMÉRICA - PACIENTES", 60)
                                    texto_colunas, lista_colunas = obter_multiplas_opcoes_dict(
                                        campos_msg,
                                        "Erro! Escolha os campos separando os números por ',' .",
                                        campos_dict
                                    )

                                    try:
                                        resultados = buscar_paciente_por_numero(conn, campo_busca, operador, valor, texto_colunas)

                                        if not resultados:
                                            limpar_terminal()
                                            print(f"\nNenhum paciente encontrado com {campo_busca} {operador} {valor}.")
                                        else:
                                            sucesso, tabela = imprimir_resultado_tabulate_oracle(resultados)
                                            if sucesso:
                                                limpar_terminal()
                                                exibir_titulo_centralizado(f"RESULTADOS - {campo_busca} {operador} {valor}", 60)
                                                print(tabela)

                                                deseja_exportar = obter_sim_nao(
                                                    "\nDeseja exportar o resultado desta pesquisa para um arquivo JSON? (S/N): ",
                                                    "Entrada inválida! Digite 'S' para Sim ou 'N' para Não."
                                                )

                                                if deseja_exportar:
                                                    nome_arquivo = input(
                                                        "\nDigite o nome do arquivo (ex: pesquisa_numerica.json): "
                                                    ).strip()

                                                    if not nome_arquivo:
                                                        nome_arquivo = f"pesquisa_{campo_busca.lower()}_{valor}.json"
                                                    elif not nome_arquivo.lower().endswith(".json"):
                                                        nome_arquivo += ".json"

                                                    sucesso_export, erro_export = exportar_para_json(resultados, nome_arquivo)
                                                    if sucesso_export:
                                                        print(f"\nPesquisa exportada com sucesso para '{nome_arquivo}'!")
                                                    else:
                                                        print(f"\nErro ao exportar para JSON: {erro_export}")
                                            else:
                                                limpar_terminal()
                                                print("\nErro ao formatar os resultados:")
                                                print(tabela)

                                    except Exception as e:
                                        limpar_terminal()
                                        print("\nErro ao realizar a pesquisa numérica:")
                                        print(e)

                                    input("\nAperte ENTER para continuar...")

                            else:
                                limpar_terminal()
                                print(f"\nNão foi possível exibir o preview dos pacientes.\n{tabela_preview}")
                                input("\nAperte ENTER para voltar ao menu principal...")

        case 3: 
            sucesso_select, resultados_preview = select_paciente(
                conn, "ID_PACIENTE, NM_COMPLETO, TIPO_CONSULTA, STATUS_CONSULTA"
            )

            if sucesso_select:
                sucesso_preview, tabela_preview = imprimir_resultado_tabulate_oracle(resultados_preview)
            else:
                sucesso_preview = False
                tabela_preview = f"Erro ao consultar pacientes: {resultados_preview}"

            if sucesso_preview:
                resp = True
                while resp:
                    limpar_terminal()
                    exibir_titulo_centralizado("ATUALIZAR REGISTROS", 60)
                    print(tabela_preview)

                    resp = obter_sim_nao("Deseja atualizar algum paciente? (S/N): ", "Erro. Digite S ou N.")
                    if not resp:
                        break

                    _id_paciente = obter_int("\nDigite o ID do paciente que deseja atualizar: ", "ID inválido. Digite um número inteiro.")

                    sucesso, resultados = select_paciente_por_id(conn, "*", _id_paciente)
                    if not resultados:
                        limpar_terminal()
                        print(f"\nNenhum paciente encontrado com ID {_id_paciente}.")
                        input("\nAperte ENTER para voltar ao menu de atualização...")
                        continue

                    limpar_terminal()
                    exibir_titulo_centralizado(f"PACIENTE - ID {_id_paciente}", 60)
                    imprimir_resultado_vertical_oracle(resultados)

                    campos_dict = {
                        1: "NM_COMPLETO",
                        2: "DATA_NASCIMENTO",
                        3: "SEXO",
                        4: "CPF",
                        5: "RG",
                        6: "ESTADO_CIVIL",
                        7: "BRASILEIRO",
                        8: "ENDERECO",
                        9: "NUMERO_ENDERECO",
                        10: "CELULAR",
                        11: "EMAIL",
                        12: "CONVENIO",
                        13: "DATA_HORA_CONSULTA",
                        14: "TIPO_CONSULTA",
                        15: "ESPECIALIDADE",
                        16: "STATUS_CONSULTA"
                    }

                    print()

                    campo = obter_opcao_dict("""Escolha o campo que deseja atualizar:
1 - Nome
2 - Data de Nascimento
3 - Sexo
4 - CPF
5 - RG
6 - Estado Civil
7 - Brasileiro?
8 - Endereço
9 - Número do Endereço
10 - Celular
11 - E-mail
12 - Convênio
13 - Data/Hora Consulta
14 - Tipo de Consulta
15 - Especialidade
16 - Status da Consulta
Escolha: """,
                        "Opção inválida!",
                        campos_dict
                    )

                    sucesso_update, erro = atualizar_coluna_paciente(conn, _id_paciente, campo)

                    if sucesso_update:
                        limpar_terminal()
                        print(f"\nCampo '{campo}' atualizado com sucesso!")
                    else:
                        limpar_terminal()
                        print(f"\nErro ao atualizar o campo '{campo}': {erro}")

                    input("\nAperte ENTER para continuar...")
            else:
                limpar_terminal()
                print(f"\nNão foi possível exibir o preview dos pacientes.\n{tabela_preview}")
                input("\nAperte ENTER para voltar ao menu principal...")

        case 4:  # REMOVER REGISTRO
            limpar_terminal()
            exibir_titulo_centralizado("REMOVER REGISTRO", 60)

            sucesso_select, resultados_preview = select_paciente(
                conn, "ID_PACIENTE, NM_COMPLETO, TIPO_CONSULTA, STATUS_CONSULTA"
            )

            if sucesso_select:
                sucesso_preview, tabela_preview = imprimir_resultado_tabulate_oracle(resultados_preview)
            else:
                sucesso_preview = False
                tabela_preview = f"Erro ao consultar pacientes: {resultados_preview}"

            if sucesso_preview:
                resp = True
                while resp:
                    limpar_terminal()
                    exibir_titulo_centralizado("REMOVER REGISTRO", 60)
                    print(tabela_preview)

                    resp = obter_sim_nao("Deseja remover algum paciente por ID? (S/N): ", "Erro. Digite S ou N.")
                    if resp:
                        _id_paciente = obter_int("\nDigite o ID do paciente a ser removido: ", "ID inválido. Digite um número inteiro.")

                        confirmar = obter_sim_nao(f"\nTem certeza que deseja remover o paciente ID {_id_paciente}? (S/N): ", "Erro. Digite S ou N.")
                        if confirmar:
                            sucesso, erro = deletar_paciente(conn, _id_paciente)
                            if sucesso:
                                print(f"\nPaciente ID {_id_paciente} removido com sucesso!")
                            else:
                                print(f"\nErro ao remover paciente: {erro}")

                        input("\nAperte ENTER para continuar...")
                    else:
                        break
            else:
                limpar_terminal()
                print(f"\nNão foi possível exibir o preview dos pacientes.\n{tabela_preview}")
                input("\nAperte ENTER para voltar ao menu principal...")

        case 5:  # LIMPAR TODOS OS REGISTROS
            limpar_terminal()
            exibir_titulo_centralizado("LIMPAR TODOS OS REGISTROS", 60)

            confirmar = obter_sim_nao("Tem certeza que deseja apagar TODOS os registros de pacientes? (S/N): ", "Erro. Digite S ou N.")
            if confirmar:
                sucesso, erro = limpar_todos_pacientes(conn)
                if sucesso:
                    print("\nTodos os registros de pacientes foram apagados com sucesso!")
                else:
                    print(f"\nErro ao apagar registros: {erro}")
            else:
                print("\nOperação cancelada pelo usuário.")

            input("\nAperte ENTER para voltar ao menu principal...")
        case 6:  # EXPORTAÇÃO PARA JSON
            limpar_terminal()
            exibir_titulo_centralizado("EXPORTAÇÃO PARA JSON", 60)

            # Perguntar ao usuário o nome do arquivo (opcional)
            nome_arquivo = input("Digite o nome do arquivo para exportação (padrão: pacientes.json): ").strip()
            if not nome_arquivo:
                nome_arquivo = "pacientes.json"

            sucesso, erro = exportar_para_json(conn, nome_arquivo)

            if sucesso:
                print(f"\nExportação concluída com sucesso! Arquivo salvo como '{nome_arquivo}'.")
            else:
                print(f"\nErro ao exportar para JSON: {erro}")

            input("\nAperte ENTER para voltar ao menu principal...")
