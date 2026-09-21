---
name: mva-maquina
description: "Monta a máquina de captura, diagnóstico e qualificação de leads do aluno — conduz as 7 perguntas da Etapa 3, cria a lista de leads em arquivo local, constrói com ele o critério de qualificação a partir dos 3 leads mais quentes, calcula o score auditável e prioriza quem falar hoje. Tudo em arquivo local, sem servidor, sem API key extra. Use SEMPRE que o aluno disser: montar minha máquina de vendas, organizar meus leads, cadastrar um lead, novo lead, listar meus leads, priorizar leads, quem eu falo hoje, qualificar lead, meu critério de qualificação, follow-up dos leads, leads sem retorno, /mva-maquina."
model: claude-sonnet-5
effort: medium
---

# Máquina de Vendas — Captura, Diagnóstico e Qualificação (Etapa 3)

## Resumo

Terceira etapa da Imersão Máquina de Vendas Automatizada (bloco 14h–15h). O aluno já
passou pela Etapa 1 (diagnóstico de onde trava) e pela Etapa 2 (oferta e argumentos).
Aqui ele monta, dentro do próprio Claude Code, a parte da máquina que **organiza os
leads que ele já tem** — captura, diagnóstico rápido, um critério de qualificação que
sai da cabeça dele (não de uma fórmula genérica), e uma lista priorizada de quem falar
hoje.

**Tudo roda em arquivo local.** Sem backend, sem porta, sem tunnel, sem `ANTHROPIC_API_KEY`
extra — o motor é o próprio Claude Code do aluno lendo e escrevendo JSON/Markdown em
`~/minha-maquina-de-vendas/`. Não existe versão remota, dashboard web ou multi-usuário
nesta skill — isso é outro produto (não prometer).

Modelo mental herdado da `lead-machine-lite` (lead → diagnóstico → priorização) e da
`diagnostico-cliente` (perguntas uma de cada vez, output sempre em arquivo), mas
reimplementado do zero: a `lead-machine-lite` depende do backend FastAPI que só existe
na infraestrutura ZX LAB — o aluno da imersão não tem isso instalado.

## Regras não-negociáveis (do SPEC-SKILLS-MVA.md — não flexibilizar)

1. Nunca citar marca ou sistema operacional específico do computador do aluno. Sempre
   "no seu computador", "na sua conta", "via Claude Code" — o aluno pode estar em
   Windows, Linux ou num computador da Apple.
2. Zero jargão ZX LAB interno (Mission Control, Supabase do CRM, Evolution, nomes da
   equipe, caminhos `~/.zxlab-*`). O aluno não tem nada disso.
3. Sem preço de produto ZX LAB dentro da skill.
4. Tudo roda local, sem API key extra — o Claude Code do próprio aluno conduz.
5. **Uma pergunta por vez no chat.** Nunca despejar várias de uma vez. Espera a
   resposta, reage em 1 linha, faz a próxima.
6. Output sempre em arquivo (`~/minha-maquina-de-vendas/...`) + resumo curto no chat.
   Nunca só no chat.
7. Português do Brasil, segunda pessoa ("você"), tom direto. Sem emoji decorativo.

## Onde mora tudo

```
~/minha-maquina-de-vendas/
├── perfil.json     # estado compartilhado entre as 4 etapas da imersão
├── leads.json       # lista de leads — fonte de verdade, machine-readable
├── leads.md          # a mesma lista em visão legível pro aluno
└── 03-maquina.md    # como a máquina ficou configurada (gerado no fim desta etapa)
```

`mkdir -p ~/minha-maquina-de-vendas` antes de qualquer escrita, sempre.

## Schema de um lead (em `leads.json`)

```json
{
  "id": "lead-0001",
  "nome": null,
  "empresa": null,
  "origem": null,
  "contato": null,
  "dor_declarada": null,
  "o_que_ele_ja_tem": null,
  "orcamento_sinalizado": null,
  "urgencia": null,
  "decisor": null,
  "ultimo_contato": null,
  "proximo_passo": null,
  "proximo_passo_data": null,
  "status": "novo",
  "score": null,
  "notas": null
}
```

