---
name: maquina-de-vendas
description: "Ponto de entrada único do aluno na Imersão Máquina de Vendas Automatizada: na primeira vez, apresenta o caminho em 4 etapas, cadastra o aluno e chama o diagnóstico; nas vezes seguintes, lê o progresso salvo, mostra o mapa do que já foi feito e retoma exatamente de onde parou, na ordem certa pro gargalo eleito. No fim das 4 etapas, gera o plano de 7 dias. NUNCA reimplementa o que as quatro etapas já fazem — só orquestra. Use SEMPRE que o aluno disser: começar a imersão, minha máquina de vendas, por onde eu começo, continuar de onde parei, onde eu tinha parado, retomar a imersão, meu progresso na imersão, qual minha próxima etapa, quero meu plano de 7 dias, /maquina-de-vendas."
model: claude-sonnet-5
effort: medium
---

# Máquina de Vendas Automatizada — ponto de entrada

## Resumo

Esta skill é a **porta de entrada única** do aluno na Imersão Máquina de Vendas
Automatizada. Ela não conduz nenhuma pergunta de diagnóstico, não define oferta, não
monta a máquina de leads e não roda o treino de conversa — **isso já está pronto nas
quatro skills que ela orquestra**: `/mva-diagnostico`, `/mva-oferta`, `/mva-maquina`,
`/mva-conversa`. O trabalho desta skill é só:

1. **Na primeira execução:** apresentar o caminho, cadastrar o aluno, criar a pasta e o
   `perfil.json` vazio, e chamar `/mva-diagnostico`.
2. **Nas execuções seguintes:** ler o `perfil.json`, mostrar o mapa de progresso, e
   retomar exatamente da primeira etapa incompleta — **na ordem certa pro gargalo
   eleito**, não na ordem 1-2-3-4 fixa.
3. **Ao final das quatro etapas:** montar o `PLANO-7-DIAS.md`, dimensionado pelo tempo
   por dia que o aluno declarou.
4. **Sob pedido ("status", "meu progresso"):** mostrar onde ele está sem avançar nada.

Tudo vive em `~/minha-maquina-de-vendas/` — a mesma pasta que as quatro etapas usam.

## Regras não-negociáveis (do SPEC compartilhado — valem aqui também)

1. **Plataforma neutra.** Nunca amarrar a linguagem a um sistema operacional
   específico. Use "no seu computador", "na sua conta", "via Claude Code" — o aluno
   pode estar em Windows, Linux ou num computador da Apple.
2. **Zero jargão ZX LAB interno.** Nada de Mission Control, Supabase, Evolution, nomes
   da equipe, caminhos `~/.zxlab-*`. O aluno só tem o Claude Code dele e esta pasta.
3. **Sem preço de produto ZX LAB.**
4. **Tudo roda local, sem API key extra.**
5. **Uma pergunta por vez** — vale só pra pergunta que ESTA skill faz (o nome do
   aluno na primeira execução). As sete perguntas de cada etapa são responsabilidade
   das quatro skills, não desta.
6. **Output sempre em arquivo** + resumo curto no chat.
7. **Português do Brasil, segunda pessoa ("você"), tom direto. Sem emoji decorativo.**

## Onde mora tudo

```
~/minha-maquina-de-vendas/
├── perfil.json          # estado compartilhado — esta skill CRIA, as 4 etapas ESCREVEM
├── 01-diagnostico.md    # gerado por /mva-diagnostico
├── 02-oferta.md         # gerado por /mva-oferta
├── leads.json           # gerado por /mva-maquina
├── leads.md             # gerado por /mva-maquina
├── 03-maquina.md        # gerado por /mva-maquina
├── 04-conversa.md       # gerado por /mva-conversa
└── PLANO-7-DIAS.md       # gerado por ESTA skill, só depois das 4 etapas concluídas
```

---

## 1. Decidir se é primeira execução ou retomada

Ler `~/minha-maquina-de-vendas/perfil.json`.

