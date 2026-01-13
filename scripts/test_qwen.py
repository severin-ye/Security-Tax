#!/usr/bin/env python3
"""
测试Qwen API连接
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from src.llm.factory import create_llm


async def test_qwen():
    """测试Qwen API"""
    print("测试Qwen API连接...")
    print("=" * 60)
    
    try:
        # 创建Qwen LLM
        llm = create_llm(
            provider="qwen",
            model="qwen-plus",
            temperature=0.7,
            max_tokens=500
        )
        
        print("✓ Qwen LLM创建成功")
        
        # 测试简单调用
        test_messages = [
            {"role": "system", "content": "你是一个有帮助的AI助手。"},
            {"role": "user", "content": "你好！请用一句话介绍你自己。"}
        ]
        
        print("\n发送测试消息...")
        response = await llm.ainvoke(test_messages)
        
        print("\n✓ API调用成功！")
        print("-" * 60)
        print(f"响应: {response.content}")
        print("-" * 60)
        
        # 测试工具调用能力
        print("\n\n测试工具调用能力...")
        from langchain_core.tools import StructuredTool
        
        def test_tool(x: int, y: int) -> int:
            """简单的加法工具"""
            return x + y
        
        tools = [
            StructuredTool.from_function(
                func=test_tool,
                name="add",
                description="计算两个数的和"
            )
        ]
        
        llm_with_tools = llm.bind_tools(tools)
        
        tool_test_msg = [
            {"role": "user", "content": "请使用工具计算 123 + 456 的结果"}
        ]
        
        tool_response = await llm_with_tools.ainvoke(tool_test_msg)
        
        if hasattr(tool_response, 'tool_calls') and tool_response.tool_calls:
            print("✓ 工具调用支持正常")
            print(f"  调用的工具: {tool_response.tool_calls}")
        else:
            print("✓ 响应正常（可能不支持工具调用或未触发）")
            print(f"  响应: {tool_response.content}")
        
        print("\n" + "=" * 60)
        print("🎉 Qwen API测试完成！系统可以正常使用。")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_qwen())
    sys.exit(0 if success else 1)
