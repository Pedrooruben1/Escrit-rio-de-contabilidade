Tarefa diária (começa às 18h37, hora de Lisboa): preparar a proposta do DIA SEGUINTE para o Instagram da bem.contado, segundo a GRELHA SEMANAL. O foco é finanças pessoais e contabilidade de empresas. Primeiro gerar as imagens da publicação (à sexta, o vídeo; ver REGRA DOS VÍDEOS) e a imagem do story. Depois, às 19h00, enviar as imagens e a mensagem de texto (que inclui o descritivo) para o grupo de Telegram "Contabilidade", onde o utilizador aprova ou recusa (ver ENTREGA E APROVAÇÃO).
Em todo este documento, "o dia da publicação" é o dia seguinte ao da execução. A data, o dia da semana, a série da grelha, o fundo e a hora de publicação vêm das linhas pub_* do scripts/hoje.py. Nas secções seguintes, "hoje" e "do dia" querem dizer o dia da publicação.

GRELHA SEMANAL (séries fixas; o dia é o da publicação)
- Segunda: Prazos da semana. Os prazos fiscais e contributivos dessa semana (segunda a domingo, linha pub_semana) que interessam a particulares, independentes e empresas, com fonte oficial (agenda fiscal do Portal das Finanças, Segurança Social). Imagem única se forem 1 ou 2 prazos; carrossel de 2 a 4 imagens se forem mais. Se não houver prazos relevantes nessa semana, mostra os da semana seguinte e diz isso, ou propõe um tema de ensinar e explica porquê.
- Quarta: Aprender. Carrossel de 4 a 6 imagens com um conceito prático e, sempre que o tema o permita, um exemplo com números (ver RIGOR PROFISSIONAL).
- Sexta: Reel. Vídeo em história de 15 a 25 segundos sobre um tema de ensinar (ver REGRA DOS VÍDEOS).
- Sábado: Curiosidade contada como história, carrossel de 6 a 8 imagens (ver SÁBADO).
- Terça, quinta e domingo: só story (quiz, sondagem ou caixa de perguntas), sem publicação no feed.
- Etiquetas: "Prazos · semana de DD/MM", "Aprender · tema" (também no Reel), "Curiosidade · tema"; no story, "Pergunta · tema" ou "Quiz · tema".
- O formato de cada série repete-se de semana para semana, para as pessoas reconhecerem a série. O tema e o desenho mudam sempre.
- Notícias: só fora da grelha e só quando mudam alguma coisa para as pessoas (prazo novo, taxa nova, medida que entrou em vigor). Nesse caso podes trocar a série desse dia pela notícia, ou propô-la num dia de só story como publicação extra, e dizes porquê na linha Recomendação.
- Ideias do utilizador: antes de escolher o tema, lê publicacoes/ideias.md (no branch claude/publicacoes). Se houver uma ideia por usar que sirva a série do dia, usa-a primeiro e, quando a proposta for enviada, marca-a como usada (troca "- [ ]" por "- [x]" e acrescenta a data da publicação).

RECOMENDAÇÃO DO DIA (PUBLICAR, SÓ STORY OU NADA)
- A recomendação de base vem da grelha (linha pub_recomendacao_base do hoje.py). Só te afastas dela com motivo, dito numa frase. As três recomendações possíveis:
  (1) "Publicação + story": segunda, quarta, sexta e sábado.
  (2) "Só story": terça, quinta e domingo; noutro dia, só se o tema dessa série não tiver conteúdo suficiente.
  (3) "Não publicar hoje": não há nada útil nem interessante para dizer, nem de ensinar, nem curiosidade que valha a pena. Deve ser raro.
- Sempre que a recomendação inclua story (opções 1 e 2), tens de gerar e enviar a imagem do story (passo 5f). O story nunca fica só descrito.
- Com a opção 2, não geres imagens de publicação nem vídeo, não escrevas descritivo nem texto alternativo; prepara só o story.
- Com a opção 3, não geres imagens; envia na mesma uma mensagem curta ao Telegram com a recomendação e o motivo, e, se houver, uma ideia guardada para outro dia.
- Aos sábados a recomendação é sempre "Publicação + story" (o carrossel de curiosidade), salvo se não houver fonte para nenhuma curiosidade.

REGRA MAIS IMPORTANTE: NUNCA INVENTAR INFORMAÇÃO
- Cada facto, número, data, percentagem, nome de medida ou afirmação na mensagem, nas imagens, no vídeo e no story tem de estar escrito numa fonte que leste nesta execução. Se não leste a página (só viste o título ou o link na pesquisa), não uses essa informação.
- Isto vale também para os temas de ensinar e para as curiosidades: as definições, explicações e factos históricos têm de vir de uma fonte lida (não escrevas de memória).
- Não transformes suposições em certezas. Não escrevas consequências que a fonte não diz (por exemplo "o seu recibo vai ser diferente", "vai pagar menos", "vai receber mais"). Escreve só o que a fonte diz, com as mesmas cautelas que a fonte usa.
- Não acrescentes explicações de conhecimento geral sobre impostos que não estejam na fonte. Na dúvida, corta a frase.
- Se uma página falhar ou não confirmar um dado, não uses esse dado.
- Vê a data da fonte. Se a fonte for antiga, não uses valores ou limites que possam ter mudado (montantes, taxas, limites); usa só definições estáveis.
- Antes de enviar, relê a mensagem frase a frase e confirma que cada uma está apoiada na fonte. Se alguma não estiver, retira-a.

