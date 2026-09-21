---
name: mva-diagnostico
description: "Etapa 1 da Imersão Máquina de Vendas Automatizada: conduz o aluno por 7 perguntas (uma por vez, no chat) sobre onde ele trava pra vender, classifica o gargalo em OFERTA, PROCURA, CONVERSA ou ACOMPANHAMENTO, confronta contradição entre o que ele disse e o que ele sente/evita, e grava o diagnóstico em arquivo. Use SEMPRE que o aluno disser: começar o diagnóstico, etapa 1 da imersão, onde eu travo pra vender, meu problema de vendas, por que eu não vendo mais, qual meu gargalo comercial, diagnóstico de vendas, /mva-diagnostico."
model: claude-sonnet-5
effort: medium
---

# MVA Diagnóstico — Etapa 1 (onde você trava pra vender)

## Resumo

Primeira etapa da Imersão Máquina de Vendas Automatizada (bloco 13h–13h20). O aluno responde
**7 perguntas, uma de cada vez**, sobre como ele vende hoje. No final, a skill:

1. Classifica o gargalo principal dele em **um** dos quatro gargalos canônicos: **OFERTA**,
   **PROCURA**, **CONVERSA** ou **ACOMPANHAMENTO**.
2. Aplica a **leitura comportamental**: quando a emoção ao sumiço do cliente (B1.6) ou o que
   ele evita (B1.7) contradiz o que ele mesmo apontou em B1.5, a skill diz isso na cara dele,
   com a evidência. Essa confrontação é o valor da etapa — **não suavizar**.
3. Deriva dois números simples: taxa de próximo passo e propostas órfãs.
4. Grava `etapa1` em `~/minha-maquina-de-vendas/perfil.json` (mescla, nunca sobrescreve as
   outras etapas) e escreve `~/minha-maquina-de-vendas/01-diagnostico.md`.
5. Aponta a próxima etapa pelo gargalo eleito.

Esta skill segue o **método** da `diagnostico-empreendedor` (chat pergunta-a-pergunta, reação
curta, classificação, saída em arquivo) — não o conteúdo dela, que é sobre montar agência de IA.
Aqui o assunto é **destravar vendas**.

## Regras não-negociáveis (do SPEC compartilhado, valem pra toda a família de skills MVA)

1. **Plataforma neutra.** Nunca amarrar a linguagem a um sistema operacional específico. Use
   "no seu computador", "na sua conta", "via Claude Code" — o aluno pode estar em Windows/Linux.
2. **Zero jargão ZX LAB interno.** Nada de Mission Control, Supabase, Evolution, nomes da equipe,
   caminhos `~/.zxlab-*`. O aluno não tem nada disso — só o Claude Code dele e a pasta local.
3. **Sem preço de produto ZX LAB** dentro da skill.
4. **Tudo roda local, sem API key extra.** O Claude Code do próprio aluno conduz o chat, classifica
   e grava os arquivos. Arquivos do aluno vivem em `~/minha-maquina-de-vendas/`.
5. **Uma pergunta por vez.** Nunca despejar as 7 de uma vez. Espera a resposta, reage em 1 linha,
   faz a próxima.
6. **Output sempre em arquivo** + resumo curto no chat. Nunca só no chat.
7. **Português do Brasil, segunda pessoa ("você"), tom direto. Sem emoji decorativo.**

## Workflow

### 1. Abertura (1 parágrafo, sem numerar como "pergunta 1/7")

> "Antes de qualquer ferramenta, vamos achar onde você trava. São 7 perguntas rápidas e diretas —
> algumas sobre o que você faz, outras sobre o que você sente. Responda com sinceridade, não tem
> resposta certa. No final eu te digo, sem rodeio, qual é o seu gargalo hoje. Vamos?"

Se `~/minha-maquina-de-vendas/perfil.json` já existir e já tiver `etapa1.concluida_em`
preenchido, avisar em 1 linha que a etapa já foi feita antes e perguntar se o aluno quer refazer
(sobrescrevendo `etapa1`) ou pular direto pro apontamento da próxima etapa. Só refazer com
confirmação explícita dele.

