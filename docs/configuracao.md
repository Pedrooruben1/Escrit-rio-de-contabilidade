# Configuração do fluxo de aprovação

Como funciona:

1. Às 8h20, a tarefa "Ideia diária" gera as imagens, guarda-as no branch `claude/publicacoes` deste repositório (é daí que vêm os links públicos) e às 8h34 envia ao grupo "Contabilidade" as fotos, o story e o texto.
2. Respondes no grupo: `sim`, `sim B`, `sim vídeo`, `não`, `não, quero algo sobre...` ou `altera, ...`.
3. Um Zap guarda cada mensagem do grupo num ficheiro de texto do Google Drive.
4. A tarefa "Respostas" corre de hora a hora (aos 57 minutos, das 8h57 às 21h57). Lê os ficheiros novos e:
   - com `sim`, publica à hora marcada (13h00 durante a semana, 18h00 ao fim de semana; na prática, na execução das 12h57 ou das 17h57) ou logo, se a hora já tiver passado;
   - com `não, ...` ou `altera, ...`, prepara outra proposta e envia-a ao grupo;
   - às 9h57 e às 18h57, vê os comentários novos no Instagram e propõe respostas (`r1 sim`, `r1 não`, `r1, texto`).
5. Os stories e o texto alternativo continuam a ser feitos à mão: a API do Instagram não permite autocolantes, e a ação do Zapier não tem campo para o texto alternativo.

Uma resposta pode demorar até uma hora a ter efeito, porque o plano gratuito do Zapier não permite avisar a tarefa no momento.

## O que tens de fazer

### 1. Bot do Telegram

No Telegram, abre o @BotFather e envia `/setprivacy`, escolhe o bot Escravo e responde `Disable`. Depois, no grupo "Contabilidade", remove o bot e volta a adicioná-lo (a mudança só tem efeito depois disso).

Sem isto, o bot só vê as mensagens que respondem diretamente às dele.

### 2. Google Drive no Zapier

A ligação atual do Google Drive não tem permissões para ler nem criar ficheiros. Em zapier.com/app/connections, abre o Google Drive, carrega nos três pontos, escolhe Reconnect e, no ecrã da Google, marca todas as caixas de permissões.

### 3. Pasta no Google Drive

Cria no teu Drive uma pasta com este nome exato: `bem.contado - respostas Telegram`

### 4. Zap

Em zapier.com, carrega em Create, Zap:

- **Gatilho:** Telegram, New Message. Conta: o bot Escravo. Chat ID: o grupo "Contabilidade". Message Type: Excludes Voice and Audio Messages.
- **Ação:** Google Drive, Create File From Text.
  - Folder: `bem.contado - respostas Telegram`
  - File Name: o campo `Message ID` do passo 1
  - File Content, em três linhas: `Date`, depois `From First Name` e depois `Text` (todos do passo 1)
  - Convert to Document: False
- Testa, envia uma mensagem de teste no grupo e confirma que aparece um ficheiro na pasta. Depois liga o Zap (Publish).

No plano gratuito, cada mensagem do grupo gasta uma tarefa do Zapier (100 por mês). Os alertas de revenda enviados pelo próprio bot não contam, porque o bot não recebe as próprias mensagens.

### 5. Histórico

O histórico deixa de estar no Projeto do Claude e passa para `historico_publicacoes.md`, no branch `claude/publicacoes`. Cola o conteúdo atual do `claude/historico_publicacoes.md` do Projeto numa conversa comigo, ou substitui tu o ficheiro no GitHub.

### 6. Ativar as tarefas

As duas tarefas novas já existem, mas estão desativadas: "Ideia diária (aprovação no Telegram)" e "Respostas do Telegram (bem.contado)". Foram criadas sem o conector do Zapier (não dá para o pôr a partir daqui). Em claude.ai/code/routines, em cada uma delas:

- Editar, Connectors: acrescenta o **Zapier**;
- Advanced settings, Repository: escolhe `Pedrooruben1/Escrit-rio-de-contabilidade`;
- guarda e ativa.

No mesmo dia em que ativares a nova "Ideia diária", desativa a antiga "Ideia diária para o Instagram", para não receberes duas propostas.

## Comandos no grupo

| Mensagem | Efeito |
| --- | --- |
| `sim` | Aprova a opção única e publica à hora marcada |
| `sim A` / `sim B` | Aprova a opção indicada |
| `sim vídeo` | Publica o vídeo como Reel em vez da imagem |
| `não` | Não publica hoje e marca a ideia como "não publicada" |
| `não, quero algo sobre ...` | Gera uma proposta nova com essa orientação |
| `altera, ...` | Corrige a proposta atual |
| `r1 sim` / `r1 não` / `r1, texto` | Responde (ou não) ao comentário n.º 1 |