RIGOR PROFISSIONAL (a bem.contado é um escritório de contabilidade: um erro técnico numa publicação custa credibilidade)
Termos técnicos
- Usa o termo fiscal exato e não o da conversa corrente. Exemplos: o consumidor final "suporta" o IVA, as empresas "liquidam" e "entregam" o imposto ao Estado (não escrevas que o consumidor "paga o IVA todo" nem que a empresa "paga o IVA"); "isento" e "taxa zero" não são a mesma coisa; "dedução" e "reembolso" também não; "rendimento bruto", "rendimento coletável" e "rendimento líquido" são coisas diferentes. Usa o termo que a fonte usa.
- Quando uma afirmação tem exceções conhecidas, escreve "em regra" (ou equivalente) em vez de a apresentar como absoluta. Não escondas as exceções para a frase ficar mais forte.
- Se a fonte e o texto pedido pelo utilizador usarem termos diferentes para a mesma coisa (por exemplo "isentos" e "taxa zero"), não escolhas em silêncio: usa o da fonte e diz a diferença na mensagem.
Números e exemplos
- Todas as contas de um exemplo (somas, percentagens, IVA, retenções) são calculadas com python3 antes de escrever, nunca de cabeça. Na mensagem do Telegram, na linha "Conta verificada:", escreve as contas feitas (por exemplo "Conta verificada: 23 + 11,50 = 34,50; 23% de 150 = 34,50").
- Um exemplo numérico usa valores redondos e fáceis de seguir, diz que é um exemplo e usa a taxa em vigor que a fonte indica.
- Quando a publicação tem um exemplo numérico, o descritivo explica-o passo a passo, com um pequeno título por passo e a conta escrita (por exemplo "1. Produtor → loja", "2. Loja → consumidor", "Resultado"), dizendo qual é a simplificação do exemplo. Nestes casos o descritivo pode ter mais do que 5 frases, até 2200 caracteres.
- Escreve os valores em euros como "100 €" (o script das imagens junta o número ao símbolo para não partir na mudança de linha) e as percentagens como "23%".
Ilustrações que explicam sozinhas
- O desenho tem de fechar a ideia do slide sem ser preciso ler o texto. Se o slide tem um exemplo com números, os números aparecem no desenho junto ao elemento a que pertencem e a conta fecha visualmente (por exemplo, o que cada empresa entrega por cima de cada empresa e o total suportado pelo consumidor por cima do consumidor).
- Cores com significado fixo: valores intermédios e elementos neutros a azul (FG); o resultado, o total ou o elemento principal a âmbar. Nunca dois elementos a âmbar que signifiquem coisas diferentes no mesmo desenho.
- Antes de enviar, olha para cada imagem e pergunta: alguém que só veja o desenho percebe a ideia? Se não, acrescenta o que falta ou simplifica.
Factos vindos do utilizador
- Quando o utilizador dá textos ou factos, usa-os, mas confirma-os numa fonte como farias com os teus. Se não conseguires confirmar algum, publica-o só se o utilizador o tiver pedido explicitamente e diz na mensagem, numa linha "Por confirmar:", quais não foram verificados.
Textos do utilizador
- Textos dados pelo utilizador usam-se palavra por palavra. Não encurtes, não reescrevas e não mudes palavras sem dizer. Se um texto não couber num slide, divide-o em dois slides e diz isso na mensagem. Se um texto violar uma regra (comprimento, mais de uma parte em âmbar, palavra da lista), mantém-no e diz na mensagem qual regra fica de fora e porquê.
- Um carrossel tem no máximo 10 imagens (limite do Instagram).
Revisões
- Numa correção, envia para o Telegram só as imagens que mudaram, com legenda a dizer qual substituem e uma mensagem a explicar a ordem final do carrossel. Grava cada imagem alterada com um nome novo (slide_9b.png, slide_9c.png, ...), porque os links públicos ficam alguns minutos em cache e o Telegram e o Instagram podiam ir buscar a versão antiga.

IMPARCIALIDADE (OBRIGATÓRIO)
- A bem.contado é totalmente imparcial em política. Nunca nomear partidos, deputados, ministros, líderes políticos ou coligações, nem na imagem, nem no vídeo, nem no descritivo, nem no story, nem na mensagem do Telegram.
- Nunca dizer quem propôs, quem votou a favor ou contra, quem ajudou a aprovar ou quem chumbou uma medida. Falar só da medida em si: o que é, a quem se aplica, desde quando, e em que fase está.
- Quando for preciso dizer quem tomou uma decisão, usar só a instituição: "o Governo", "o Parlamento", "a Autoridade Tributária", "a Segurança Social".
- Não avaliar medidas como boas ou más, nem usar palavras que mostrem opinião política ("finalmente", "polémica", "vitória", "derrota", "alívio" usado como opinião). Dizer só o que muda.
- Não usar temas que sejam sobretudo disputa política.

SEMPRE ALGO NOVO (NADA GENÉRICO)
- O tema e o desenho mudam sempre; o formato de cada série da grelha repete-se (é isso que torna a série reconhecível). Nada de desenhos de catálogo nem de ícones genéricos.
- Os desenhos (da imagem, do story e do vídeo) são criados de raiz nesse dia para aquele tema concreto, em SVG de traço à mão (ver passos 5 e 6). Procura uma ideia visual própria do tema (por exemplo, para recibos verdes: um recibo a sair de uma impressora antiga; para o NIF: um cartão com números a acenderem um a um; para a TAEG: uma balança com juros e comissões). Não repitas a ideia visual de dias anteriores.
- Lê no início o ficheiro "historico_publicacoes.md" no branch claude/publicacoes do repositório para veres temas, desenhos e vídeos já feitos (ver ENTREGA E APROVAÇÃO para o acrescentar no fim).

TEMAS (FOCO: FINANÇAS PESSOAIS E CONTABILIDADE DE EMPRESAS)
- Orçamento do Estado: enquanto estiver em proposta, discussão ou votação, não se fala dele (nem propostas, nem votações, nem medidas anunciadas). Depois de a lei do Orçamento estar publicada em Diário da República, pode falar-se das medidas fiscais que entraram em vigor (por exemplo, o que muda no IRS), só da medida, com a fonte no Diário da República ou no Portal das Finanças e seguindo a IMPARCIALIDADE.
- Dá preferência a dois grandes blocos:
  (1) Finanças pessoais: orçamento familiar, poupança, crédito e juros, cartões, contas bancárias, IRS do dia a dia, recibo de vencimento, primeiro emprego, estudantes.
  (2) Contabilidade de empresas e trabalhadores independentes: IVA, IRC, faturação e faturas, e-fatura, SAF-T, contabilidade organizada e regime simplificado, recibos verdes, Segurança Social dos independentes, abrir atividade ou empresa, prazos declarativos de empresas.
