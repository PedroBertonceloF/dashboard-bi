import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))
from dataset_ingestion import process_and_clean_dataset

try:
    res = process_and_clean_dataset("adocao_ia_DIRTY.csv", "Data", "Setor", "Valor_Investido")
    print(res)
except Exception as e:
    print("Error:", e)
