select l.codigo_locacao
     , c.nome as nome_cliente
     , ca.placa
     , ca.modelo
     , l.data_inicio_locacao
     , l.data_previsao_locacao
     , l.valor_total
  from locacao l
  inner join clientes c
    on l.cpf = c.cpf
  inner join carros ca
    on l.placa = ca.placa
 order by l.codigo_locacao