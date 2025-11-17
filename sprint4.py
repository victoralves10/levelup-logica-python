# IMPORTS
import os
import oracledb
import pandas
from datetime import datetime,date
import json
import requests

# =============================================
#       FUNÇÕES E PROCEDIMENTOS
"""
Limpa a tela do terminal, dependendo do sistema operacional.

No Windows, usa o comando 'cls'.
Em sistemas Unix/Linux/Mac, usa o comando 'clear'.
"""
def limparTela():
    os.system('cls' if os.name =='nt' else "clear")

"""
    Exibe um título centralizado com linhas de destaque acima e abaixo.

    Args:
        titulo (str): Texto do título a ser exibido.
"""
def exibirTitulo(titulo:str)->None:
    print(f"{'='*40}\n{titulo:^40}\n{'='*40}")

"""
    Exibe mensagem indicando que o campo é opcional e pode ser pulado.
 """
def campoOpcional()->None:
    print("CAMPO OPCIONAL : Aperte [enter] para pular")

# ============================================
#       FUNÇÕES DE COLETA DE DADOS
#         ----  GERAIS ----
"""
    Coleta as credenciais de autenticação do usuário.

    Solicita ao usuário que digite um login e uma senha, realizando
    validações básicas (mínimo de 6 caracteres). Retorna um dicionário
    com os dados prontos para inserção na tabela de autenticação.

    Returns:
        dict: Dicionário contendo:
            - "login" (str): Login do usuário.
            - "senha" (str): Senha do usuário.
            - "st_login" (str): Status do login, definido como 'I' (inicial).
"""
def coletaAutenticacao()->dict:
    return {
            "login":obterLogin(),
            "senha":obterSenha(),
            "st_login": 'I'
        } 
"""
    Coleta os dados pessoais de um paciente, incluindo informações básicas e endereço.

    Solicita ao usuário o preenchimento de dados pessoais como nome, CPF, data de nascimento,
    sexo, RG, escolaridade, estado civil, grupo sanguíneo, altura e peso. 
    Também permite informar o CEP e consulta o endereço completo via API ViaCEP. 
    Campos opcionais podem ser deixados em branco.

    Args:
        FK_id_autentica (int): Chave estrangeira da tabela de autenticação do paciente.

    Returns:
        dict: Dicionário com os dados coletados, pronto para inserção no banco. Exemplo de chaves:
            - "id_autentica" (int)
            - "nm_paciente" (str)
            - "nr_cpf" (str)
            - "dt_nascimento" (datetime)
            - "fl_sexo" (str)
            - "nr_rg" (str | None)
            - "ds_escolaridade" (str | None)
            - "ds_estado_civil" (str | None)
            - "tip_grupo_sanguineo" (str | None)
            - "nr_altura" (float | None)
            - "nr_peso" (float | None)
            - "cep" (str | None)
            - "logradouro", "bairro", "cidade", "estado" (str | None)
"""
def coletaDadosPessoais(FK_id_autentica: int) -> dict:
    dados = {
        "id_autentica": FK_id_autentica,
        "nm_paciente": obterNome(),
        "nr_cpf": obterCPF(),
        "dt_nascimento": obterDataNascimento(),
        "fl_sexo": obterSexo(),
        "nr_rg": obterRG(),
        "ds_escolaridade": obterEscolaridade(),
        "ds_estado_civil": obterEstadoCivil(),
        "tip_grupo_sanguineo": obterGrupoSanguineo(),
        "nr_altura": obterAltura(),
        "nr_peso": obterPeso()
    }

    # CEP e endereço via API
    cep = obterCEP()
    dados["cep"] = cep
    if cep:
        endereco = consultar_via_cep(cep)
        if endereco:
            dados.update(endereco)
        else:
            dados.update({"logradouro": None, "bairro": None, "cidade": None, "estado": None})
    else:
        dados.update({"logradouro": None, "bairro": None, "cidade": None, "estado": None})

    return dados


#          ---- VALIDAÇÕES ESPECÍFICAS AO CAMPO ----

"""
    Solicita ao usuário uma resposta S/N e não retorna até que seja válida.

    Args:
        prompt (str): Mensagem exibida para o usuário.

    Retorna: 'S' ou 'N'
"""
def obter_resposta_sn(prompt: str) -> str:
    while True:
        resposta = input(prompt).strip().upper()
        if resposta == "":
            print("Resposta obrigatória. Digite 'S' para Sim ou 'N' para Não.")
            continue
        if resposta[0] in ('S', 'N'):
            return resposta[0]
        else:
            print("Resposta inválida! Digite apenas 'S' ou 'N'.")

"""
    Solicita ao usuário a entrada de um CEP (Código de Endereçamento Postal) brasileiro.

    O campo é opcional; se o usuário pressionar Enter sem digitar nada, retorna None.
    Valida que o CEP tenha exatamente 8 dígitos numéricos, removendo hífens se houver.

    Returns:
        str | None: 
            - CEP válido (8 dígitos) como string, ou
            - None caso o usuário não informe o CEP.
"""
def obterCEP() -> str | None:
    while True:
        cep = input("\tDigite o CEP (apenas números, opcional): ").strip().replace("-", "")
        if cep == "":
            return None  # Campo opcional
        if not cep.isdigit() or len(cep) != 8:
            print("ATENÇÃO || CEP inválido. Deve conter 8 números.")
            continue
        return cep
    
