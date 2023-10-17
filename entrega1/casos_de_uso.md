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