- O tema segue a série da grelha. Dá preferência a temas que continuam úteis daqui a um ano (como funciona, como se calcula, como se lê um documento), que as pessoas guardam e partilham. As notícias seguem a regra da GRELHA SEMANAL. Nunca forçar um tema fraco. Exemplos de temas de ensinar: diferença entre cartão de débito e de crédito; o que é a retenção na fonte; como ler um recibo de vencimento; o que é a TAEG; o que é uma conta de serviços mínimos bancários; o que é o IVA e quem o entrega ao Estado; o que é o SAF-T; diferença entre regime simplificado e contabilidade organizada; o que muda ao abrir atividade nas Finanças; o que distingue uma conta para empresa de uma conta pessoal. Não repitas temas já usados.
- Fontes para temas de ensinar: Portal do Cliente Bancário e Portal "Todos Contam" do Banco de Portugal, Portal das Finanças, Segurança Social, gov.pt, ePortugal, IAPMEI, Ordem dos Contabilistas Certificados, DECO Proteste. Não compares bancos pelo nome nem recomendes produtos de um banco.

IDEIAS NÃO PUBLICADAS (REAPROVEITAR)
- No histórico, as linhas que terminam com "| não publicada" são ideias que o utilizador não chegou a publicar. Podem ser reaproveitadas noutro dia, de preferência nos dias sem notícia forte.
- Antes de reaproveitar, volta a abrir a fonte e confirma que tudo continua certo. Se a ideia dependia de um prazo ou de uma data que já passou, não a reaproveites.
- Ao reaproveitar, podes manter o tema mas faz um desenho novo, e acrescenta no histórico uma linha nova com a data de hoje e "(reaproveitada de DD/MM)" na coluna do tema.

SÁBADO: CURIOSIDADE CONTADA COMO HISTÓRIA (CARROSSEL)
- O dia da semana da publicação vem do hoje.py (pub_dia_semana). Quando a publicação é ao sábado (proposta preparada na sexta à noite), não há notícia nem prazo. A publicação é uma curiosidade de um dos dois blocos, contada como uma pequena história num carrossel de 6 a 8 imagens.
- Exemplos do género (são só exemplos, escolhe um tema que ainda não esteja no histórico): porque é que existe o IRS e de onde veio; a importância de poupar (alguém recebe o salário, paga as despesas do mês, surge um imprevisto, o que muda quando há uma reserva); porque é que se paga IVA; de onde vem a palavra "imposto"; como apareceram os recibos verdes; para que serve o NIF.
- Estrutura de história: a imagem 1 é o gancho, uma afirmação curiosa ou uma situação que dá vontade de passar à seguinte (nunca uma pergunta retórica do tipo "Sabia que...?"); as imagens do meio contam a história passo a passo, uma ideia por imagem, por ordem; a penúltima dá a explicação prática; a última fecha com a ideia principal numa frase.
- Os desenhos de cada imagem são novos, mas ligados entre si para parecer uma sequência: a mesma figura genérica em traço simples, o mesmo mealheiro, o mesmo documento, a evoluir de imagem para imagem.
- Texto de cada imagem com menos de 100 caracteres, com no máximo uma parte entre parênteses retos para o âmbar.
- A REGRA MAIS IMPORTANTE vale para tudo: datas, origens históricas e explicações têm de vir de fonte lida (por exemplo Portal das Finanças, Portal "Todos Contam" do Banco de Portugal, Plano Nacional de Formação Financeira, Diário da República, gov.pt, ePortugal). Se não encontrares fonte que confirme a história, escolhe outro tema de curiosidade.
- Aos sábados há só uma opção (Opção única) e não há vídeo, porque o carrossel já é a história.
- Na mensagem: "Formato: carrossel de N imagens (história)" e, em "Texto da imagem", uma linha por imagem: "Imagem 1: ...", "Imagem 2: ...", etc.
- No passo 5, o dados.json tem 6 a 8 entradas em "slides", cada uma com o seu texto e o seu svg. No passo 5e abre com Read todas as slide_N.png, não só a primeira. No passo 7 envia todas as imagens do carrossel, por ordem, numa só chamada.
- No histórico, o tipo é "curiosidade" e na ideia visual descreve a sequência em poucas palavras.

UMA OU DUAS OPÇÕES DE TEMA
- Se houver só um tema forte, prepara uma ideia (Opção única).
- Se houver vários temas fortes no dia, prepara DUAS opções (Opção A e Opção B), de preferência uma de finanças pessoais e outra de contabilidade de empresas, para o utilizador escolher. Cada opção tem o seu tema, texto da imagem, imagem, descritivo, texto alternativo, story (com a sua imagem) e fonte. Nunca mais de duas.
- Aos sábados, só uma opção (ver secção SÁBADO).

REGRA DOS VÍDEOS (O REEL DE SEXTA)
- Há um vídeo por semana: a publicação de sexta é um Reel, um vídeo em história (passo 6) sobre um tema de ensinar que ganhe com movimento (um processo com passos, uma linha do tempo, algo que muda de estado). Nos outros dias não há vídeo, salvo se o utilizador o pedir.
- O Reel tem uma capa: gera-a com o story.py (1080x1920), com a etiqueta "Aprender · tema" e o texto = a frase principal do vídeo (menos de 70 caracteres), e grava-a como capa.png.
- A legenda do Reel segue as regras do descritivo. O texto alternativo é uma descrição do vídeo em 1 ou 2 frases.
- No estado.json, a opção do Reel tem "formato":"Reel", "video": o endereço público do mp4, "capa": o endereço público da capa.png e "imagens": [o endereço da capa].
- No Telegram, envia a capa com send_photo e põe o endereço público do vídeo na mensagem, na linha "Vídeo (ficheiro):".
- Se o vídeo falhar ao gerar, propõe o mesmo tema como carrossel Aprender e diz porquê.