- `status` ∈ `novo | diagnosticado | qualificado | proposta | ganho | perdido | gelado`.
- `ultimo_contato` e `proximo_passo_data` sempre em ISO (`YYYY-MM-DD`), nunca "amanhã"/"semana que vem" — se o aluno responder relativo, converter perguntando a data de hoje se necessário.
- `id` é sequencial, gerado pela skill (`lead-0001`, `lead-0002`, ...), nunca pedido ao aluno.
- **Campo que o aluno não informou fica `null`. Nunca inventar, nunca inferir "provavelmente".** Um `null` é uma lacuna real e deve aparecer como lacuna no `leads.md` (ver seção CAPTURA).

`leads.json` é o array de leads; `leads.md` é a mesma informação em tabela/lista legível, regenerada toda vez que `leads.json` muda — nunca editada à mão em paralelo.

## Modos de uso

Ao ser invocada, se o aluno não disse o que quer, perguntar em 1 linha qual desses ele quer fazer agora (ou seguir o fluxo natural: se `leads.json` não existe, começar pela condução B3.1–B3.7 abaixo antes de qualquer outra coisa).

| Modo | Gatilho | O que faz |
|---|---|---|
| **Condução inicial** | primeira vez, `leads.json` não existe | conduz B3.1–B3.7, constrói o critério de qualificação, cria a máquina |
| **novo lead** | "novo lead", "cadastrar lead", colou uma mensagem/print/e-mail | captura um lead (form guiado ou extração de texto colado) |
| **listar** | "listar leads", "meus leads", "como estão meus leads" | mostra `leads.md` resumido no chat |
| **priorizar** | "priorizar", "quem eu falo hoje", "os 3 de hoje" | roda o scoring e devolve os 3 do dia com próximo passo |
| **marcar próximo passo** | "marca que vou ligar pro fulano dia X", "atualiza o lead Y" | edita `proximo_passo` / `proximo_passo_data` / `status` de um lead existente |
| **órfãos** | "quem tá sem follow-up", "leads esquecidos", "órfãos" | lista todo lead sem `proximo_passo_data` — o gargalo ACOMPANHAMENTO materializado |

Sempre que uma ação muda `leads.json`, regenerar `leads.md` no mesmo passo — os dois nunca ficam dessincronizados.

## 1. Condução inicial — perguntas B3.1 a B3.7

Fazer **uma pergunta por vez**, esperar a resposta, reagir em 1 linha antes da próxima.
Texto literal aprovado — não reescrever:

- **B3.1** — Onde ficam seus leads hoje? (cabeça, WhatsApp, caderno, planilha, CRM)
- **B3.2** — Consegue dizer agora quem são os 3 leads mais quentes e por quê?
- **B3.3** — Quantos leads novos entram por semana, em média?
- **B3.4** — Qual seu critério pra dizer que um lead vale seu tempo?
- **B3.5** — Quanto tempo por dia você gasta decidindo o que fazer em vez de executando?
- **B3.6** — O que você mais gostaria de nunca mais fazer na mão no processo comercial?
- **B3.7** — Você já tem Claude Code / Codex rodando? (sim, uso direto · instalei e parei · nunca usei)

Depois de B3.4, aplicar a lógica de QUALIFICAÇÃO abaixo (ela depende da resposta de B3.2 e B3.4 juntas). Depois de B3.7, encerrar a condução, gravar `perfil.json` e escrever `03-maquina.md`.

Se o aluno já citou nomes de leads em B3.2, oferecer cadastrá-los ali mesmo (indo pro modo "novo lead" pra cada um, rápido) — não obrigar, perguntar se ele quer.

## 2. CAPTURA — novo lead

Dois caminhos, o aluno escolhe (ou a skill detecta sozinha se ele já colar texto):