- **Não existe** (ou existe mas está vazio/corrompido) → seguir a seção **2. Primeira
  execução**.
- **Existe e tem conteúdo válido** → seguir a seção **3. Execuções seguintes**.

---

## 2. Primeira execução

### 2.1 Apresentação do caminho (5 linhas, sem enrolar)

> "Vamos montar sua máquina de vendas em 4 etapas. Primeiro eu descubro onde você trava
> hoje — oferta, achar cliente, a conversa, ou o acompanhamento. Esse gargalo decide a
> ordem das próximas três: quem trava em oferta ataca oferta primeiro; quem trava em
> achar cliente ataca a máquina de leads primeiro; e assim por diante. No fim, você sai
> com um plano de 7 dias pra usar isso de verdade. Bora achar seu gargalo?"

### 2.2 Perguntar o nome do aluno (uma pergunta, só essa)

> "Antes de começar, como você se chama?"

Esperar a resposta. Não pedir e-mail nem WhatsApp aqui — esses campos existem no schema
do `aluno` mas ficam em branco até alguma etapa precisar deles; não são bloqueio.

### 2.3 Criar a pasta e o `perfil.json` vazio

Rodar via Bash:

```bash
python3 - <<'PYEOF'
import json, os, time

caminho = os.path.expanduser("~/minha-maquina-de-vendas/perfil.json")
os.makedirs(os.path.dirname(caminho), exist_ok=True)

NOME_ALUNO = "SUBSTITUIR"  # nome literal coletado no passo 2.2

perfil_vazio = {
    "aluno": {"nome": NOME_ALUNO, "email": "", "whatsapp": ""},
    "etapa1": {
        "publico": "", "prox_passo_10": None, "propostas_sem_followup": None,
        "origem_ultimo_cliente": "", "gargalo": "", "emocao_sumico": "",
        "evita": "", "concluida_em": "",
    },
    "etapa2": {
        "oferta_frase": "", "sintoma_cliente": "", "preco": "", "como_precificou": "",
        "entrega": "", "objecao_trava": "", "reacao_caro": "", "conviccao_0_10": None,
        "concluida_em": "",
    },
    "etapa3": {
        "onde_ficam_leads": "", "top3_quentes": "", "leads_semana": None,
        "criterio_qualificacao": "", "tempo_decidindo": "", "quer_automatizar": "",
        "usa_claude_code": "", "concluida_em": "",
    },
    "etapa4": {
        "cliente_decide": "", "decisor": "", "o_que_convenceu": "",
        "fala_ou_pergunta": "", "script_ou_principio": "", "trava_antes_ou_depois": "",
        "tempo_dia": "", "concluida_em": "",
    },
}

if os.path.exists(caminho):
    # já existe algo (corrida rara, ex: skill chamada 2x) — não sobrescrever conteúdo real
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            existente = json.load(f)
        if existente:
            print(f"perfil.json já existe com conteúdo em {caminho} — não sobrescrevendo.")
            raise SystemExit
    except (json.JSONDecodeError, UnicodeDecodeError):
        corrompido = f"{caminho}.corrompido-{int(time.time())}"
        os.rename(caminho, corrompido)
        print(f"perfil.json corrompido — preservado em {corrompido}, criando um novo.")

tmp = f"{caminho}.tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(perfil_vazio, f, ensure_ascii=False, indent=2)
os.replace(tmp, caminho)
print(f"perfil.json criado em {caminho}")
PYEOF
```

Substituir `SUBSTITUIR` pelo nome literal que o aluno deu. A gravação é atômica
(escreve em `.tmp` e substitui) — nunca deixa o arquivo pela metade.

### 2.4 Chamar a etapa 1

Confirmar em 1 linha ("Pasta criada. Vamos pro diagnóstico.") e invocar `/mva-diagnostico`
(Skill tool). Esta skill não faz nenhuma das 7 perguntas de diagnóstico — isso é
inteiramente da `mva-diagnostico`.

