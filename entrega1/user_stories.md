## Estória de Usuário 1: Autenticação no Sistema

**Como** *usuário* do EcadNet, **quero** ser capaz de fazer *login* no sistema **para** acessar as funcionalidades específicas da minha *entidade* (dono de estabelecimento, musicista ou representante de associação).

## Estória de Usuário 2: Declarar Músicas Utilizadas

**Como** *dono de estabelecimento*, **quero poder** *declarar* as *músicas* que foram *usadas* em meu estabelecimento durante o mês **para** calcular o valor a ser *pago* ao Ecad e evitar *atrasos* no *pagamento*.

## Estória de Usuário 3: Notificação de Atraso no Pagamento

**Como** *dono de estabelecimento*, **quero** *receber* notificações **em caso de** atraso no *pagamento* das *músicas* utilizadas em meu estabelecimento **para** garantir que minha *situação* esteja em dia e *evitar* penalizações.

## Estória de Usuário 4: Cadastrar e Certificar uma Música

**Como** *musicista*, **quero poder** *cadastrar* uma nova *música* e obter um *certificado* de *propriedade intelectual*, se a música for única, **para** proteger meus *direitos autorais*.

## Estória de Usuário 5: Visualizar Relatório de Recebimento de Royalties

**Como** *musicista*, **quero** ser capaz de* *gerar* e *visualizar* *relatórios* **detalhados** de meus *ganhos*, *incluindo todos os* **cálculos** e *descontos*, **para** entender melhor como meus *rendimentos* são *calculados* e garantir a *transparência* nas *transações*.

## Estória de Usuário 6: Acompanhar em Série Histórica os Recebimentos do Artista**

*Como* **musicista**, **quero** ser capaz de *acompanhar em série histórica* os meus *recebimentos* ao longo do tempo, **para** ter uma visão clara e detalhada dos meus ganhos em períodos específicos.


## Estória de Usuário 7: Pedir Adiantamento à Associação**

**Nome da Estória de Usuário:** Solicitar Adiantamento de Rendimentos

**Descrição:**
Como músico afiliado a uma associação de compositores, desejo solicitar um adiantamento de meus rendimentos para cobrir despesas ou investir em minha carreira. Isso me permitirá obter acesso antecipado a uma parte dos meus ganhos gerados pelo Ecad.

**Critérios de Aceitação:**
- O sistema deve permitir que o músico acesse a função de solicitar adiantamento.
- O músico deve visualizar o valor máximo disponível para solicitação, com base em seus rendimentos dos últimos 6 meses.
- O músico deve selecionar o valor desejado para o adiantamento (dentro dos limites estabelecidos).
- O sistema deve registrar a solicitação de adiantamento.
- A associação deve analisar e aprovar ou rejeitar a solicitação.
- Se aprovada, o valor do adiantamento será descontado dos rendimentos futuros do músico.
- Se o adiantamento ultrapassar os rendimentos de um mês, o músico não receberá rendimentos naquele mês e será notificado sobre o saldo devedor à associação.
- O valor do adiantamento não pago será descontado nos meses subsequentes até que a dívida seja quitada.

## Estória de Usuário 8: Pedir para Musicista Trocar de Associação

**Nome da Estória de Usuário:** Solicitar Troca de Associação

**Descrição:**
Como músico afiliado a uma associação de compositores, desejo solicitar a troca de associação para me unir a uma associação diferente. Isso me permitirá explorar novas oportunidades e benefícios oferecidos por outra associação.

**Critérios de Aceitação:**
- O sistema deve permitir que o músico acesse a função de solicitar a troca de associação.
- O músico deve escolher a associação para a qual deseja trocar.
- Duas solicitações devem ser enviadas: uma para a liberação da saída da associação atual e outra para a entrada na nova associação.
- Ambas as associações envolvidas devem analisar e aprovar ou rejeitar as solicitações.
- Se ambas as solicitações forem aprovadas, o músico muda de associação.
- Os relatórios futuros do músico terão seu somatório calculado com a porcentagem de desconto da nova associação.
- Se uma ou ambas as solicitações forem rejeitadas, o músico solicitante será notificado sobre a rejeição.

## Estória de Usuário 9: Acompanhar Fluxo de Turnover dos Artistas de uma Associação**

**Nome da Estória de Usuário:** Acompanhar Saídas de Associados

**Descrição:**
Como representante de uma associação de compositores, desejo acompanhar o fluxo de saída de associados durante um período específico para entender o turnover. Isso me permitirá tomar decisões informadas sobre o engajamento dos associados e atração de novos membros.

**Critérios de Aceitação:**
- O sistema deve permitir que o representante da associação acesse a função de acompanhamento do fluxo de saída.
- O representante deve escolher um período, especificando a data de início e fim da análise.
- O sistema deve gerar um gráfico exibindo o número de saídas de associados em cada mês dentro do período selecionado.
- O sistema deve fornecer informações sobre as associações para as quais os associados saídos migraram.
- O sistema deve apresentar o total de associados que se desligaram da associação no período.

## Estória de Usuário 10: Acompanhar Rendimentos em Série Histórica dos Artistas Membros de uma Associação

**Nome da Estória de Usuário:** Acompanhar Rendimentos Históricos

**Descrição:**
Como representante de uma associação de compositores, desejo acompanhar os rendimentos dos artistas membros ao longo de um período específico, com a capacidade de aplicar filtros para análise detalhada. Isso me permitirá avaliar o desempenho dos membros e tomar decisões informadas.

**Critérios de Aceitação:**
- O sistema deve permitir que o representante da associação acesse a função de acompanhamento de rendimentos em série histórica.
- O representante deve escolher um período, especificando a data de início e fim da análise.
- O sistema deve gerar uma visualização com todos os rendimentos dos artistas membros nesse período.
- O sistema deve calcular os somatórios dos rendimentos com todos os cálculos de descontos (para o Ecad e a associação).
- O representante deve poder aplicar filtros por cidade, estado, musicista e música para analisar dados


