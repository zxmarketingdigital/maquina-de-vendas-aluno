---
name: analise-call
description: "Analisa call de vendas colada no chat. Identifica objeções perdidas, gatilhos não usados, próximos passos sugeridos e script de follow-up sugerido. Output em Markdown. Use quando aluno disser: analisar call de vendas, revisar call comercial, feedback de call, análise call cliente, call coach, melhorar próxima call, follow-up call vendas, /analise-call."
model: claude-sonnet-5
effort: high
---

# analise-call — Análise de Call de Vendas

## Resumo

Skill local que recebe a transcrição ou o resumo de uma call de vendas colado no chat, gera análise estruturada (score, strengths, blockers, improvements, objections, qualification, next_call_focus) e salva o resultado em Markdown em `~/minha-maquina-de-vendas/calls/{cliente-slug}/call-{YYYY-MM-DD}.md`.

## Workflow

### Etapa 1 — Coleta da transcrição

O aluno deve sempre colar no chat a transcrição ou o resumo da call. Usar o texto colado diretamente como `transcript_text`. Pedir o título (`call_title`) se não estiver óbvio.

### Etapa 2 — Coletar contexto opcional do vendedor

Se aluno informar (ou já estiver no contexto do projeto), montar o bloco `user_context`:

```
- nome
- momento_profissional
- maior_dificuldade
- experiencia_ia
```

Não inventar. Se não tiver, omitir o bloco.

### Etapa 3 — Executar análise

**SYSTEM_PROMPT (literal — não editar):**

```
Você é um especialista em análise de calls de vendas. Seu papel é avaliar transcrições de ligações comerciais e fornecer feedback estratégico, prático e objetivo.

REGRAS CRÍTICAS:
1. Responda EXCLUSIVAMENTE no formato JSON especificado pela função "analyze_call"
2. Nunca inclua markdown, explicações ou texto fora do JSON
3. Use português brasileiro (pt-BR)
4. Seja objetivo e estratégico - sem frases motivacionais ou genéricas
5. O score deve ser um número inteiro de 0 a 100
6. Se a transcrição estiver curta, incompleta ou de baixa qualidade, aponte isso em blockers e sugira melhorias

CRITÉRIOS DE AVALIAÇÃO:
- Score 0-30: Call com problemas graves (sem rapport, sem qualificação, sem próximo passo)
- Score 31-50: Call básica com melhorias significativas necessárias
- Score 51-70: Call razoável com pontos a melhorar
- Score 71-85: Boa call com pequenos ajustes
- Score 86-100: Call excelente, modelo a seguir

CRITÉRIOS MÍNIMOS:
- strengths: 3 a 6 itens específicos
- blockers: 3 a 6 itens (erros que travam fechamento)
- improvements: 4 a 8 itens práticos com exemplos de frase
- objections: 2 a 5 itens (se não houver, indicar "não identificada claramente" e orientar como descobrir)
- next_call_focus: exatamente 3 itens prioritários
- qualification: sempre preenchido; se não houver informação, indicar "não identificado na call" e sugerir pergunta
```

**USER_PROMPT (template literal):**

```
Analise a seguinte call de vendas:

Título: {call_title}{contextInfo}

TRANSCRIÇÃO:
{transcript_text}

Forneça uma análise completa usando a função analyze_call.
```

Onde `contextInfo` é, se houver `user_context`:

```
\n\nContexto do vendedor:
Nome do vendedor: ...
Momento profissional: ...
Maior dificuldade: ...
Experiência com IA: ...
```

A skill (rodando dentro do Claude) executa o raciocínio diretamente — não há HTTP. Mas o output JSON deve respeitar **literalmente** o schema abaixo.

### Etapa 4 — Schema de output

