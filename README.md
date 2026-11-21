# bem.contado

Material de apoio ao Instagram @bem.contadopt: os scripts que geram as imagens da ideia diária, uma verificação automática do texto e respostas-tipo para comentários e mensagens.

As propostas diárias vão para o grupo de Telegram e só são publicadas no Instagram depois de aprovadas lá. Ver `docs/configuracao.md`.

O branch `claude/publicacoes` guarda as imagens de cada dia (é daí que vêm os links públicos usados pelo Telegram e pelo Instagram), o estado de aprovação e o histórico.

## Estrutura

```
scripts/
  gerar.py       imagens da publicação (1080x1350), uma por slide
  story.py       imagem do story (1080x1920), com a zona do autocolante livre
  video.py       vídeo em história (1080x1920, mp4)
  verificar.py   verifica a mensagem do dia e os dados*.json antes de publicar
  hoje.py        dia da publicação (o seguinte), série da grelha, fundo e hora
config/
  aprovadores.txt   quem pode dar comandos no grupo (vazio = todos)
site/
  index.html, estilo.css, site.js   site bemcontadopt.pt (versão "a abrir em breve")
  fonts/, favicon.svg, og.png         letra Manrope, ícone e imagem de partilha
prompt/
  regras.md                 todas as regras da ideia diária (lidas pelas tarefas)
  tarefa-ideia.md           prompt da tarefa da véspera (18h37)
  tarefa-respostas.md       prompt da tarefa de hora a hora (respostas, publicação, comentários, controlos)
  ideia-diaria.md           prompt antigo, de 20/11/2026 (referência)
  alteracoes-propostas.md   alterações ao prompt antigo (já incluídas em regras.md)
docs/
  configuracao.md           como funciona o fluxo: horários, grelha, comandos, controlos
  respostas-tipo.md         bases para responder a comentários e mensagens
exemplos/
  dados.json, dados_story.json, mensagem-boa.txt, mensagem-com-erros.txt
```

As tarefas agendadas clonam este repositório e correm os scripts daqui. Mudar uma regra ou um script aqui muda o comportamento da tarefa seguinte.

## Correr localmente

Precisa de Python 3.10 ou mais recente, Playwright com Chromium e, para o vídeo, ffmpeg.

```
pip install playwright && playwright install chromium
npm pack @fontsource/manrope@5.0.20 && tar xzf fontsource-manrope-5.0.20.tgz

python3 scripts/gerar.py exemplos/dados.json package/files .
python3 scripts/story.py exemplos/dados_story.json package/files story.png
```

## Verificar o texto antes de publicar

```
python3 scripts/verificar.py mensagem.txt dados.json dados_story.json
```

A mensagem tem o formato do passo 3 do prompt ("Recomendação:", "Descritivo para o Instagram:", "Texto alternativo:", "Story:", "Fonte:").

Dá **erro** (código de saída 1) quando encontra:

- travessões, emojis, caracteres invisíveis ou negrito;
- palavras e expressões da lista "sem linguagem de IA";
- brasileirismos ("você", "equipe", "está fazendo", "registro", ...);
- nomes de partidos ou referências ao Orçamento do Estado;
- mais de um conector ("além disso", "no entanto", ...);
- primeira frase do descritivo com 125 caracteres ou mais, ou descritivo a abrir com uma pergunta;
- menos de 3 ou mais de 5 hashtags, ou hashtags repetidas;
- texto de imagem com 100 caracteres ou mais (70 no story e no vídeo), ou mais de uma parte em âmbar;
- falta de texto alternativo, story ou fonte quando a recomendação os exige;
- cores fora da marca ou elementos não permitidos nos SVG.

Dá **aviso** para o que precisa de olhos humanos: siglas a confirmar se estão explicadas, gerúndios a fechar frases, "Chega" ou "Livre" com maiúscula, palavras com tom de opinião, frases a começar sempre da mesma maneira.

O script não confirma factos. A regra de não inventar informação continua a depender da leitura da fonte.

## Site (bemcontadopt.pt)

A pasta `site/` é o site da bem.contado na versão "a abrir em breve": apresenta o projeto, o Instagram e a app Poupança, com o email de contacto. Não anuncia serviços, não tem formulário, não faz promessas nem mostra números inventados, e não tem nomes nem números da OCC enquanto a inscrição não estiver feita.

O que o GitHub Pages serve é o branch `claude/site`, que tem os mesmos ficheiros na raiz e o `CNAME` com `bemcontadopt.pt`. Quando mudar alguma coisa em `site/`, é preciso copiar também para esse branch, sem apagar o que lá existe a mais.

Partes automáticas, que só existem no branch `claude/site` e são escritas pela tarefa de publicação (`scripts/site_atualizar.py`):
- `ultima/`: a imagem e os dados da última publicação do Instagram. A página principal mostra-a no lugar do desenho do telemóvel.
- `prazos/`: a página "Prazos da semana", gerada a partir do `prazos.json` da publicação de segunda-feira.
