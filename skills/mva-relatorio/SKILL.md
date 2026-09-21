---
name: mva-relatorio
description: "Gera, no seu computador, o PDF do seu relatório da Imersão Máquina de Vendas Automatizada, juntando o diagnóstico, a oferta, a máquina de leads, a conversa e o plano de 7 dias que você já registrou nas etapas anteriores. Use SEMPRE que você disser: gerar meu relatório, quero meu PDF, relatório da imersão, exportar meu diagnóstico, meu relatório em PDF, juntar minhas etapas num PDF, ou /mva-relatorio."
model: claude-sonnet-5
effort: medium
---

# MVA Relatório — seu PDF da imersão

## O que esta skill faz

Junta tudo o que você já registrou em `~/minha-maquina-de-vendas/` — diagnóstico,
oferta, máquina de leads, conversa e o plano de 7 dias, quando existir — num único
PDF, gerado **no seu computador**. Quem monta o texto do PDF é o script
`gerar-pdf.py`, não esta conversa: ele só lê os arquivos que as outras etapas já
gravaram e nunca inventa conteúdo — etapa que você não fez entra no relatório como
uma lacuna declarada, com o comando pra completá-la.

## Passo 1 — Conferir o que já existe

Rode:

```bash
python3 - <<'PYEOF'
import json
from pathlib import Path

pasta = Path.home() / "minha-maquina-de-vendas"
etapas = [
    (1, "Diagnóstico", "01-diagnostico.md", "/mva-diagnostico"),
    (2, "Oferta", "02-oferta.md", "/mva-oferta"),
    (3, "Máquina de leads", "03-maquina.md", "/mva-maquina"),
    (4, "Conversa", "04-conversa.md", "/mva-conversa"),
]

if not pasta.exists():
    print("PASTA_AUSENTE")
else:
    for numero, nome, arquivo, comando in etapas:
        caminho = pasta / arquivo
        feita = caminho.exists() and caminho.read_text(encoding="utf-8").strip()
        print(f"{'OK' if feita else 'FALTA'} etapa{numero} {nome} {comando}")
    plano = pasta / "PLANO-7-DIAS.md"
    print("PLANO_OK" if plano.exists() and plano.read_text(encoding="utf-8").strip() else "PLANO_AUSENTE")
PYEOF
```

- **`PASTA_AUSENTE`** → você ainda não começou a imersão. Diga isso e ofereça chamar
  `/maquina-de-vendas` para começar. Não siga para os próximos passos.
- **Todas as etapas `FALTA`** → não há nada para colocar num relatório ainda. Diga
  isso e ofereça `/maquina-de-vendas` para começar pela etapa 1. Não gere o PDF.
- **Pelo menos uma etapa `OK`** → siga para o Passo 2.

## Passo 2 — Contar pra ele o que entra e o que falta

Antes de gerar qualquer coisa, diga em poucas linhas quais etapas **entram** no
relatório e quais **etapas faltam** (com o comando de cada uma). Se faltar alguma
etapa, **pergunte** se ele quer completá-la agora (chamando a skill correspondente)
antes de gerar o PDF, ou se prefere gerar assim mesmo, com a lacuna declarada.
Nunca decidir isso por conta própria — é a preferência dele.

Se ele pedir para completar uma etapa, chame a skill dela (Skill tool) e, quando
ela terminar, volte para o Passo 1 antes de seguir.

## Passo 3 — Rodar o gerador

O script vem junto com esta skill, sempre no mesmo lugar:

```bash
python3 ~/.claude/skills/mva-relatorio/gerar-pdf.py
```

Se o arquivo não existir aí, a instalação foi parcial. Passe pra ele o comando de
instalação de novo (é seguro rodar quantas vezes quiser):

```bash
git clone https://github.com/zxmarketingdigital/maquina-de-vendas-aluno.git /tmp/mva-$$ && bash /tmp/mva-$$/install.sh && rm -rf /tmp/mva-$$
```

## Passo 4 — Ler a saída

O script:
- Lê `~/minha-maquina-de-vendas/` e monta o relatório (capa com o nome dele, cada
  etapa concluída na ordem, o plano de 7 dias quando existir).
- Salva o PDF em `~/minha-maquina-de-vendas/meu-relatorio.pdf`.
- Se não conseguir gerar PDF nesta máquina (raro — falta engine de PDF instalada),
  salva um `.html` no lugar e explica como abrir e "Imprimir → Salvar como PDF"
  pelo navegador. Ainda assim ele sai com o relatório pronto, só não em PDF.

Leia a saída do script no terminal — ela já diz exatamente qual arquivo foi gerado
e onde.

## Passo 5 — Dizer onde o arquivo ficou

Ao final, diga em 1-2 linhas:
- Se o PDF saiu: o caminho exato (`~/minha-maquina-de-vendas/meu-relatorio.pdf`).
- Se caiu no fallback de HTML: o caminho do `.html` e o passo de abrir no navegador
  e usar "Imprimir → Salvar como PDF".
- Se alguma etapa ficou de fora do relatório: repetir qual, e o comando para
  completá-la depois (o PDF pode ser gerado de novo a qualquer momento).

## O que este PDF não faz

🔴 **O relatório fica só no seu computador.** Este script não manda e-mail, não
manda WhatsApp, não fala com nenhum servidor e não precisa de nenhuma chave de API
— ele só lê arquivos locais e escreve o PDF do lado. Nada é enviado para ninguém
automaticamente. Se você quiser mandar o relatório para alguém (o grupo da imersão,
um sócio, quem for), é você quem anexa o arquivo e envia — esta skill não faz isso
por você.