"""
    Consulta informações de endereço a partir de um CEP utilizando a API ViaCEP.

    A função realiza uma requisição HTTP para a API pública ViaCEP e, caso o CEP seja válido,
    retorna um dicionário contendo logradouro, bairro, cidade e estado.  
    Caso o CEP não exista, seja inválido ou ocorra erro na requisição, retorna None.

    Args:
        cep (str): CEP válido contendo 8 dígitos numéricos (sem traços ou espaços).

    Returns:
        dict | None:
            - Um dicionário com as chaves: "logradouro", "bairro", "cidade", "estado" caso a consulta seja bem-sucedida.
            - None caso o CEP seja inválido, inexistente ou haja falha na consulta.
"""    
def consultar_via_cep(cep: str) -> dict | None:
    try:
        response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        if response.status_code == 200:
            dados = response.json()
            if "erro" not in dados:
                return {
                    "logradouro": dados.get("logradouro"),
                    "bairro": dados.get("bairro"),
                    "cidade": dados.get("localidade"),
                    "estado": dados.get("uf")
                }
        return None
    except Exception as e:
        print(f"Erro ao consultar ViaCEP: {e}")
        return None    

"""
    Solicita e valida o login do usuário (mínimo 6 caracteres).

    Returns:
        str: Login válido
"""    
def obterLogin()->str:
    login=""

    while login=="" or len(login)<6:

        login = input(f"{"\tLogin:":<40}").strip()

        if login == "":
            print("ATENÇÃO || O campo Login é Obrigatório. ",end="\n")

            continue

        if len(login)<6:
            print("ATENÇÃO || Seu login deve ter ao menos 6 dígitos. ",end="\n")

            continue

    return login

"""
    Solicita e valida a senha do usuário (mínimo 6 caracteres).

    Returns:
        str: Senha válida
"""
def obterSenha()->str:
    senha = ""

    while senha=="" or len(senha)<6:
        senha = input(f"\t{"Senha:":<40}").strip()

        if senha=="":
            print("ATENÇÃO || O campo Senha é Obrigatório. ",end="\n")

            continue

        if len(senha)<6:
            print("ATENÇÃO || Sua senha deve ter ao menos 6 dígitos. ",end="\n")

            continue
    return senha

"""
    Solicita e valida o nome completo do paciente.

    Returns:
        str: Nome válido do paciente

    Example:
        nome = obterNome()
    """
def obterNome() -> str:
    nm_paciente = ""
    
    while nm_paciente == "" :
        nm_paciente = input(f"{"\tNome Completo:":<40}").strip()

        if nm_paciente == "":
            print("ATENÇÃO || O nome é obrigatório.")
            continue
            
    return nm_paciente

"""
    Solicita ao usuário a digitação de um CPF válido.

    O CPF deve conter exatamente 11 dígitos numéricos, sem pontos ou traços.
    A função continuará solicitando a entrada até que o valor informado seja válido.

    Returns:
        str: O CPF validado contendo exatamente 11 caracteres numéricos.
"""
def obterCPF() -> str:
    nr_cpf = ""
    
    while nr_cpf == "" or len(nr_cpf) != 11 or not nr_cpf.isdigit():
        nr_cpf = input(f"{"\tCPF (apenas números):":<40}").strip()
        
        if nr_cpf == "":
            print("ATENÇÃO || O CPF é obrigatório.")
            continue

        if not nr_cpf.isdigit():
            print("ATENÇÃO || O CPF deve conter apenas números.")
            continue

        if len(nr_cpf) != 11:
            print("ATENÇÃO || O CPF deve ter exatamente 11 dígitos.")
            continue

    return nr_cpf

"""
    Solicita ao usuário uma data de nascimento válida no formato DD/MM/AAAA.

    A função continua solicitando a entrada até que:
    - A data seja fornecida,
    - Esteja no formato correto (DD/MM/AAAA),
    - Não seja uma data futura ou inválida para idade (mínimo 1 ano de vida).

    Returns:
        datetime: Objeto datetime referente à data de nascimento informada.
 """
def obterDataNascimento() -> datetime:
    dt_nascimento = ""
    formato = "%d/%m/%Y"
    
    while True:
        dt_nascimento = input(f"{"\tData de Nascimento (DD/MM/AAAA):":<40}").strip()
        
        if dt_nascimento == "":
            print("ATENÇÃO || A data de nascimento é obrigatória.")
            continue

        try:
            data_nascimento = datetime.strptime(dt_nascimento, formato)
            
            if data_nascimento.year > datetime.now().year - 1:
                 print("ATENÇÃO || Data de nascimento inválida ou no futuro.")
                 continue

        except ValueError:
            print("ATENÇÃO || Formato incorreto. Use DD/MM/AAAA.")
            continue 

        return data_nascimento
    
"""
    Solicita ao usuário o sexo, aceitando apenas 'M' (Masculino) ou 'F' (Feminino).

    A função permanece solicitando a entrada até que o usuário informe
    uma das opções válidas, desconsiderando letras minúsculas.

    Returns:
        str: 'M' para Masculino ou 'F' para Feminino.
"""    
def obterSexo() -> str:
    fl_sexo = ""
    
    while fl_sexo not in ('M', 'F'):
        fl_sexo = input(f"{"\tSexo ('M' ou 'F'):":<40}").strip().upper()
        
        if fl_sexo not in ('M', 'F'):
            print("ATENÇÃO || Digite 'M' para Masculino ou 'F' para Feminino.")
            continue

    return fl_sexo

"""
    Solicita ao usuário a digitação do RG (Registro Geral).

    O campo é opcional. Caso o usuário pressione Enter sem digitar nada,
    a função retorna `None`. Caso seja informado um valor, ele deve conter
    exatamente 9 dígitos numéricos.

    Returns:
        str | None:
            - RG contendo 9 dígitos numéricos, ou
            - None caso o usuário opte por não informar o RG.
 """
def obterRG() -> str | None:

    while True:
        campoOpcional()
        nr_rg = input(f"{"\tDigite o seu RG (apenas os 9 números):":<40}").strip()
        if nr_rg=="":
            return None

        
        if not(nr_rg.isdigit()):
            print("ATENÇÃO || O RG deve conter apenas números.")
            continue

        if len(nr_rg)!= 9:
            print("ATENÇÃO || O RG deve conter 9 números.")

        return nr_rg   