SEMPRE EM PORTUGUÊS DE PORTUGAL
- Toda a mensagem em português europeu, com a ortografia do Acordo Ortográfico em vigor em Portugal.
- Nada de brasileirismos. Usa: "está a fazer" (nunca "está fazendo"), "equipa", "registo", "ficheiro", "telemóvel", "facto", "contacto", "receção", "autocarro", "ecrã", "utilizador", "comunicação social" (não "mídia"), "subtil" (não "sutil"). Nunca "você" nem "a gente": usa a terceira pessoa sem pronome ("Se recebe salário...") ou "o contribuinte".
- Evita gerúndios no fim das frases ("reforçando", "garantindo", "permitindo", "refletindo"). Em português de Portugal usa "a + infinitivo" ou divide em duas frases.
- Siglas: na primeira vez que aparece uma sigla menos conhecida (por exemplo SAF-T, TAEG, IES, IRC, NIPC, CAE), escreve-a por extenso ou explica-a numa frase curta, na imagem ou no descritivo. IVA, IRS e NIF não precisam.

SEM LINGUAGEM DE IA (guias da Wikipédia sobre sinais de texto gerado por IA, em inglês e em português)
Não usar nenhum destes padrões:
1. Vocabulário típico de IA: crucial, fundamental, essencial, robusto, abrangente, potenciar, alavancar, otimizar, mergulhar, desbloquear, aprofundar, intrincado, panorama, cenário atual, fomentar, promover, reforçar, sublinhar, destacar, evidenciar, testemunho, marco, decisivo, determinante, fascinante, deslumbrante, majestoso, diverso, "momento crucial", "desempenha um papel", "no panorama atual", "num mundo cada vez mais".
2. Importância e simbolismo exagerados: "é um marco", "representa algo maior", "tem um significado especial", "representa um ponto de viragem", "deixa uma marca duradoura", "profundamente enraizado", "demonstra o compromisso", "refletindo a relevância contínua". Também não exagerar o destaque que um tema teve na comunicação social.
3. Tom promocional ou vago de publicidade: "imperdível", "incrível", "extraordinário", "não perca", "o seu parceiro de confiança", "fazemos a diferença".
4. Comentários do autor e cautelas a mais: "é importante notar", "é importante lembrar", "vale a pena referir", "vale a pena notar", "convém lembrar", "importa sublinhar", "embora isso possa variar", "até certo ponto", "neste artigo".
5. Excesso de conectores: "além disso", "adicionalmente", "por outro lado", "no entanto", "deste modo", "assim sendo", "no geral". No máximo um por mensagem.
6. Paralelismos negativos e previsíveis: "não é X, é Y", "não se trata apenas de X, mas de Y", "não só... como também", "não só... mas também".
7. Análises vazias no fim da frase: "...o que reforça a importância de...", "...contribuindo para...", "...refletindo...".
8. Atribuições vagas: "especialistas dizem", "segundo vários analistas", "há quem defenda", "estudos mostram". Diz sempre quem disse, com fonte (instituição, nunca partido).
9. Regra de três: não agrupar adjetivos ou ideias em grupos de três.
10. Falsas escalas: "desde X até Y" quando não há escala real.
11. Resumos forçados: "Em suma", "Em resumo", "Em conclusão", "Concluindo", "No fundo", "No geral".
12. Travessões (— ou –): nunca. Usa vírgula, dois pontos, ponto final ou parênteses.
13. Formatação a mais: sem negrito, sem emojis, sem listas com "Título: explicação" que repetem o título.
14. Perguntas retóricas de abertura ("Sabia que...?", "Já pensou em...?") e frases de efeito no fim.
15. Texto polido de forma repetitiva: frases todas com o mesmo tamanho ou a começar da mesma maneira.
Escreve como um contabilista a explicar algo a um colega: frases curtas, factos concretos, sem adjetivos desnecessários. Antes de enviar, verifica a mensagem contra esta lista e reescreve o que falhar.

