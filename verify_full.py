import multiprocessing
from benchmark_engine import BenchmarkEngine

def verify():
    print("Starting SiliconBench Verification Run...")
    engine = BenchmarkEngine(log_callback=print)
    
    print("Running Suite...")
    try:
        results = engine.run_suite(run_sc=True, run_mc=True, run_extra=False) # Skip extra to save time
        print("\nVerification Successful!")
        print(f"SC Score: {results['sc_score']}")
        print(f"MC Score: {results['mc_score']}")
        
        if results['mc_score'] > results['sc_score']:
             print("SUCCESS: MC Score is greater than SC Score (Throughput Scaling verified).")
        else:
             print("WARNING: MC Score is NOT greater than SC Score (Check scaling logic).")
             
    except Exception as e:
        print(f"\nVerification FAILED: {e}")
        raise e

if __name__ == '__main__':
    multiprocessing.freeze_support()
    verify()