"""
    Solicita ao usuário o nível de escolaridade.

    Exibe uma lista numerada de opções de escolaridade.  
    O campo é opcional — caso o usuário pressione Enter sem escolher uma opção, será retornado `None`.

    Returns:
        str | None:
            - Descrição textual do nível de escolaridade selecionado, ou
            - None caso o usuário não informe valor.
"""
def obterEscolaridade() -> str |None:
    opcoes_escolares = {
        "1": "Ensino Fundamental (Incompleto)",
        "2": "Ensino Fundamental (Completo)",
        "3": "Ensino Médio (Incompleto)",
        "4": "Ensino Médio (Completo)",
        "5": "Ensino Superior (Incompleto)",
        "6": "Ensino Superior (Completo)",
        "7": "Pós-Graduação (Completa)",
        "8": "Mestrado/Doutorado (Completo)"
    }
    
    print("\n" + "="*50)
    print("NÍVEIS DE ESCOLARIDADE:")
    for key, value in opcoes_escolares.items():
        print(f"[{key}] - {value}")
    print(f"[{'Enter'}] - Campo Opcional (Não Informado)")
    print("="*50 + "\n")
    
    while True:
        nivel_escolaridade = input(f"{"\tQual é o seu nível de Escolaridade (Opcional):":<40}").strip()

        if nivel_escolaridade =="":
            return None
        
        if nivel_escolaridade in opcoes_escolares.keys():
            return opcoes_escolares[nivel_escolaridade]
        else:
            print("ATENÇÃO || Código inválido. Digite o número correspondente (1 a 8) ou deixe vazio.")
            continue

        #return nivel_escolaridade

"""
    Solicita ao usuário o estado civil.

    Exibe uma lista numerada de opções de estado civil.  
    O campo é opcional — caso o usuário pressione Enter sem escolher uma opção, será retornado `None`.

    Returns:
        str | None:
            - Descrição textual do estado civil selecionado, ou
            - None caso o usuário não informe valor.
"""
def obterEstadoCivil() -> str | None:
    opcoes_civil = {
        "1": "Solteiro",
        "2": "Casado",
        "3": "Separado Judicialmente",
        "4": "Divorciado",
        "5": "Viúvo"
    }
    
    print("\n" + "="*50)
    print("ESTADO CIVIL (JURÍDICO):")
    for key, value in opcoes_civil.items():
        print(f"[{key}] - {value}")
    print(f"[{'Enter'}] - Campo Opcional (Não Informado)")
    print("="*50 + "\n")

    while True:
        estado_civil = input(f"{"\tSelecione o código de Estado Civil (Opcional):":<40}").strip()


        if estado_civil == "":
            return None
        
        if estado_civil in opcoes_civil:
             return opcoes_civil[estado_civil]
        else:
             print("ATENÇÃO || Código inválido. Digite o número correspondente (1 a 5) ou deixe vazio.")
             continue

"""
    Solicita ao usuário a entrada do grupo sanguíneo.

    O campo é opcional. Caso o usuário pressione Enter sem digitar nada,
    a função retorna `None`. Se informado, deve ser um dos grupos válidos:
    'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'.

    Returns:
        str | None:
            - Grupo sanguíneo válido (ex: 'O+', 'AB-'), ou
            - None caso o usuário não informe valor.
"""
def obterGrupoSanguineo() -> str | None: 
    grupos_validos = ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')
    
    while True:
        tip_grupo_sanguineo = input(f"{"\tGrupo Sanguíneo (Ex: O+ | Opcional):":<40}").strip().upper()
        
        if tip_grupo_sanguineo == "":
            return None
            
        if tip_grupo_sanguineo in grupos_validos:
            return tip_grupo_sanguineo
        else:
            print("ATENÇÃO || Grupo sanguíneo inválido. Digite um valor como 'A+', 'O-' ou deixe vazio.")
            continue 

"""
Solicita ao usuário a entrada da altura em metros.

    O campo é opcional. Caso o usuário pressione Enter sem digitar nada,
    a função retorna `None`. Caso informado, deve ser um número positivo
    (ex: 1.75). Valores inválidos ou negativos são rejeitados e solicitados novamente.

    Returns:
        float | None:
            - Altura em metros como número decimal, ou
            - None caso o usuário não informe valor.
"""
def obterAltura() -> float | None:
    while True:
        nr_altura_str = input(f"{"\tAltura em Metros (Ex: 1.75 | Opcional):":<40}").strip().replace(',','.')

        if nr_altura_str == "":
            return None
    
        try:
            nr_altura = float(nr_altura_str)

            if nr_altura<=0 :
                print("ATENÇÃO || Por favor, digite um valor positivo (Ex: 1,75).")
                continue
        except ValueError:
            print("ATENÇÃO || Por favor, digite um número válido (Ex: 1,75).")
            continue

        return nr_altura

"""
    Solicita ao usuário a entrada do peso em quilogramas.

    O campo é opcional. Caso o usuário pressione Enter sem digitar nada,
    a função retorna `None`. Caso informado, deve ser um número positivo
    (ex: 75.5). Valores inválidos ou negativos são rejeitados e solicitados novamente.

    Returns:
        float | None:
            - Peso em quilogramas como número decimal, ou
            - None caso o usuário não informe valor.
"""
def obterPeso() -> float | None:
    while True:
        nr_peso_str = input(f"{"\tPeso em Kg (Ex: 75.5 | Opcional):":<40}").strip().replace(',','.')
        
        if nr_peso_str == "":
            return None

        try:
            
            nr_peso = float(nr_peso_str)
            if nr_peso > 0:
                 return nr_peso
            else:
                 print("ATENÇÃO || Peso deve ser maior que zero.")
                 continue
                 
        except ValueError:
            print("ATENÇÃO || Por favor, digite um número válido (Ex: 75.5).")
            continue
            
# ============================================
#             INSERT