---

## 3. Execuções seguintes — mapa de progresso e retomada

### 3.1 Ler o perfil e montar o mapa

```bash
python3 - <<'PYEOF'
import json, os

caminho = os.path.expanduser("~/minha-maquina-de-vendas/perfil.json")

try:
    with open(caminho, "r", encoding="utf-8") as f:
        perfil = json.load(f)
except (json.JSONDecodeError, UnicodeDecodeError):
    print("CORROMPIDO")
    raise SystemExit

etapas = {
    "etapa1": {"nome": "Etapa 1 — Diagnóstico", "skill": "/mva-diagnostico"},
    "etapa2": {"nome": "Etapa 2 — Oferta",       "skill": "/mva-oferta"},
    "etapa3": {"nome": "Etapa 3 — Máquina de leads", "skill": "/mva-maquina"},
    "etapa4": {"nome": "Etapa 4 — Conversa",     "skill": "/mva-conversa"},
}

for chave, info in etapas.items():
    bloco = perfil.get(chave, {}) or {}
    feito = bool(bloco.get("concluida_em"))
    marca = "✅" if feito else "⬜"
    quando = bloco.get("concluida_em") or "pendente"
    print(f"{marca} {info['nome']:<28} {quando}")

gargalo = (perfil.get("etapa1") or {}).get("gargalo", "")
print(f"\nGargalo eleito: {gargalo or '(ainda não diagnosticado)'}")
PYEOF
```

- Se o script imprimir `CORROMPIDO`: renomear o arquivo pra
  `perfil.json.corrompido-<timestamp>` (nunca apagar) e tratar como **primeira
  execução** (seção 2) a partir daqui, avisando o aluno em 1 linha do que aconteceu.
- Se `etapa1.concluida_em` estiver vazio: a primeira etapa incompleta é sempre a
  etapa 1, independente de qualquer outra coisa — ela é quem elege o gargalo, e sem
  gargalo não existe ordem pra decidir. Chamar `/mva-diagnostico` direto, sem mostrar
  tabela de roteamento ainda (ela só faz sentido depois que o gargalo existe).

### 3.2 Mostrar o mapa e retomar pela ordem do gargalo

Com o gargalo eleito (`etapa1.gargalo`), aplicar a **tabela de roteamento por gargalo**
(seção 4) pra saber a ordem das etapas 2/3/4. Percorrer essa ordem e chamar a primeira
que ainda não tiver `concluida_em` preenchido.

Se todas as quatro já estiverem concluídas: não chamar nenhuma etapa — ir direto pra
seção 5 (gerar/mostrar o `PLANO-7-DIAS.md`), a menos que ele já exista e o aluno não
tenha pedido para refazer nada (nesse caso, mostrar o mapa completo + avisar que o
plano já está pronto em `~/minha-maquina-de-vendas/PLANO-7-DIAS.md` e perguntar se ele
quer revisar alguma etapa).

**Nunca chamar de novo uma etapa que já tem `concluida_em` preenchido sem o aluno pedir
explicitamente.** Se ele pedir pra refazer uma etapa específica, é a própria etapa
(`/mva-oferta`, etc.) que decide como tratar isso — esta skill só encaminha o pedido.

### 3.3 Mostrar o mapa (formato de saída)

```
Seu progresso na Imersão Máquina de Vendas Automatizada:

✅ Etapa 1 — Diagnóstico            2026-09-18T13:15:02
⬜ Etapa 2 — Oferta                 pendente
⬜ Etapa 3 — Máquina de leads       pendente
⬜ Etapa 4 — Conversa               pendente

Gargalo eleito: OFERTA
Sua ordem, porque o gargalo é OFERTA: Oferta → Máquina de leads → Conversa
Próximo passo: /mva-oferta
```

A linha "Sua ordem, porque o gargalo é..." é obrigatória sempre que houver gargalo
eleito — o aluno precisa entender que a sequência não é arbitrária.