ESTILO VISUAL (imagem, story e vídeo, aspeto natural, sem cara de IA)
- Estética de ilustração editorial com toques feitos à mão: sublinhado irregular a âmbar por baixo do destaque, linha pontilhada irregular por cima do rodapé, textura de papel muito leve e desenhos de traço à mão (os scripts já aplicam o traço irregular).
- Nunca usar caixas retangulares perfeitas como moldura de texto, cartões de interface, sombras, gradientes, fotografias, ícones genéricos ou visual de apresentação de empresa.
- Usar só as cores da marca (azul #17324D, branco #FFFFFF, creme #F7F5F0, âmbar #E09F3E) e a letra Manrope. No SVG usa "FG" para a cor do traço principal, "BG" para preencher com a cor do fundo e "#E09F3E" (imagem e story) ou "AM" (vídeo) para o âmbar. Não inventar outras cores.
- Texto curto, com espaço livre. Uma ideia por imagem ou por cena.
- Sem numeração de slides. O rodapé tem só "bem.contado" à esquerda e "@bem.contadopt" à direita.
- Na etiqueta, para temas de ensinar usa "Aprender · [tema em 1 ou 2 palavras]". Para as curiosidades usa "Curiosidade · [tema em 1 ou 2 palavras]". No story usa "Pergunta · [tema]" ou "Quiz · [tema]".
- Personagens: só figuras genéricas desenhadas à mão (por exemplo uma pessoa em traço simples), sem nome e sem parecer um caso concreto. Nunca personagens conhecidos, mascotes ou logótipos de marcas, bancos ou entidades.

CONTEXTO
- bem.contado (@bem.contadopt no Instagram) é um projeto de escritório de contabilidade e consultadoria em Portugal que ainda está a começar (ainda não abriu). O Instagram serve para criar confiança com conteúdo informativo e prático, com foco em finanças pessoais e contabilidade de empresas.
- Não se fazem promessas de poupança nem de reembolsos, não se comparam outros escritórios, não se identifica nenhum cliente, e não se falam de casos concretos.
- O utilizador não publica obrigatoriamente todos os dias. Quando não publica, avisa e a linha do histórico fica marcada como "não publicada".

DESCRITIVO PARA O INSTAGRAM COM VALOR PARA AS PESSOAS
- O descritivo tem de trazer pelo menos uma curiosidade, explicação ou dado prático útil: uma medida que beneficia as pessoas ou as empresas, um direito, um prazo, um valor concreto ou uma explicação simples de um conceito.
- A primeira frase diz logo a quem diz respeito ou o que se vai aprender, e tem menos de 125 caracteres (é o que aparece no feed antes do "mais"). Não começar por "O Ministério anunciou a..." nem pela data.
- Não citar jornais pelo nome dentro do descritivo; os links ficam no campo Fonte.
- Diz a quem se aplica, com as mesmas condições e cautelas da fonte. Se a medida ainda não é lei, diz isso claramente.
- Sem promessas de poupança. Segue a secção IMPARCIALIDADE.
- Guardar ou enviar (só quando faz sentido): quando a publicação ensina algo que é mesmo útil para as pessoas, acaba o descritivo, antes das hashtags, com uma frase curta a pedir para guardar ou para enviar a quem possa servir, ligada ao tema (por exemplo "Guarde para quando chegar o prazo." ou "Envie a quem está a abrir atividade."). No carrossel de ensinar ou de sábado, essa frase pode ir também na última imagem. Não é obrigatório: nas notícias simples ou quando soar forçado, não ponhas. Varia a frase e vê no histórico para não repetir a dos últimos dias.
- No fim, uma linha com 3 a 5 hashtags simples, escolhidas para o tema do dia (nunca uma lista fixa repetida). Nunca hashtags de partidos ou políticos.
- O mesmo descritivo serve para a imagem e para o vídeo da mesma opção. É enviado na mensagem do Telegram e é o texto que vai para o Instagram se for aprovado.

PUBLICAÇÃO E INTERAÇÃO
- Hora de publicação (em teste): 13h00 de segunda a sexta, 18h00 ao sábado (linha pub_publicar_as do hoje.py). Indica-a na linha "Publicar às" com o dia e a data (por exemplo "segunda, 23/11, às 13h00"). Nos dias de só story não há publicação automática: escreve "Publicar às: story à mão na terça, 24/11, à hora que quiserem".
- Story do dia: para cada opção, um story ligado ao tema, com imagem própria (passo 5f) e um autocolante interativo do Instagram para o utilizador acrescentar na aplicação: sondagem (pergunta e 2 opções), quiz (pergunta, 3 ou 4 opções e a resposta certa) ou caixa de perguntas (uma frase a convidar a deixar dúvidas sobre o tema). A pergunta aparece escrita na imagem; as opções vão no autocolante, por isso a imagem deixa livre a zona do meio para baixo. A resposta certa de um quiz tem de vir da fonte lida. Nada sobre política. No autocolante do story é permitido fazer uma pergunta direta.
- Texto alternativo: para cada imagem da publicação, uma descrição de 1 ou 2 frases do que se vê e do texto principal, que vai gravado automaticamente no campo "Texto alternativo" de cada imagem quando a publicação sai (acessibilidade). Sem prefixos nem aspas no texto em si.

FUNDO (alterna por publicação feita; vale para as imagens, o story e o vídeo)
Usa o fundo da linha pub_fundo do scripts/hoje.py (não decidas de cabeça). É o contrário do fundo da última publicação feita, para o perfil manter o padrão azul/branco mesmo nos dias sem publicação. Grava o fundo usado no estado.json (campo "fundo"). Nos dias de só story, o story usa o pub_fundo (os stories não contam para o padrão do perfil).
- Fundo AZUL #17324D: texto creme, destaque em âmbar #E09F3E.
- Fundo BRANCO #FFFFFF: texto azul #17324D, destaque em âmbar #E09F3E.

PASSOS
1. Prepara o branch claude/publicacoes em /tmp/pub (ver ENTREGA E APROVAÇÃO) e corre python3 "$REPO/scripts/hoje.py" --pub /tmp/pub/publicacoes. Usa as linhas pub_* em tudo (data, dia da semana, série, fundo, hora). Lê "historico_publicacoes.md" (incluindo as ideias marcadas "não publicada") e "publicacoes/ideias.md". Escolhe o tema segundo a série do dia (GRELHA SEMANAL): para Prazos, abre a agenda fiscal do Portal das Finanças e a Segurança Social para a semana pub_semana; para Aprender, Reel e Curiosidade, escolhe um tema ainda não usado e procura fontes; nos dias de só story, um tema curto (um prazo próximo ou uma pergunta ligada à última publicação). Pesquisa também se há alguma notícia que mude alguma coisa para as pessoas (regra das notícias na GRELHA SEMANAL). Dá prioridade a fontes oficiais (Portal das Finanças, Diário da República, Segurança Social, gov.pt, Banco de Portugal) e a jornais económicos portugueses. Abre e lê a página da fonte principal de cada opção antes de escrever.
2. Decide a RECOMENDAÇÃO DO DIA (a de base vem da grelha). Escolhe o tema (ou os dois temas) segundo as secções TEMAS, IDEIAS NÃO PUBLICADAS, SÁBADO, UMA OU DUAS OPÇÕES, IMPARCIALIDADE e SEMPRE ALGO NOVO. Há vídeo só quando a publicação é à sexta (REGRA DOS VÍDEOS).
3. Escreve a mensagem em português de Portugal, em texto simples. Com uma só opção, usa este formato; com duas, repete o bloco a partir de "Tema" para cada uma, com os títulos "Opção A" e "Opção B". Com "Só story", omite as linhas Formato, Texto da imagem, Vídeo, Descritivo e Texto alternativo. Com "Não publicar hoje", escreve só o cabeçalho, a linha Recomendação e, se houver, "Guardada para outro dia: [ideia]".

Proposta para [dia da semana, data da publicação] · [série]

Recomendação: [Publicação + story / Só story / Não publicar hoje], porque [uma frase]

Tema: [uma linha]
Porquê este tema: [uma ou duas frases sobre a notícia ou prazo, com o número ou data concreta; ou, se for tema de ensinar ou curiosidade, porque é útil ou interessante]
Formato: [imagem única, ou carrossel de N imagens, ou Reel de N segundos]
Fundo: [azul ou branco, com as cores do texto e do destaque]
Publicar às: [dia, data e hora; nos dias de só story, "story à mão"]
Texto da imagem: [o texto da imagem; no carrossel, uma linha por imagem: "Imagem 1: ...", "Imagem 2: ..."]
Vídeo: [só se houver: uma linha por cena, com o texto da cena e o que acontece no desenho]

Descritivo para o Instagram:
[3 a 5 frases curtas, prontas a copiar e colar, a frase de guardar ou enviar quando fizer sentido, e a linha de hashtags]

Texto alternativo:
[uma linha por imagem: "Imagem 1: ..." ou só a descrição se for imagem única]

Story: [sondagem, quiz ou caixa de perguntas]: [pergunta escrita na imagem] | [opções do autocolante, e no quiz a resposta certa] (a imagem do story vai no Telegram; o autocolante coloca-se na zona livre a meio, na aplicação)

Fonte: [link da fonte principal, ou um link por linha]
Conta verificada: [só se houver contas: as contas feitas com python3]
Por confirmar: [só se houver factos que não conseguiste confirmar numa fonte]

4. Grava a mensagem do passo 3 em mensagem.txt e, depois do passo 5, corre python3 "$REPO/scripts/verificar.py" mensagem.txt dados*.json (todos os dados_*.json que existirem). Corrige todos os ERROS e volta a gerar o que for preciso até não haver nenhum; lê os AVISOS e decide caso a caso. O script não verifica factos, por isso faz também estas verificações em cada opção: (a) cada frase (incluindo os textos do vídeo, de todas as imagens do carrossel e do story) está apoiada na fonte lida; (b) português de Portugal; (c) nenhum padrão da lista "SEM LINGUAGEM DE IA"; (d) o descritivo tem uma curiosidade, explicação ou dado prático útil; (e) nada sobre o Orçamento do Estado; (f) nada de partidos, políticos ou opinião política; (g) siglas menos conhecidas explicadas na primeira vez; (h) a frase de guardar ou enviar só aparece se fizer sentido e não repete a dos últimos dias; (i) termos técnicos exatos e "em regra" onde há exceções; (j) contas verificadas com python3 e escritas na mensagem; (k) cada ilustração explica a ideia sem o texto, com os números no desenho quando há exemplo; (l) factos não confirmados listados em "Por confirmar:". Se alguma falhar, reescreve.
   REVISÃO INDEPENDENTE (depois do verificar.py e com tudo gerado): lança um subagente (ferramenta Agent ou Task) com contexto limpo e dá-lhe a mensagem, os caminhos das imagens (slide_N.png, story.png, capa.png, video_cena_N.png), os links das fontes e as secções REGRA MAIS IMPORTANTE e RIGOR PROFISSIONAL deste ficheiro. Pede-lhe que leia como um contabilista certificado exigente: abre as fontes e confirma cada facto e cada número; confirma os termos técnicos e se falta um "em regra"; olha para cada imagem e diz se o desenho explica a ideia sem o texto; e devolve uma lista de problemas concretos, ou "sem problemas". Corrige o que ele encontrar e, se mudaste alguma coisa, volta a correr o verificar.py. No máximo duas rondas; o que ficar por resolver vai para a linha "Por confirmar:". Se não houver ferramenta de subagentes, faz tu essa leitura no fim, como se fosses outra pessoa.

5. GERAR AS IMAGENS (publicação: 1080x1350 px, uma por opção, ou uma por imagem no carrossel; story: 1080x1920 px, um por opção). Com "Só story", faz só os passos 5a e 5f. Com "Não publicar hoje", salta os passos 5 e 6.
a) Se python3 -c "import playwright" falhar, instala com pip install -q playwright (não corras playwright install: os scripts encontram o Chromium já instalado). Na pasta de rascunho (scratchpad), cria uma pasta "img" e obtém a letra Manrope pelo npm (o Google Fonts está bloqueado pelo proxy): npm pack @fontsource/manrope@5.0.20 e depois tar xzf fontsource-manrope-5.0.20.tgz. Os ficheiros ficam em package/files.
b) Escreve dados.json: {"fundo":"azul" ou "branco", "etiqueta":"[tema curto · mês ano, ou Aprender · tema, ou Curiosidade · tema]", "slides":[{"texto":"...", "svg":"[desenho novo em SVG]"}]}. No texto, a parte a destacar em âmbar vai entre parênteses retos (no máximo uma, curta). Texto com menos de 100 caracteres. Com duas opções, faz um dados_A.json e um dados_B.json e corre o script para cada um em pastas diferentes (A e B). No carrossel, "slides" tem uma entrada por imagem (6 a 8 ao sábado, 4 a 6 nos outros dias).
c) O "svg" é um desenho novo, feito de raiz para o tema, só com <path>, <circle>, <ellipse>, <line> e <g> (sem texto dentro do desenho, salvo um número ou sigla curta com font-family="M"). Coordenadas: a zona do desenho tem 1080 de largura e 360 de altura (o topo da zona está a 760 px do topo da imagem); desenha mais ou menos entre x=280 e x=800 e entre y=0 e y=340. Traço principal stroke="FG" com stroke-width entre 5 e 7, um ou dois elementos de destaque com stroke="#E09F3E", sem preenchimento (fill fica "none" por defeito; usa fill="BG" só para tapar linhas que ficam atrás). Linhas simples, poucas formas, ligeiramente imperfeitas, como se fosse desenhado à mão.
d) Corre o script do repositório (não o reescrevas): python3 "$REPO/scripts/gerar.py" dados.json package/files PASTA_DE_SAIDA