"""
    Cadastra um novo paciente no banco de dados Oracle.

    O processo inclui:
        1. Coleta de login e senha do paciente.
        2. Inserção na tabela de autenticação (T_WTS_AUTENTICA) e captura do ID retornado.
        3. Coleta de dados pessoais do paciente, incluindo:
            - Nome, CPF, data de nascimento, sexo
            - RG, escolaridade, estado civil, grupo sanguíneo
            - Altura, peso
            - CEP e endereço consultado via API (ViaCEP)
        4. Inserção na tabela de pacientes (T_WTS_PACIENTE).

    Parâmetros:
        conn (oracledb.Connection): Conexão aberta com o banco de dados Oracle.

    Retorna:
        tuple[bool, str]:
            - True e mensagem de sucesso se o paciente for cadastrado corretamente.
            - False e mensagem de erro em caso de falha de validação ou erro no banco de dados.
"""
def inserirPaciente(conn: oracledb.Connection) -> tuple[bool, str]:
    """
    Cadastra um novo paciente no banco de dados Oracle.

    Passos:
        1. Coleta login e senha do paciente.
        2. Insere na tabela T_WTS_AUTENTICA e captura o ID retornado.
        3. Coleta dados pessoais do paciente.
        4. Insere os dados na tabela T_WTS_PACIENTE.
    """
    inst_cadastro = gerarCursorBD(conn)

    try:
        # Coleta autenticação
        pac_auth = coletaAutenticacao()

        # Preparar variável para capturar o ID retornado
        id_autentica_retornado = inst_cadastro.var(int)

        # Inserir autenticação e capturar ID
        insert_auth_sql = """
            INSERT INTO T_WTS_AUTENTICA (login, senha, st_login)
            VALUES (:login, :senha, :st_login)
            RETURNING id_autentica INTO :id_retornado
        """
        inst_cadastro.execute(
            insert_auth_sql,
            {
                "login": pac_auth["login"],
                "senha": pac_auth["senha"],
                "st_login": pac_auth["st_login"],
                "id_retornado": id_autentica_retornado
            }
        )

        # Obter o ID retornado
        fk_id_autentica = id_autentica_retornado.getvalue()[0]

        # Coleta dados pessoais com o ID de autenticação
        pac_dadosPessoais = coletaDadosPessoais(fk_id_autentica)

        # Inserir dados pessoais na tabela T_WTS_PACIENTE
        insert_dadosPessoais_sql = """
            INSERT INTO T_WTS_PACIENTE (
                id_autentica, nm_paciente, nr_cpf, dt_nascimento, fl_sexo, 
                nr_rg, ds_escolaridade, ds_estado_civil, tip_grupo_sanguineo, nr_altura, nr_peso,
                cep, logradouro, bairro, cidade, estado
            )
            VALUES (
                :id_autentica, :nm_paciente, :nr_cpf, :dt_nascimento, :fl_sexo,
                :nr_rg, :ds_escolaridade, :ds_estado_civil, :tip_grupo_sanguineo, :nr_altura, :nr_peso,
                :cep, :logradouro, :bairro, :cidade, :estado
            )
        """
        inst_cadastro.execute(insert_dadosPessoais_sql, pac_dadosPessoais)

        # Commit da transação
        conn.commit()

    except ValueError:
        conn.rollback()
        return False, "Erro de Validação: Dados Inválidos."

    except Exception as e:
        conn.rollback()
        return False, f"Erro no Banco de Dados: {e}"

    else:
        return True, "Paciente cadastrado com sucesso!"



# ============================================
#             SELECT

"""
    Realiza a consulta de todos os pacientes cadastrados na tabela T_WTS_PACIENTE.

    Exibe os resultados em um DataFrame no terminal e oferece a opção de
    exportar os dados para um arquivo JSON.

    Parâmetros:
        conn (oracledb.Connection): Conexão ativa com o banco de dados Oracle.

    Retorna:
        None. Os resultados são exibidos no terminal e podem ser exportados para JSON.

    Comportamento:
        1. Executa SELECT * FROM T_WTS_PACIENTE.
        2. Se houver registros:
            - Limpa a tela e exibe título.
            - Constrói um DataFrame com os registros e o exibe.
            - Pergunta se deseja gerar um arquivo JSON.
        3. Se não houver registros:
            - Exibe mensagem informando que não há pacientes cadastrados.
        4. Trata erros de banco de dados e exceções inesperadas.
"""
def consultarPacientes_Geral(conn: oracledb.Connection) -> None:
    inst_consulta = gerarCursorBD(conn)
    select_sql = """SELECT * FROM T_WTS_PACIENTE"""

    try:
        inst_consulta.execute(select_sql)
        pacs = inst_consulta.fetchall()

        if pacs:
            limparTela()
            exibirTitulo("RESULTADO DA CONSULTA GERAL")
            df_completo = gerarDataframe(pacs)
            exibirDataframe(df_completo)
        else:
            print("\nNão há pacientes cadastrados na base de dados.")
            return

        resposta = obter_resposta_sn("Você gostaria de gerar um arquivo JSON? (S/N): ")
        if resposta == "S":
            nome_arquivo = input("Digite o nome do arquivo JSON (sem extensão, ENTER para padrão 'pacientes'): ").strip()
            if nome_arquivo == "":
                nome_arquivo = "pacientes"
            sucesso, msg = exportar_para_json(conn, f"{nome_arquivo}.json")
            if sucesso:
                print(f"Arquivo JSON gerado com sucesso: {nome_arquivo}.json")
            else:
                print(f"Falha ao gerar JSON: {msg}")
            
    except oracledb.DatabaseError as dbe:
        error, = dbe.args
        print(f"\nERRO no Banco de Dados durante a consulta (ORA-{error.code}): {error.message}")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado durante a consulta: {e}")
    finally:
        inst_consulta.close()

