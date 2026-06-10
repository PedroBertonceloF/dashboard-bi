# 📊 Dashboard Guide

## Visão Geral

O Dashboard permite:
1. ✅ Upload de arquivos CSV
2. ✅ Mapeamento de colunas (Data, Categoria, Valor)
3. ✅ Limpeza automática de dados
4. ✅ Visualização de KPIs
5. ✅ Gráficos interativos (Time Series, Categorias, Pizza)
6. ✅ Export de dados processados

## Fluxo de Uso

### 1. Upload de CSV

**Passo 1:** Clique na aba "📁 Upload"

**Passo 2:** Selecione um arquivo CSV

**Passo 3:** Veja a prévia dos dados

**Requisitos do CSV:**
- Formato: `.csv`
- Deve ter colunas com Data, Categoria e Valor
- Pode ter colunas extras (serão preservadas)

**Exemplo de CSV válido:**
```csv
Data,Categoria,Valor,Coluna_Extra
2024-01-01,Vendas,100.50,Extra1
2024-01-02,Vendas,200.00,Extra2
2024-01-03,Lucro,300.75,Extra3
```

### 2. Mapeamento de Colunas

**Passo 1:** Clique na aba "🔗 Column Mapping"

**Passo 2:** Selecione as colunas:
- **📅 Date Column:** Coluna com datas (ex: "Data", "Date", "data_venda")
- **🏷️ Category Column:** Coluna com categorias (ex: "Categoria", "Category", "tipo")
- **💰 Value Column:** Coluna com valores numéricos (ex: "Valor", "Value", "amount")

**Passo 3:** Clique em "Process Dataset"

**O que acontece:**
- Dados são limpados (linhas com valores vazios/inválidos são removidas)
- Espaços em branco são removidos
- Colunas extras são preservadas
- Você vê quantas linhas foram mantidas/removidas

### 3. Dashboard

**Passo 1:** Clique na aba "📊 Dashboard"

**Você verá:**

#### KPIs (Key Performance Indicators)
- **💵 Total Sum:** Soma de todos os valores
- **📊 Average:** Média dos valores
- **📈 Row Count:** Número de linhas processadas

#### Gráficos

**📈 Time Series**
- Mostra valores ao longo do tempo
- Útil para ver tendências
- Eixo X: Data
- Eixo Y: Valor

**🏷️ By Category**
- Mostra valores por categoria
- Gráfico de barras
- Eixo X: Categoria
- Eixo Y: Valor

**🥧 Category Distribution**
- Mostra proporção de cada categoria
- Gráfico de pizza
- Percentual de cada categoria

#### Export
- Clique em "📥 Export as CSV" para baixar dados processados

## Exemplos de Uso

### Exemplo 1: Análise de Vendas

**CSV:**
```csv
Data,Categoria,Valor
2024-01-01,Vendas,1000
2024-01-02,Vendas,1500
2024-01-03,Vendas,1200
2024-01-04,Lucro,500
2024-01-05,Lucro,600
```

**Resultado:**
- Total Sum: $4800
- Average: $960
- Row Count: 5
- Gráfico mostra tendência de vendas
- Pizza mostra 60% Vendas, 40% Lucro

### Exemplo 2: Análise de Receita por Região

**CSV:**
```csv
Data,Região,Receita
2024-01-01,Norte,5000
2024-01-01,Sul,3000
2024-01-02,Norte,5500
2024-01-02,Sul,3200
```

**Resultado:**
- Total Sum: $16700
- Average: $4175
- Gráfico mostra receita por região
- Pizza mostra proporção de cada região

## Tratamento de Erros

### Erro: "Please select a CSV file"
**Causa:** Arquivo não é CSV
**Solução:** Selecione um arquivo `.csv`

### Erro: "Please select all required columns"
**Causa:** Não selecionou todas as 3 colunas
**Solução:** Selecione Date, Category e Value columns

### Erro: "Upload failed"
**Causa:** Arquivo muito grande ou formato inválido
**Solução:** Verifique se o CSV está bem formatado

### Erro: "Failed to load dashboard data"
**Causa:** Problema na API
**Solução:** Verifique se backend está rodando

## Dicas

### 1. Nomes de Colunas
O sistema tenta auto-detectar colunas com nomes comuns:
- Data: "Data", "Date", "data_venda", "data"
- Categoria: "Categoria", "Category", "tipo", "categoria"
- Valor: "Valor", "Value", "amount", "valor"

### 2. Formato de Data
Aceita múltiplos formatos:
- `YYYY-MM-DD` (2024-01-01)
- `DD/MM/YYYY` (01/01/2024)
- `DD-MM-YYYY` (01-01-2024)

### 3. Valores Numéricos
Aceita:
- Inteiros: `100`
- Decimais: `100.50`
- Negativos: `-50`

### 4. Limpeza de Dados
O sistema remove automaticamente:
- Linhas com Data vazia ou inválida
- Linhas com Categoria vazia
- Linhas com Valor vazio ou não-numérico
- Espaços em branco no início/fim

### 5. Colunas Extras
Todas as colunas não mapeadas são preservadas no export

## Troubleshooting

### Gráficos não aparecem
**Causa:** Dados insuficientes
**Solução:** Verifique se o CSV tem pelo menos 2 linhas válidas

### Valores incorretos
**Causa:** Formato de data ou valor inválido
**Solução:** Verifique o CSV e corrija os valores

### Export não funciona
**Causa:** Problema na API
**Solução:** Verifique se backend está rodando

## Recursos Utilizados

- **React 19:** Framework frontend
- **Recharts:** Biblioteca de gráficos
- **Vite:** Build tool
- **TypeScript:** Tipagem estática
- **CSS3:** Estilos responsivos

## Próximos Passos

1. ✅ Upload de CSV
2. ✅ Mapeamento de colunas
3. ✅ Visualização de KPIs
4. ✅ Análise de gráficos
5. ✅ Export de dados

Aproveite! 🎉