---

## 4. Tabela de roteamento por gargalo

A etapa 1 é **sempre** a primeira — ela é quem elege o gargalo, então não existe ordem
pra decidir antes dela terminar. A partir daí, a ordem das etapas 2, 3 e 4 muda conforme
o gargalo eleito: o aluno ataca primeiro a etapa que resolve o que trava mais, deixando
o resto pra depois — atacar as quatro fora de ordem é diluir o esforço em algo que hoje
não é o problema dele.

| Gargalo eleito | Ordem das etapas 2/3/4 | Por quê (explicar ao aluno em 1 linha) |
|---|---|---|
| **OFERTA** | Oferta → Máquina de leads → Conversa (`/mva-oferta` → `/mva-maquina` → `/mva-conversa`) | Sem saber o que vender numa frase, organizar leads e treinar conversa é otimizar em cima de uma oferta que ainda não convence. |
| **PROCURA** | Máquina de leads → Oferta → Conversa (`/mva-maquina` → `/mva-oferta` → `/mva-conversa`) | O problema dele não é o que dizer, é pra quem falar — organizar quem já tem e priorizar vem antes de refinar a frase. |
| **CONVERSA** | Conversa → Oferta → Máquina de leads (`/mva-conversa` → `/mva-oferta` → `/mva-maquina`) | Ele já sabe o que vender e pra quem — o vazamento é na call. Treinar a conversa primeiro estanca a perda antes de gerar mais volume pra perder do mesmo jeito. |
| **ACOMPANHAMENTO** | Máquina de leads → Conversa → Oferta (`/mva-maquina` → `/mva-conversa` → `/mva-oferta`) | A venda já está sendo feita e esfriando depois — a máquina de leads é onde o próximo passo fica registrado (e onde os órfãos aparecem), então ela vem primeiro; a conversa reforça o fechamento com data antes de refinar a oferta. |

Esta tabela mapeia exatamente `etapa2 = mva-oferta`, `etapa3 = mva-maquina`,
`etapa4 = mva-conversa` — o mesmo mapeamento de skill usado na seção 3.

---

## 5. Ao final das quatro etapas — gerar o `PLANO-7-DIAS.md`

Só gerar depois que **todas as quatro** tiverem `concluida_em` preenchido. Ler
`perfil.json` inteiro pra montar o plano com dados reais — nunca genérico.

### 5.1 Dimensionar pelo tempo disponível (M4.7 / `etapa4.tempo_dia`)

