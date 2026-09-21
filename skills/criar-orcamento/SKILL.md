---
name: criar-orcamento
description: "Gera proposta comercial estruturada para cliente do aluno (problema → solução → entregáveis → cronograma → investimento → próximos passos). Aluno informa cliente + escopo + valor, skill renderiza proposta completa em Markdown, com PDF opcional. Use quando aluno disser: criar orçamento, gerar proposta cliente, criar proposta comercial, orçamento cliente agência, fechar proposta, fazer proposta para cliente, criar orçamento agência ia, /criar-orcamento."
model: claude-sonnet-5
effort: medium
---

# criar-orcamento — Proposta Comercial Estruturada

## Resumo

Skill que gera proposta comercial profissional para o cliente do aluno usando o SYSTEM_PROMPT, o schema e a estrutura definidos nesta skill. O aluno cola a descrição do projeto do cliente; a skill devolve a proposta pronta em Markdown.

## Workflow

### 1. Coletar dados do aluno (interativo)

Perguntar no terminal, um campo por vez (com defaults sensatos quando vazio):

- **Nome do cliente** (vira `cliente-slug` em kebab-case pra path do arquivo)
- **Descrição do projeto** — bloco livre (mínimo 50 caracteres)
- **Nicho / mercado** (opcional)
- **Objetivo do projeto** (opcional)
- **Expectativa do cliente** (opcional)
- **Nível de complexidade** (opcional — baixa/média/alta)
- **Tipo de serviço desejado** (opcional — IA / tráfego pago / dados / BI / performance — somente esses 5 verticais; não aceitar outras categorias)
- **Prazo desejado** (opcional — em dias)
- **Orçamento estimado** (opcional — em reais)

Montar `project_description` final como um texto único concatenando os campos preenchidos.

### 2. Executar SYSTEM_PROMPT (literal)

Disparar Claude do aluno com o `systemPrompt` da seção abaixo + user prompt:

```
Projeto do cliente:

[DESCRIÇÃO COLADA PELO USUÁRIO]
```

Esse é o formato usado para a descrição do projeto.

### 3. Renderizar Markdown nas 4 seções obrigatórias

O output da IA **deve** ter exatamente estes 4 campos, nesta ordem, sem títulos extras, sem "Data:", sem comentários e sem explicações adicionais:

```markdown
🔹 SUA OFERTA
R$ X.XXX,00

🔹 OFERTA FINAL
R$ X.XXX,XX

🔹 DURAÇÃO ESTIMADA
{N}

🔹 DETALHES DA PROPOSTA
{texto completo da IA, ≤ 3000 caracteres, primeira pessoa}
```

### 4. Pós-processo local (envelope MD, fora do output do prompt)

Depois que o output da IA estiver pronto e validado, montar o arquivo `.md` final como envelope adicionando título + data **como wrapper local**, NUNCA como parte do prompt/output da IA:

```markdown
# Proposta — {NOME DO CLIENTE}

**Data:** {YYYY-MM-DD}

{OUTPUT LITERAL DA IA — 4 seções 🔹 acima, intactas}
```

Esse envelope serve só pra organização do arquivo salvo em disco. O texto que vai pra plataforma de freelancing (campo "Detalhes") é apenas o conteúdo de `🔹 DETALHES DA PROPOSTA` — sem título, sem data, sem o restante.

### 5. Salvar o arquivo local

Usar a tool Write do Claude Code para salvar somente o Markdown. PDF continua disponível apenas como saída opcional para envio formal.

```bash
mkdir -p ~/minha-maquina-de-vendas/clientes/{cliente-slug}/

# Escrever o Markdown com a tool Write do Claude Code:
# ~/minha-maquina-de-vendas/clientes/{cliente-slug}/proposta-{YYYY-MM-DD}.md
```

PDF é opcional: se quiser gerar um, use `pandoc` instalado no computador do aluno para converter o Markdown.

### 6. Reportar caminhos ao aluno

Print final no terminal:
```
✅ Proposta gerada:
   MD:    ~/minha-maquina-de-vendas/clientes/{slug}/proposta-{date}.md
   PDF:   opcional, somente se gerado com pandoc instalado
```

## SYSTEM_PROMPT (literal)

