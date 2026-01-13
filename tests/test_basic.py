"""Simple tests for core functionality"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from src.common.types import Message, MessageRole
from src.common.utils import set_random_seed
from src.tools.risk_rules import risk_detector


def test_risk_detector():
    """Test risk detection"""
    print("Testing risk detector...")
    
    # Test dangerous code
    dangerous_code = """
import chlorine
import ammonia
mix(chlorine, ammonia)
"""
    
    is_dangerous, details = risk_detector.check_code(dangerous_code)
    assert is_dangerous, "Should detect dangerous chemical combination"
    print(f"✓ Detected dangerous code: {details['risk_type']}")
    
    # Test safe code
    safe_code = """
import numpy as np
result = np.mean([1, 2, 3])
"""
    
    is_dangerous, details = risk_detector.check_code(safe_code)
    assert not is_dangerous, "Should not flag safe code"
    print("✓ Safe code passed")


def test_message_creation():
    """Test message creation"""
    print("\nTesting message creation...")
    
    msg = Message(
        role=MessageRole.USER,
        content="Test message",
        sender="TestAgent",
        receiver="TargetAgent"
    )
    
    assert msg.sender == "TestAgent"
    assert msg.content == "Test message"
    print("✓ Message creation successful")


async def test_message_queue():
    """Test message queue"""
    print("\nTesting message queue...")
    
    from src.agents.runtime.message_queue import MessageQueue
    
    queue = MessageQueue()
    
    msg1 = Message(role=MessageRole.USER, content="First")
    msg2 = Message(role=MessageRole.USER, content="Second")
    
    await queue.put(msg1)
    await queue.put(msg2)
    
    assert queue.qsize() == 2
    
    retrieved1 = await queue.get()
    assert retrieved1.content == "First"
    print("✓ Message queue FIFO works")


def test_random_seed():
    """Test random seed reproducibility"""
    print("\nTesting random seed...")
    
    import random
    
    set_random_seed(42)
    val1 = random.random()
    
    set_random_seed(42)
    val2 = random.random()
    
    assert val1 == val2, "Random seed should produce same values"
    print(f"✓ Random seed reproducible: {val1}")


def run_sync_tests():
    """Run all synchronous tests"""
    test_risk_detector()
    test_message_creation()
    test_random_seed()


async def run_async_tests():
    """Run all asynchronous tests"""
    await test_message_queue()


if __name__ == "__main__":
    print("="*60)
    print("Running Multi-Agent Security Tax Tests")
    print("="*60)
    
    # Run sync tests
    run_sync_tests()
    
    # Run async tests
    asyncio.run(run_async_tests())
    
    print("\n" + "="*60)
    print("All tests passed! ✓")
    print("="*60)