- Se `etapa4.tempo_dia` estiver vazio ou ausente: **assumir "30min"** e dizer isso
  explicitamente no topo do arquivo e no chat ("Você não informou quanto tempo tem por
  dia — assumi 30min/dia, o mais conservador. Se tiver mais tempo, me diga e eu
  redimensiono.").
- **30min/dia** → 1 tarefa concreta por dia, a mais alavancada pro gargalo, sem tarefa
  secundária.
- **1h/dia** → 1 tarefa principal + 1 tarefa de revisão/registro (ex: atualizar
  `leads.json`, revisar o roteiro do dia anterior).
- **2h+/dia** → tarefa principal + revisão + uma rodada extra (ex: treino de conversa
  adicional, ou cadastrar mais leads).

### 5.2 Conteúdo dos dias 1–6 — puxar das etapas, não inventar

Cada dia é **uma tarefa concreta**, amarrada num artefato que já existe:

| Fonte | Tarefa-tipo pro dia |
|---|---|
| `01-diagnostico.md` / `etapa1.gargalo` | Reler o gargalo eleito e a contradição apontada — decidir 1 mudança de comportamento pro dia. |
| `02-oferta.md` / `etapa2.oferta_frase`, `objecao_trava` | Testar a frase da oferta numa conversa real; usar a resposta pronta da objeção de `objecao_trava` na próxima vez que ela aparecer. |
| `leads.json` / `leads.md` (via `/mva-maquina`) | Rodar "os 3 de hoje" e falar com os 3; marcar próximo passo com data em todo lead sem `proximo_passo_data`. |
| `04-conversa.md` / `etapa4.formato_entrega` | Rodar um treino de roleplay (`/mva-conversa`) contra o tipo de cliente identificado; aplicar o feedback do treino anterior. |

Montar os 6 dias intercalando essas fontes, priorizando a que corresponde ao gargalo
eleito nos dias 1–2 (a ordem da seção 4 já diz qual entra primeiro), e cobrindo as
demais etapas nos dias seguintes. **Nunca inventar tarefa que não vem de um artefato
real do aluno** — se um arquivo não existir ainda (ex.: `leads.json` vazio), a tarefa do
dia é criar o mínimo dele, não pular pra outra coisa genérica.

### 5.3 Dia 7 — sempre medição

O dia 7 nunca é tarefa nova: é **comparar o número de B1.2 do diagnóstico inicial**
(`etapa1.prox_passo_10` — quantas das últimas 10 conversas terminaram com próximo passo
e data) **com o mesmo número, medido de novo, depois dos 6 dias de execução**.

```markdown
## Dia 7 — Meça o resultado

Antes de qualquer coisa nova: repita a pergunta que abriu esse processo.

**Das suas últimas 10 conversas de venda, quantas terminaram com próximo passo e data
marcada?**

No diagnóstico inicial (dia 0), esse número era: **{etapa1.prox_passo_10}/10** (ou "não
informado" se `null`).

Compare com o de hoje. Se subiu, é sinal de que atacar o gargalo certo primeiro
funcionou — continue nele mais uma semana antes de trocar de foco. Se ficou igual ou
caiu, o gargalo pode ter mudado (revise com `/mva-diagnostico` se quiser refazer o
diagnóstico) ou a execução dos 6 dias não aconteceu de verdade — sem julgamento, só
constate e ajuste.
```

Se `etapa1.prox_passo_10` for `null` ("não informado" no diagnóstico original), dizer
isso e comparar de qualquer forma com o número de hoje — o dia 7 vira também a primeira
vez que esse número existe.

### 5.4 Escrever o arquivo — template completo

```markdown
# Plano de 7 dias — Máquina de Vendas Automatizada

**Aluno:** {aluno.nome}
**Gerado em:** {data}
**Gargalo eleito:** {etapa1.gargalo}
**Tempo disponível por dia:** {etapa4.tempo_dia} {"(assumido — você não informou)" se ausente}

Este plano ataca primeiro o que mais trava você hoje ({etapa1.gargalo}) e usa os
arquivos que você já construiu nas 4 etapas — nada aqui é genérico.

## Dia 1 — {tarefa concreta, alavancada pelo gargalo eleito}
{descrição de 2-4 linhas, citando o artefato/dado real}

## Dia 2 — {tarefa concreta}
{...}

## Dia 3 — {tarefa concreta}
{...}

## Dia 4 — {tarefa concreta}
{...}

## Dia 5 — {tarefa concreta}
{...}

## Dia 6 — {tarefa concreta}
{...}

## Dia 7 — Meça o resultado
{bloco da seção 5.3, com os números reais}

## Onde estão seus outros materiais
- Diagnóstico: `~/minha-maquina-de-vendas/01-diagnostico.md`
- Oferta: `~/minha-maquina-de-vendas/02-oferta.md`
- Leads: `~/minha-maquina-de-vendas/leads.md`
- Conversa: `~/minha-maquina-de-vendas/04-conversa.md`
```

Gravar em `~/minha-maquina-de-vendas/PLANO-7-DIAS.md` (mesmo padrão atômico:
`.tmp` + `os.replace`). Depois, resumo curto no chat — os 7 títulos de dia, sem colar
o arquivo inteiro.

---

## 6. Comando de status ("meu progresso", "onde eu estou")

Quando o aluno pedir status sem querer avançar nada: rodar o script da seção 3.1, e
mostrar:

```
Seu progresso na Imersão Máquina de Vendas Automatizada:

{mapa das 4 etapas, ✅/⬜ + data}

Gargalo eleito: {gargalo ou "ainda não diagnosticado"}
Sua oferta em uma frase: {etapa2.oferta_frase ou "ainda não definida"}
Falta: {lista das etapas ⬜ restantes, na ordem certa pro gargalo}
```

Não avançar nenhuma etapa nem chamar nenhuma skill nesse modo — é só leitura.

---

## Compartilhar no grupo da imersão

Duas ocasiões, as duas **perguntando, nunca automático**:

**1. A cada etapa concluída** — quem oferece é a própria skill da etapa; esta aqui não
repete a oferta. Se o aluno pedir aqui ("quero postar o que fiz"), ler
`~/minha-maquina-de-vendas/compartilhar-grupo.md` e mostrar o bloco que já foi gerado,
em vez de escrever outro.

**2. Ao fechar as quatro etapas**, junto com o `PLANO-7-DIAS.md`:

> Quer o resumo da sua máquina pronto pra colar no grupo da imersão?

```
Máquina de vendas montada ✅

Gargalo que eu ataquei: {gargalo eleito}
Minha oferta: "{a frase da etapa 2}"
Leads organizados: {n}
Meus 7 dias começam com: {a tarefa do dia 1}

Volto aqui pra contar o resultado.
```

A última linha fica — é ela que traz o aluno de volta ao grupo com o resultado, que é o
que faz o grupo valer pra quem ainda não começou.

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

- **Refazer uma etapa já concluída sem o aluno pedir.** `concluida_em` preenchido é
  sinal de "feito" — retomar sempre pula pra próxima incompleta, nunca repete.
- **Seguir a ordem 1-2-3-4 fixa ignorando o gargalo eleito.** A ordem das etapas 2/3/4
  vem da tabela da seção 4, nunca da ordem numérica do schema. Só a etapa 1 é fixa.
- **Gerar plano de 1h ou 2h/dia pra quem declarou 30min (ou vice-versa).** O
  dimensionamento do `PLANO-7-DIAS.md` segue `etapa4.tempo_dia` estritamente — se ele
  não respondeu, assumir 30min e dizer que assumiu, nunca chutar um valor maior.
- **Reimplementar aqui o que já está nas quatro skills.** Esta skill nunca faz as 7
  perguntas de nenhuma etapa, nunca calcula score de lead, nunca roda roleplay — ela só
  lê `perfil.json`, decide a ordem, e chama a skill certa. Se sentir vontade de
  "adiantar" uma pergunta de outra etapa, é sinal de que devia estar chamando a skill,
  não fazendo o trabalho dela.
- **Inventar tarefa no plano de 7 dias que não vem de um artefato real do aluno.** Toda
  tarefa cita o arquivo/dado de onde ela nasceu — se o dado não existe, a tarefa é criar
  o mínimo dele, nunca uma tarefa genérica de preenchimento.
- **Gerar o plano antes das quatro etapas estarem concluídas.** Só a seção 5 roda com
  as quatro `concluida_em` preenchidas — antes disso, a resposta certa é retomar a
  etapa pendente.
- **Apagar um `perfil.json` corrompido.** Sempre renomear pra
  `perfil.json.corrompido-<timestamp>` e seguir com um arquivo novo.
- **Usar linguagem de plataforma específica** (amarrar a explicação a um sistema
  operacional determinado) ou **jargão interno ZX LAB** em qualquer mensagem desta
  skill — o aluno só tem o Claude Code dele e a pasta `~/minha-maquina-de-vendas/`.
- **Enviar qualquer coisa no lugar do aluno.** Esta skill entrega o texto pronto; quem posta no grupo é ele.
- **Pôr nome de cliente, empresa ou valor de contrato no texto do grupo** — some sempre, mesmo que o aluno tenha contado na conversa.