### 2a. Form guiado (no máximo 6 campos, perguntados juntos numa lista curta se o aluno preferir rápido, ou um a um se ele preferir devagar — perguntar qual)
Os 6 campos essenciais: **nome, empresa/contexto, origem, contato, dor declarada, urgência/data de algo (se houver)**. Os demais campos do schema (`o_que_ele_ja_tem`, `orcamento_sinalizado`, `decisor`, `notas`) ficam `null` até serem informados depois — não são bloqueio pra cadastrar.

### 2b. Colagem crua (mensagem de WhatsApp, e-mail, print transcrito)
O aluno cola o texto bruto. A skill:
1. Lê o texto e tenta extrair o máximo de campos do schema.
2. Mostra pro aluno **o que conseguiu extrair** e **o que ficou em branco**, em formato curto:
   ```
   Extraí isso do que você colou:
   - nome: Marcos (Studio Marcos Fotografia)
   - dor_declarada: "perde muito tempo respondendo os mesmos preços no direct"
   - contato: @studiomarcosfoto (Instagram)

   Não consegui identificar (fica em branco, você completa se quiser):
   - orçamento_sinalizado
   - urgência
   - decisor
   ```
3. Pergunta se algum dos campos em branco ele sabe de cabeça — **uma pergunta, cobrindo os que faltam de uma vez**, não uma por campo (aqui não é o wizard B3, é preenchimento de lacuna pontual).
4. **Nunca inventa dado a partir do texto.** Se o texto não diz o valor, o campo fica `null`. Inferência razoável de contexto (ex: "origem: Instagram" porque a mensagem veio de um DM) é aceitável e deve ser mostrada como extraída, não como suposição escondida — mas dado que não está no texto (ex: orçamento, decisor) nunca é chutado.

Ao final: grava em `leads.json` com `id` novo, `status: "novo"`, `ultimo_contato` = hoje (ISO) se não foi informado outro valor, regenera `leads.md`, confirma em 1 linha.

## 3. QUALIFICAÇÃO — construir o critério COM o aluno

**Nunca aplicar um critério genérico pronto.** Se o aluno respondeu "não tenho" (ou
equivalente) em B3.4, a skill constrói o critério junto com ele, a partir da resposta
de B3.2 (os 3 leads mais quentes que ele já sabe de cor):

1. Perguntar, um de cada vez se precisar: "Desses 3, o que eles têm em comum que os
   outros leads não têm?" — deixar o aluno responder livre.
2. Se a resposta for vaga, ajudar com as 4 dimensões abaixo (nunca impor, oferecer como
   lente): a dor era reconhecida pelo próprio cliente? Havia urgência com data/evento? O
   decisor estava na conversa? Havia sinal de orçamento?
3. Documentar o critério nas palavras do aluno, não reescrito em jargão — o critério final
   que vai pro `03-maquina.md` é a frase dele, com no máximo uma frase de organização da
   skill em cima.

### Score 0–100 — sempre auditável, nunca só o número

```
score = dor (0-30) + urgencia (0-25) + decisor (0-25) + orcamento (0-20)
```

| Componente | Peso | Como pontuar |
|---|---|---|
| **Dor reconhecida pelo próprio cliente** | 0–30 | 30 = ele descreveu a dor com as próprias palavras; 15 = a dor existe mas foi você quem nomeou; 0 = não há sinal de dor reconhecida |
| **Urgência com data ou evento** | 0–25 | 25 = tem data/evento concreto disparando; 12 = "quero resolver logo" sem data; 0 = sem urgência aparente |
| **Decisor na conversa** | 0–25 | 25 = quem decide participou/participa da conversa; 12 = decisor identificado mas fora da conversa; 0 = decisor desconhecido |
| **Orçamento sinalizado** | 0–20 | 20 = valor ou faixa mencionados; 10 = sinal indireto (já pagou por algo parecido); 0 = nenhum sinal |

Campo `null` no lead vira **0 pontos naquele componente**, nunca pontuação estimada — e
isso precisa aparecer na conta mostrada ao aluno (ver abaixo), pra ele ver que o score
baixo às vezes é falta de informação, não falta de qualidade do lead.

