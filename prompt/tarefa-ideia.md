Tarefa diária da bem.contado (começa às 18h37, hora de Lisboa): preparar a proposta do dia seguinte para o Instagram, segundo a grelha semanal, e enviá-la às 19h00 ao grupo de Telegram "Contabilidade" para aprovação.

1. Repositório. Procura um clone de github.com/Pedrooruben1/Escrit-rio-de-contabilidade na pasta de trabalho. Se não existir, usa a ferramenta add_repo (owner "Pedrooruben1", repo "Escrit-rio-de-contabilidade", access "push") e clona-o como a ferramenta indicar (se pedir, chama register_repo_root). Guarda o caminho em REPO e atualiza-o com git pull no branch por defeito.

2. Lê o ficheiro "$REPO/prompt/regras.md" do princípio ao fim e segue-o. Esta execução é a da véspera: faz os passos 1 a 12 para o dia seguinte (linhas pub_* do scripts/hoje.py) e ignora a secção REVISÃO.

3. Se já existir publicacoes/[data do dia seguinte]/estado.json no branch claude/publicacoes, a proposta desse dia já foi feita: não faças outra e termina sem enviar nada.

4. Se o repositório não estiver acessível (add_repo recusado, clone ou push falhados), não tentes outros caminhos: envia uma notificação com PushNotification a dizer qual foi o erro e termina.
