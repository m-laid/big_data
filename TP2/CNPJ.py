import pandas as pd
import dask.dataframe as dd
from memory_profiler import memory_usage
import time
import os
import logging

# إعداد تسجيل الأحداث
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

folder_path = "D:/CNPJ"
output_file = "performance_results.csv"  
reference_file = "D:/CNPJ/reference.csv" 

def measure_time_memory(func, *args):
    start_time = time.time()
    mem_usage = memory_usage((func, args), max_iterations=1)
    exec_time = time.time() - start_time
    return exec_time, max(mem_usage) - min(mem_usage)

def process_with_chunking(file_path):
    chunksize = 1000000
    try:
        for chunk in pd.read_csv(file_path, chunksize=chunksize, on_bad_lines='skip', delimiter=",", dtype=str, engine="c"):
            chunk = chunk.dropna(how='all') 
            logging.info(f"Processing chunk with shape: {chunk.shape}")
    except Exception as e:
        logging.error(f"Error processing with chunking: {e}")

def process_with_dask(file_path):
    try:
        df = dd.read_csv(file_path, assume_missing=True, dtype=str, delimiter=",", on_bad_lines='skip')
        logging.info("Processing with Dask...")
        logging.info(df.head())
        df.sample(frac=0.05).compute()
    except Exception as e:
        logging.error(f"Error processing with Dask: {e}")

def process_entire_file(file_path):
    try:
        df = pd.read_csv(file_path, on_bad_lines='skip', delimiter=",", dtype=str, engine="c", low_memory=False).dropna(how='all')
        df_ref = pd.read_csv(reference_file, on_bad_lines='skip', delimiter=",", dtype=str, engine="c", low_memory=False).dropna(how='all')

        # مقارنة البيانات وإيجاد الاختلافات
        diff = df.merge(df_ref, indicator=True, how='outer').query('_merge != "both"').drop(columns=['_merge'])
        logging.info(f"File {file_path} compared with reference file. Differences found: {len(diff)} rows")

        if not diff.empty:
            diff.to_csv(f"D:/CNPJ/differences_{os.path.basename(file_path)}", index=False)
    except Exception as e:
        logging.error(f"Error comparing file: {e}")

if __name__ == '__main__':
    results = []
    csv_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".csv")]
    
    for file_path in csv_files:
        logging.info(f"\nProcessing file: {file_path}\n")

        logging.info("** Processing with Chunking **")
        exec_time, mem_usage = measure_time_memory(process_with_chunking, file_path)
        results.append([file_path, "Chunking", exec_time, mem_usage])

        logging.info("** Processing with Dask **")
        exec_time, mem_usage = measure_time_memory(process_with_dask, file_path)
        results.append([file_path, "Dask", exec_time, mem_usage])

        logging.info("** Processing Entire File (Comparison) **")
        exec_time, mem_usage = measure_time_memory(process_entire_file, file_path)
        results.append([file_path, "Full File Comparison", exec_time, mem_usage])

    df_results = pd.DataFrame(results, columns=["File", "Method", "Execution Time (s)", "Memory Usage (MB)"])
    df_results.to_csv(output_file, index=False)
    logging.info(f"Performance results saved to {output_file}")