"""
    Realiza a consulta de pacientes com base em um campo específico: ID, Nome ou CPF.

    Exibe os resultados em um DataFrame no terminal e oferece a opção de
    exportar os dados filtrados para um arquivo JSON.

    Parâmetros:
        conn (oracledb.Connection): Conexão ativa com o banco de dados Oracle.

    Retorna:
        None. Os resultados são exibidos no terminal e podem ser exportados para JSON.

    Comportamento:
        1. Pergunta ao usuário qual campo será usado para a pesquisa:
            - ID do paciente
            - Nome completo
            - CPF
        2. Solicita o valor correspondente ao campo escolhido.
        3. Executa a query filtrada na tabela T_WTS_PACIENTE.
        4. Se houver registros:
            - Exibe os resultados em um DataFrame.
            - Constrói uma lista de dicionários com os registros para exportação JSON.
            - Pergunta se deseja gerar arquivo JSON.
        5. Se não houver registros:
            - Exibe mensagem informando que o paciente não foi encontrado.
        6. Trata exceções inesperadas.
"""
def consultarPacientes_Personalizado(conn: oracledb.Connection) -> None:
    inst_consulta = gerarCursorBD(conn)
    
    print("\nBuscar Paciente por:")
    print("[1] ID")
    print("[2] Nome")
    print("[3] CPF")
    
    escolha = input("Escolha: ").strip()
    campo = ""
    
    if escolha == "1":
        campo = "id_paciente"
    elif escolha == "2":
        campo = "nm_paciente"
    elif escolha == "3":
        campo = "nr_cpf"
    else:
        print("Opção inválida.")
        return

    valor = input(f"Digite o valor de {campo}: ").strip()
    sql = f"SELECT * FROM T_WTS_PACIENTE WHERE {campo} = :val"
    
    try:
        inst_consulta.execute(sql, {"val": valor})
        pacs = inst_consulta.fetchall()

        if pacs:
            colunas_ordem = ['id_paciente', 'nm_paciente','nr_cpf','nr_rg','dt_nascimento','fl_sexo',
                             'ds_escolaridade','ds_estado_civil','tip_grupo_sanguineo',
                             'nr_altura','nr_peso','id_autentica','cep','logradouro','bairro','cidade','estado']

            df = pandas.DataFrame(pacs, columns=colunas_ordem)
            exibirDataframe(df)

            registros_json = df.to_dict(orient="records")

            # Converter datas para string legível
            for registro in registros_json:
                for chave in ['dt_nascimento']:
                    if chave in registro and isinstance(registro[chave], (datetime, date)):
                        registro[chave] = registro[chave].strftime("%d/%m/%Y")

            resposta = obter_resposta_sn("\nDeseja gerar um arquivo JSON desta pesquisa? (S/N): ")
            if resposta == 'S':
                nome_arquivo = input("Digite o nome do arquivo JSON (sem extensão, ENTER para padrão 'pacientes'): ").strip()
                if nome_arquivo == "":
                    nome_arquivo = "pacientes"

                sucesso, msg = exportar_para_json_personalizado(registros_json, f"{nome_arquivo}.json")
                if sucesso:
                    print(f"Arquivo JSON gerado com sucesso: {nome_arquivo}.json")
                else:
                    print(f"Falha ao gerar JSON: {msg}")

        else:
            print("\nPaciente não encontrado.")

    except Exception as e:
        print(f"\nOcorreu um erro na consulta: {e}")
    finally:
        inst_consulta.close()

  
"""
    Retorna um mapeamento dos códigos numéricos para os nomes de colunas
    da tabela T_WTS_PACIENTE, utilizado para seleção ou atualização de campos.

    Retorna:
        dict: Dicionário com chave como código (str) e valor como nome da coluna (str).

"""        
def colunas_T_WTS_Paciente()->dict:
    return {
    "1": "nm_paciente", 
    "2": "nr_cpf",
    "3": "nr_rg",
    "4": "dt_nascimento",
    "5": "fl_sexo",            
    "6": "nr_altura",         
    "7": "nr_peso",           
    "8": "ds_escolaridade",    
    "9": "ds_estado_civil",    
    "10": "tip_grupo_sanguineo", 
    "11": "id_autentica",     
    }

"""
    Exibe de forma organizada os campos de uma tabela ou dicionário de colunas.

    Args:
        tabela (dict): Dicionário onde a chave é o código do campo (str) 
                       e o valor é o nome da coluna (str).

    Retorna:
        None. Imprime os campos no terminal formatados.

"""
def exibirColunas(tabela:dict)->None:
    colunas = tabela.items()
    print("---------- CAMPOS ----------")
    for i, col in colunas:
        print(f"\t[{i}] - {col:>20}")

#      ------- DATAFRAME's -------

"""
    Constrói um DataFrame do Pandas a partir de uma lista de registros.

    Args:
        dados_DataFrame (list): Lista de tuplas ou listas representando os registros.
        colunasPersonalizadas (list, opcional): Lista de nomes de colunas a serem usadas.
            Se None, será utilizado o conjunto padrão de colunas.

    Returns:
        pandas.DataFrame: DataFrame contendo os registros, indexado por 'id_paciente'.

"""
def gerarDataframe(dados_DataFrame:list, colunasPersonalizadas:list = None) ->pandas.DataFrame:

    colunas_padrao = [
        'id_paciente', 'id_autentica', 'nm_paciente', 'nr_cpf', 'nr_rg', 
        'dt_nascimento', 'fl_sexo', 'nr_altura', 'nr_peso', 
        'ds_escolaridade', 'ds_estado_civil', 'tip_grupo_sanguineo', 
        'cep', 'logradouro', 'bairro', 'cidade', 'estado'
    ]

    if colunasPersonalizadas == None:
        return pandas.DataFrame.from_records(dados_DataFrame, columns=['id_paciente',"nm_Paciente","nr_cpf","nr_rg","dt_nascimento","fl_sexo","ds_escolaridade","ds_estado_civil","tip_grupo_sanguineo","nr_altura","nr_peso","id_autentica", 'cep', 'logradouro', 'bairro', 'cidade', 'estado'], index='id_paciente')
    else:
        return pandas.DataFrame.from_records(dados_DataFrame, columns=colunasPersonalizadas, index='id_paciente')

