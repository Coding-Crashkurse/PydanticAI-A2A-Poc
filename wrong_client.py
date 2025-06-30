import asyncio
import httpx
from uuid import uuid4
import traceback
import json

from a2a.client import A2AClient, A2ACardResolver, A2AClientHTTPError
from a2a.client.helpers import create_text_message_object
from a2a.types import MessageSendParams, SendMessageRequest, Role

BASE_URL = "http://localhost:7000"

async def main():
    print(f"▶️  Connecting to the A2A Agent at {BASE_URL}...")

    try:
        async with httpx.AsyncClient(timeout=30.0) as httpx_client:
            resolver = A2ACardResolver(httpx_client=httpx_client, base_url=BASE_URL)
            agent_card = await resolver.get_agent_card()
            client = A2AClient(httpx_client=httpx_client, agent_card=agent_card)

            print(f"✅ Successfully connected to Agent: '{agent_card.name}'")
            print("-" * 50)

            user_message = create_text_message_object(
                role=Role.user,
                content="What do you have for appetizers?",
            )
            
            request = SendMessageRequest(
                params=MessageSendParams(message=user_message),
                id=f"request-{uuid4().hex}",
            )
            
            await client.send_message(request)

            print("\n❌ SURPRISE! The server unexpectedly accepted the request.")

    except A2AClientHTTPError as e:
        print("\n✅ ERROR CAUGHT AS EXPECTED!")
        print("-" * 50)
        print(f"   The server responded with an HTTP error: {e.status_code}")
        
        server_response_text = e.message
        print("\n--- RESPONSE FROM SERVER ---")
        try:
            parsed_error = json.loads(server_response_text)
            print(json.dumps(parsed_error, indent=2))
        except json.JSONDecodeError:
            print(server_response_text)
    except httpx.ConnectError:
        print(f"\n❌ Connection error. Is the server running at {BASE_URL}?")
    except Exception as e:
        print(f"\n🚨 An unexpected error occurred: {type(e).__name__}: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
