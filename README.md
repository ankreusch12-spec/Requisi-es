# Acompanhamento de Requisições

Página para cadastrar e acompanhar requisições do Workday: vagas, buffer, candidatos, treinamento, ALO e alertas. Substitui a planilha *Acompanhamento de Requisição.xlsx*.

**Versão em uso (dados compartilhados):** https://claude.ai/artifact/69dHyQrvVCBFMs5TLCH5ee

## Arquivos

| Arquivo | O que é |
|---|---|
| `index.html` | A página completa (HTML, CSS e JS num arquivo só). |
| `scripts/build_seed.py` | Converte a planilha em `seed.json`, usado pelo botão **Importar histórico**. |

Os dados (`seed.json` e a planilha `.xlsx`) **não** ficam no repositório, porque ele é público. Estão no `.gitignore`.

## Como funciona

- A página roda como Artifact do claude.ai e guarda os dados no banco compartilhado do artefato (`db`): coleções `reqs` e `carteiras` e o documento `config/feriados`.
- Fora do claude.ai, a página abre em modo somente leitura e mostra o `seed.json`, se ele estiver na mesma pasta.

## Gerar o seed a partir da planilha

```bash
pip install openpyxl
python3 scripts/build_seed.py "Acompanhamento de Requisição.xlsx" seed.json
```

## Regras de cálculo

- **Buffer:** 50% da necessidade, ajustável em cada requisição.
- **Total:** necessidade + buffer.
- **Presentes:** selecionados − no show. Se houver lista de candidatos, a contagem sai da lista.
- **ALO:** início do treinamento + dias de treinamento, contando de segunda a sábado e pulando os feriados cadastrados.
- **Início sugerido:** hoje + 21 dias úteis (segunda a sexta). Se cair no dia 25 ou depois, usa o dia 24 do mês.
- **Alertas:**
  - ALO vencido sem completar a necessidade.
  - Treinamento em até 7 dias sem o total selecionado.
  - Sem acompanhamento há 7 dias.
  - Workday duplicado.