"""
    Exibe um DataFrame do Pandas no terminal, limpando a tela antes da exibição.

    Args:
        dataFrame (pandas.DataFrame): DataFrame a ser exibido.

    Retorna:
        None. Imprime o DataFrame no terminal.
"""
def exibirDataframe(dataFrame :pandas.DataFrame)->None:
    limparTela()
    print(dataFrame)

#      ------- JSON -------

"""
    Consulta todos os registros da tabela T_WTS_PACIENTE e retorna como lista de dicionários.

    Args:
        _conexao (oracledb.Connection): Conexão aberta com o banco de dados Oracle.
        _campos (str): String contendo os campos desejados para SELECT (ex: "id_paciente, nm_paciente").

    Returns:
        tuple[bool, any]: 
            - True e lista de dicionários representando os pacientes, se sucesso.
            - False e objeto Exception ou mensagem de erro, em caso de falha.

"""
def select_pacientes(_conexao: oracledb.Connection, _campos: str) -> tuple[bool, any]:
    """
    Retorna registros da tabela T_PACIENTE como lista de dicionários.
    Recebe uma string com os campos para SELECT (ex: id_paciente, nm_completo).
    """
    try:
        query = f"SELECT * FROM T_WTS_PACIENTE"

        with _conexao.cursor() as cur:
            cur.execute(query)

            colunas_cursor = []
            for c in cur.description:
                colunas_cursor.append(c[0].lower())

            resultados = cur.fetchall()
            df = pandas.DataFrame(resultados, columns=colunas_cursor)

            for coluna in ['dt_nascimento']:
                if coluna in df.columns:
                    df[coluna] = df[coluna].apply(lambda x: x.strftime("%d/%m/%Y") if isinstance(x, (datetime, date)) else None)


        return True, df.to_dict(orient="records")

    except Exception as e:
        return False, e

"""
    Exporta uma lista de registros para um arquivo JSON.

    Args:
        lista_registros (list[dict]): Lista de dicionários representando registros de pacientes.
        _nome_arquivo (str, opcional): Nome do arquivo JSON a ser gerado. Padrão é 'pacientes.json'.

    Returns:
        tuple[bool, any]: 
            - True, None: se a exportação foi realizada com sucesso.
            - False, mensagem/exception: se ocorreu algum erro ou se a lista estiver vazia.

    Detalhes:
        - Datas do tipo datetime ou date são formatadas automaticamente para strings legíveis.
        - O JSON é salvo com indentação de 4 espaços e codificação UTF-8.

"""
def exportar_para_json_personalizado(lista_registros: list[dict], _nome_arquivo: str = "pacientes.json") -> tuple[bool, any]:
    """
    Exporta uma lista de registros (resultado de pesquisa) para JSON.
    """
    try:
        if not lista_registros:
            return False, "Nenhum registro para exportar."
        
        # Formatar datas
        for registro in lista_registros:
            for chave, valor in registro.items():
                if isinstance(valor, datetime):
                    registro[chave] = valor.strftime("%d/%m/%Y %H:%M")
                elif isinstance(valor, date):
                    registro[chave] = valor.strftime("%d/%m/%Y")
        
        with open(_nome_arquivo, "w", encoding="utf-8") as arquivo_json:
            json.dump(lista_registros, arquivo_json, ensure_ascii=False, indent=4)
        
        return True, None

    except Exception as e:
        return False, e

"""
    Exporta todos os pacientes da tabela T_WTS_PACIENTE para um arquivo JSON.
    
    Parâmetros:
        _conexao: Conexão aberta com o banco de dados Oracle.
        _nome_arquivo: Nome do arquivo JSON a ser criado (com extensão .json).

    Retorna:
        (True, None) se o arquivo foi gerado com sucesso.
        (False, mensagem ou exceção) em caso de erro ou se não houver registros.
"""
def exportar_para_json(_conexao: oracledb.Connection, _nome_arquivo: str = "pacientes.json") -> tuple[bool, any]:
    
    try:
        cols = colunas_T_WTS_Paciente().values()
        campos = ', '.join(cols)

        sucesso, lista_pacientes = select_pacientes(_conexao, campos)
        if not sucesso:
            return False, lista_pacientes
        if not lista_pacientes:
            return False, "Nenhum paciente encontrado para exportar."

        for paciente in lista_pacientes:
            for chave, valor in paciente.items():
                if isinstance(valor, datetime):
                    paciente[chave] = valor.strftime("%d/%m/%Y %H:%M")
                elif isinstance(valor, date):
                    paciente[chave] = valor.strftime("%d/%m/%Y")


        with open(_nome_arquivo, "w", encoding="utf-8") as arquivo_json:
            json.dump(lista_pacientes, arquivo_json, ensure_ascii=False, indent=4)

        return True, None 

    except Exception as e:
        return False, e 

# =======================================================
#           UPDATE

"""
    Retorna um mapeamento entre os nomes dos campos da tabela T_WTS_PACIENTE
    e suas respectivas funções de coleta/validação de dados.

    Args:
        campo (str): Nome do campo da tabela (não utilizado diretamente na função,
                     mas mantém compatibilidade com chamada futura).

    Returns:
        dict: Um dicionário onde a chave é o nome do campo e o valor é a função
              que coleta e valida o dado correspondente.
"""
def MapearAcaoComCampoDigitado(campo:str)->dict:
    return {
        "nm_paciente": obterNome,
        "nr_cpf": obterCPF,
        "nr_rg": obterRG,
        "dt_nascimento": obterDataNascimento,
        "fl_sexo": obterSexo,
        "nr_altura": obterAltura,
        "nr_peso": obterPeso,
        "ds_escolaridade": obterEscolaridade,
        "ds_estado_civil": obterEstadoCivil,
        "tip_grupo_sanguineo": obterGrupoSanguineo
    }

