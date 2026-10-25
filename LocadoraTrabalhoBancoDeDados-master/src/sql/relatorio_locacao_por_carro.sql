select c.placa
     , c.modelo
     , count(l.codigo_locacao) as quantidade_locacoes
  from carros c
  left join locacao l
    on l.placa = c.placa
 group by c.placa, c.modelo
 order by quantidade_locacoes desc