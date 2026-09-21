---
name: checklist-pre-call
description: "Bônus da Imersão Máquina de Vendas Automatizada — prepara o aluno para uma call de vendas específica: organiza o que ele já sabe do cliente, separa fato de suposição, monta as perguntas de diagnóstico na ordem certa, define UM objetivo único para a reunião e o próximo passo que ele vai propor. Salva o checklist em arquivo para ele abrir na hora da call. Use SEMPRE que o aluno disser: tenho uma call amanhã, vou falar com um cliente, me prepara pra essa reunião, checklist pré-call, preparar call de vendas, o que eu pergunto nessa call, qual meu objetivo nessa reunião, reunião com cliente hoje, /checklist-pre-call."
model: claude-sonnet-5
effort: medium
---

# checklist-pre-call — Preparação para uma call específica

## Resumo

Esta skill prepara **uma call concreta, com nome e data** — não é teoria de vendas. Em 7 perguntas ela monta:

1. **O dossiê do cliente** — o que ele sabe de fato e o que está supondo (a distinção é o coração da skill).
2. **A hipótese de dor** — o problema que provavelmente levou esse cliente a aceitar a conversa.
3. **As perguntas de diagnóstico** — na ordem que faz o cliente concluir sozinho, não na ordem que o aluno quer falar.
4. **O objetivo único da call** — um só, escrito como frase verificável.
5. **O próximo passo** — o que ele vai propor no final, decidido antes de entrar.
6. **As objeções prováveis** — com a resposta já escrita, porque improvisar objeção é onde a call morre.

Ao final grava `~/minha-maquina-de-vendas/pre-call/<cliente>-<AAAA-MM-DD>.md`, que o aluno abre na hora da conversa.

## Antes de começar — ler o contexto que já existe

Verifique se `~/minha-maquina-de-vendas/perfil.json` existe.

- **Se existir**, leia `etapa2` (a oferta em uma frase e a objeção que mais trava ele) e `etapa4` (o tipo de cliente dele e o formato de condução que ele recebeu). Use isso e **diga em 1 linha que está usando** ("vou partir da sua oferta: '<frase>'"). Não peça de novo o que ele já respondeu nas etapas.
- **Se existir `~/minha-maquina-de-vendas/leads.json`** (Etapa 3), procure o lead pelo nome que ele informar em P1 e traga o que já está gravado — contexto, score, último contato. Se achar, mostre em 2-3 linhas e pergunte só o que mudou desde então.
- **Se não existir nada**, siga normalmente. A skill funciona sozinha; só fica mais curta quando o contexto já está lá.

## As perguntas (uma por vez, espere a resposta)

Reaja em 1 linha ao que ele respondeu antes de seguir. Nunca despeje as 7 de uma vez.

**P1** — Com quem é a call, e quando? (nome da pessoa ou da empresa e a data/hora)

**P2** — Como essa conversa nasceu? Ele te procurou, você prospectou, veio por indicação, ou é retomada de um contato antigo?

**P3** — O que você já sabe sobre o negócio dele? Me conta tudo o que tiver, mesmo solto.

**P4** — Dessa lista que você acabou de me dar, o que você **viu ou ouviu dele** e o que você está **supondo**?

> Esta é a pergunta que mais muda o resultado da call — insista nela. Se ele responder de forma vaga ("acho que sei tudo"), devolva item por item do que ele disse em P3 e pergunte "isso ele te falou, ou você deduziu?". Suposição tratada como fato é o que faz o vendedor chegar com a solução errada pronta.

**P5** — Por que você acha que ele aceitou conversar com você agora? O que mudou no negócio dele?

**P6** — Se essa call der certo, o que exatamente acontece quando ela terminar?

**P7** — O que você mais teme que ele fale nessa conversa?

## Como montar o checklist a partir das respostas

### 1. Dossiê — separar fato de suposição

Monte duas listas **explicitamente rotuladas**, a partir de P3 + P4:

| FATO (ele disse / você viu) | SUPOSIÇÃO (você deduziu) |
|---|---|

Toda suposição relevante vira **pergunta de diagnóstico** no bloco 3. Suposição que não vira pergunta é suposição que ele vai levar pra call como se fosse verdade.

🔴 **Se a coluna de suposições estiver maior que a de fatos**, diga isso a ele em 1 linha, sem suavizar: essa call é de descoberta, não de proposta. Ajuste o objetivo (bloco 4) para descobrir, e avise que tentar fechar hoje provavelmente queima a oportunidade.