"""
    Retorna um dicionário com as colunas utilizadas como identificadores únicos
    na tabela T_WTS_PACIENTE.

    Returns:
        dict: Um dicionário onde a chave é um número (string) usado para seleção
              pelo usuário e o valor é o nome do campo correspondente na tabela.

"""
def colunasIdentificacao_T_WTS_Paciente()->dict:
    return {
    "1":"id_paciente",
    "2": "nr_cpf",
    "3": "nr_rg"
    }

"""
    Permite ao usuário escolher qual campo será usado como identificador único
    para localizar ou manipular registros de pacientes.

    Usa a função `colunasIdentificacao_T_WTS_Paciente` para exibir os campos
    disponíveis e valida a entrada do usuário.

    Returns:
        str: Nome do campo escolhido pelo usuário (ex: "id_paciente", "nr_cpf", "nr_rg").

"""
def escolherCampoIdentificacao()->str:
    colunas = colunasIdentificacao_T_WTS_Paciente()
    while True:
        exibirColunas(colunas)
        identificador= input("Digite o n° correspondente ao campo único:")
        if identificador not in colunas.keys():
            print("Digite um valor válido")
            continue
        break
    return(colunas[identificador])

"""
    Permite ao usuário escolher qual campo do paciente será atualizado.
    Exibe os campos disponíveis, exceto os IDs que não podem ser alterados.

    Returns:
        str: Nome do campo escolhido para atualização.
"""
def escolherCampoAtualizado()->str:
    colunas_update = colunas_T_WTS_Paciente() 
    
    while True:
        limparTela()
        
        exibirColunas(colunas_update)
        
        campo = input("Digite o n° correspondente ao campo que será atualizado: ").strip()

        if campo == "1" or campo =="11":
            print("ID não podem ser alterados")
            continue
        
        if campo not in colunas_update.keys():
            print("\nATENÇÃO || Digite um código de campo válido.")
            input("Pressione Enter para tentar novamente...")
            continue
            
        return colunas_update[campo]

"""
    Retorna o nome do campo da tabela T_WTS_PACIENTE correspondente ao código fornecido.

    Args:
        campo (str): Código do campo a ser atualizado (como chave do dicionário de colunas).

    Returns:
        str: Nome do campo correspondente no banco de dados.
"""
def escolherValorAtualizado(campo:str)->str:
    colunas = colunas_T_WTS_Paciente()
    return (colunas[campo])

"""
Atualiza um campo específico de um paciente na tabela T_WTS_PACIENTE.

O usuário escolhe:
    1. Campo de identificação do paciente (ID, CPF ou RG)
    2. Campo a ser atualizado
    3. Novo valor para o campo (com validação apropriada)

Exibe mensagens claras de sucesso ou alerta quando não há alteração.
"""
def atualizarDados(conn: oracledb.Connection) -> str:
    inst_atualizar = gerarCursorBD(conn) 

    campoIdentificador = escolherCampoIdentificacao()
    campoAtualizado = escolherCampoAtualizado()
    
    valorID = input(f"Digite o valor atual de {campoIdentificador} para identificar o paciente: ").strip()
    
    mapeamento = MapearAcaoComCampoDigitado(campoAtualizado)
    if campoAtualizado not in mapeamento.keys():
        mensagem = f"\nERRO LÓGICO: Nenhuma função de coleta/validação encontrada para '{campoAtualizado}'."
        print(mensagem)
        return mensagem
    
    funcao_coleta = mapeamento[campoAtualizado]

    try:
        inst_atualizar.execute(
            f"SELECT {campoAtualizado} FROM T_WTS_PACIENTE WHERE {campoIdentificador} = :id_valor",
            {'id_valor': valorID}
        )
        resultado = inst_atualizar.fetchone()
        if not resultado:
            mensagem = f"\n⚠️ Paciente com {campoIdentificador} = '{valorID}' não encontrado."
            print(mensagem)
            return mensagem
        valorAtual = resultado[0]
    except Exception as e:
        mensagem = f"\nErro ao buscar valor atual: {e}"
        print(mensagem)
        return mensagem

    print(f"\nCampo selecionado: {campoAtualizado}")
    print(f"Valor atual: {valorAtual}")
    valorNovo = funcao_coleta()
    
    if valorNovo == valorAtual:
        mensagem = "\nO valor informado é igual ao valor atual. Nenhuma alteração feita."
        print(mensagem)
        return mensagem
    
    sql = f"""
        UPDATE T_WTS_PACIENTE
        SET {campoAtualizado} = :novo_valor
        WHERE {campoIdentificador} = :id_valor
    """
    try:
        inst_atualizar.execute(sql, {
            'novo_valor': valorNovo,
            'id_valor': valorID
        })
        conn.commit()
        mensagem = f"\nSucesso! {inst_atualizar.rowcount} registro(s) atualizado(s) com sucesso."
        print(mensagem)
        return mensagem
    except oracledb.DatabaseError as dbe:
        conn.rollback()
        error, = dbe.args
        mensagem = f"\nERRO no Banco de Dados (ORA-{error.code}): {error.message}"
        print(mensagem)
        return mensagem
    except Exception as e:
        conn.rollback()
        mensagem = f"\nOcorreu um erro inesperado: {e}"
        print(mensagem)
        return mensagem
    finally:
        inst_atualizar.close()


# =======================================================
#               DELETAR

"""
    Localiza o ID_AUTENTICA de um paciente na tabela T_WTS_PACIENTE.

    Args:
        inst_cursor (oracledb.Cursor): Cursor do Oracle já criado.
        campo_id (str): Nome do campo identificador (ex: 'nr_cpf', 'id_paciente').
        valor_id (str): Valor do campo identificador a ser buscado.

    Returns:
        int | None: Retorna o ID_AUTENTICA se encontrado, ou None se não existir ou ocorrer erro.
"""
def obterIdAutentica(inst_cursor: oracledb.Cursor, campo_id: str, valor_id: str) -> int | None:
    """
    Passo 1: Encontra o ID_AUTENTICA do paciente na T_WTS_PACIENTE.
    Recebe o cursor, o campo identificador ('nr_cpf', 'id_paciente', etc.) e o valor.
    Retorna o ID_AUTENTICA (int) ou None em caso de falha/não encontrado.
    """
    sql_select_autentica = f"""
        SELECT ID_AUTENTICA 
        FROM T_WTS_PACIENTE 
        WHERE {campo_id} = :id_valor
    """
    
    try:
        inst_cursor.execute(sql_select_autentica, {"id_valor": valor_id})
        resultado = inst_cursor.fetchone()
        
        if resultado:
            return resultado[0] 
            
        return None 
            
    except oracledb.DatabaseError as dbe:
        error, = dbe.args
        print(f"\nERRO durante a busca do ID_AUTENTICA (ORA-{error.code}): {error.message}")
        return None
    except Exception as e:
        print(f"\nErro inesperado ao buscar ID_AUTENTICA: {e}")
        return None

