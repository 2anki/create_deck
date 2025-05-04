from typing import Dict, Any
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

def add_task(task_data: Dict[str, Any]) -> str:
    """
    Add a task to the Redis queue.
    
    Args:
        task_data (Dict[str, Any]): Data for the task
        
    Returns:
        str: The task ID
    """
    task_id = f"task_{redis_client.incr('task_counter')}"
    redis_client.rpush('task_queue', task_id)
    redis_client.hset(f'task:{task_id}', mapping=task_data)
    return task_id

def get_task_status(task_id: str) -> Dict[str, Any]:
    """
    Get the status of a task.
    
    Args:
        task_id (str): The ID of the task
        
    Returns:
        Dict[str, Any]: Task status information
    """
    task_data = redis_client.hgetall(f'task:{task_id}')
    return {
        'status': 'pending' if task_data else 'not_found',
        'data': {k.decode(): v.decode() for k, v in task_data.items()}
    }
