import redis
import os
from dotenv import load_dotenv

load_dotenv()

# Redis connection
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0
)

def process_task(task_id: str):
    """
    Process a background task from the Redis queue.
    
    Args:
        task_id (str): The ID of the task to process
    """
    # TODO: Implement task processing logic
    print(f"Processing task: {task_id}")

if __name__ == "__main__":
    print("Starting Redis worker...")
    while True:
        try:
            # Get a task from the queue
            task = redis_client.blpop('task_queue', 0)
            task_id = task[1].decode('utf-8')
            
            # Process the task
            process_task(task_id)
            
        except KeyboardInterrupt:
            print("\nShutting down worker...")
            break
        except Exception as e:
            print(f"Error processing task: {e}")
