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

# Lista fixa e explícita das 10 skills da imersão — nunca "tudo que tiver
# na pasta skills/", pra nunca instalar algo que não seja da imersão.
# As 6 primeiras são as etapas da imersão; as 4 últimas são as skills
# comerciais que vieram como bônus.
SKILL_NAMES="maquina-de-vendas mva-diagnostico mva-oferta mva-maquina mva-conversa mva-relatorio checklist-pre-call simulador-vendas analise-call criar-orcamento"

TIMESTAMP="$(date +%Y%m%d-%H%M%S)"

# Interrupção (Ctrl-C, terminal fechado) não deixa pasta temporária para trás.
trap 'rm -rf "${DEST_DIR}"/.instalando-*-$$' EXIT INT TERM

instalados=""
atualizados=""
inalterados=""
ausentes_no_repo=""
falhas=""

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
  #
  # O timestamp tem resolução de 1 segundo: duas rodadas no mesmo segundo, ou um
  # backup antigo com o mesmo nome, faria o mv APAGAR aquele backup. Por isso o
  # nome é escolhido até achar um livre, nunca reutilizado.
  backup="${dest}.bak-${TIMESTAMP}"
  sufixo=2
  while [ -e "${backup}" ]; do
    backup="${dest}.bak-${TIMESTAMP}-${sufixo}"
    sufixo=$((sufixo + 1))
  done

  # A nova versão é copiada PRIMEIRO, para um temporário ao lado. Só depois o
  # que o aluno tinha sai de cena. Fazer na ordem inversa (mover e depois copiar)
  # deixaria a skill SIMPLESMENTE AUSENTE se a cópia falhasse no meio — disco
  # cheio, permissão — e o aluno perderia o comando sem ganhar o novo.
  # Nome começa com ponto: se o instalador for interrompido no meio, a sobra não
  # aparece para o Claude Code como se fosse uma skill.
  novo_tmp="${DEST_DIR}/.instalando-${nome}-$$"
  rm -rf "${novo_tmp}"
  if ! cp -R "${src}" "${novo_tmp}"; then
    rm -rf "${novo_tmp}"
    echo "  ${nome}: não consegui preparar a versão nova — sua versão atual ficou intacta." >&2
    falhas="${falhas} ${nome}"
    continue
  fi
  mv "${dest}" "${backup}"
  if ! mv "${novo_tmp}" "${dest}"; then
    # Não conseguiu pôr a nova no lugar: devolve a do aluno e segue.
    mv "${backup}" "${dest}"
    rm -rf "${novo_tmp}"
    echo "  ${nome}: falhei ao instalar a versão nova — sua versão anterior foi restaurada." >&2
    falhas="${falhas} ${nome}"
    continue
  fi
  atualizados="${atualizados} ${nome}"
  echo "  ${nome}: já existia versão diferente — backup salvo em ${backup}"
done

echo ""

if [ -z "${instalados}" ] && [ -z "${atualizados}" ] && [ -z "${inalterados}" ]; then
  total_skills=0
  for _ in ${SKILL_NAMES}; do total_skills=$((total_skills + 1)); done
  echo "Nada para instalar: nenhuma das ${total_skills} skills foi encontrada em ${SOURCE_DIR}."
  echo "Confirme se você clonou o repositório completo (a pasta skills/ precisa"
  echo "ter as ${total_skills} subpastas)."
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

if [ -n "${falhas}" ]; then
  echo ""
  echo "Não consegui atualizar:${falhas}"
  echo "O que você já tinha continua no lugar. Rode de novo; se persistir, chame no grupo."
fi

echo ""
echo "Pronto. Agora feche e abra o Claude Code de novo (ou reinicie a sessão atual)"
echo "e digite /maquina-de-vendas para começar."