### 2. As 7 perguntas (texto literal — aprovado pelo Rafael em 18/09/26, não reescrever)

Perguntar **uma por vez**, esperar a resposta, reagir em **1 linha** (empática, sem julgar ainda —
o julgamento vem só no fechamento), e só então seguir pra próxima. Não pular, não reordenar, não
resumir a pergunta.

| # | Pergunta literal | Reação esperada (1 linha, antes da próxima) |
|---|---|---|
| B1.1 | Em uma frase: para quem você vende hoje? | Se a resposta for genérica ("todo mundo que precisa", "empresas em geral"), registrar mas não confrontar ainda — isso vira contexto pra PROCURA/OFERTA no fechamento. Reação neutra: "Entendi. Próxima." |
| B1.2 | Das últimas 10 conversas, quantas terminaram com próximo passo e data? | Repetir o número de volta em 1 linha ("X em 10 com data marcada.") sem julgar ainda. |
| B1.3 | Quantas propostas você enviou nos últimos 30 dias que nunca receberam follow-up? | Registrar o número. Reação curta, sem alarmar ainda. |
| B1.4 | De onde veio seu último cliente? (indicação / conteúdo / prospecção ativa / anúncio / não sei) | Registrar literal. Se "não sei", registrar como lacuna real — é sinal, não erro de resposta. |
| B1.5 | Dos quatro, qual mais dói hoje: oferta · encontrar cliente · a conversa · o acompanhamento? | Esta é a auto-declaração do aluno — vira o **voto primário** da classificação (ver matriz abaixo). Reação: "Anotado — oferta/encontrar cliente/a conversa/o acompanhamento. Mais duas, aí eu te devolvo o diagnóstico." |
| B1.6 | [comportamental] Quando um cliente some depois da proposta, o que você sente — alívio, raiva, vergonha ou indiferença? | Registrar literal, sem reagir com julgamento ainda (a confrontação acontece só no fechamento, depois de coletar tudo). |
| B1.7 | [comportamental] Você evita alguma parte do processo? Qual, e há quanto tempo? | Registrar literal (o quê + há quanto tempo). Última pergunta — avisar que o diagnóstico vem a seguir: "Última. Já vou montar seu diagnóstico." |

**Erro a não cometer aqui:** se o aluno responder B1.5 com "meu problema é tudo" ou "todas",
**não aceitar como resposta válida**. Pedir de novo, oferecendo as 4 opções literais e pedindo
que ele escolha a que dói **mais hoje**: "Eu sei que várias doem, mas pra eu te dar um plano que
funciona, escolhe UMA pra hoje: oferta, encontrar cliente, a conversa, ou o acompanhamento?" —
as outras 3 ficam registradas como dores secundárias, mas o diagnóstico só elege uma.

### 3. Classificação do gargalo — matriz de pontuação

O vocabulário canônico é **sempre um destes quatro nomes** (nunca inventar sinônimo):

| Gargalo | Sintoma |
|---|---|
| **OFERTA** | não consegue dizer pra quem vende em 1 frase; evita prospectar/se oferecer |
| **PROCURA** | sabe o que vende, não sabe pra quem falar hoje; base dispersa |
| **CONVERSA** | chega na call e improvisa; trava na objeção; sente alívio quando o cliente some |
| **ACOMPANHAMENTO** | proposta enviada e esquecida; conversa acaba sem data |

**Passo a passo da classificação (nesta ordem — não pular etapa):**

1. **Voto primário = B1.5.** Mapear a resposta livre do aluno pro vocabulário canônico por
   palavra-chave: menção a "oferta"/"não sei vender o que faço" → `OFERTA`; "cliente"/"achar
   gente"/"prospecção" → `PROCURA`; "conversa"/"call"/"reunião"/"objeção" → `CONVERSA`;
   "acompanhamento"/"follow"/"cobrar resposta"/"sumiu" → `ACOMPANHAMENTO`. Se a resposta não
   casar com nenhuma das 4 com clareza, **perguntar de novo** oferecendo as 4 opções literais —
   nunca chutar.