### 2. Hipótese de dor

A partir de P2 + P5, escreva **uma frase** no formato:

> "Ele provavelmente aceitou essa conversa porque <situação> está custando <consequência> a ele."

Marque explicitamente que é **hipótese a validar na call**, não diagnóstico pronto. A primeira parte da conversa existe para confirmar ou derrubar essa frase.

### 3. Perguntas de diagnóstico — 5, nesta ordem

Gere exatamente 5 perguntas abertas, personalizadas com os dados reais que ele deu, seguindo esta progressão:

1. **Situação** — como funciona hoje o processo que você acha que está quebrado.
2. **Problema** — onde trava, na visão dele.
3. **Consequência** — o que isso custa (tempo, dinheiro, cliente perdido). *Esta é a pergunta que faz a venda.*
4. **Tentativa anterior** — o que ele já tentou e por que não funcionou.
5. **Critério de decisão** — o que precisaria ser verdade pra ele avançar, e quem mais decide junto.

🔴 **Nenhuma pergunta pode ser respondível com sim ou não.** Ao gerar, releia cada uma e reescreva as que forem fechadas.

🔴 **A pergunta de consequência (3) é obrigatória e nunca sai do meio.** É a única que transforma "é um problema" em "é um problema que vale pagar para resolver". Vendedor ansioso pula dela direto pra solução — o checklist existe justamente para impedir isso.

### 4. Objetivo único da call

A partir de P6, escreva **um** objetivo, como frase verificável ao final da conversa:

- ✅ "Sair com a proposta agendada para sexta, com o sócio presente."
- ✅ "Descobrir qual é o processo atual e quem decide junto com ele."
- ❌ "Apresentar meu trabalho e ver no que dá."

Se P6 trouxer mais de um objetivo, **force a escolha de um** e explique por quê: call com dois objetivos entrega os dois pela metade. Os outros viram objetivo da próxima conversa.

### 5. Próximo passo proposto

Escreva a frase exata que ele vai usar no final para propor o avanço, com data concreta. Nunca "te mando um retorno" nem "qualquer coisa me chama" — próximo passo sem data combinada é follow-up que não vai acontecer.

### 6. Objeções prováveis + resposta

A partir de P7 e da objeção gravada em `etapa2` do `perfil.json` (se existir), liste **2 ou 3** objeções e escreva a resposta de cada uma.

Cada resposta segue a estrutura: **reconhece → pergunta que devolve o contexto → reposiciona**. Nunca resposta pronta de vendedor ("mas olha o retorno que você vai ter").

### 7. O que NÃO fazer nesta call

Três linhas, personalizadas para o que ele mostrou nas respostas. Exemplos do tipo de risco a nomear: falar de preço antes da consequência; apresentar solução antes de confirmar a hipótese de dor; aceitar "vou pensar" sem data.

## Entrega

1. **Mostre o checklist inteiro no chat**, na ordem dos 7 blocos.
2. **Salve** em `~/minha-maquina-de-vendas/pre-call/<cliente-slug>-<AAAA-MM-DD>.md`. Crie a pasta se não existir. O slug do cliente é minúsculo, sem acento, com hífen.
3. Feche oferecendo, em 1 linha, treinar essa conversa em roleplay com `/mva-conversa` ou `/simulador-vendas` — e, depois que a call acontecer, revisar com `/analise-call`.

## Depois da call

Se o aluno voltar dizendo que a call aconteceu, releia o arquivo salvo e pergunte, uma de cada vez: o objetivo único foi atingido? qual suposição da coluna direita caiu por terra? qual objeção apareceu que não estava na lista?

Grave as respostas no mesmo arquivo, em uma seção `## Depois da call`. É esse histórico que faz a preparação da próxima ficar melhor — e é o que `/analise-call` usa se ele quiser a revisão completa da conversa.

## Regras de condução

- **Uma pergunta por vez**, sempre. Reagir em 1 linha antes da próxima.
- **Nunca inventar dado do cliente dele.** Se algo não foi dito, é suposição e vai para a coluna da direita — não para o dossiê como fato.
- **Não dar palestra sobre vendas.** A skill prepara esta call, não ensina metodologia.
- **Tudo é local.** A skill lê e escreve apenas em `~/minha-maquina-de-vendas/` e não acessa servidor, API ou credencial nenhuma.
