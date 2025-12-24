# SiliconBench
#A simple and lightweight benchmarking software written in Python.
🚀 Key Features
Pure Python: Built entirely with the standard library (multiprocessing, tkinter, time), making it lightweight and portable with zero external dependencies.
Real-World Workload Simulation: Uses specific "kernels" that mimic real software behavior rather than abstract loops.
Throughput-Based Scoring: Unlike some benchmarks that average results, SiliconBench measures Total System Throughput for its multi-core score, rewarding high core count and efficient SMT (Simultaneous Multi-Threading).
🧠 Workload Suites
1. Single-Core (Latency)
Measures the raw speed of a single execution thread. Crucial for gaming and responsive desktop usage.

Integer ALU: Heavy integer arithmetic, bitwise operations, and logic gates.
Branch Prediction: Complex, unpredictable if/else chains to stress the CPU's branch predictor.
Scientific Compute: Small Matrix Multiplication (DGEMM-like) and FFT (Fast Fourier Transform).
Cryptography & Compression: Simulated AES encryption rounds and LZ77 compression logic.
2. Multi-Core (Throughput)
Spawns independent instances of the Single-Core suite on every available logical core.

This tests the CPU's ability to handle massive parallel loads (rendering, video export, compilation).
Scaling Factor: The score reflects how well the CPU scales. (e.g., A 8-core CPU should ideally score ~8x the Single-Core score).
3. System & Scaling (Structure)
Specialized tests designed to find bottlenecks in memory and synchronization.

Memory Stream: Read/Write bandwidth tests on large arrays.
Resource Contention: Multiple threads fighting for shared locks and hash maps.
Producer/Consumer: Simulates complex message-passing application architectures.
🛠️ Requirements
Python 3.8+
Works on Windows, Linux, and macOS (multiprocessing support included).