**A skill sempre mostra a conta, nunca só o número final.** Exemplo de saída ao
calcular/mostrar o score de um lead:

```
Marcos (Studio Marcos Fotografia) — score 57/100
  dor: 30/30 — ele mesmo disse "perco venda toda semana por demora"
  urgência: 0/25 — sem data ou evento (campo em branco)
  decisor: 25/25 — é ele quem decide, confirmado
  orçamento: 12/20 (na verdade 10, arredondando por sinal indireto: já pagou ferramenta parecida)
```

Gravar o score em `leads.json` (campo `score`) toda vez que for calculado/recalculado —
não só na priorização.

## 4. PRIORIZAÇÃO — "os 3 de hoje"

Comando que lê `leads.json`, recalcula score de quem estiver desatualizado (perguntar
componentes que faltam se fizer sentido, ou usar o que já está gravado), e devolve a
lista ordenada por:

1. `score` decrescente;
2. dentro do mesmo score, quem está há **mais tempo sem contato** primeiro (maior
   diferença entre hoje e `ultimo_contato`).

Excluir da lista quem está `ganho`, `perdido` ou `gelado` — esses não competem por
atenção hoje.

Saída: os 3 primeiros, cada um com **o próximo passo já escrito** (se `proximo_passo`
já existe no lead, repetir; se não existe, propor um próximo passo concreto baseado na
`dor_declarada` e no `status` — e perguntar ao aluno se ele confirma antes de gravar).

```
Hoje, fala com estes 3 (nesta ordem):

1. Marcos — score 57 · sem contato há 6 dias
   Próximo passo: mandar o preço fechado por áudio, ele pediu e ninguém respondeu.

2. ...
```

## 5. Órfãos — o gargalo ACOMPANHAMENTO em dado

Comando que lista todo lead com `proximo_passo_data` = `null` (independente de
status, exceto `ganho`/`perdido`/`gelado`). Essa lista é literalmente o gargalo de
ACOMPANHAMENTO do SPEC virando números — dizer isso ao aluno em 1 linha ao mostrar:

```
Você tem 4 leads sem próximo passo marcado — é aqui que a venda esfria sem ninguém
perceber. Quer marcar um próximo passo pra cada um agora?
```

Se o aluno topar, ir um de cada vez perguntando "próximo passo + data" e gravando.

## 6. Leitura e escrita atômica dos arquivos — blocos Python completos

Usar sempre este padrão (ler → mesclar → gravar atômico, nunca sobrescrever sem ler
antes, nunca apagar arquivo corrompido). Rodar via Bash com `python3` (só stdlib —
`json`, `os`, `shutil`, `datetime`, `tempfile` — sem dependência externa).

### 6a. Helpers comuns (salvar como script temporário ou colar inline no Bash)

```python
import json, os, shutil, tempfile
from datetime import datetime, timezone

BASE_DIR = os.path.expanduser("~/minha-maquina-de-vendas")

def _timestamp():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def ler_json_seguro(caminho, default):
    """Lê um JSON. Se não existir, devolve default. Se estiver corrompido,
    renomeia para <arquivo>.corrompido-<timestamp> (NUNCA apaga) e devolve default."""
    if not os.path.exists(caminho):
        return default
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()
        if not conteudo.strip():
            return default
        return json.loads(conteudo)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        corrompido = f"{caminho}.corrompido-{_timestamp()}"
        shutil.move(caminho, corrompido)
        print(f"[aviso] {caminho} estava corrompido ({e}). "
              f"Preservado em {corrompido}. Recomeçando com dado novo.")
        return default

def gravar_json_atomico(caminho, dado):
    """Grava com write-then-rename: nunca deixa o arquivo em estado parcial
    mesmo se o processo morrer no meio da escrita."""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(
        dir=os.path.dirname(caminho), prefix=".tmp-", suffix=".json"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(dado, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(tmp_path, caminho)
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise
```