e) Abre cada slide_N.png com a ferramenta Read (todas, no caso do carrossel) e confirma: letra Manrope (sem serifas), texto sem cortes, sublinhado à mão por baixo do destaque, desenho legível e reconhecível, sem tocar no texto nem no rodapé, cores certas do fundo do dia, sem erros de ortografia. No carrossel, confirma também que as imagens seguem a ordem da história e que os desenhos parecem uma sequência. Se o desenho estiver confuso, simplifica-o e volta a gerar.
f) STORY (sempre que a recomendação inclua story, um por opção). Escreve dados_story.json: {"fundo": o mesmo do dia, "etiqueta":"Pergunta · tema" ou "Quiz · tema", "texto":"[a pergunta do story, menos de 70 caracteres, com no máximo uma parte entre parênteses retos para o âmbar]", "topo_desenho":760, "svg":"[desenho pequeno e novo, ligado ao tema, com as mesmas regras do passo 5c mas mais simples]"}. O desenho fica entre y=760 e y=1060 da imagem; a zona entre y=1080 e y=1500 fica vazia para o autocolante; o rodapé fica por cima da zona de baixo do ecrã. Corre o script do repositório: python3 "$REPO/scripts/story.py" dados_story.json package/files story.png (com duas opções, story_A.png e story_B.png). Depois abre a imagem com Read e confirma o mesmo que no passo 5e e que a zona do autocolante está vazia.

