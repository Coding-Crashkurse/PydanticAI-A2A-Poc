# run_client.py
import asyncio
import httpx
import json
from fasta2a.client import A2AClient, Message, UnexpectedResponseError
from fasta2a.schema import TextPart

async def main():
    """
    Uses the fasta2a client with extensive debugging to diagnose the 'failed' status.
    """
    print("➡️  Sending request to the A2A server...")
    
    client = A2AClient(base_url="http://localhost:7000")
    current_task = {}

    try:
        user_message = Message(
            role="user",
            parts=[TextPart(type="text", text="How much does Tiramisu cost?")]
        )

        print("▶️  Sending 'send_task' request...")
        send_response = await client.send_task(message=user_message)
        
        print("\n--- DEBUG: INITIAL RESPONSE ---")
        print(json.dumps(send_response, indent=2))
        print("-----------------------------\n")
        
        task = send_response['result']
        task_id = task['id']
        print(f"✅ Task successfully submitted. Task ID: {task_id}")

        current_task = task
        final_states = ["completed", "failed", "canceled", "rejected"]

        while current_task['status']['state'] not in final_states:
            print(f"   Current status: {current_task['status']['state']}. Waiting 2 seconds...")
            await asyncio.sleep(2)

            get_response = await client.get_task(task_id)
            
            print("\n--- DEBUG: POLLING RESPONSE ---")
            print(json.dumps(get_response, indent=2))
            print("-----------------------------\n")

            current_task = get_response['result']
            
        print(f"   Final status reached: {current_task['status']['state']}")
        
        if current_task['status']['state'] == "completed" and current_task.get('artifacts'):
            final_text = current_task['artifacts'][0]['parts'][0]['text']
            print(f"\n✅ DONE! Response received: '{final_text}'")
        else:
            print(f"\n❌ Task did not complete successfully. Status: {current_task['status']['state']}")
            if current_task.get('status', {}).get('message'):
                 print("   Last server message:", json.dumps(current_task['status']['message'], indent=2))


    except UnexpectedResponseError as e:
        print(f"\n🚨 Error from server: {e.status_code}\n   Response: {e.content}")
    except httpx.ConnectError:
        print(f"\n❌ Connection error. Is the server running?")
    except KeyError as e:
        print(f"\n🚨 Key Error: The expected key '{e}' was not found in the server response.")
        print("   Here is the last task structure we received:")
        print(json.dumps(current_task, indent=2))
    except Exception as e:
        print(f"\n🚨 Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())