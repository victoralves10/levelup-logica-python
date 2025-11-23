-- ##################################################################
-- # 3. SCRIPT DE INSERÇÃO (DML)
-- ##################################################################

-- 1. T_ENDERECO (40 REGISTROS EXCLUSIVOS, conforme a regra de negócio)
-- Endereços 1 a 10: Para T_PESSOA
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('01000-001', 'BRA', 'SP', 'São Paulo', 'Bela Vista', 'Rua A', 10, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('02123-457', 'BRA', 'RJ', 'Rio de Janeiro', 'Leme', 'Rua B', 20, 'Apt 2B');
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('03456-790', 'BRA', 'MG', 'Belo Horizonte', 'Lourdes', 'Rua C', 30, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('04567-891', 'BRA', 'PR', 'Curitiba', 'Centro Cívico', 'Rua D', 40, 'Sala 4');
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('05678-902', 'BRA', 'RS', 'Porto Alegre', 'Petrópolis', 'Rua E', 50, 'Casa');
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('06789-013', 'BRA', 'BA', 'Salvador', 'Rio Vermelho', 'Rua F', 60, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('07890-124', 'BRA', 'CE', 'Fortaleza', 'Aldeota', 'Rua G', 70, 'Apt 7C');
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('08901-235', 'BRA', 'DF', 'Brasília', 'Asa Norte', 'Rua H', 80, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('09012-346', 'BRA', 'AM', 'Manaus', 'Adrianópolis', 'Rua I', 90, 'Loja 9');
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('10123-457', 'BRA', 'PE', 'Recife', 'Pina', 'Rua J', 100, NULL);
-- Endereços 11 a 20: Para T_EMPRESA
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('11000-001', 'BRA', 'SP', 'São Paulo', 'Faria Lima', 'Av. Tech', 110, 'Torre A');
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('12123-457', 'BRA', 'RJ', 'Rio de Janeiro', 'Botafogo', 'Rua Empresarial', 120, 'Sala 12');
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('13456-790', 'BRA', 'MG', 'Contagem', 'Industrial', 'Av. Prod', 130, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('14567-891', 'BRA', 'PR', 'Londrina', 'Comercial', 'Rua Com', 140, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('15678-902', 'BRA', 'RS', 'Caxias', 'Logístico', 'Rua Log', 150, 'Galpão 5');
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('16789-013', 'BRA', 'BA', 'Lauro de Freitas', 'Centro', 'Rua do Sol', 160, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('17890-124', 'BRA', 'CE', 'Caucaia', 'Polo', 'Rua das Indústrias', 170, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('18901-235', 'BRA', 'DF', 'Taguatinga', 'Comercial', 'Rua do Escritório', 180, 'Sala 18');
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('19012-346', 'BRA', 'AM', 'Tefé', 'Central', 'Rua do Rio', 190, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('20123-457', 'BRA', 'PE', 'Petrolina', 'Nova', 'Av. Principal', 200, 'Edifício');
-- Endereços 21 a 30: Para T_INST_ACADEMICA
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('21000-001', 'BRA', 'SP', 'São Paulo', 'Vila Mariana', 'Rua da Escola', 210, 'Campus A');
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('22123-457', 'BRA', 'RJ', 'Niterói', 'Icaraí', 'Rua da Praia', 220, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('23456-790', 'BRA', 'MG', 'Juiz de Fora', 'Centro', 'Rua do Saber', 230, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('24567-891', 'BRA', 'PR', 'Ponta Grossa', 'Universitário', 'Rua da Ciência', 240, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('25678-902', 'BRA', 'RS', 'Santa Maria', 'Central', 'Rua da Arte', 250, 'Prédio Novo');
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('26789-013', 'BRA', 'BA', 'Feira de Santana', 'Centro', 'Rua da Cultura', 260, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('27890-124', 'BRA', 'CE', 'Sobral', 'Polo Educ.', 'Rua do Ensino', 270, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('28901-235', 'BRA', 'DF', 'Plano Piloto', 'Asa Sul', 'Rua da Inovação', 280, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('29012-346', 'BRA', 'AM', 'Itacoatiara', 'Central', 'Rua da Aprendizagem', 290, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('30123-457', 'BRA', 'PE', 'Caruaru', 'Nova', 'Rua do Conhecimento', 300, 'Unidade II');
-- Endereços 31 a 40: Para T_LVUP_EVENTO
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('31000-001', 'BRA', 'SP', 'São Paulo', 'Pinheiros', 'Rua dos Eventos', 310, 'Espaço A');
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('32123-457', 'BRA', 'RJ', 'Rio de Janeiro', 'Barra', 'Av. Exposição', 320, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('33456-790', 'BRA', 'MG', 'Ouro Preto', 'Histórico', 'Rua do Centro', 330, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('34567-891', 'BRA', 'PR', 'Maringá', 'Central', 'Rua da Convenção', 340, 'Auditório');
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('35678-902', 'BRA', 'RS', 'Gramado', 'Turístico', 'Rua das Festas', 350, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('36789-013', 'BRA', 'BA', 'Porto Seguro', 'Praia', 'Rua do Sol', 360, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('37890-124', 'BRA', 'CE', 'Juazeiro', 'Central', 'Rua da Feira', 370, 'Pavilhão B');
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('38901-235', 'BRA', 'DF', 'Núcleo Bandeirante', 'Comercial', 'Rua do Encontro', 380, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('39012-346', 'BRA', 'AM', 'Parintins', 'Ilha', 'Rua da Cultura', 390, NULL);
INSERT INTO T_ENDERECO (cep, pais, estado, cidade, bairro, rua, numero, complemento) VALUES ('40123-457', 'BRA', 'PE', 'Olinda', 'Histórico', 'Rua do Carnaval', 400, 'Praça');

-- 2. T_CATEGORIA_EMPRESA (10 registros)
INSERT INTO T_CATEGORIA_EMPRESA (setor, subsetor, segmento) VALUES ('Tecnologia', 'Software', 'Desenvolvimento');
INSERT INTO T_CATEGORIA_EMPRESA (setor, subsetor, segmento) VALUES ('Tecnologia', 'Hardware', 'Fabricação');
INSERT INTO T_CATEGORIA_EMPRESA (setor, subsetor, segmento) VALUES ('Financeiro', 'Bancos', 'Varejo');
INSERT INTO T_CATEGORIA_EMPRESA (setor, subsetor, segmento) VALUES ('Educação', 'Ensino Superior', 'Privado');
INSERT INTO T_CATEGORIA_EMPRESA (setor, subsetor, segmento) VALUES ('Saúde', 'Hospitais', 'Geral');
INSERT INTO T_CATEGORIA_EMPRESA (setor, subsetor, segmento) VALUES ('Varejo', 'Supermercados', 'Alimentos');
INSERT INTO T_CATEGORIA_EMPRESA (setor, subsetor, segmento) VALUES ('Indústria', 'Automotiva', 'Montadora');
INSERT INTO T_CATEGORIA_EMPRESA (setor, subsetor, segmento) VALUES ('Consultoria', 'RH', 'Treinamento');
INSERT INTO T_CATEGORIA_EMPRESA (setor, subsetor, segmento) VALUES ('Logística', 'Transporte', 'Rodoviário');
INSERT INTO T_CATEGORIA_EMPRESA (setor, subsetor, segmento) VALUES ('Mídia', 'Entretenimento', 'Streaming');

-- 3. T_CATEGORIA_VAGA (10 registros)
INSERT INTO T_CATEGORIA_VAGA (setor, subsetor, segmento) VALUES ('TI', 'Desenvolvimento', 'Backend');
INSERT INTO T_CATEGORIA_VAGA (setor, subsetor, segmento) VALUES ('TI', 'Desenvolvimento', 'Frontend');
INSERT INTO T_CATEGORIA_VAGA (setor, subsetor, segmento) VALUES ('Marketing', 'Digital', 'SEO');
INSERT INTO T_CATEGORIA_VAGA (setor, subsetor, segmento) VALUES ('Vendas', 'Comercial', 'B2B');
INSERT INTO T_CATEGORIA_VAGA (setor, subsetor, segmento) VALUES ('RH', 'Recrutamento', 'Técnico');
INSERT INTO T_CATEGORIA_VAGA (setor, subsetor, segmento) VALUES ('Financeiro', 'Contabilidade', 'Fiscal');
INSERT INTO T_CATEGORIA_VAGA (setor, subsetor, segmento) VALUES ('Design', 'Gráfico', 'UX/UI');
INSERT INTO T_CATEGORIA_VAGA (setor, subsetor, segmento) VALUES ('Engenharia', 'Civil', 'Obras');
INSERT INTO T_CATEGORIA_VAGA (setor, subsetor, segmento) VALUES ('Logística', 'Supply Chain', 'Armazenamento');
INSERT INTO T_CATEGORIA_VAGA (setor, subsetor, segmento) VALUES ('Jurídico', 'Contencioso', 'Cível');

-- 4. T_VAGA_EMPRESA (10 registros)
INSERT INTO T_VAGA_EMPRESA (vaga_tema, des_vaga, st_vaga) VALUES ('Desenvolvedor Backend Junior (Java)', 'Desenvolvimento e manutenção de APIs e serviços. Necessário Java 11+.', 'A');
INSERT INTO T_VAGA_EMPRESA (vaga_tema, des_vaga, st_vaga) VALUES ('Analista de Projetos Sênior', 'Gestão de projetos de consultoria, metodologia PMP.', 'A');
INSERT INTO T_VAGA_EMPRESA (vaga_tema, des_vaga, st_vaga) VALUES ('Estagiário em Marketing Digital', 'Suporte na criação de conteúdo e campanhas de SEO.', 'A');
INSERT INTO T_VAGA_EMPRESA (vaga_tema, des_vaga, st_vaga) VALUES ('Vendedor B2B Pleno', 'Prospecção e negociação de contratos de software.', 'A');
INSERT INTO T_VAGA_EMPRESA (vaga_tema, des_vaga, st_vaga) VALUES ('Técnico de Enfermagem', 'Atendimento e suporte ao paciente em ambiente hospitalar.', 'A');
INSERT INTO T_VAGA_EMPRESA (vaga_tema, des_vaga, st_vaga) VALUES ('Analista de Mídia Social', 'Criação e gestão de campanhas em plataformas de streaming.', 'A');
INSERT INTO T_VAGA_EMPRESA (vaga_tema, des_vaga, st_vaga) VALUES ('Desenvolvedor Frontend Sênior (React)', 'Foco em performance e experiência do usuário (UX).', 'A');
INSERT INTO T_VAGA_EMPRESA (vaga_tema, des_vaga, st_vaga) VALUES ('Engenheiro de Produção Junior', 'Otimização de processos na linha de montagem automotiva.', 'A');
INSERT INTO T_VAGA_EMPRESA (vaga_tema, des_vaga, st_vaga) VALUES ('Assistente de Logística', 'Controle de estoque e gestão de rotas de transporte.', 'A');
INSERT INTO T_VAGA_EMPRESA (vaga_tema, des_vaga, st_vaga) VALUES ('Designer UX/UI Pleno', 'Criação de protótipos e testes de usabilidade para produtos digitais.', 'A');

-- 5. T_LVUP_LOGIN (10 registros - Chaves Primárias para Pessoa, Empresa e Instituição)
-- IDs 1 a 4: Pessoas | IDs 5 a 7: Empresas | IDs 8 a 10: Instituições
INSERT INTO T_LVUP_LOGIN (login, senha, st_ativo, id_pessoa) VALUES ('joao.silva', 'senha123', 'S', 1);
INSERT INTO T_LVUP_LOGIN (login, senha, st_ativo, id_pessoa) VALUES ('maria.souza', 'senha123', 'S', 2);
INSERT INTO T_LVUP_LOGIN (login, senha, st_ativo, id_pessoa) VALUES ('pedro.santos', 'senha123', 'S', 3);
INSERT INTO T_LVUP_LOGIN (login, senha, st_ativo, id_pessoa) VALUES ('ana.ferreira', 'senha123', 'S', 4);
INSERT INTO T_LVUP_LOGIN (login, senha, st_ativo, id_empresa) VALUES ('techco.adm', 'empresa123', 'S', 1);
INSERT INTO T_LVUP_LOGIN (login, senha, st_ativo, id_empresa) VALUES ('bankx.adm', 'empresa123', 'S', 2);
INSERT INTO T_LVUP_LOGIN (login, senha, st_ativo, id_empresa) VALUES ('globalcorp.adm', 'empresa123', 'S', 3);
INSERT INTO T_LVUP_LOGIN (login, senha, st_ativo, id_instAcademica) VALUES ('univabc.adm', 'inst123', 'S', 1);
INSERT INTO T_LVUP_LOGIN (login, senha, st_ativo, id_instAcademica) VALUES ('faculdef.adm', 'inst123', 'S', 2);
INSERT INTO T_LVUP_LOGIN (login, senha, st_ativo, id_instAcademica) VALUES ('escolaghi.adm', 'inst123', 'S', 3);

-- 6. T_PESSOA (10 registros - usando ENDERECO 1 a 10 e LOGIN 1 a 4)
INSERT INTO T_PESSOA (nm_pessoa, cpf_pessoa, dt_nascimento, id_endereco, id_login) VALUES ('João Silva', '111.111.111-11', DATE '2000-01-15', 1, 1);
INSERT INTO T_PESSOA (nm_pessoa, cpf_pessoa, dt_nascimento, id_endereco, id_login) VALUES ('Maria Souza', '222.222.222-22', DATE '1999-05-20', 2, 2);
INSERT INTO T_PESSOA (nm_pessoa, cpf_pessoa, dt_nascimento, id_endereco, id_login) VALUES ('Pedro Santos', '333.333.333-33', DATE '1985-11-10', 3, 3);
INSERT INTO T_PESSOA (nm_pessoa, cpf_pessoa, dt_nascimento, id_endereco, id_login) VALUES ('Ana Ferreira', '444.444.444-44', DATE '2001-08-01', 4, 4);
INSERT INTO T_PESSOA (nm_pessoa, cpf_pessoa, dt_nascimento, id_endereco) VALUES ('Lucas Costa', '555.555.555-55', DATE '2002-03-25', 5);
INSERT INTO T_PESSOA (nm_pessoa, cpf_pessoa, dt_nascimento, id_endereco) VALUES ('Juliana Lima', '666.666.666-66', DATE '1998-12-12', 6);
INSERT INTO T_PESSOA (nm_pessoa, cpf_pessoa, dt_nascimento, id_endereco) VALUES ('Rafaela Mendes', '777.777.777-77', DATE '2003-07-30', 7);
INSERT INTO T_PESSOA (nm_pessoa, cpf_pessoa, dt_nascimento, id_endereco) VALUES ('Gustavo Rocha', '888.888.888-88', DATE '1995-04-18', 8);
INSERT INTO T_PESSOA (nm_pessoa, cpf_pessoa, dt_nascimento, id_endereco) VALUES ('Carla Oliveira', '999.999.999-99', DATE '2000-09-05', 9);
INSERT INTO T_PESSOA (nm_pessoa, cpf_pessoa, dt_nascimento, id_endereco) VALUES ('Felipe Alves', '000.000.000-00', DATE '2001-02-28', 10);

-- 7. T_EMPRESA (10 registros - usando ENDERECO 11 a 20 e LOGIN 5 a 7)
INSERT INTO T_EMPRESA (nm_empresa, cnpj_empresa, email_empresa, dt_cadastro, st_empresa, id_endereco, id_login) VALUES ('TechCo Software', '01.000.000/0001-01', 'contato@techco.com', DATE '2018-01-01', 'A', 11, 5);
INSERT INTO T_EMPRESA (nm_empresa, cnpj_empresa, email_empresa, dt_cadastro, st_empresa, id_endereco, id_login) VALUES ('Bank X S.A.', '02.000.000/0001-02', 'rh@bankx.com', DATE '2015-05-10', 'A', 12, 6);
INSERT INTO T_EMPRESA (nm_empresa, cnpj_empresa, email_empresa, dt_cadastro, st_empresa, id_endereco, id_login) VALUES ('Global Corp Consultoria', '03.000.000/0001-03', 'info@globalcorp.com', DATE '2019-07-20', 'A', 13, 7);
INSERT INTO T_EMPRESA (nm_empresa, cnpj_empresa, email_empresa, dt_cadastro, st_empresa, id_endereco) VALUES ('Varejo Top LTDA', '04.000.000/0001-04', 'contato@varejotop.com', DATE '2020-03-01', 'A', 14);
INSERT INTO T_EMPRESA (nm_empresa, cnpj_empresa, email_empresa, dt_cadastro, st_empresa, id_endereco) VALUES ('Logística Rápida', '05.000.000/0001-05', 'frotas@logistica.com', DATE '2017-11-11', 'A', 15);
INSERT INTO T_EMPRESA (nm_empresa, cnpj_empresa, email_empresa, dt_cadastro, st_empresa, id_endereco) VALUES ('Saúde Total Hospitais', '06.000.000/0001-06', 'adm@saudetotal.com', DATE '2016-06-06', 'A', 16);
INSERT INTO T_EMPRESA (nm_empresa, cnpj_empresa, email_empresa, dt_cadastro, st_empresa, id_endereco) VALUES ('Automotiva Futurista', '07.000.000/0001-07', 'vendas@autoft.com', DATE '2021-02-14', 'A', 17);
INSERT INTO T_EMPRESA (nm_empresa, cnpj_empresa, email_empresa, dt_cadastro, st_empresa, id_endereco) VALUES ('Mídia Streaming Plus', '08.000.000/0001-08', 'imprensa@streamplus.com', DATE '2022-09-01', 'A', 18);
INSERT INTO T_EMPRESA (nm_empresa, cnpj_empresa, email_empresa, dt_cadastro, st_empresa, id_endereco) VALUES ('Design Criativo Estúdio', '09.000.000/0001-09', 'jobs@designc.com', DATE '2019-04-20', 'A', 19);
INSERT INTO T_EMPRESA (nm_empresa, cnpj_empresa, email_empresa, dt_cadastro, st_empresa, id_endereco) VALUES ('RH Solutions Treinamento', '10.000.000/0001-10', 'treinamento@rhsol.com', DATE '2014-10-05', 'A', 20);

-- 8. T_INST_ACADEMICA (10 registros - usando ENDERECO 21 a 30 e LOGIN 8 a 10)
INSERT INTO T_INST_ACADEMICA (nm_instAcademica, st_ativo, cnpj_inst_academica, id_endereco, id_login) VALUES ('Universidade ABC', 'S', '11.000.000/0001-11', 21, 8);
INSERT INTO T_INST_ACADEMICA (nm_instAcademica, st_ativo, cnpj_inst_academica, id_endereco, id_login) VALUES ('Faculdade DEF', 'S', '12.000.000/0001-12', 22, 9);
INSERT INTO T_INST_ACADEMICA (nm_instAcademica, st_ativo, cnpj_inst_academica, id_endereco, id_login) VALUES ('Escola Técnica GHI', 'S', '13.000.000/0001-13', 23, 10);
INSERT INTO T_INST_ACADEMICA (nm_instAcademica, st_ativo, cnpj_inst_academica, id_endereco) VALUES ('Instituto JKL', 'S', '14.000.000/0001-14', 24);
INSERT INTO T_INST_ACADEMICA (nm_instAcademica, st_ativo, cnpj_inst_academica, id_endereco) VALUES ('Centro de Ensino MNO', 'S', '15.000.000/0001-15', 25);
INSERT INTO T_INST_ACADEMICA (nm_instAcademica, st_ativo, cnpj_inst_academica, id_endereco) VALUES ('Pós-Graduação PQR', 'S', '16.000.000/0001-16', 26);
INSERT INTO T_INST_ACADEMICA (nm_instAcademica, st_ativo, cnpj_inst_academica, id_endereco) VALUES ('Faculdade de Direito STU', 'S', '17.000.000/0001-17', 27);
INSERT INTO T_INST_ACADEMICA (nm_instAcademica, st_ativo, cnpj_inst_academica, id_endereco) VALUES ('Universidade de Engenharia VWX', 'S', '18.000.000/0001-18', 28);
INSERT INTO T_INST_ACADEMICA (nm_instAcademica, st_ativo, cnpj_inst_academica, id_endereco) VALUES ('Faculdade de Saúde YZA', 'S', '19.000.000/0001-19', 29);
INSERT INTO T_INST_ACADEMICA (nm_instAcademica, st_ativo, cnpj_inst_academica, id_endereco) VALUES ('Escola de Negócios BCD', 'S', '20.000.000/0001-20', 30);

-- 9. T_LVUP_EVENTO (10 registros - usando ENDERECO 31 a 40)
INSERT INTO T_LVUP_EVENTO (nm_evento, descricao_evento, qt_dias, dt_inicio_evento, id_instAcademica, id_endereco, id_vagaEmpresa) VALUES ('Feira de Carreiras 2025', 'Evento para conectar alunos e empresas.', 1, DATE '2025-10-20', 1, 31, 1);
INSERT INTO T_LVUP_EVENTO (nm_evento, descricao_evento, qt_dias, dt_inicio_evento, id_instAcademica, id_endereco, id_vagaEmpresa) VALUES ('Workshop de Java', 'Imersão em desenvolvimento Backend.', 2, DATE '2025-11-05', 1, 32, 7);
INSERT INTO T_LVUP_EVENTO (nm_evento, descricao_evento, qt_dias, dt_inicio_evento, id_instAcademica, id_endereco, id_vagaEmpresa) VALUES ('Palestra sobre Marketing Digital', 'Novas tendências em SEO e Mídia.', 1, DATE '2025-10-25', 2, 33, 3);
INSERT INTO T_LVUP_EVENTO (nm_evento, descricao_evento, qt_dias, dt_inicio_evento, id_instAcademica, id_endereco) VALUES ('Recrutamento Rápido', 'Sessão de entrevistas com 5 empresas.', 1, DATE '2025-12-01', 3, 34);
INSERT INTO T_LVUP_EVENTO (nm_evento, descricao_evento, qt_dias, dt_inicio_evento, id_instAcademica, id_endereco) VALUES ('Hackathon de Inovação', 'Competição de 48 horas para soluções tecnológicas.', 2, DATE '2026-01-15', 4, 35);
INSERT INTO T_LVUP_EVENTO (nm_evento, descricao_evento, qt_dias, dt_inicio_evento, id_instAcademica, id_endereco, id_vagaEmpresa) VALUES ('Semana de RH', 'Foco em gestão de pessoas e benefícios.', 5, DATE '2025-09-01', 5, 36, 9);
INSERT INTO T_LVUP_EVENTO (nm_evento, descricao_evento, qt_dias, dt_inicio_evento, id_instAcademica, id_endereco, id_vagaEmpresa) VALUES ('Treinamento em Vendas B2B', 'Focado em negociação e fechamento de grandes contas.', 3, DATE '2025-11-20', 6, 37, 4);
INSERT INTO T_LVUP_EVENTO (nm_evento, descricao_evento, qt_dias, dt_inicio_evento, id_instAcademica, id_endereco) VALUES ('Simpósio Jurídico', 'Debate sobre novas leis e regulamentações.', 1, DATE '2026-03-10', 7, 38);
INSERT INTO T_LVUP_EVENTO (nm_evento, descricao_evento, qt_dias, dt_inicio_evento, id_instAcademica, id_endereco, id_vagaEmpresa) VALUES ('Exposição de Design', 'Apresentação de projetos de interface e gráficos.', 1, DATE '2025-12-15', 8, 39, 10);
INSERT INTO T_LVUP_EVENTO (nm_evento, descricao_evento, qt_dias, dt_inicio_evento, id_instAcademica, id_endereco, id_vagaEmpresa) VALUES ('Jornada de Saúde Mental', 'Palestras sobre bem-estar no ambiente de trabalho.', 2, DATE '2025-10-05', 9, 40, 5);

-- 10. T_TELEFONE_EMPRESA (Tabela Fraca - Depende de T_EMPRESA)
INSERT INTO T_TELEFONE_EMPRESA (ddi, ddd, numero, st_telefone, id_empresa) VALUES ('55', '11', '98888-1111', 'C', 1);
INSERT INTO T_TELEFONE_EMPRESA (ddi, ddd, numero, st_telefone, id_empresa) VALUES ('55', '11', '3000-1000', 'F', 1);
INSERT INTO T_TELEFONE_EMPRESA (ddi, ddd, numero, st_telefone, id_empresa) VALUES ('55', '21', '98888-2222', 'C', 2);
INSERT INTO T_TELEFONE_EMPRESA (ddi, ddd, numero, st_telefone, id_empresa) VALUES ('55', '31', '3000-3000', 'F', 3);
INSERT INTO T_TELEFONE_EMPRESA (ddi, ddd, numero, st_telefone, id_empresa) VALUES ('55', '41', '98888-4444', 'C', 4);
INSERT INTO T_TELEFONE_EMPRESA (ddi, ddd, numero, st_telefone, id_empresa) VALUES ('55', '51', '3000-5000', 'F', 5);
INSERT INTO T_TELEFONE_EMPRESA (ddi, ddd, numero, st_telefone, id_empresa) VALUES ('55', '71', '98888-6666', 'C', 6);
INSERT INTO T_TELEFONE_EMPRESA (ddi, ddd, numero, st_telefone, id_empresa) VALUES ('55', '85', '3000-7000', 'F', 7);
INSERT INTO T_TELEFONE_EMPRESA (ddi, ddd, numero, st_telefone, id_empresa) VALUES ('55', '61', '98888-8888', 'C', 8);
INSERT INTO T_TELEFONE_EMPRESA (ddi, ddd, numero, st_telefone, id_empresa) VALUES ('55', '92', '3000-9000', 'F', 9);

-- 11. EMPRESA_CATEGORIA (Associação M:N)
INSERT INTO EMPRESA_CATEGORIA (id_empresa, id_categoriaEmpresa) VALUES (1, 1);
INSERT INTO EMPRESA_CATEGORIA (id_empresa, id_categoriaEmpresa) VALUES (1, 8);
INSERT INTO EMPRESA_CATEGORIA (id_empresa, id_categoriaEmpresa) VALUES (2, 3);
INSERT INTO EMPRESA_CATEGORIA (id_empresa, id_categoriaEmpresa) VALUES (3, 8);
INSERT INTO EMPRESA_CATEGORIA (id_empresa, id_categoriaEmpresa) VALUES (4, 6);
INSERT INTO EMPRESA_CATEGORIA (id_empresa, id_categoriaEmpresa) VALUES (5, 9);
INSERT INTO EMPRESA_CATEGORIA (id_empresa, id_categoriaEmpresa) VALUES (6, 5);
INSERT INTO EMPRESA_CATEGORIA (id_empresa, id_categoriaEmpresa) VALUES (7, 7);
INSERT INTO EMPRESA_CATEGORIA (id_empresa, id_categoriaEmpresa) VALUES (8, 10);
INSERT INTO EMPRESA_CATEGORIA (id_empresa, id_categoriaEmpresa) VALUES (10, 8);

-- 12. EMPRESA_VAGA (Associação M:N)
INSERT INTO EMPRESA_VAGA (id_empresa, id_vagaEmpresa) VALUES (1, 1);
INSERT INTO EMPRESA_VAGA (id_empresa, id_vagaEmpresa) VALUES (1, 7);
INSERT INTO EMPRESA_VAGA (id_empresa, id_vagaEmpresa) VALUES (2, 3);
INSERT INTO EMPRESA_VAGA (id_empresa, id_vagaEmpresa) VALUES (3, 2);
INSERT INTO EMPRESA_VAGA (id_empresa, id_vagaEmpresa) VALUES (4, 4);
INSERT INTO EMPRESA_VAGA (id_empresa, id_vagaEmpresa) VALUES (6, 5);
INSERT INTO EMPRESA_VAGA (id_empresa, id_vagaEmpresa) VALUES (7, 8);
INSERT INTO EMPRESA_VAGA (id_empresa, id_vagaEmpresa) VALUES (8, 6);
INSERT INTO EMPRESA_VAGA (id_empresa, id_vagaEmpresa) VALUES (10, 9);
INSERT INTO EMPRESA_VAGA (id_empresa, id_vagaEmpresa) VALUES (9, 10);

-- 13. PESSOA_EVENTO (Associação M:N)
INSERT INTO PESSOA_EVENTO (id_pessoa, id_evento) VALUES (1, 1);
INSERT INTO PESSOA_EVENTO (id_pessoa, id_evento) VALUES (1, 2);
INSERT INTO PESSOA_EVENTO (id_pessoa, id_evento) VALUES (2, 3);
INSERT INTO PESSOA_EVENTO (id_pessoa, id_evento) VALUES (3, 1);
INSERT INTO PESSOA_EVENTO (id_pessoa, id_evento) VALUES (4, 4);
INSERT INTO PESSOA_EVENTO (id_pessoa, id_evento) VALUES (5, 5);
INSERT INTO PESSOA_EVENTO (id_pessoa, id_evento) VALUES (6, 6);
INSERT INTO PESSOA_EVENTO (id_pessoa, id_evento) VALUES (7, 7);
INSERT INTO PESSOA_EVENTO (id_pessoa, id_evento) VALUES (8, 9);
INSERT INTO PESSOA_EVENTO (id_pessoa, id_evento) VALUES (9, 10);

-- 14. VAGA_CATEGORIA (Associação M:N)
INSERT INTO VAGA_CATEGORIA (id_vagaEmpresa, id_categoria_vaga) VALUES (1, 1);
INSERT INTO VAGA_CATEGORIA (id_vagaEmpresa, id_categoria_vaga) VALUES (1, 5);
INSERT INTO VAGA_CATEGORIA (id_vagaEmpresa, id_categoria_vaga) VALUES (2, 3);
INSERT INTO VAGA_CATEGORIA (id_vagaEmpresa, id_categoria_vaga) VALUES (3, 6);
INSERT INTO VAGA_CATEGORIA (id_vagaEmpresa, id_categoria_vaga) VALUES (4, 4);
INSERT INTO VAGA_CATEGORIA (id_vagaEmpresa, id_categoria_vaga) VALUES (5, 9);
INSERT INTO VAGA_CATEGORIA (id_vagaEmpresa, id_categoria_vaga) VALUES (6, 7);
INSERT INTO VAGA_CATEGORIA (id_vagaEmpresa, id_categoria_vaga) VALUES (7, 1);
INSERT INTO VAGA_CATEGORIA (id_vagaEmpresa, id_categoria_vaga) VALUES (9, 5);
INSERT INTO VAGA_CATEGORIA (id_vagaEmpresa, id_categoria_vaga) VALUES (10, 7);