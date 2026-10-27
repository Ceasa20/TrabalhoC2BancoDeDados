# Registro de prompts

Este arquivo registra solicitações feitas a ferramentas de IA durante o desenvolvimento, a fonte e o que o grupo fez com as respostas. Para mensagens antigas resumidas no histórico da conversa, os prompts abaixo estão descritos de forma resumida, sem pretensão de transcrição literal.

## 1. Entender consultas SQL de locação

- **Prompt utilizado (resumido):** Explique o que as consultas SQL de locação fazem, se estão corretas e como funcionam `JOIN`, aliases e cálculo do valor total.
- **Fonte:** Copilot no VS Code.
- **O que o grupo fez com a resposta:** Comparou as consultas com os nomes reais de tabelas e colunas do esquema e ajustou as consultas apresentadas durante a conversa.

## 2. Revisar referências ao esquema de locações

- **Prompt utilizado (resumido):** Verifique se as referências à tabela de locações e suas colunas estão consistentes no projeto; inicialmente, sem alterar arquivos.
- **Fonte:** Copilot no VS Code.
- **O que o grupo fez com a resposta:** Usou a revisão para localizar referências legadas e incompatibilidades entre controllers, scripts de dados e esquema.

## 3. Corrigir operações do controller de locação

- **Prompt utilizado (resumido):** Revise e corrija problemas no controller de locação, incluindo atualização da locação, argumentos do modelo e exclusão.
- **Fonte:** Copilot no VS Code.
- **O que o grupo fez com a resposta:** Corrigiu a montagem de objetos `Locacao`, organizou métodos na classe e ajustou a atualização para recalcular o total quando o carro é trocado. A exclusão de carro não foi incluída na exclusão de locação.

## 4. Ajustar relatórios de locação

- **Prompt utilizado (resumido):** Ajuste os relatórios para mostrar dados da locação e contar locações por carro.
- **Fonte:** Copilot no VS Code.
- **O que o grupo fez com a resposta:** Atualizou consultas de relatório, incluindo a contagem por carro e o relatório geral com dados relacionados à locação.

## 5. Parametrizar SQL nos controllers

- **Prompt utilizado (resumido):** Explique o risco de interpolar dados digitados diretamente no SQL e corrija as consultas e alterações para usar parâmetros vinculados.
- **Fonte:** Copilot no VS Code.
- **O que o grupo fez com a resposta:** Os métodos de execução do Oracle passaram a aceitar parâmetros, e as consultas dos controllers foram convertidas para binds.

## 6. Corrigir caminhos de arquivos SQL e credenciais

- **Prompt utilizado (resumido):** Explique por que caminhos relativos dependem do diretório de execução e corrija-os para que os arquivos sejam encontrados ao iniciar a aplicação de outros diretórios.
- **Fonte:** Copilot no VS Code.
- **O que o grupo fez com a resposta:** Os caminhos dos scripts e dos arquivos SQL dos relatórios passaram a ser resolvidos a partir da localização dos módulos.

## 7. Corrigir dados de exemplo e consistência geral

- **Prompt utilizado (resumido):** Verifique inconsistências entre `DIAS_LOCACAO`, o esquema e os dados de exemplo; depois, corrija os inserts.
- **Fonte:** Copilot no VS Code.
- **O que o grupo fez com a resposta:** Os inserts de locação foram ajustados para usar a coluna `DIAS_LOCACAO`.

## 8. Evitar cadastro duplicado de carro

- **Prompt utilizado (resumido):** Reutilize a placa informada inicialmente no cadastro de carro, sem perguntar novamente, e evite que a segunda placa passe sem validação.
- **Fonte:** Copilot no VS Code.
- **O que o grupo fez com a resposta:** O fluxo de cadastro foi ajustado para continuar usando a placa já informada na verificação de existência.

## 9. Inativar carros em vez de apagá-los

- **Prompt utilizado (resumido):** Adicione um status ativo/inativo para carros: carros novos começam ativos, a edição permite alterar o status e locações não podem usar carros inativos.
- **Fonte:** Copilot no VS Code.
- **O que o grupo fez com a resposta:** O status `ATIVO` foi adicionado ao modelo, esquema, controller e relatório. O fluxo de remoção passou a inativar o carro, e a seleção/validação para locação passou a exigir carro ativo. Foi criada uma migração para bancos existentes.

## 10. Validar data prevista da locação

- **Prompt utilizado (resumido):** Explique como manter o usuário no pedido da data até que informe uma data válida e posterior à data atual.
- **Fonte:** Copilot no VS Code.
- **O que o grupo fez com a resposta:** Foi implementada uma solicitação repetida que valida o formato ISO e rejeita datas de hoje ou anteriores.