"""
    Remove um paciente da tabela T_WTS_PACIENTE e seu login da T_WTS_AUTENTICA.
    Solicita confirmação do usuário antes de executar a exclusão.
"""
def removerPaciente(con: oracledb.Connection) -> None:
    inst_remocao = gerarCursorBD(con)
    
    limparTela()
    exibirTitulo("EXCLUSÃO DE CADASTRO")

    campoIdentificador = escolherCampoIdentificacao()
    
    while True:
        valorIdentificador = input(f"Digite o valor de {campoIdentificador} do paciente que deseja DELETAR: ").strip()
        if not valorIdentificador:
            print("\nOperação cancelada. O valor identificador não pode ser vazio.")
            continue 
        break
        
    id_autentica_paciente = obterIdAutentica(inst_remocao, campoIdentificador, valorIdentificador)
    
    if id_autentica_paciente is None:
        print(f"\nPaciente com {campoIdentificador} '{valorIdentificador}' não encontrado ou erro na busca. Nenhuma exclusão realizada.")
        inst_remocao.close()
        return None

    while True:
        confirmacao = input(f"\nATENÇÃO! Confirma a EXCLUSÃO IRREVERSÍVEL do paciente e seu login com {campoIdentificador}={valorIdentificador}? (S/N): ").strip().upper()
        if confirmacao == "":
            print("Resposta inválida. Digite 'S' para Sim ou 'N' para Não.")
            continue
        if confirmacao[0] == 'S':
            break
        elif confirmacao[0] == 'N':
            print("\nExclusão cancelada pelo usuário.")
            inst_remocao.close()
            return None
        else:
            print("Resposta inválida. Digite 'S' para Sim ou 'N' para Não.")
            continue
            
    sql_delete_paciente = f"""DELETE FROM T_WTS_PACIENTE WHERE {campoIdentificador} = :id_valor"""
    sql_delete_autentica = """DELETE FROM T_WTS_AUTENTICA WHERE ID_AUTENTICA = :id_autentica_valor"""
    
    try:
        inst_remocao.execute(sql_delete_paciente, {"id_valor": valorIdentificador})
        paciente_deletado = inst_remocao.rowcount > 0
        
        inst_remocao.execute(sql_delete_autentica, {"id_autentica_valor": id_autentica_paciente})
        autentica_deletada = inst_remocao.rowcount > 0
        
        if paciente_deletado and autentica_deletada:
            con.commit()
            print(f"\nSucesso! Paciente e registro de autenticação ({id_autentica_paciente}) deletados com sucesso.")
        else:
            con.rollback()
            print("\nFalha nas exclusões. Transação desfeita para evitar dados parciais.")
            
    except oracledb.DatabaseError as dbe:
        con.rollback()
        error, = dbe.args
        print(f"\nERRO no Banco de Dados durante a deleção (ORA-{error.code}): {error.message}")
    except Exception as e:
        con.rollback()
        print(f"\nOcorreu um erro inesperado durante a deleção: {e}")
    finally:
        inst_remocao.close()


# =======================================================
#       FUNÇÃO RELACIONADAS À BANCO DE DADOS

"""
    Conecta ao banco Oracle com credenciais fornecidas.
    Retorna o objeto de conexão ou None em caso de falha.
"""
def conectarBD()-> oracledb.Connection | None:
    conn = None 

    try :
        conn = oracledb.connect(user = "rm565698",password = "200591",dsn = "oracle.fiap.com.br:1521/ORCL")
        print("Conexão concluída com sucesso ...")
        return conn
    except oracledb.DatabaseError as dbe:
            
        error, = dbe.args
        print(f" ERRO no Banco de Dados (ORA-{error.code}): {error.message}")
        return None
            
    except Exception as e:
        print(e)
        return None  
    
"""
    Gera e retorna um cursor Oracle a partir da conexão fornecida.
"""    
def gerarCursorBD(con)->oracledb.Cursor:
    return con.cursor()
#==================================

con = conectarBD()

while con!=None:
        limparTela()
        exibirTitulo("SISTEMA DE GESTÃO DE PACIENTES")
        print("[1] Cadastrar Novo Paciente")
        print("[2] Consultar Paciente ")
        print("[3] Atualizar Dados")
        print("[4] Remover Paciente")
        print("[5] Sair do Programa")
        
        escolha = input("\nEscolha uma opção: ").strip()


        match escolha:
            case '1':
                sucesso, mensagem = inserirPaciente(con)
                limparTela()
                exibirTitulo("STATUS DO CADASTRO")
                print(mensagem)
                input("\nPressione Enter para continuar...")

            case '2':
                consultarPacientes_Geral(con)

                opt = obter_resposta_sn("\nGostaria de realizar uma pesquisa personalizada? [S/N]: ")
                if opt == 'S':
                    consultarPacientes_Personalizado(con)

            case '3':
                
                atualizarDados(con)
            case '4':
                
                removerPaciente(con)
            case '5':
                con.close()
                print("\nSaindo do programa...")
                break
                
            case _:
                print("\nOpção inválida ou não implementada. Tente novamente.")
                input("\nPressione Enter para continuar...")
        input("\nPressione Enter para continuar...")
