## Caso de Uso 1: Login

**Ator Principal:**
Usuário do Sistema (Proprietário de Estabelecimento, Músico ou Representante de Associação)

**Summary Description:**
Este caso de uso descreve o processo de um usuário do sistema fazendo login, fornecendo suas credenciais e selecionando seu tipo de entidade (Proprietário de Estabelecimento, Músico ou Representante de Associação). Com base em sua seleção, o sistema redireciona o usuário para a área correspondente.

**Pre-Condition:**
- O usuário tem acesso à página de login do sistema.

**Post-Condition:**
- O usuário faz login com sucesso e é direcionado para a seção apropriada do sistema com base no tipo de entidade escolhido.

**Basic Path:**
1. O usuário acessa a página de login do sistema.
2. O sistema apresenta opções para o usuário escolher seu tipo de entidade:
   - Proprietário de Estabelecimento
   - Músico
   - Representante de Associação
3. O usuário seleciona seu tipo de entidade.
4. O sistema solicita credenciais de autenticação, incluindo um nome de usuário e senha.
5. O usuário fornece suas credenciais de autenticação.
6. O sistema verifica as credenciais e a identidade do usuário.
7. Com base na escolha do usuário, o sistema o redireciona para a seção específica correspondente ao seu tipo de entidade.


## Use Case 2: Enviar Músicas Usadas no Mês

**Ator Principal:** Dono de estabelecimento.

**Summary Description:**
Neste caso de uso, o dono de estabelecimento envia as informações sobre as músicas utilizadas no mês, o sistema calcula o valor a ser pago com base nas músicas enviadas e oferece opções de pagamento ao usuário.

**Pre-Condition:**
- O dono do estabelecimento tem acesso à área específica para proprietários de estabelecimentos.

**Post-Condition:**
- As músicas usadas no mês são registradas no sistema, e o valor a ser pago é calculado e as opções de pagamento são oferecidas ao dono do estabelecimento.

**Basic Path:**
1. O dono do estabelecimento acessa a área específica para proprietários de estabelecimentos.
2. O dono do estabelecimento seleciona a opção para enviar as músicas usadas no mês.
3. O sistema permite ao usuário enviar um arquivo contendo as informações das músicas usadas.
4. O sistema calcula o valor a ser pago com base nas músicas enviadas.
5. O sistema oferece opções de pagamento ao usuário, como cartão de crédito ou transferência bancária.

## Use Case 3: Atraso no Pagamento

**Ator Principal:** Dono de estabelecimento.

**Summary Description:**
Neste caso de uso, o sistema identifica que o pagamento do dono de estabelecimento está atrasado e notifica o representante do estabelecimento. O representante do estabelecimento, ao receber a notificação, acessa a área do sistema para enviar as músicas do mês. O sistema recalcula o valor a ser pago, incluindo um acréscimo devido ao atraso.

**Pre-Condition:**
- O sistema identifica que o pagamento do dono de estabelecimento está atrasado.

**Post-Condition:**
- O valor a ser pago é recalculado, incluindo o acréscimo devido ao atraso, após o representante do estabelecimento enviar as músicas do mês.

**Basic Path:**
1. O sistema identifica que o pagamento do dono de estabelecimento está atrasado.
2. O sistema envia uma notificação ao representante do estabelecimento, seja por e-mail ou SMS, informando sobre o atraso no pagamento.
3. O representante do estabelecimento acessa a área do sistema.
4. O representante do estabelecimento envia as músicas do mês.
5. O sistema recalcula o valor a ser pago, incluindo um acréscimo devido ao atraso.

## Use Case 4: Cadastrar uma Música e Certificá-la

**Actor:**
Musicista

**Summary Description:**
Neste caso de uso, um musicista acessa a área específica para músicos, cadastra uma nova música enviando um arquivo de texto (obra) ou um arquivo de áudio (fonograma). O sistema verifica se a música é diferente de outras obras já inseridas no banco de dados. Se a música for única, o sistema emite um certificado de propriedade intelectual. Se a música não for única, o sistema emite um aviso de não exclusividade.

**Pre-Condition:**
- O musicista tem acesso à área específica para músicos.

**Post-Condition:**
- A música é cadastrada no sistema, e o certificado de propriedade intelectual é emitido se a música for única.

**Basic Path:**
1. O musicista acessa a área específica para músicos.
2. O musicista seleciona a opção para cadastrar uma nova música.
3. O musicista envia um arquivo de texto (obra) ou um arquivo de áudio (fonograma).
4. O sistema verifica se a música é diferente de outras obras já inseridas no banco de dados.
5. Se a música for única, o sistema emite um certificado de propriedade intelectual.
6. Se a música não for única, o sistema emite um aviso de não exclusividade.


## Use Case 5: Gerar Relatório de Recebimento para Musicista

**Actor:**
Musicista

**Summary Description:**
Neste caso de uso, um musicista acessa a área do sistema onde pode gerar relatórios de recebimento de royalties. O musicista seleciona a opção para visualizar os rendimentos do último mês. O sistema gera um arquivo que lista todos os rendimentos registrados para o musicista no mês. O arquivo mostra todos os cálculos, incluindo descontos (valor para o Ecad e associação), que levaram ao valor final.

**Pre-Condition:**
- O musicista tem acesso à área do sistema para gerar relatórios de recebimento de royalties.

