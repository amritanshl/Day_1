import time

def benchmark_membership_testing():
    print("\n" + "="*60)
    print("DEMO 1: MEMBERSHIP TESTING TRAP (LIST VS SET)")
    print("="*60)
    
    # Generate 100,000 sequential numeric IDs
    total_elements = 100000
    raw_data_ids = list(range(total_elements))
    
    # Cast identical data into a C-optimized Hash Set
    optimized_set = set(raw_data_ids)
    
    # Target element to search for (using a worst-case scenario element near the end)
    search_target = 99999
    
    # --- Test Path A: The Sequential List ---
    start_time = time.perf_counter()
    # Runs an O(N) linear scan look-loop
    for _ in range(1000): # Repeat lookup to amplify the measurement window
        _ = search_target in raw_data_ids
    list_duration = time.perf_counter() - start_time
    print(f"-> Traditional List Lookup O(N) Duration : {list_duration:.6f} seconds")
    
    # --- Test Path B: The Hash Set ---
    start_time = time.perf_counter()
    # Runs an O(1) constant time direct lookup
    for _ in range(1000):
        _ = search_target in optimized_set
    set_duration = time.perf_counter() - start_time
    print(f"-> Optimized Set Lookup O(1) Duration    : {set_duration:.6f} seconds")
    
    performance_gap = list_duration / max(set_duration, 1e-9)
    print(f"STATUS: Set lookup was approx {performance_gap:.1f}x faster than the list!")


def benchmark_string_concatenation():
    print("\n" + "="*60)
    print("DEMO 2: STRING CONCATENATION PITFALL (+ VS JOIN)")
    print("="*60)
    
    # Array of 50,000 small text log segments
    iterations = 50000
    log_chunks = ["Log_Entry_Row_Item_Index_" for _ in range(iterations)]
    
    # --- Test Path A: Loop-based string addition ---
    start_time = time.perf_counter()
    vulnerable_string = ""
    for chunk in log_chunks:
        vulnerable_string += chunk  # Forces continuous memory re-allocation blocks
    loop_duration = time.perf_counter() - start_time
    print(f"-> Inefficient Loop Addition (+) Duration: {loop_duration:.6f} seconds")
    
    # --- Test Path B: The C-Optimized .join method ---
    start_time = time.perf_counter()
    # Forces single memory allocation block assignment pass
    secure_string = "".join(log_chunks)
    join_duration = time.perf_counter() - start_time
    print(f"-> Optimized String .join() Duration     : {join_duration:.6f} seconds")
    
    performance_gap = loop_duration / max(join_duration, 1e-9)
    print(f"STATUS: .join() was approx {performance_gap:.1f}x faster than loop additions!")


# ==========================================
# MAIN ROUTINE EXECUTION CORE
# ==========================================
if __name__ == "__main__":
    print("=== STARTING ARCHITECTURAL PERFORMANCE BENCHMARKING LAB ===")
    
    benchmark_membership_testing()
    benchmark_string_concatenation()
    
    print("\n" + "="*60)
    print("Performance Sandbox Auditing Successfully Closed.")