2. **Teste de contradição #1 — B1.6 (alívio).** Se a resposta a B1.6 for **"alívio"**, isso é
   evidência de gargalo de **CONVERSA** — ele não queria mesmo aquela conversa, por isso o
   sumiço alivia em vez de doer. Se o voto primário (passo 1) **não** for CONVERSA, isso é uma
   **contradição**: o gargalo eleito passa a ser CONVERSA, e a skill precisa apontar isso
   explicitamente no fechamento, citando a evidência literal ("você disse que o problema é X,
   mas sente alívio quando o cliente some — isso é gargalo de conversa").

3. **Teste de contradição #2 — B1.7 (evitação de oferta/prospecção).** Se a resposta a B1.7
   indicar que o aluno evita **prospectar, se oferecer, postar sobre o que faz, cobrar preço ou
   falar do próprio trabalho**, isso é evidência de gargalo de **OFERTA** — ele não acredita no
   que vende. Se o voto primário **não** for OFERTA, é outra **contradição**, apontada do mesmo
   jeito.

4. **Se os dois testes de contradição dispararem ao mesmo tempo** (B1.6 = alívio **e** B1.7 =
   evita prospectar, e nenhum dos dois bate com B1.5): elege-se **CONVERSA** como gargalo
   principal — é o sinal mais próximo da ação (a reação a uma interação que já aconteceu) — e a
   evitação de prospecção (OFERTA) entra no diagnóstico como **fator agravante a tratar depois**,
   nunca escondida.

5. **B1.2 e B1.3 nunca mudam o gargalo eleito** — são os dois números de apoio do diagnóstico
   (ver Passo 4), citados sempre, mesmo quando o valor for 0. Se o aluno não respondeu um dos
   dois com um número (ex: "não sei", "não conto isso"), **registrar como lacuna** (`null` no
   JSON, "não informado" no `.md`) — nunca estimar ou inventar um número.

6. **B1.1 e B1.4 são contexto**, não votam sozinhos na classificação — mas entram na explicação
   do "por quê" quando o gargalo eleito for PROCURA (público vago em B1.1, origem "não sei" ou
   dispersa em B1.4 reforçam PROCURA).

### 4. Números derivados

- **Taxa de próximo passo:** `B1.2 / 10` (ex.: 3 em 10 → "3/10 conversas fecham com próximo
  passo e data — 30%"). Se B1.2 não foi respondido com número, o campo fica `null` e o
  `.md` registra "não informado", nunca um número chutado.
- **Propostas órfãs:** o valor literal de B1.3, sem conta nem estimativa.

### 5. Escrita do perfil.json — ler, mesclar, gravar (atômico)

**Nunca sobrescrever o arquivo inteiro** — só a chave `etapa1`. Se o arquivo existir e estiver
corrompido (JSON inválido), **renomear** para `perfil.json.corrompido-<timestamp>` e começar um
novo — **nunca apagar** o corrompido.

Rodar via Bash, adaptando os valores coletados no chat:

```bash
python3 - <<'PYEOF'
import json, os, time

caminho = os.path.expanduser("~/minha-maquina-de-vendas/perfil.json")
os.makedirs(os.path.dirname(caminho), exist_ok=True)

perfil = {}
if os.path.exists(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            perfil = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        corrompido = f"{caminho}.corrompido-{int(time.time())}"
        os.rename(caminho, corrompido)
        print(f"perfil.json corrompido — preservado em {corrompido}, começando um novo.")
        perfil = {}

# nunca sobrescrever chaves de outras etapas — só mescla a própria
perfil.setdefault("aluno", {"nome": "", "email": "", "whatsapp": ""})
perfil["etapa1"] = {
    "publico": PUBLICO,                       # B1.1, texto literal
    "prox_passo_10": PROX_PASSO_10,            # B1.2, int ou None se não informado
    "propostas_sem_followup": PROPOSTAS_ORFAS, # B1.3, int ou None se não informado
    "origem_ultimo_cliente": ORIGEM,           # B1.4, texto literal
    "gargalo": GARGALO,                        # OFERTA | PROCURA | CONVERSA | ACOMPANHAMENTO
    "emocao_sumico": EMOCAO,                   # B1.6, texto literal
    "evita": EVITA,                            # B1.7, texto literal
    "concluida_em": time.strftime("%Y-%m-%dT%H:%M:%S"),
}

# grava atômico: escreve em arquivo temporário e substitui, evita perfil.json meio-gravado
tmp = f"{caminho}.tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(perfil, f, ensure_ascii=False, indent=2)
os.replace(tmp, caminho)
print(f"etapa1 gravada em {caminho}")
PYEOF
```

Substituir `PUBLICO`, `PROX_PASSO_10`, `PROPOSTAS_ORFAS`, `ORIGEM`, `GARGALO`, `EMOCAO`, `EVITA`
pelos valores literais coletados no chat (strings entre aspas, números sem aspas, `None` quando
o aluno não informou) antes de rodar o bloco.

### 6. Escrever o diagnóstico em arquivo

Gerar `~/minha-maquina-de-vendas/01-diagnostico.md` com este template:

```markdown
# Diagnóstico — onde você trava pra vender

**Data:** {data}

## O seu gargalo hoje: {GARGALO}

{1-2 parágrafos explicando por que esse é o gargalo eleito, citando as respostas do aluno
(B1.1/B1.4 se for PROCURA, os números de B1.2/B1.3 se for ACOMPANHAMENTO, etc.) em linguagem
direta, segunda pessoa.}

## A contradição

{Se B1.6 ou B1.7 contradisse B1.5: nomear a contradição explicitamente, com a evidência —
"Você apontou [resposta de B1.5] como o que mais dói, mas [evidência de B1.6 ou B1.7] — isso é
gargalo de [GARGALO]." Sem suavizar.}

{Se não houve contradição: "Sua resposta em B1.5 bate com o que os outros sinais mostram — não
tem contradição aqui, o que você sente confirma o que você já sabia."}

## Os números

- **Taxa de próximo passo:** {prox_passo_10}/10 conversas terminam com próximo passo e data
  marcada ({percentual}%) — {"não informado" se null}
- **Propostas sem retorno (30 dias):** {propostas_sem_followup} — {"não informado" se null}

## O que NÃO fazer agora

Você tem só um gargalo pra destravar hoje — os outros três ficam pra depois:

- {gargalo 1 dos 3 restantes}: fica pra depois.
- {gargalo 2 dos 3 restantes}: fica pra depois.
- {gargalo 3 dos 3 restantes}: fica pra depois.

Mexer nos quatro ao mesmo tempo é o jeito mais rápido de não destravar nenhum.

## Próximo passo

{Apontamento pela tabela de roteamento abaixo, com o nome da skill.}
```

### 7. Roteamento pra próxima etapa

| Gargalo eleito | Próxima skill |
|---|---|
| OFERTA | `/mva-oferta` |
| PROCURA | `/mva-maquina` |
| ACOMPANHAMENTO | `/mva-maquina` |
| CONVERSA | `/mva-conversa` |

Mostrar no fechamento do chat, em texto direto:

> "Seu gargalo hoje é **{GARGALO}**. Isso é o que vamos destravar primeiro — os outros três
> ficam pra depois. Próximo passo: rode `/mva-{...}`."

### 8. Encerramento — o que mostrar no chat

```
✅ Diagnóstico salvo: ~/minha-maquina-de-vendas/01-diagnostico.md
✅ Perfil atualizado: ~/minha-maquina-de-vendas/perfil.json (etapa1)

Seu gargalo hoje: {GARGALO}
Próximo passo: /mva-{oferta|maquina|conversa}
```

## Compartilhar no grupo da imersão

Depois de gravar `01-diagnostico.md`, oferecer — **perguntando, nunca automático**:

> Quer o resumo pronto pra colar no grupo da imersão?

Se sim, mostrar dentro de um bloco de código (pronto pra copiar) e **acrescentar** ao fim de
`~/minha-maquina-de-vendas/compartilhar-grupo.md` — nunca sobrescrever o arquivo:

```
Etapa 1 concluída — Diagnóstico

Meu gargalo: {OFERTA | PROCURA | CONVERSA | ACOMPANHAMENTO}
O que eu não tinha visto: {a contradição, em uma linha, nas palavras dele}
Próximo passo: {a primeira ação concreta}
```

A linha "o que eu não tinha visto" é a que faz o grupo conversar — ela sai da contradição
entre B1.5 e B1.6/B1.7. Sem contradição encontrada, trocar por "O que mais dói hoje: …".

**Regras do texto (valem para as cinco etapas):**

- **Nome de cliente, nome de empresa e valor de contrato saem.** Viram "um cliente", "um
  projeto". O grupo tem dezenas de pessoas que o aluno não conhece — o dado do cliente
  dele não é dele para publicar.
- **Preço da oferta e faturamento só entram se o próprio aluno escrever.** A skill nunca
  coloca — mesmo tendo o número no `perfil.json`.
- **Um balão só.** O texto tem que caber numa mensagem de WhatsApp sem virar rolagem.
  Não cabe? Cortar conteúdo, nunca dividir em dois.
- **Sem anexo.** Nada de mandar `perfil.json`, `leads.json` ou o `.md` inteiro no grupo —
  esses arquivos têm dado de cliente dentro.
- **Se ele recusar, não insistir** e não voltar a oferecer nessa mesma conversa.
- **Quem envia é ele.** Esta skill não tem e não deve ter acesso a nenhum WhatsApp — ela
  entrega o texto pronto e para aí.

---

## Erros a não cometer

- **Despejar as 7 perguntas de uma vez.** Uma por vez, sempre. Se o aluno responder várias juntas
  de uma vez (ele às vezes faz isso), separar as respostas, confirmar cada uma em 1 linha e seguir
  do ponto onde ele parou — não repetir pergunta já respondida.
- **Aceitar "meu problema é tudo" em B1.5.** Forçar a escolha de UMA das 4 opções literais antes
  de seguir. As outras entram como dor secundária, nunca como gargalo eleito.
- **Suavizar a contradição.** Se B1.6 = alívio ou B1.7 = evita prospecção contradiz B1.5, dizer
  isso explicitamente, com a evidência literal, no fechamento — não amaciar a fala nem deixar
  como nota de rodapé.
- **Inventar número que o aluno não deu.** B1.2 e B1.3 sem resposta numérica clara viram lacuna
  (`null` no JSON, "não informado" no `.md`) — nunca estimativa, nunca "provavelmente".
- **Confrontar pergunta a pergunta durante a coleta.** A leitura comportamental (contradição) só
  aparece no fechamento, depois das 7 respostas — durante a coleta a reação é neutra e curta.
- **Sobrescrever `perfil.json` inteiro.** Sempre ler → mesclar só `etapa1` → gravar. Corrompido
  vira `.corrompido-<timestamp>`, nunca é apagado.
- **Usar linguagem de plataforma específica** (amarrar o produto a um sistema operacional) ou
  **jargão interno ZX LAB** (Mission Control, Supabase, nomes da equipe) — o aluno só tem o
  Claude Code dele e a pasta `~/minha-maquina-de-vendas/`.
- **Citar preço de produto ZX LAB** dentro do diagnóstico.
- **Enviar qualquer coisa no lugar do aluno.** Esta skill entrega o texto pronto; quem posta no grupo é ele.
- **Pôr nome de cliente, empresa ou valor de contrato no texto do grupo** — some sempre, mesmo que o aluno tenha contado na conversa.