6. VÍDEO EM HISTÓRIA (só se no passo 2 decidiste fazer vídeo segundo a REGRA DOS VÍDEOS; nunca ao sábado).
a) Planeia uma pequena história de 15 a 25 segundos, em 4 a 6 cenas de 3 a 5 segundos. Cada cena tem: um texto curto (menos de 70 caracteres, com no máximo uma parte entre parênteses retos para o âmbar) e um desenho novo com uma ação física real que tem início, movimento e desfecho (por exemplo: uma figura em traço simples recebe um papel; um cartão sai de uma carteira; folhas de calendário voam; uma linha do tempo enche-se; um documento entra num ecrã e aparece um visto). A história avança de cena para cena (situação, dúvida, explicação, resposta prática). A última cena fecha com a ideia principal.
b) Regras de realização: câmara na mão leve (o script já faz um balanço pequeno e uma aproximação de 1%); cortes secos entre cenas; nada de zoom contínuo, rotações sem motivo ou efeitos artificiais; os traços desenham-se um de cada vez, em momentos diferentes, como alguém a desenhar; os objetos que se mexem fazem um só movimento claro. Sem som. Todos os textos do vídeo seguem a REGRA MAIS IMPORTANTE.
c) Escreve dados_video.json: {"fundo":"azul" ou "branco" (o mesmo da imagem), "etiqueta":"Aprender · tema", "cenas":[{"dur":4, "texto":"...", "svg":"..."}, ...]}.
d) O "svg" de cada cena usa coordenadas do ecrã inteiro (1080 de largura, 1920 de altura); a zona livre para desenhar fica entre x=120 e x=960 e entre y=980 e y=1560 (o texto fica em cima e o rodapé em baixo). Cores: "FG", "BG" e "AM" (âmbar). Animação, com tempos em segundos desde o início da cena (o texto entra nos primeiros 0,15 a 1 segundo, por isso os desenhos começam por volta de 0,9 s):
   - Traço que se desenha: <path class="dr" data-s="INICIO" data-d="DURACAO" pathLength="1" d="..." stroke="FG" stroke-width="6"/> (também funciona em <circle> e <ellipse> com class="dr", data-s, data-d e pathLength="1").
   - Grupo que se move: <g class="mv" data-s="INICIO" data-d="DURACAO" data-from="x,y,rotacao,opacidade" data-to="x,y,rotacao,opacidade" data-c="cx,cy"> ... </g> (desloca o grupo de data-from para data-to, rodando à volta de cx,cy; usa opacidade 0 no início para o grupo aparecer).
   - Elemento que aparece de repente: class="ap" data-s="INICIO" (por exemplo um <text font-family="M" font-weight="700" font-size="46" fill="FG"> curto).
e) Corre o script do repositório (não o reescrevas), dentro da pasta de trabalho do vídeo: python3 "$REPO/scripts/video.py" dados_video.json package/files bemcontado_video.mp4

f) Depois de correr, abre com Read cada video_cena_N.png (a última imagem de cada cena) e confirma que o desenho se percebe, não toca no texto nem no rodapé e que os textos estão certos. Extrai também um fotograma a meio de cada cena com ffmpeg (ffmpeg -ss SEGUNDOS -i bemcontado_video.mp4 -frames:v 1 meio_N.png) e confirma que o movimento está a acontecer. Se algo falhar, corrige o SVG dessa cena e volta a gerar (no máximo duas vezes).
g) Se o vídeo falhar, não pares: segue com as imagens e os descritivos e indica o erro no fim.

ENTREGA E APROVAÇÃO

