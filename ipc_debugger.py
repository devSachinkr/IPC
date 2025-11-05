import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import queue

class IPCDebugger:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("IPC Debugger Tool - By Sachin, Nitish, Ahsan")
        self.window.geometry("800x600")
        self.setup_gui()
        
        # IPC- variables (multiprocessing removed)
        self.message_queue = queue.Queue()
        self.shared_data = {"value": 0, "lock": threading.Lock()}
        self.pipe_messages = []  # Simulate pipes with list
        
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Inter-Process Communication (IPC) Debugger", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # IPC Methods Frame
        methods_frame = ttk.LabelFrame(main_frame, text="IPC Methods", padding="10")
        methods_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Buttons for different IPC methods
        ttk.Button(methods_frame, text="Test Pipes", command=self.test_pipes).grid(row=0, column=0, padx=5)
        ttk.Button(methods_frame, text="Test Message Queue", command=self.test_message_queue).grid(row=0, column=1, padx=5)
        ttk.Button(methods_frame, text="Test Shared Memory", command=self.test_shared_memory).grid(row=0, column=2, padx=5)
        ttk.Button(methods_frame, text="Simulate Deadlock", command=self.simulate_deadlock).grid(row=0, column=3, padx=5)
        
        # Input Frame
        input_frame = ttk.LabelFrame(main_frame, text="Test Data Input", padding="10")
        input_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(input_frame, text="Enter Message:").grid(row=0, column=0)
        self.message_entry = ttk.Entry(input_frame, width=50)
        self.message_entry.grid(row=0, column=1, padx=5)
        self.message_entry.insert(0, "Hello from IPC Debugger!")
        
        ttk.Button(input_frame, text="Send Test Data", command=self.send_test_data).grid(row=0, column=2, padx=5)
        
        # Output Frame
        output_frame = ttk.LabelFrame(main_frame, text="Debug Output", padding="10")
        output_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, width=80, height=20)
        self.output_text.grid(row=0, column=0, columnspan=2)
        
        # Clear button
        ttk.Button(output_frame, text="Clear Output", command=self.clear_output).grid(row=1, column=0, pady=5)
        
        # Configure grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
    def log_message(self, message):
        """Add message to output text area"""
        self.output_text.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.output_text.see(tk.END)
        
    def clear_output(self):
        """Clear the output text area"""
        self.output_text.delete(1.0, tk.END)
        
    def test_pipes(self):
        """Test pipe communication simulation"""
        self.log_message("🧪 Testing PIPE Communication...")
        
        message = self.message_entry.get()
        
        def pipe_worker():
            try:
                # Simulate pipe processing
                time.sleep(1)
                result = f"Processed: {message}"
                self.pipe_messages.append(result)
                self.log_message(f"✅ Pipe Response: {result}")
            except Exception as e:
                self.log_message(f"❌ Pipe Error: {e}")
        
        # Start thread for pipe simulation
        thread = threading.Thread(target=pipe_worker)
        thread.start()
        
    def test_message_queue(self):
        """Test message queue communication"""
        self.log_message("🧪 Testing MESSAGE QUEUE...")
        
        def queue_worker():
            try:
                message = self.message_entry.get()
                # Simulate processing
                time.sleep(1)
                self.message_queue.put(f"Queue Response: {message.upper()}")
                
                # Check queue and display result
                response = self.message_queue.get(timeout=2)
                self.log_message(f"✅ {response}")
            except Exception as e:
                self.log_message(f"❌ Queue Error: {e}")
        
        thread = threading.Thread(target=queue_worker)
        thread.start()
        
    def test_shared_memory(self):
        """Test shared memory simulation"""
        self.log_message("🧪 Testing SHARED MEMORY...")
        
        def memory_worker():
            try:
                with self.shared_data["lock"]:
                    original_value = self.shared_data["value"]
                    self.shared_data["value"] += 5
                    time.sleep(1)  # Simulate work
                    result = self.shared_data["value"]
                    self.log_message(f"✅ Shared Memory Updated: {original_value} → {result}")
            except Exception as e:
                self.log_message(f"❌ Shared Memory Error: {e}")
        
        thread = threading.Thread(target=memory_worker)
        thread.start()
        
    def simulate_deadlock(self):
        """Simulate a deadlock scenario"""
        self.log_message("⚠️ Simulating DEADLOCK Scenario...")
        
        # Create two locks for deadlock simulation
        lock1 = threading.Lock()
        lock2 = threading.Lock()
        
        def worker1():
            self.log_message("Worker 1: Acquiring Lock 1...")
            lock1.acquire()
            time.sleep(1)
            self.log_message("Worker 1: Trying to acquire Lock 2... (DEADLOCK)")
            lock2.acquire()  # This will cause deadlock
            lock1.release()
            lock2.release()
            
        def worker2():
            self.log_message("Worker 2: Acquiring Lock 2...")
            lock2.acquire()
            time.sleep(1)
            self.log_message("Worker 2: Trying to acquire Lock 1... (DEADLOCK)")
            lock1.acquire()  # This will cause deadlock
            lock2.release()
            lock1.release()
        
        # Start both workers
        t1 = threading.Thread(target=worker1)
        t2 = threading.Thread(target=worker2)
        
        t1.start()
        t2.start()
        
        # Check for deadlock after 3 seconds
        def check_deadlock():
            t1.join(timeout=2)
            t2.join(timeout=2)
            
            if t1.is_alive() or t2.is_alive():
                self.log_message("🔴 DEADLOCK DETECTED! Both threads are stuck")
                self.log_message("💡 Solution: Use timeout in lock acquisition or consistent lock ordering")
            else:
                self.log_message("✅ No deadlock occurred")
        
        self.window.after(3000, check_deadlock)
        
    def send_test_data(self):
        """Send test data using all IPC methods"""
        message = self.message_entry.get()
        self.log_message(f"📤 Sending test data: '{message}'")
        
        # Test all methods with delay
        self.window.after(500, self.test_pipes)
        self.window.after(1500, self.test_message_queue)
        self.window.after(2500, self.test_shared_memory)
        
    def run(self):
        """Start the application"""
        self.log_message("🚀 IPC Debugger Started Successfully!")
        self.log_message("💡 Use buttons to test different IPC methods")
        self.window.mainloop()

if __name__ == "__main__":
    # Create & run the debugger
    debugger = IPCDebugger()
    debugger.run()