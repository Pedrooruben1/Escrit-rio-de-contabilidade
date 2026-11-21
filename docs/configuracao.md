# Como funciona o fluxo de publicação

## Dia a dia

1. Às 18h37, a tarefa "Ideia diária (aprovação no Telegram)" prepara a proposta para o dia seguinte, segundo a grelha semanal. Gera as imagens (à sexta, o vídeo), passa tudo pelo verificador e por uma revisão independente, guarda as imagens no branch `claude/publicacoes` (é daí que vêm os links públicos) e às 19h00 envia ao grupo "Contabilidade" as fotos, o story e o texto.
2. Respondem no grupo (comandos abaixo). Um Zap guarda cada mensagem do grupo num ficheiro de texto do Google Drive.
3. A tarefa "Respostas do Telegram (bem.contado)" corre de hora a hora, aos 57 minutos, das 8h57 às 21h57. Lê as respostas novas e:
   - com `sim`, publica à hora marcada (13h00 durante a semana, 18h00 ao sábado; na prática, na execução das 12h57 ou das 17h57) ou logo, se a hora já tiver passado;
   - com `não, ...` ou `altera, ...`, prepara outra proposta e envia-a;
   - às 9h57 e às 18h57, vê os comentários novos no Instagram e propõe respostas;
   - faz os controlos diários (abaixo).
4. O texto alternativo vai com a publicação, pela API do Instagram. Os stories são publicados à mão, porque a API não permite autocolantes.

Uma resposta pode demorar até uma hora a ter efeito: as respostas são lidas de hora a hora.

## Grelha semanal

| Dia | Publicação |
| --- | --- |
| Segunda | Prazos da semana (imagem única ou carrossel de 2 a 4) |
| Terça | Só story |
| Quarta | Aprender: carrossel de 4 a 6 com um exemplo com números |
| Quinta | Só story |
| Sexta | Reel: vídeo animado de 15 a 25 segundos |
| Sábado | Curiosidade: carrossel de 6 a 8 contado como história |
| Domingo | Só story |

Notícias só quando mudam alguma coisa para as pessoas (prazo novo, taxa nova, medida em vigor): podem trocar a série do dia ou entrar num dia de só story.

O fundo alterna por publicação feita (azul, branco, azul...), não por dia, para o perfil manter o padrão.

## Comandos no grupo

| Mensagem | Efeito |
| --- | --- |
| `sim` | Aprova a proposta à espera e publica à hora marcada |
| `sim A` / `sim B` | Aprova a opção indicada, quando há duas |
| `sim hoje` / `sim amanhã` | Quando há duas propostas à espera (a de hoje e a de amanhã) |
| `sim vídeo` | Publica o vídeo como Reel em vez da imagem |
| `não` | Não publica e marca a ideia como "não publicada" |
| `não, quero algo sobre ...` | Gera uma proposta nova com essa orientação |
| `altera, ...` | Corrige a proposta atual |
| `ideia, ...` | Guarda um tema na lista de espera, sem mexer na proposta |
| `r1 sim` / `r1 não` / `r1, texto` | Responde (ou não) ao comentário n.º 1 |

Se `config/aprovadores.txt` tiver nomes, só esses podem dar comandos. Sem nomes, qualquer membro do grupo pode.

## Controlos automáticos

- Às 19h57, se a proposta para o dia seguinte não tiver chegado, aviso no grupo.
- Às 9h57, verificação das tarefas do Zapier: aviso aos 80% do limite e 3 dias antes do fim do teste do plano Pro.
- À segunda, às 9h57, relatório da semana no grupo: seguidores e gostos e comentários de cada publicação. O alcance e os guardados precisam de uma permissão do Instagram que a ligação atual não tem.

## Zapier

A conta está num teste do plano Pro (1000 tarefas) até 2/12/2026; depois passa ao plano gratuito (100 tarefas por mês). Até 23/11/2026 às 17h00, cada chamada das tarefas ao Zapier custa 2 tarefas; a partir daí, segundo o Zapier, custa 0. As mensagens escritas no grupo gastam 1 tarefa cada (é o Zap que as copia para o Drive). No dia 2/12 convém confirmar que tudo continua a funcionar no plano gratuito.

## Peças

| Peça | Onde se gere |
| --- | --- |
| Tarefas "Ideia diária (aprovação no Telegram)" e "Respostas do Telegram (bem.contado)" | claude.ai/code/routines (conector Zapier e este repositório associados) |
| Zap "Telegram message to Google Drive file" | zapier.com |
| Pasta "bem.contado - respostas Telegram" (Drive de bemcontado194@gmail.com) | Google Drive |
| Bot "Contabilidade" (@alertas_revenda_pedro_bot), com a privacidade desligada | Telegram, @BotFather |
| Instagram for Business (ligado pela Página de Facebook da bem.contado) | zapier.com |
| Regras, scripts, verificador, respostas-tipo | este repositório, branch por defeito |
| Imagens, estado de cada dia, histórico, ideias, métricas | branch `claude/publicacoes` |

A tarefa antiga "Ideia diária para o Instagram" está desativada mas não foi apagada: é o plano de recurso.
