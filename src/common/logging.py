"""Logging utilities for events, messages, and tool calls"""

import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

from src.common.types import Event, Message, ToolCall
from src.common.utils import append_jsonl, ensure_dir

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class SimulationLogger:
    """Centralized logger for simulation events, messages, and tool calls"""
    
    def __init__(self, output_dir: Path):
        """
        Initialize logger with output directory
        
        Args:
            output_dir: Directory to save log files
        """
        self.output_dir = ensure_dir(output_dir)
        self.events_file = self.output_dir / "events.jsonl"
        self.messages_file = self.output_dir / "messages.jsonl"
        self.tool_calls_file = self.output_dir / "tool_calls.jsonl"
        
        # Standard Python logger for console output
        self.logger = logging.getLogger("SimulationLogger")
    
    def log_event(self, event: Event) -> None:
        """Log a simulation event"""
        event_dict = event.model_dump(mode='json')
        append_jsonl(event_dict, self.events_file)
        
        # Also log to console for important events
        if event.event_type.value in ['simulation_start', 'simulation_end', 'explosion', 'attack_injected']:
            self.logger.info(f"Event: {event.event_type.value} - {event.details}")
    
    def log_message(self, message: Message) -> None:
        """Log an agent message"""
        message_dict = message.model_dump(mode='json')
        append_jsonl(message_dict, self.messages_file)
        
        # Log to console with truncated content
        content_preview = message.content[:100] + "..." if len(message.content) > 100 else message.content
        self.logger.debug(f"Message [{message.sender} -> {message.receiver}]: {content_preview}")
    
    def log_tool_call(self, tool_call: ToolCall) -> None:
        """Log a tool call"""
        tool_call_dict = tool_call.model_dump(mode='json')
        append_jsonl(tool_call_dict, self.tool_calls_file)
        
        self.logger.debug(f"Tool call: {tool_call.tool_type.value} by {tool_call.caller}")
    
    def info(self, message: str) -> None:
        """Log info message to console"""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log warning message to console"""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log error message to console"""
        self.logger.error(message)