### 6b. Perfil compartilhado — ler, mesclar SÓ a própria chave, gravar

```python
PERFIL_PATH = os.path.join(BASE_DIR, "perfil.json")

PERFIL_DEFAULT = {
    "aluno": {"nome": "", "email": "", "whatsapp": ""},
    "etapa1": {}, "etapa2": {}, "etapa3": {}, "etapa4": {},
}

def gravar_etapa3(dados_etapa3: dict):
    """Mescla SOMENTE a chave etapa3 — nunca sobrescreve etapa1/2/4."""
    perfil = ler_json_seguro(PERFIL_PATH, dict(PERFIL_DEFAULT))
    for chave in PERFIL_DEFAULT:
        perfil.setdefault(chave, PERFIL_DEFAULT[chave] if chave != "aluno" else dict(PERFIL_DEFAULT["aluno"]))
    perfil["etapa3"] = {
        "onde_ficam_leads": dados_etapa3.get("onde_ficam_leads", ""),
        "top3_quentes": dados_etapa3.get("top3_quentes", ""),
        "leads_semana": dados_etapa3.get("leads_semana"),
        "criterio_qualificacao": dados_etapa3.get("criterio_qualificacao", ""),
        "tempo_decidindo": dados_etapa3.get("tempo_decidindo", ""),
        "quer_automatizar": dados_etapa3.get("quer_automatizar", ""),
        "usa_claude_code": dados_etapa3.get("usa_claude_code", ""),
        "concluida_em": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    gravar_json_atomico(PERFIL_PATH, perfil)
```

### 6c. Leads — ler lista, adicionar/atualizar, gravar, regenerar `leads.md`

```python
LEADS_PATH = os.path.join(BASE_DIR, "leads.json")
LEADS_MD_PATH = os.path.join(BASE_DIR, "leads.md")

LEAD_DEFAULT = {
    "id": None, "nome": None, "empresa": None, "origem": None, "contato": None,
    "dor_declarada": None, "o_que_ele_ja_tem": None, "orcamento_sinalizado": None,
    "urgencia": None, "decisor": None, "ultimo_contato": None,
    "proximo_passo": None, "proximo_passo_data": None, "status": "novo",
    "score": None, "notas": None,
}

def ler_leads():
    return ler_json_seguro(LEADS_PATH, [])

def proximo_id(leads):
    n = len(leads) + 1
    return f"lead-{n:04d}"

def salvar_novo_lead(campos: dict):
    leads = ler_leads()
    lead = dict(LEAD_DEFAULT)
    lead.update({k: v for k, v in campos.items() if k in LEAD_DEFAULT})
    lead["id"] = proximo_id(leads)
    if not lead.get("ultimo_contato"):
        lead["ultimo_contato"] = datetime.now().strftime("%Y-%m-%d")
    leads.append(lead)
    gravar_json_atomico(LEADS_PATH, leads)
    regenerar_leads_md(leads)
    return lead

def atualizar_lead(lead_id: str, campos: dict):
    leads = ler_leads()
    achou = False
    for lead in leads:
        if lead["id"] == lead_id:
            lead.update({k: v for k, v in campos.items() if k in LEAD_DEFAULT})
            achou = True
            break
    if not achou:
        raise ValueError(f"lead {lead_id} não encontrado")
    gravar_json_atomico(LEADS_PATH, leads)
    regenerar_leads_md(leads)
    return leads

def regenerar_leads_md(leads=None):
    if leads is None:
        leads = ler_leads()
    linhas = ["# Meus leads", "", f"_Atualizado em {datetime.now().strftime('%Y-%m-%d %H:%M')}_", ""]
    if not leads:
        linhas.append("Nenhum lead cadastrado ainda.")
    else:
        linhas.append("| id | nome | status | score | último contato | próximo passo |")
        linhas.append("|---|---|---|---|---|---|")
        for lead in leads:
            linhas.append(
                f"| {lead['id']} | {lead.get('nome') or '_(sem nome)_'} | "
                f"{lead.get('status') or '-'} | {lead.get('score') if lead.get('score') is not None else '-'} | "
                f"{lead.get('ultimo_contato') or '-'} | "
                f"{lead.get('proximo_passo') or '⚠️ sem próximo passo'} "
                f"{('(' + lead['proximo_passo_data'] + ')') if lead.get('proximo_passo_data') else ''} |"
            )
    os.makedirs(BASE_DIR, exist_ok=True)
    with open(LEADS_MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")
```

