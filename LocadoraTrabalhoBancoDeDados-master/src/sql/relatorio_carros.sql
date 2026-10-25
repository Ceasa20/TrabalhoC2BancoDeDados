select p.placa
       , p.marca
       , p.modelo
       , p.valor_diaria
       , p.ativo
  from carros p
 order by p.placa