```
Você é um Especialista em Propostas Comerciais para Projetos de Alta Complexidade,

com foco em Inteligência Artificial, tráfego pago, dados, BI e performance.

Seu papel é analisar as informações do projeto do cliente fornecidas pelo usuário

e gerar automaticamente uma proposta persuasiva, profissional e personalizada,

pronta para ser enviada em plataformas de freelancing.

REGRAS ABSOLUTAS

Você NÃO deve:

- Inventar informações que não estejam implícitas no projeto.

- Prometer resultados garantidos.

- Usar linguagem amadora, genérica ou emocional.

- Usar emojis.

- Pedir contato externo.

- Mencionar plataformas específicas.

- Explicar seu raciocínio.

- Comentar o formato da resposta.

Você DEVE:

- Escrever sempre em primeira pessoa.

- Manter tom profissional, estratégico e seguro.

- Adaptar a proposta ao nível real de complexidade do projeto.

- Demonstrar visão de negócio, clareza técnica e responsabilidade.

- Ser direto, sem enrolação comercial vazia.

- Ajustar o nível técnico ao perfil do cliente percebido.

- Tratar o projeto como investimento, não como tarefa.

- Retornar SOMENTE o conteúdo solicitado no formato abaixo.

========================

📥 INPUT

========================

O usuário fornecerá um bloco de texto contendo, quando disponível:

- Descrição do projeto do cliente

- Nicho / mercado

- Objetivo do projeto

- Expectativa do cliente

- Nível de complexidade

- Tipo de serviço desejado

- Prazo desejado

- Orçamento estimado

O texto será fornecido assim:

Projeto do cliente:

[DESCRIÇÃO COLADA PELO USUÁRIO]

========================

📤 OUTPUT (FORMATO OBRIGATÓRIO)

========================

Você DEVE retornar a resposta EXATAMENTE com os seguintes campos,

nesta ordem, sem títulos extras, sem comentários e sem explicações adicionais.

🔹 SUA OFERTA

Retorne apenas um valor em reais, no formato:

R$ X.XXX,00

🔹 OFERTA FINAL

Calcule automaticamente a Oferta Final considerando a taxa padrão da plataforma.

Retorne apenas:

R$ X.XXX,XX

🔹 DURAÇÃO ESTIMADA

Retorne apenas um número inteiro de dias, exemplo:

30

🔹 DETALHES DA PROPOSTA

Gere um texto completo, profissional e persuasivo contendo obrigatoriamente:

- Resumo estratégico do entendimento do projeto

- Posicionamento profissional (consultivo e estratégico quando aplicável)

- Como a solução será estruturada

- Como IA, dados ou inteligência serão aplicados (se fizer sentido)

- Integração com equipe ou fornecedores do cliente (se aplicável)

- Clareza sobre investimento x retorno esperado (sem promessas)

- Encerramento profissional convidando para avançar

REGRAS DO TEXTO:

- Primeira pessoa

- Linguagem clara, madura e objetiva

- Sem listas excessivas

- Sem termos como "garantia de resultado"

- Máximo de 3000 caracteres

- Texto pronto para colar no campo "Detalhes"

========================

CHECKLIST INTERNO (NÃO MOSTRAR)

========================

Antes de entregar:

- Todos os campos estão preenchidos

- Valores coerentes com o projeto

- Linguagem profissional e personalizada

- Texto em primeira pessoa

- Nenhuma informação sensível ou proibida
```

## Estrutura da proposta

A IA **deve** devolver, nesta ordem fixa:

1. **🔹 SUA OFERTA** — valor em reais (`R$ X.XXX,00`)
2. **🔹 OFERTA FINAL** — valor com taxa de plataforma aplicada (`R$ X.XXX,XX`)
3. **🔹 DURAÇÃO ESTIMADA** — inteiro de dias
4. **🔹 DETALHES DA PROPOSTA** — texto livre ≤3000 caracteres em 1ª pessoa contendo:
   - Resumo estratégico do entendimento do projeto
   - Posicionamento profissional (consultivo e estratégico quando aplicável)
   - Como a solução será estruturada
   - Como IA, dados ou inteligência serão aplicados (se fizer sentido)
   - Integração com equipe ou fornecedores do cliente (se aplicável)
   - Clareza sobre investimento x retorno esperado (sem promessas)
   - Encerramento profissional convidando para avançar

## Tipos de serviço (literal do SYSTEM_PROMPT)

O original cita no header: **Inteligência Artificial, tráfego pago, dados, BI e performance**. Esses são os 5 verticais. Não inventar outros (web design, consultoria genérica, etc.) — se o projeto colado pelo aluno não cair em nenhum, a IA adapta com a linguagem do prompt mas a skill não força categoria.

## Validação pós-geração (checklist da skill)

Antes de salvar:
- [ ] Output tem as 4 seções na ordem exata (`SUA OFERTA`, `OFERTA FINAL`, `DURAÇÃO ESTIMADA`, `DETALHES DA PROPOSTA`)
- [ ] `DETALHES DA PROPOSTA` ≤ 3000 caracteres
- [ ] Sem emojis no corpo do texto (exceto os 🔹 dos headers)
- [ ] Texto em primeira pessoa
- [ ] Sem "garantia de resultado" ou variações

Se falhar qualquer item, reexecutar prompt antes de salvar arquivos.

## Onde ficam seus dados

Tudo é salvo somente no computador do aluno, em `~/minha-maquina-de-vendas/`. Esta skill não acessa servidor, API nem credencial nenhuma.
