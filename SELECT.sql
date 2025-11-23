-- =======================
--      CONSULTAS (QUERIES)
-- =======================

-- CONSULTA SIMPLES DE PESSOAS COMECAM COM A LETRA DO NOME = 'A'
SELECT * FROM T_PESSOA
    WHERE nm_pessoa LIKE 'A%';

-- COSULTA DE EMPRESAS ATIVAS LOCALIZADAS EM SP
SELECT
    EMP.nm_empresa,
    END.cidade,
    END.estado
FROM
    T_EMPRESA EMP
JOIN
    T_ENDERECO END ON EMP.id_endereco = END.id_endereco
WHERE
    END.estado = 'SP' AND EMP.st_empresa = 'A' -- Cláusula WHERE obrigatória
ORDER BY
    EMP.nm_empresa ASC;

-- CONSULTA DAS TODAS AS CIDADES 
--(SEJAM DE EVENTOS, EMPRESAS, INSTITUIÇÕES ACADEMICAS OU PESSOAS)
SELECT CIDADE,COUNT(CIDADE) FROM t_endereco
    GROUP BY CIDADE -- agrupar valores iguais
    ORDER BY CIDADE ASC; -- ordenar os valores
    

-- SELECT ESTADO, CIDADE, COUNT(*) FROM T_ENDERECO GROUP BY ESTADO, CIDADE ORDER BY ESTADO, COUNT(*) DESC;


    
-- CONSULTA DO NOME E CEP DA EMPRESA
--SELECT emp.nm_empresa , end.cep
--    FROM t_empresa emp INNER JOIN t_endereco end
--    ON emp.id_endereco = end.id_endereco
--    ORDER BY emp.nm_empresa ASC;

--SELECT p.nm_pessoa,l.login,l.senha
--    FROM T_PESSOA p INNER JOIN T_LVUP_LOGIN l 
--    ON p.id_login = l.id_login;
    
-- SELECT end.pais, end.estado, COUNT(p.id_pessoa) As Qt_Pessoas
--    FROM t_pessoa p INNER JOIN t_endereco end
--    ON p.id_endereco = end.id_endereco
--    GROUP BY end.pais,end.estado
--    ORDER BY end.estado ASC
   -- ;
   
--CONSULTANDO INSTITUIÇÕES ACADEMICAS QUE TENHAM MAIS DE UM EVENTO REGISTRADO
SELECT 
    a.nm_instacademica AS NOME_INSTITUICAO,
    COUNT(e.id_evento) AS QDT_EVENTOS
    FROM t_inst_academica a JOIN t_lvup_evento e
    ON a.id_instacademica=e.id_instacademica
    GROUP BY a.nm_instacademica
    HAVING COUNT(e.id_evento) >1 ;
    