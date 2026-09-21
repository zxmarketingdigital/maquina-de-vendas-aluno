# Histórico de Sessões — maquina-de-vendas-aluno

> Registro do que foi feito a cada sessão de trabalho neste projeto (mais recente no topo).
> Mantido pelo `/encerrar` via `zx-worklog.py`. Ler no início pra recuperar contexto.

---

## 2026-09-21 — Publicar as 6 skills da Imersao MVA como repo publico para o aluno

**Feito:** repo publico zxmarketingdigital/maquina-de-vendas-aluno com 6 skills (maquina-de-vendas, mva-diagnostico, mva-oferta, mva-maquina, mva-conversa, mva-relatorio) + install.sh idempotente. Mensagem de instalacao enviada ao grupo da imersao em 21/09 19:58.
**Arquivos:** install.sh (copy-first + swap + rollback, trap de limpeza), skills/mva-relatorio/gerar-pdf.py (weasyprint -> navegador headless -> HTML), README.md.
**Review:** luna-review em loop ate 0 ALTO (5 ALTO + 5 MEDIO corrigidos; 1 falso positivo documentado no commit 341d8ae).
**Deploy:** push verificado por zx-run-verificado --git-push (SHA no remote), gh repo view = PUBLIC/main. Teste ponta a ponta contra HOME temporario com o comando exato da mensagem: 6 skills instaladas, 2a rodada idempotente, PDF com assinatura %PDF- em 1s.
**Pendencias:** decidir se o aluno envia o perfil.json de volta — gerar_relatorio_mva.py (Resend + Evolution) esta pronto e revisado, mas nenhum fluxo aponta pra ele.

