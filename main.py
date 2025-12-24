import tkinter as tk
from tkinter import ttk, messagebox
import threading
import platform
import multiprocessing
from benchmark_engine import BenchmarkEngine

class SiliconBenchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SiliconBench - High Performance Synthetic Benchmark")
        self.root.geometry("800x600")
        self.root.configure(bg="#202020") 
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#202020")
        style.configure("TLabel", background="#202020", foreground="#e0e0e0", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#00aaff")
        style.configure("ScoreBox.TLabel", font=("Segoe UI", 24, "bold"), foreground="#ffffff")
        style.configure("ScoreTitle.TLabel", font=("Segoe UI", 10, "bold"), foreground="#aaaaaa")
        style.configure("TCheckbutton", background="#202020", foreground="#e0e0e0")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), background="#333333", foreground="#ffffff")
        
        # Header
        header_frame = ttk.Frame(root)
        header_frame.pack(fill=tk.X, padx=20, pady=15)
        
        title_lbl = ttk.Label(header_frame, text="SILICONBENCH", style="Header.TLabel")
        title_lbl.pack(side=tk.LEFT)
        
        sys_info = f"{platform.system()} | {platform.processor()} | {multiprocessing.cpu_count()} Cores"
        sys_lbl = ttk.Label(header_frame, text=sys_info)
        sys_lbl.pack(side=tk.RIGHT, pady=10)
        
        # Options
        file_frame = ttk.Frame(root)
        file_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.var_sc = tk.BooleanVar(value=True)
        self.var_mc = tk.BooleanVar(value=True)
        self.var_ex = tk.BooleanVar(value=True)
        
        c1 = ttk.Checkbutton(file_frame, text="Single-Core", variable=self.var_sc)
        c1.pack(side=tk.LEFT, padx=10)
        
        c2 = ttk.Checkbutton(file_frame, text="Multi-Core (Throughput)", variable=self.var_mc)
        c2.pack(side=tk.LEFT, padx=10)
        
        c3 = ttk.Checkbutton(file_frame, text="System Scaling", variable=self.var_ex)
        c3.pack(side=tk.LEFT, padx=10)
        
        # Run Button
        self.run_btn = ttk.Button(file_frame, text="RUN BENCHMARK", command=self.start_benchmark)
        self.run_btn.pack(side=tk.RIGHT, padx=10)

        # Scores Area (Grid)
        score_frame = ttk.Frame(root)
        score_frame.pack(fill=tk.X, padx=40, pady=20)
        score_frame.columnconfigure(0, weight=1)
        score_frame.columnconfigure(1, weight=1)
        score_frame.columnconfigure(2, weight=1)
        
        # SC Score
        sc_box = ttk.Frame(score_frame, borderwidth=2, relief="groove")
        sc_box.grid(row=0, column=0, padx=10, sticky="ew")
        ttk.Label(sc_box, text="SINGLE-CORE", style="ScoreTitle.TLabel").pack(pady=(10,0))
        self.lbl_sc = ttk.Label(sc_box, text="---", style="ScoreBox.TLabel")
        self.lbl_sc.pack(pady=(0,10))
        
        # MC Score
        mc_box = ttk.Frame(score_frame, borderwidth=2, relief="groove")
        mc_box.grid(row=0, column=1, padx=10, sticky="ew")
        ttk.Label(mc_box, text="MULTI-CORE", style="ScoreTitle.TLabel").pack(pady=(10,0))
        self.lbl_mc = ttk.Label(mc_box, text="---", style="ScoreBox.TLabel")
        self.lbl_mc.pack(pady=(0,10))
        
        # Extra Score
        ex_box = ttk.Frame(score_frame, borderwidth=2, relief="groove")
        ex_box.grid(row=0, column=2, padx=10, sticky="ew")
        ttk.Label(ex_box, text="SYSTEM", style="ScoreTitle.TLabel").pack(pady=(10,0))
        self.lbl_ex = ttk.Label(ex_box, text="---", style="ScoreBox.TLabel")
        self.lbl_ex.pack(pady=(0,10))
        

        # Progress
        progress_frame = ttk.Frame(root)
        progress_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.lbl_status = ttk.Label(progress_frame, text="Ready to benchmark.")
        self.lbl_status.pack(anchor=tk.W)
        
        self.progress = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.pack(fill=tk.X, pady=5)
        
        # Log Area
        log_frame = ttk.Frame(root)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.txt_log = tk.Text(log_frame, height=10, bg="#101010", fg="#00ff00", font=("Consolas", 9), relief="flat")
        self.txt_log.pack(fill=tk.BOTH, expand=True)

        self.engine = BenchmarkEngine(log_callback=self.log_gui, progress_callback=self.prog_gui)
        self.thread = None

    def log_gui(self, msg):
        self.root.after(0, lambda: self._append_log(msg))

    def _append_log(self, msg):
        self.txt_log.insert(tk.END, msg + "\n")
        self.txt_log.see(tk.END)
        # Update status label with generic info if 'Running' is in msg
        if "Running" in msg:
            self.lbl_status.config(text=msg)

    def prog_gui(self, current, total):
        self.root.after(0, lambda: self.progress.config(value=(current/total)*100))

    def start_benchmark(self):
        if not (self.var_sc.get() or self.var_mc.get() or self.var_ex.get()):
            messagebox.showwarning("Warning", "Select at least one suite!")
            return
            
        self.run_btn.config(state=tk.DISABLED)
        # Reset scores
        self.lbl_sc.config(text="---", foreground="#ffffff")
        self.lbl_mc.config(text="---", foreground="#ffffff")
        self.lbl_ex.config(text="---", foreground="#ffffff")
        self.txt_log.delete(1.0, tk.END)
        
        self.thread = threading.Thread(target=self._worker)
        self.thread.start()

    def _worker(self):
        results = self.engine.run_suite(
            run_sc=self.var_sc.get(),
            run_mc=self.var_mc.get(),
            run_extra=self.var_ex.get()
        )
        self.root.after(0, lambda: self._finish(results))

    def _finish(self, results):
        self.run_btn.config(state=tk.NORMAL)
        self.lbl_status.config(text="Benchmark Complete.")
        
        if results:
            self.lbl_sc.config(text=f"{results['sc_score']}", foreground="#00aaff")
            self.lbl_mc.config(text=f"{results['mc_score']}", foreground="#00aaff")
            self.lbl_ex.config(text=f"{results['extra_score']}", foreground="#00aaff")
            
            summary = (f"\n=== FINAL SCORES ===\n"
                       f"Single-Core: {results['sc_score']}\n"
                       f"Multi-Core:  {results['mc_score']}\n"
                       f"System:      {results['extra_score']}\n")
            self._append_log(summary)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    root = tk.Tk()
    app = SiliconBenchApp(root)
    root.mainloop()