```json
{
  "type": "object",
  "properties": {
    "score": { "type": "integer", "minimum": 0, "maximum": 100, "description": "Score geral da call de 0 a 100" },
    "strengths": { "type": "array", "items": { "type": "string" }, "minItems": 3, "maxItems": 6, "description": "Lista de 3 a 6 pontos fortes identificados na call" },
    "blockers": { "type": "array", "items": { "type": "string" }, "minItems": 3, "maxItems": 6, "description": "Lista de 3 a 6 erros ou bloqueios que travam o fechamento" },
    "improvements": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "title": { "type": "string", "description": "Título curto da melhoria" },
          "detail": { "type": "string", "description": "Explicação detalhada do que melhorar" },
          "example_phrase": { "type": "string", "description": "Exemplo de frase que poderia ser usada" }
        },
        "required": ["title", "detail", "example_phrase"]
      },
      "description": "Lista de 4 a 8 melhorias práticas com exemplos",
      "minItems": 4,
      "maxItems": 8
    },
    "next_call_focus": { "type": "array", "items": { "type": "string" }, "minItems": 3, "maxItems": 3, "description": "Exatamente 3 focos prioritários para a próxima call" },
    "objections": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "objection": { "type": "string", "description": "A objeção identificada ou 'não identificada claramente'" },
          "how_handled": { "type": "string", "description": "Como foi tratada na call" },
          "better_way": { "type": "string", "description": "Forma melhor de tratar essa objeção" }
        },
        "required": ["objection", "how_handled", "better_way"]
      },
      "description": "Lista de 2 a 5 objeções analisadas",
      "minItems": 2,
      "maxItems": 5
    },
    "qualification": {
      "type": "object",
      "properties": {
        "dor": { "type": "string", "description": "Dor/problema do cliente identificado ou 'não identificado na call - sugestão de pergunta'" },
        "urgencia": { "type": "string", "description": "Nível de urgência do cliente ou 'não identificado na call - sugestão de pergunta'" },
        "budget": { "type": "string", "description": "Orçamento disponível ou 'não identificado na call - sugestão de pergunta'" },
        "decisor": { "type": "string", "description": "Quem é o decisor ou 'não identificado na call - sugestão de pergunta'" },
        "proximo_passo": { "type": "string", "description": "Próximo passo acordado ou 'não identificado na call - sugestão de pergunta'" }
      },
      "required": ["dor", "urgencia", "budget", "decisor", "proximo_passo"],
      "description": "Qualificação do lead baseada na call"
    }
  },
  "required": ["score", "strengths", "blockers", "improvements", "next_call_focus", "objections", "qualification"]
}
```

**Pós-processamento:**

- `score = Math.max(0, Math.min(100, Math.round(Number(score) || 0)))`
- `model_version = "v1"` (constante)
- Se algum array vier vazio, manter `[]`
- `qualification` ausente → preencher cada campo com `"não identificado na call"`

### Etapa 5 — Renderizar Markdown

Estrutura do arquivo `~/minha-maquina-de-vendas/calls/{cliente-slug}/call-{YYYY-MM-DD}.md`:

```markdown
# Análise de Call — {call_title}

**Data:** {YYYY-MM-DD} · **Score:** {score}/100 · **Modelo:** v1

## Qualificação (BANT+)
- **Dor:** {qualification.dor}
- **Urgência:** {qualification.urgencia}
- **Budget:** {qualification.budget}
- **Decisor:** {qualification.decisor}
- **Próximo passo:** {qualification.proximo_passo}

## Pontos Fortes
- ...

## Bloqueios (travam fechamento)
- ...

## Objeções
### {objection}
- **Como foi tratada:** {how_handled}
- **Forma melhor:** {better_way}

## Melhorias Práticas
### {title}
{detail}

> Frase exemplo: "{example_phrase}"

## Foco das próximas 3 calls
1. ...
2. ...
3. ...

## Script de Follow-up sugerido
(Claude gera mensagem WhatsApp/email curta baseada em `next_call_focus` + `qualification.proximo_passo` — esta seção é EXTRA, não vem do schema, fica claramente marcada.)
```

### Etapa 6 — Salvar Markdown

```bash
mkdir -p ~/minha-maquina-de-vendas/calls/{slug}/

# Escrever o Markdown com a tool Write do Claude Code:
# ~/minha-maquina-de-vendas/calls/{slug}/call-{date}.md

echo "✅ MD: ~/minha-maquina-de-vendas/calls/{slug}/call-{date}.md"
echo "Score {score}/100"
```

`{slug}` = derivado do `call_title` (lowercase, sem acento, hífen).

## Onde ficam seus dados

Tudo é salvo somente no computador do aluno, em `~/minha-maquina-de-vendas/`. Esta skill não acessa servidor, API nem credencial nenhuma.