**Post-Condition:**
- Um arquivo de relatório é gerado, listando todos os rendimentos do musicista no último mês, incluindo cálculos detalhados.

**Basic Path:**
1. O musicista acessa a área do sistema onde pode gerar relatórios de recebimento de royalties.
2. O musicista seleciona a opção para visualizar os rendimentos do último mês.
3. O sistema gera um arquivo que lista todos os rendimentos registrados para o musicista no mês.
4. O arquivo mostra todos os cálculos, incluindo descontos (valor para o Ecad e associação), que levaram ao valor final.

## Use Case 6: Acompanhar em série histórica os recebimentos do artista

**Actor:**
Musicista

**Summary Description:**
Neste caso de uso, um musicista tem a capacidade de acompanhar em série histórica os recebimentos ao longo de um período escolhido. O musicista seleciona as datas de início e fim para visualizar os rendimentos desse período. O sistema retorna uma visualização com todos os rendimentos e o somatório de rendimentos, incluindo cálculos de descontos (valor para o Ecad e associação), até o valor final recebido nesse período. Além disso, o musicista tem a opção de filtrar os rendimentos por cidade, estado e música.

**Pre-Condition:**
- O musicista tem acesso à funcionalidade de acompanhamento de série histórica de recebimentos.

**Post-Condition:**
- O musicista obtém uma visualização detalhada dos rendimentos, incluindo o somatório, para o período especificado.

**Basic Path:**
1. O musicista escolhe as datas de início e fim do período que deseja ver os rendimentos.
2. O sistema retorna uma visualização com todos os rendimentos para o período especificado.
3. O sistema calcula o somatório dos rendimentos, incluindo cálculos de descontos (valor para o Ecad e associação), até o valor final recebido nesse período.
4. O musicista tem a opção de filtrar os rendimentos por cidade, estado e música.

**Use Case 7:** Pedir Adiantamento à Associação

**Actor:** Musicista

**Summary Description:** O musicista deseja solicitar um adiantamento financeiro à sua associação de compositores por meio do sistema.

**Pre-Condition:**
- O musicista está autenticado no sistema.
- A associação à qual o musicista está afiliado aceita pedidos de adiantamento.
- O valor máximo que pode ser solicitado como adiantamento foi previamente definido.

**Post-Condition:**
- O adiantamento é aprovado ou rejeitado.
- Caso seja aprovado, o montante solicitado será descontado dos futuros rendimentos do musicista.

**Basic Path:**
1. O musicista faz login no sistema.
2. O musicista acessa a opção de solicitar adiantamento.
3. O sistema exibe o valor máximo que pode ser solicitado com base nos últimos 6 meses.
4. O musicista escolhe o valor que deseja adiantar, dentro dos limites estabelecidos.
5. O musicista envia a solicitação de adiantamento à sua associação.
6. A associação analisa a solicitação.
7. Se a solicitação for aprovada:
   a. Os futuros rendimentos do musicista terão o valor do adiantamento descontado.
   b. Se o valor do adiantamento ultrapassar os rendimentos do mês, o musicista não receberá rendimentos, e um aviso de saldo devedor à associação será gerado.
   c. O valor do adiantamento não pago será descontado integralmente nos próximos meses até que a dívida seja quitada.
8. Se a solicitação for rejeitada, o musicista solicitante recebe um aviso de rejeição.

**Use Case 8:** Pedir para Musicista Trocar de Associação

**Actor:** Musicista

**Summary Description:** O musicista deseja solicitar a troca de associação para outra no sistema.

**Pre-Condition:**
- O musicista está autenticado no sistema.
- O musicista deseja mudar de associação.
- A solicitação de troca de associação é permitida.

**Post-Condition:**
- A troca de associação é aprovada ou rejeitada, afetando os relatórios futuros do musicista.

**Basic Path:**
1. O musicista faz login no sistema.
2. O musicista acessa a opção de solicitar a troca de associação.
3. O musicista seleciona a associação para a qual deseja trocar.
4. Duas solicitações são enviadas: uma para a liberação da saída da associação atual e outra para a entrada na nova associação.
5. Ambas as associações analisam as solicitações.
6. Se ambas as solicitações forem aprovadas:
   a. O musicista muda de associação.
   b. Os relatórios futuros terão seu somatório calculado com a porcentagem de desconto da nova associação.
7. Se uma ou ambas as solicitações forem rejeitadas, o musicista solicitante recebe um aviso de rejeição.

**Use Case 9:** Acompanhar Fluxo de Turnover dos Artistas de uma Associação

**Actor:** Representante da Associação

**Summary Description:** O representante da associação deseja acompanhar o fluxo de saída de associados ao longo de um período específico.

**Pre-Condition:**
- O representante da associação está autenticado no sistema.
- A opção de acompanhamento do fluxo de turnover está disponível.

**Post-Condition:**
- O representante obtém informações sobre o número de saídas de associados, as associações para as quais eles migraram e o total de associados desligados.

**Basic Path:**
1. O representante da associação faz login no sistema.
2. O representante seleciona a opção de acompanhar o fluxo de turnover.
3. O representante escolhe um período, especificando a data de início e fim da análise.
4. O sistema gera um gráfico exibindo o número de saídas de associados em cada mês dentro do período selecionado.
5. O sistema fornece informações sobre as associações para as quais os associados saídos migraram.
6. O sistema apresenta o total de associados que se desligaram da associação no período.