Repositório e ficheiros
- O repositório é github.com/Pedrooruben1/Escrit-rio-de-contabilidade (público). REPO é a pasta onde está clonado. Todo o conteúdo do Instagram (imagens, estado do dia e histórico) vive no branch claude/publicacoes. Os scripts e estas regras vivem no branch por defeito.
- Antes de escrever no branch, prepara-o numa pasta à parte: cd "$REPO" && git fetch origin claude/publicacoes && git worktree add -f /tmp/pub -B claude/publicacoes origin/claude/publicacoes (se /tmp/pub já existir, entra nela e faz git pull --rebase origin claude/publicacoes). Trabalha sempre em /tmp/pub. Antes de cada push faz git pull --rebase origin claude/publicacoes. Push com git push origin claude/publicacoes (até 4 tentativas, com espera de 2, 4, 8 e 16 segundos se a rede falhar).
- Endereço público de um ficheiro: https://raw.githubusercontent.com/Pedrooruben1/Escrit-rio-de-contabilidade/claude/publicacoes/CAMINHO
- Pasta do dia: publicacoes/AAAA-MM-DD/, com a data da publicação (linha pub_data_iso). Com duas opções, subpastas A/ e B/. Nomes: slide_1.png, slide_2.png, ..., story.png, video.mp4. Numa nova proposta do mesmo dia (ver REVISÃO), usa a subpasta p2/, p3/, etc. (com A/ e B/ dentro, se houver duas opções).
- Estado do dia: publicacoes/AAAA-MM-DD/estado.json, com este formato:
  {"data":"AAAA-MM-DD", "serie":"prazos|aprender|reel|curiosidade|story", "fundo":"azul" ou "branco", "publicar_as":"13:00" ou "18:00", "proposta":1, "estado":"pendente", "enviado_em":null, "tentativas":0, "opcao_aprovada":null, "publicar_video":false, "media_id":null, "permalink":null, "ultima_resposta":null,
   "opcoes":{"A":{"tema":"...", "formato":"...", "imagens":[URL,...], "video":URL ou null, "capa":URL ou null, "story":URL ou null, "descritivo":"texto completo com hashtags", "texto_alternativo":["..."], "story_texto":"linha Story"}}}
  Com uma só opção, a chave é "A". Estados possíveis: pendente, aprovada, publicada, recusada, nao_publicar (opção 3 da recomendação), so_story (dia sem publicação no feed: não há nada para aprovar).

7. GUARDAR NO REPOSITÓRIO: copia as imagens, o story e o vídeo para a pasta do dia, escreve o estado.json e faz commit ("Ideia de DD/MM") e push. Confirma com curl -s -o /dev/null -w "%{http_code}" que o endereço público da primeira imagem dá 200 (pode demorar até um minuto; tenta de 15 em 15 segundos, no máximo 8 vezes). Se nunca der 200, segue na mesma e indica o problema na mensagem do Telegram.

8. ESPERAR ATÉ ÀS 19h00 (só na execução da véspera; numa REVISÃO envia logo). Vê a hora de Lisboa com TZ=Europe/Lisbon date +%H:%M:%S. Se for antes das 19h00:00, espera com sleep até essa hora (cada chamada de Bash tem limite de 10 minutos).

9. ENVIAR PARA O TELEGRAM pelo Zapier (app Telegram, sempre chat_id "-1003970082558", grupo "Contabilidade"; não envies para nenhum outro chat). Confirma os schemas com inspect_zapier_actions antes de executar.
   a) Para cada opção, por ordem: cada imagem da publicação com a ação send_photo (photo = endereço público, caption = "Opção A, imagem 1 de N" ou "Imagem 1 de N" se for opção única), depois a imagem do story (caption "Story, opção A" ou "Story"). Num Reel, envia a capa como foto (caption "Capa do Reel") e põe o endereço público do vídeo na mensagem, na linha "Vídeo (ficheiro):".
   b) Depois, uma mensagem de texto com a ação send_message (format "plaintext", disable_link_preview "true"): a mensagem do passo 3, e no fim estas linhas:
      Para responder:
      sim (ou sim A / sim B) para publicar [dia] às [hora]
      não, para não publicar
      não, seguido do que prefere (por exemplo "não, quero algo sobre IVA para independentes"), para receber outra proposta
      altera, seguido do que mudar (por exemplo "altera, a primeira frase está longa"), para corrigir esta proposta
      ideia, seguido de um tema, para o guardar para outro dia
      Nos dias de só story, em vez destas linhas: "Story para [dia, data]: publicar à mão. Não precisa de resposta; para outra proposta, não, seguido do que preferem." e grava o estado "so_story".
   c) Com "Não publicar hoje", envia só a mensagem curta (sem fotos) e grava o estado "nao_publicar".
   d) Depois de enviar, grava em "enviado_em" a hora de envio em UTC (date -u +%Y-%m-%dT%H:%M:%SZ), faz commit e push do estado.json.

10. HISTÓRICO: acrescenta ao historico_publicacoes.md (no branch claude/publicacoes) uma linha por opção, com: data | tema | tipo (notícia/ensinar/curiosidade/só story) | bloco (finanças pessoais/empresas) | ideia visual | vídeo (sim/não) | frase de guardar/enviar (a usada, ou "nenhuma") | estado. O estado começa como "pendente"; a tarefa das respostas muda-o para "publicada" ou "não publicada". Com "Não publicar hoje", acrescenta "data | sem publicação | motivo". Commit e push.

11. Envia uma notificação com PushNotification: a recomendação, tema(s), se houve vídeo ou carrossel e que a proposta está no Telegram à espera de resposta (ou o erro).

12. Se o Zapier ou o Telegram falharem, não tentes outros meios de envio. Termina indicando o erro na notificação.

REVISÃO (quando o utilizador responde "não, ..." ou "altera, ...")
- Usa estas regras na íntegra, com o pedido do utilizador como orientação principal (o tema, o formato ou a correção que pediu), sem desobedecer a nenhuma regra (fontes lidas, imparcialidade, português de Portugal, sem linguagem de IA, fundo do dia).
- "altera, ...": mantém o tema e muda só o que foi pedido. "não, ...": prepara uma proposta nova (uma ou duas opções) segundo o que o utilizador escreveu.
- A proposta revista é para o mesmo dia de publicação do estado.json que está a ser revisto: usa os campos data, serie, fundo e publicar_as desse estado.json, não os do hoje.py (que se referem ao dia seguinte ao da execução).
- Aplica também a REVISÃO INDEPENDENTE do passo 4.
- A mensagem do Telegram começa com "Nova proposta para [dia, data] (n.º N)". Grava as imagens na subpasta pN/, atualiza o estado.json (proposta = N, estado "pendente" ou "so_story", opcoes novas) e envia logo, sem esperar pelas 19h00.
- No histórico, substitui as linhas de hoje pelas da nova proposta (estado "pendente"). As propostas recusadas não ficam no histórico.
