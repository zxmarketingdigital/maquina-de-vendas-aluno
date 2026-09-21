#!/usr/bin/env bash
# Instalador dos comandos da Imersão Máquina de Vendas Automatizada.
#
# Copia as skills de ./skills/<nome> para ~/.claude/skills/<nome>.
# Idempotente: rodar de novo só atualiza o que mudou. Nunca apaga nada
# que você já tinha — se uma skill já existir e for diferente da do
# repositório, ela é salva em backup antes de ser sobrescrita.
#
# Compatível com bash 3.2 (o padrão do macOS) e Linux — sem declare -A,
# sem mapfile, sem nenhum recurso de bash 4+.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="${SCRIPT_DIR}/skills"
DEST_DIR="${HOME}/.claude/skills"

# Lista fixa e explícita das 6 skills da imersão — nunca "tudo que tiver
# na pasta skills/", pra nunca instalar algo que não seja da imersão.
SKILL_NAMES="maquina-de-vendas mva-diagnostico mva-oferta mva-maquina mva-conversa mva-relatorio"

TIMESTAMP="$(date +%Y%m%d-%H%M%S)"

instalados=""
atualizados=""
inalterados=""
ausentes_no_repo=""

echo "Instalando os comandos da Máquina de Vendas Automatizada..."
echo ""

mkdir -p "${DEST_DIR}"

for nome in ${SKILL_NAMES}; do
  src="${SOURCE_DIR}/${nome}"
  dest="${DEST_DIR}/${nome}"

  if [ ! -d "${src}" ]; then
    # Skill ainda não está nesta cópia do repositório (ex.: skills/
    # vazia, só com o .gitkeep). Não é erro — só não há o que copiar.
    ausentes_no_repo="${ausentes_no_repo} ${nome}"
    continue
  fi

  if [ ! -e "${dest}" ]; then
    cp -R "${src}" "${dest}"
    instalados="${instalados} ${nome}"
    continue
  fi

  if diff -rq "${src}" "${dest}" > /dev/null 2>&1; then
    inalterados="${inalterados} ${nome}"
    continue
  fi

  # Já existe e é diferente do que vem do repositório: nunca sobrescrever
  # sem backup. O backup preserva exatamente o que o aluno tinha.
  backup="${dest}.bak-${TIMESTAMP}"
  mv "${dest}" "${backup}"
  cp -R "${src}" "${dest}"
  atualizados="${atualizados} ${nome}"
  echo "  ${nome}: já existia versão diferente — backup salvo em ${backup}"
done

echo ""

if [ -z "${instalados}" ] && [ -z "${atualizados}" ] && [ -z "${inalterados}" ]; then
  echo "Nada para instalar: nenhuma das 5 skills foi encontrada em ${SOURCE_DIR}."
  echo "Confirme se você clonou o repositório completo (a pasta skills/ precisa"
  echo "ter as 5 subpastas, não só o .gitkeep)."
  exit 0
fi

if [ -n "${instalados}" ]; then
  echo "Instaladas agora:"
  for nome in ${instalados}; do
    echo "  - ${nome}"
  done
fi

if [ -n "${atualizados}" ]; then
  echo "Atualizadas (versão anterior salva em backup):"
  for nome in ${atualizados}; do
    echo "  - ${nome}"
  done
fi

if [ -n "${inalterados}" ]; then
  echo "Já estavam atualizadas (nada mudou):"
  for nome in ${inalterados}; do
    echo "  - ${nome}"
  done
fi

if [ -n "${ausentes_no_repo}" ]; then
  echo ""
  echo "Aviso: não encontrei no repositório as skills:${ausentes_no_repo}"
  echo "(normal se você clonou uma versão parcial; rode 'git pull' e instale de novo)."
fi

echo ""
echo "Pronto. Agora feche e abra o Claude Code de novo (ou reinicie a sessão atual)"
echo "e digite /maquina-de-vendas para começar."
