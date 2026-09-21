# Máquina de Vendas Automatizada — seus comandos

Este repositório instala, no Claude Code do seu computador, os 10 comandos que você ganhou na Imersão Máquina de Vendas Automatizada — as 6 etapas da imersão e as 4 skills comerciais que vieram como bônus. Com eles você faz um diagnóstico de onde trava pra vender, define sua oferta em uma frase, organiza seus leads, treina a conversa de venda, sai com um plano de 7 dias e gera o seu relatório completo em PDF — tudo rodando dentro do seu próprio Claude Code, sem depender de nenhum site ou login novo.

## Instalação

Copie e cole o bloco abaixo no terminal do seu computador. Pode rodar mais de uma vez sem problema — ele só atualiza o que já existe.

```bash
git clone https://github.com/zxmarketingdigital/maquina-de-vendas-aluno.git /tmp/mva-$$ && bash /tmp/mva-$$/install.sh && rm -rf /tmp/mva-$$
```

Se já tiver clonado o repositório antes, também funciona rodar direto na pasta:

```bash
cd maquina-de-vendas-aluno && git pull && bash install.sh
```

## Como começar

Abra o Claude Code no seu computador e digite:

```
/maquina-de-vendas
```

Na primeira vez, esse comando explica o caminho das 4 etapas, pergunta seu nome e já te leva pro diagnóstico. Nas próximas vezes, ele lembra onde você parou e continua exatamente dali — na ordem certa pro que mais trava você hoje, não numa ordem fixa.

## As 6 etapas da imersão

| Comando | O que faz |
|---|---|
| `/maquina-de-vendas` | Ponto de entrada — mostra seu progresso e te leva pra próxima etapa certa |
| `/mva-diagnostico` | Etapa 1 — 7 perguntas pra achar onde você trava pra vender hoje |
| `/mva-oferta` | Etapa 2 — define sua oferta em uma frase que qualquer pessoa entende |
| `/mva-maquina` | Etapa 3 — organiza seus leads e mostra quem priorizar hoje |
| `/mva-conversa` | Etapa 4 — treina a conversa de venda antes da call de verdade |
| `/mva-relatorio` | Junta tudo o que você respondeu num relatório em PDF, no seu computador |

## As 4 skills comerciais (bônus)

Enquanto as skills acima montam o seu processo, estas quatro trabalham **uma venda específica** — do preparo da call até a proposta. Use quando quiser, em qualquer ordem.

| Comando | O que faz |
|---|---|
| `/checklist-pre-call` | Prepara uma call com nome e data: separa o que você sabe do que está supondo, monta as perguntas de diagnóstico e fixa um objetivo único |
| `/simulador-vendas` | Você treina vendendo e o Claude faz o cliente, no perfil e na dificuldade que você escolher; no fim, feedback com plano de melhoria |
| `/analise-call` | Você cola a transcrição ou o resumo de uma call real e recebe objeções, bloqueios, ajustes e o foco das próximas conversas |
| `/criar-orcamento` | Transforma escopo e valor numa proposta estruturada, pronta para enviar ao cliente |

Um caminho que funciona bem: `/checklist-pre-call` antes da conversa, `/simulador-vendas` para treinar, e `/analise-call` depois que ela acontecer.

Você não precisa rodar os comandos das etapas manualmente na ordem da tabela — use sempre `/maquina-de-vendas` para começar ou continuar, e ele chama a etapa certa por você. O `/mva-relatorio` você chama quando quiser o PDF, com quantas etapas tiver feito.

## Onde ficam seus dados

Tudo o que você responde fica salvo só no seu computador, na pasta:

```
~/minha-maquina-de-vendas/
```

Nada do que você escreve sai daí. Essas skills não têm acesso a nenhuma API, servidor ou credencial — nem sua, nem de ninguém. Elas leem e escrevem arquivos locais e conversam com você pelo próprio Claude Code, só isso.

## Problemas comuns

**O comando não aparece / dá erro de comando não encontrado.** Feche e abra o Claude Code de novo (reinicie a sessão). Os comandos só ficam disponíveis depois que o Claude Code recarrega a lista de skills instaladas.

**Rodei o instalador e não sei se funcionou.** Rode de novo — é seguro, e o instalador mostra no final a lista do que foi instalado ou atualizado.

**Continua sem funcionar, ou tenho outra dúvida.** Pergunte no grupo da imersão — é lá que a gente resolve.
