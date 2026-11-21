> Estado: estas alterações já estão incluídas em `regras.md`. Este ficheiro fica como registo.

# Alterações propostas ao prompt da tarefa

Ainda não aplicadas. O prompt em vigor está em `ideia-diaria.md` (cópia de 20/11/2026, 21:02).

A tarefa agendada não tem acesso a este repositório: corre sem repositório associado e só lê o Projeto "Escritório de contabilidade". Por isso, qualquer script que a tarefa precise de correr tem de estar dentro do prompt ou num documento do Projeto.

## 1. Primeira frase do descritivo com menos de 125 caracteres

No feed, a legenda é cortada por volta dos 125 caracteres e o resto fica escondido atrás de "mais". Na secção DESCRITIVO PARA O INSTAGRAM, a seguir a "A primeira frase diz logo a quem diz respeito...", acrescentar:

```text
- A primeira frase tem menos de 125 caracteres (é o que aparece no feed antes do "mais").
```

E na verificação do passo 4, acrescentar a alínea:

```text
(i) a primeira frase do descritivo tem menos de 125 caracteres.
```

## 2. Fundo do dia calculado por comando

Hoje o modelo conta os dias desde 18/11 de cabeça. Funciona, mas é o tipo de conta que falha ao fim de uns meses. Substituir o primeiro parágrafo da secção FUNDO por:

```text
Calcula o fundo com este comando (não contes de cabeça):
python3 -c "from datetime import datetime,date;from zoneinfo import ZoneInfo;n=(datetime.now(ZoneInfo('Europe/Lisbon')).date()-date(2026,11,18)).days;print('azul' if n%2==0 else 'branco')"
```

## 3. Scripts no Projeto em vez de no prompt

O prompt tem cerca de 47 mil caracteres, e quase metade são os três scripts (`gerar.py`, `story.py`, `video.py`), que o modelo tem de copiar todos os dias "sem alterar". Isto gasta contexto em todas as execuções e mais tarde ou mais cedo vai sair um erro de cópia.

Proposta: criar no Projeto quatro documentos (`claude/gerar.py`, `claude/story.py`, `claude/video.py` e `claude/verificar.py`, com o conteúdo da pasta `scripts/` deste repositório) e trocar cada bloco de código do prompt por:

```text
Lê o documento "claude/gerar.py" do Projeto (project_read) e grava-o tal e qual em gerar.py.
```

Isto tem de ser feito por ti no Projeto, porque esta sessão não tem acesso a ele.

## 4. Verificação automática do texto

Só faz sentido depois do ponto 3, porque o `verificar.py` é demasiado grande para ir dentro do prompt. No passo 4, antes das verificações manuais:

```text
Grava a mensagem do passo 3 em mensagem.txt e corre:
python3 verificar.py mensagem.txt dados.json dados_story.json (e dados_video.json, se houver)
Corrige todos os ERROS e volta a correr até não haver nenhum. Lê os AVISOS e decide caso a caso.
Depois faz na mesma a releitura frase a frase contra a fonte: o script não verifica factos.
```
