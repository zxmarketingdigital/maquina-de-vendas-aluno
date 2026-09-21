# Máquina de Vendas Automatizada — seus comandos

Este repositório instala, no Claude Code do seu computador, os 6 comandos que você ganhou na Imersão Máquina de Vendas Automatizada. Com eles você faz um diagnóstico de onde trava pra vender, define sua oferta em uma frase, organiza seus leads, treina a conversa de venda, sai com um plano de 7 dias e gera o seu relatório completo em PDF — tudo rodando dentro do seu próprio Claude Code, sem depender de nenhum site ou login novo.

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

## Os 6 comandos

| Comando | O que faz |
|---|---|
| `/maquina-de-vendas` | Ponto de entrada — mostra seu progresso e te leva pra próxima etapa certa |
| `/mva-diagnostico` | Etapa 1 — 7 perguntas pra achar onde você trava pra vender hoje |
| `/mva-oferta` | Etapa 2 — define sua oferta em uma frase que qualquer pessoa entende |
| `/mva-maquina` | Etapa 3 — organiza seus leads e mostra quem priorizar hoje |
| `/mva-conversa` | Etapa 4 — treina a conversa de venda antes da call de verdade |
| `/mva-relatorio` | Junta tudo o que você respondeu num relatório em PDF, no seu computador |

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
