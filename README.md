# bem.contado

Material de apoio ao Instagram @bem.contadopt: os scripts que geram as imagens da ideia diária, uma verificação automática do texto e respostas-tipo para comentários e mensagens.

A publicação é feita à mão. Nada neste repositório publica no Instagram nem envia para o Telegram.

## Estrutura

```
scripts/
  gerar.py       imagens da publicação (1080x1350), uma por slide
  story.py       imagem do story (1080x1920), com a zona do autocolante livre
  video.py       vídeo em história (1080x1920, mp4)
  verificar.py   verifica a mensagem do dia e os dados*.json antes de publicar
  hoje.py        dia da semana, fundo do dia, cores e hora de publicação
prompt/
  ideia-diaria.md           prompt em vigor da tarefa "Ideia diária para o Instagram"
  alteracoes-propostas.md   alterações sugeridas ao prompt, ainda não aplicadas
docs/
  respostas-tipo.md         bases para responder a comentários e mensagens
exemplos/
  dados.json, dados_story.json, mensagem-boa.txt, mensagem-com-erros.txt
```

`gerar.py`, `story.py` e `video.py` são cópias exatas dos scripts que estão dentro do prompt. Quando um mudar, muda o outro.

A tarefa agendada não lê este repositório (não tem repositório associado). Isto é a cópia de referência, com histórico de alterações.

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
