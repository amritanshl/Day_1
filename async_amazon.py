import asyncio
import time

# 1. Define an Asynchronous Coroutine using 'async def'
async def fetch_amazon_api_data(api_name, delay_seconds):
    print(f"[API START] Requesting data from Amazon {api_name} Engine...")
    
    # We use asyncio.sleep() to simulate a network delay.
    # The 'await' keyword pauses this specific function and hands control back to the Event Loop.
    await asyncio.sleep(delay_seconds)
    
    print(f"[API COMPLETE] Successfully retrieved data from {api_name} Engine.")
    return {api_name: "Production_Data_Payload"}


# 2. Define the Master Coroutine to orchestrate the tasks
async def main():
    start_time = time.perf_counter()
    print("Initializing Asynchronous Inventory Dashboard Pipeline...")
    print("-" * 60)

    # We wrap our coroutines into explicit Task objects. 
    # This tells the Event Loop to prepare them for immediate execution.
    task_1 = asyncio.create_task(fetch_amazon_api_data("Pricing_API", 1.0))
    task_2 = asyncio.create_task(fetch_amazon_api_data("Review_API", 10.0))
    task_3 = asyncio.create_task(fetch_amazon_api_data("Logistics_API", 1.0))

    # asyncio.gather() blocks the main thread here until ALL tasks wrapped inside are resolved.
    # However, inside that window, the tasks run completely concurrently!
    combined_results = await asyncio.gather(task_1, task_2, task_3)
    
    print("-" * 60)
    print(f"All dashboards loaded successfully. Data Aggregated: {combined_results}")
    
    end_time = time.perf_counter()
    print(f"Total Asynchronous Execution Time: {end_time - start_time:.4f} seconds")

# =========================================================================
# RUNTIME ENGINE TRIGGER
# =========================================================================
if __name__ == "__main__":
    # To start an async application from scratch, we use asyncio.run().
    # This boots up the background Event Loop, inserts our main() coroutine, 
    # and shuts down the loop safely once everything concludes.
    asyncio.run(main())