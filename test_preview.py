import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))
from dataset_ingestion import save_and_preview_csv

try:
    with open("adocao_ia_DIRTY.csv", "rb") as f:
        res = save_and_preview_csv(f, "test_preview.csv")
    print(res)
except Exception as e:
    import traceback
    traceback.print_exc()
