import sys
import unittest
from unittest.mock import MagicMock
from benchmark_engine import BenchmarkEngine
from workloads_sc import SCWorkloads
from workloads_mc import MCWorkloads

# Patch methods to run fast
def fast_sc(*args): return 1
def fast_mc(*args): return 1

class TestBenchmark(unittest.TestCase):
    def test_run(self):
        print("Initializing Engine...")
        engine = BenchmarkEngine()
        
        # Monkey patch the task lists in run_suite to use small iterations? 
        # Actually easier to just monkey patch the methods on the instance.
        
        # Patch SC
        for attr in dir(engine.sc):
            if not attr.startswith("__") and callable(getattr(engine.sc, attr)):
                setattr(engine.sc, attr, fast_sc)
        
        # Patch MC
        for attr in dir(engine.mc):
            if not attr.startswith("__") and callable(getattr(engine.mc, attr)):
                # MC methods take kwargs usually, safe to patch
                setattr(engine.mc, attr, fast_mc)

        print("Running Suite (Patched)...")
        results = engine.run_suite(run_sc=True, run_mc=True)
        
        print("Results:", results)
        self.assertIsNotNone(results)
        self.assertGreater(results['total_score'], 0)
        self.assertEqual(results['sc_score'], 0) # Baseline 0.05 / nearly 0 time -> high score likely, but fast_sc returns int 1? No, wait. 
        # The engine calls func(*args). fast_sc returns 1. 
        # Engine measures TIME it takes to run fast_sc. It will be very close to 0. 
        # Baseline / Time -> Score.
        # It should work.

if __name__ == '__main__':
    unittest.main()