## 11. Corrigir execução e mensagens do script de criação

- **Prompt utilizado (resumido):** Explique o risco de o script de criação informar sucesso após falhas e corrija os caminhos dos scripts.
- **Fonte:** Copilot no VS Code.
- **O que o grupo fez com a resposta:** Os caminhos dos scripts foram ancorados no módulo e erros de DDL passaram a ser relançados, evitando continuar como se a criação tivesse sido concluída.

## 12. Ignorar cache Python

- **Prompt utilizado (resumido):** Explique o que é `__pycache__` e adicione regras para ignorar os arquivos de cache Python.
- **Fonte:** Copilot no VS Code.
- **O que o grupo fez com a resposta:** Foi criado `.gitignore` com regras para `__pycache__/` e arquivos `*.py[cod]`.

## 13. Fazer revisões gerais do projeto

- **Prompt utilizado (resumido):** Revise o projeto em busca de erros e inconsistências, primeiro em escopo parcial e depois considerando o projeto completo.
- **Fonte:** Copilot no VS Code.
- **O que o grupo fez com a resposta:** Usou as revisões para corrigir problemas encontrados e manter uma lista de riscos, como a consistência de consultas, integridade referencial, conexão e inicialização. A revisão mais recente de erros críticos não alterou arquivos.

## 14. Inativar clientes e impedir novas locações

- **Prompt utilizado:** “Implementa a mesma coisa para clientes igual fizemos para carros”, evitando falha ao excluir clientes que tenham locações associadas.
- **Fonte:** Copilot no VS Code.
- **O que o grupo fez com a resposta:** Foi adicionado o status `ATIVO` para clientes, com valor padrão ativo, edição do status, inativação em vez de exclusão e bloqueio de novos aluguéis para clientes inativos. O relatório e a migração do banco também foram atualizados.

## 15. Ignorar trechos vazios ao executar scripts SQL

- **Prompt utilizado:** “Faz essa correção pra mim”, referindo-se a ignorar comandos vazios depois de dividir scripts pelo ponto e vírgula.
- **Fonte:** Copilot no VS Code.
- **O que o grupo fez com a resposta:** Nos processadores de criação e carga, cada trecho SQL agora recebe `strip()` e só é enviado ao Oracle se não estiver vazio.

## 16. Finalizar locações em vez de excluí-las

- **Prompt utilizado (resumido):** Remova a opção de excluir locação, adicione uma opção para finalizá-la e impeça alterar uma locação já finalizada.
- **Fonte:** Copilot no VS Code.
- **O que o grupo fez com a resposta:** A ação passou a preencher `DATA_FIM_LOCACAO`; a atualização verifica se a locação foi finalizada; o menu, a listagem e o relatório geral foram atualizados.

## 17. Validar opções de menu e valores numéricos

- **Prompt utilizado (resumido):** Complete a validação das entradas para que opções incorretas repitam a pergunta e dados não numéricos não encerrem o programa com `ValueError`.
- **Fonte:** Copilot no VS Code.
- **O que o grupo fez com a resposta:** Os menus agora repetem a solicitação até receber opções permitidas; a diária exige valor numérico positivo e finito; os códigos de locação exigem inteiro positivo.

## 18. Registrar a revisão considerando a VM Linux

- **Prompt utilizado (resumido):** Considerando a execução em uma VM Linux com Oracle, revise o projeto em busca de erros críticos, sem alterar arquivos, e diferencie problemas confirmados dos que dependem da configuração.
- **Fonte:** Copilot no VS Code.
- **O que o grupo fez com a resposta:** Registrou para avaliação o risco de permitir mais de uma locação em andamento para o mesmo carro e verificou os pontos de configuração de schema e de execução inicial dos scripts. A observação sobre o comando `clear` foi considerada não aplicável ao ambiente Linux planejado.

## 19. Adicionar exclusão permanente sem remover a desativação

- **Prompt utilizado (resumido):** Mantenha a função atual de desativar clientes e carros e finalizar locações, mas adicione uma nova opção no menu para excluir permanentemente registros, com listagem, seleção e confirmação. Para clientes e carros com locações vinculadas, pergunte se as locações também devem ser excluídas.
- **Fonte:** Copilot no VS Code.
- **O que o grupo fez com a resposta:** O menu passou a oferecer separadamente a desativação/finalização e a exclusão permanente. A exclusão lista os registros com chave primária e campos descritivos, permite seleção numerada e exige confirmação. Para cliente ou carro com locações vinculadas, a confirmação permite excluir as locações dependentes e o registro principal em uma única transação; sem essa confirmação, a exclusão é bloqueada.
