"""Minimal test to isolate the chatbot endpoint issue."""
import asyncio
import sys
sys.path.insert(0, '.')

from src.api.chatbot.schemas import MessageRequest
from src.chatbot.context_manager import context_manager
from src.chatbot.intent_parser import get_intent_parser

async def test_minimal():
    """Test just the intent parsing part."""
    print("1. Creating session...")
    session = context_manager.create_session()
    print(f"   Session created: {session.id}")

    print("\n2. Getting intent parser...")
    intent_parser = get_intent_parser()
    print(f"   Parser model: {intent_parser.model}")

    print("\n3. Parsing intent (this is where it might hang)...")
    try:
        intent = await asyncio.wait_for(
            intent_parser.parse_intent("add task to buy milk", session.context_window),
            timeout=15
        )
        print(f"   SUCCESS! Intent: {intent.action}, confidence: {intent.confidence}")
        return True
    except asyncio.TimeoutError:
        print("   TIMEOUT after 15 seconds")
        return False
    except Exception as e:
        print(f"   ERROR: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_minimal())
    sys.exit(0 if result else 1)