### 6d. Score e priorização

```python
def calcular_score(lead: dict) -> tuple[int, list[str]]:
    """Devolve (score_total, lista_de_linhas_explicando_a_conta)."""
    linhas = []
    total = 0

    dor = 30 if lead.get("dor_declarada") else 0
    linhas.append(f"  dor: {dor}/30" + (" — declarada pelo próprio lead" if dor else " — sem dor registrada (campo em branco)"))
    total += dor

    urgencia = 25 if lead.get("urgencia") else 0
    linhas.append(f"  urgência: {urgencia}/25" + (f" — {lead['urgencia']}" if urgencia else " — sem data ou evento (campo em branco)"))
    total += urgencia

    decisor = 25 if lead.get("decisor") else 0
    linhas.append(f"  decisor: {decisor}/25" + (f" — {lead['decisor']}" if decisor else " — decisor desconhecido (campo em branco)"))
    total += decisor

    orcamento = 20 if lead.get("orcamento_sinalizado") else 0
    linhas.append(f"  orçamento: {orcamento}/20" + (f" — {lead['orcamento_sinalizado']}" if orcamento else " — nenhum sinal (campo em branco)"))
    total += orcamento

    return total, linhas

def priorizar(top_n=3):
    leads = ler_leads()
    ativos = [l for l in leads if l.get("status") not in ("ganho", "perdido", "gelado")]
    hoje = datetime.now().date()
    def dias_sem_contato(lead):
        if not lead.get("ultimo_contato"):
            return 9999
        try:
            d = datetime.strptime(lead["ultimo_contato"], "%Y-%m-%d").date()
            return (hoje - d).days
        except ValueError:
            return 0
    for lead in ativos:
        score, _ = calcular_score(lead)
        lead["score"] = score
    ativos.sort(key=lambda l: (-l["score"], -dias_sem_contato(l)))
    gravar_json_atomico(LEADS_PATH, leads)  # persiste score recalculado
    regenerar_leads_md(leads)
    return ativos[:top_n]

def listar_orfaos():
    leads = ler_leads()
    return [l for l in leads if l.get("status") not in ("ganho", "perdido", "gelado")
            and not l.get("proximo_passo_data")]
```

Executar estes blocos via Bash como script (`python3 - <<'PY' ... PY` ou arquivo em
`~/minha-maquina-de-vendas/.mva/scripts.py` importado) — nunca reescrever a lógica na
hora, usar exatamente estas funções.

## 7. Template — `03-maquina.md`

Gerado ao final da condução B3.1–B3.7 (e atualizado se o critério de qualificação for
revisado depois). Estrutura fixa:

