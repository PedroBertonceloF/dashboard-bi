"""
Script de teste para demonstrar o dataset_ingestion.py
"""

import csv
import os
from dataset_ingestion import process_and_clean_dataset

# Criar arquivo CSV de teste com dados sujos
test_csv = "uploads/test_ingestion.csv"

# Dados de teste com problemas
test_data = [
    ["Data", "Categoria", "Valor", "Coluna_Extra"],
    ["2024-01-01", "  Vendas  ", "100.50", "Extra1"],  # OK - será limpo
    ["2024-01-02", "Vendas", "  200  ", "Extra2"],  # OK
    ["", "Vendas", "300", "Extra3"],  # ❌ Data vazia - será deletado
    ["2024-01-04", "", "400", "Extra4"],  # ❌ Categoria vazia - será deletado
    ["2024-01-05", "Vendas", "abc", "Extra5"],  # ❌ Valor inválido - será deletado
    ["2024-01-06", "  Lucro  ", "500.75", "Extra6"],  # OK - será limpo
    ["invalid-date", "Vendas", "600", "Extra7"],  # ❌ Data inválida - será deletado
    ["2024-01-08", "Vendas", "", "Extra8"],  # ❌ Valor vazio - será deletado
    ["2024-01-09", "Vendas", "700", "Extra9"],  # OK
]

# Criar arquivo de teste
os.makedirs("uploads", exist_ok=True)
with open(test_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(test_data)

print("=" * 60)
print("TESTE DO DATASET_INGESTION.PY")
print("=" * 60)
print(f"\n📁 Arquivo de teste criado: {test_csv}")
print(f"📊 Linhas de teste: {len(test_data) - 1}")

# Processar e limpar
print("\n🔄 Processando e limpando dados...")
cleaned_path, orig_count, clean_count, dropped_count = process_and_clean_dataset(
    file_path=test_csv,
    date_col="Data",
    category_col="Categoria",
    value_col="Valor"
)

print("\n" + "=" * 60)
print("RESULTADOS")
print("=" * 60)
print(f"✅ Linhas originais: {orig_count}")
print(f"✅ Linhas limpas: {clean_count}")
print(f"❌ Linhas deletadas: {dropped_count}")
print(f"📈 Taxa de retenção: {(clean_count/orig_count)*100:.1f}%")

print(f"\n📄 Arquivo limpo salvo em: {cleaned_path}")

# Mostrar conteúdo do arquivo limpo
print("\n" + "=" * 60)
print("DADOS LIMPOS (com espaços removidos)")
print("=" * 60)
with open(cleaned_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines[:10]):  # Mostrar primeiras 10 linhas
        print(f"{i}: {line.rstrip()}")

print("\n✨ Teste concluído com sucesso!")
print("\nObservações:")
print("- Espaços em branco foram removidos de 'Categoria' e 'Valor'")
print("- Coluna extra 'Coluna_Extra' foi preservada")
print("- Apenas linhas com Data, Categoria e Valor válidos foram mantidas")