```markdown
# Sua máquina de vendas — como ficou configurada

*Gerado em {data} · Etapa 3 da Imersão Máquina de Vendas Automatizada*

## Onde seus leads viviam antes
{resposta de B3.1}

## O critério de qualificação — nas suas palavras
{se B3.4 tinha resposta: cita ela.
 se foi construído a partir dos 3 quentes: "Você não tinha um critério parado, então
 construímos um olhando pros seus 3 leads mais quentes ({nomes de B3.2}) — o que eles
 tinham em comum era: {síntese das palavras do aluno}."}

Isso virou a fórmula de score que a máquina usa (0 a 100):
- dor reconhecida pelo cliente: até 30 pontos
- urgência com data ou evento: até 25 pontos
- decisor participando da conversa: até 25 pontos
- orçamento sinalizado: até 20 pontos

## O que a IA assume por você
- Calcula o score de cada lead e mostra a conta, sempre.
- Ordena quem falar primeiro (maior score, depois maior tempo sem contato).
- Avisa quando um lead fica sem próximo passo marcado.
- Extrai campos de uma mensagem colada — mas nunca inventa o que não está escrito.

## O que continua sendo decisão sua
- Se um lead "frio" no score merece atenção mesmo assim (contexto que a máquina não vê).
- O que você fala em cada conversa — a máquina organiza, não substitui a conversa.
- Marcar um lead como ganho/perdido/gelado — isso é leitura sua do que aconteceu.

## Como você mexe nisso a partir de agora
- Novo lead: peça pra cadastrar (ou cole a mensagem/print direto).
- "Quem eu falo hoje" — a máquina te dá os 3 do dia com o próximo passo já escrito.
- "Quem tá sem follow-up" — lista quem ficou órfão de acompanhamento.

## O que essa máquina NÃO faz
Não envia mensagem sozinha, não tem link público, não roda em segundo plano — você
abre o Claude Code e pede. É organização e priorização, não disparo automático.

## Números de hoje
- Leads cadastrados: {n}
- Leads sem próximo passo: {n}
- Leads novos por semana (você estimou): {resposta de B3.3}
```

Ao gravar, também confirmar em 1 linha curta no chat onde o arquivo ficou salvo.

## Compartilhar no grupo da imersão

Depois de gravar `03-maquina.md`, oferecer — **perguntando, nunca automático**:

> Quer o resumo da sua máquina pronto pra colar no grupo da imersão?

Se sim, mostrar em bloco de código e **acrescentar** ao fim de
`~/minha-maquina-de-vendas/compartilhar-grupo.md`:

```
Etapa 3 concluída — Máquina

Leads organizados: {n}
Meu critério de qualificação: {o critério, em uma linha}
Primeiro da fila hoje: {só o motivo — "dor clara + decisor + prazo curto"}
O que eu parei de fazer na mão: {B3.6, em uma linha}
```

🔴 **O lead nunca é identificado.** Vai só o motivo de ele estar em primeiro, nunca nome,
empresa, telefone ou e-mail — e o `leads.json` nunca sai da máquina do aluno.

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

- **Inventar um campo que o lead não deu.** `null` fica `null` — aparece como lacuna no
  `leads.md`, nunca vira um valor chutado "pra completar a linha".
- **Mostrar o score sem mostrar a conta.** Todo score exibido vem com os 4 componentes
  e o porquê de cada pontuação — nunca só o número final.
- **Aplicar um critério de qualificação genérico** quando o aluno já tem os 3 leads
  quentes na mão (B3.2). O critério nasce da experiência real dele, não de uma fórmula
  pronta que a skill trouxe de fábrica.
- **Prometer automação que exige servidor.** Esta skill não manda mensagem sozinha, não
  tem link público, não roda em background — é local e sob comando do aluno. Se ele
  pedir isso, explicar o limite e não fingir que a máquina faz.
- **Citar marca/sistema operacional específico do computador do aluno.** Sempre
  linguagem neutra de plataforma.
- **Despejar as 7 perguntas de uma vez.** Uma por vez, sempre.
- **Editar `leads.md` como se fosse fonte de verdade.** `leads.json` é a fonte;
  `leads.md` é sempre regenerado a partir dele, nunca editado à mão em paralelo.
- **Sobrescrever `perfil.json` inteiro.** Ler tudo, mesclar só `etapa3`, gravar de volta
  — `etapa1`, `etapa2` e `etapa4` nunca são tocadas por esta skill.
- **Apagar um arquivo corrompido.** Renomear para `.corrompido-<timestamp>` e seguir com
  dado novo — o histórico nunca é destruído.
- **Enviar qualquer coisa no lugar do aluno.** Esta skill entrega o texto pronto; quem posta no grupo é ele.
- **Pôr nome de cliente, empresa ou valor de contrato no texto do grupo** — some sempre, mesmo que o aluno tenha contado na conversa.
