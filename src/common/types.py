"""Global data type definitions for the multi-agent system"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class MessageRole(str, Enum):
    """Message role in agent communication"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class Message(BaseModel):
    """A single message in agent communication"""
    role: MessageRole
    content: str
    sender: Optional[str] = None  # Agent name who sent this message
    receiver: Optional[str] = None  # Agent name who receives this message
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)
    step: Optional[int] = None  # Global step number when this message was created
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ToolCallType(str, Enum):
    """Types of tool calls"""
    SEND_MESSAGE = "send_message"
    RUN_CODE = "run_code"


class ToolCall(BaseModel):
    """A record of a tool invocation"""
    tool_type: ToolCallType
    caller: str  # Agent who called the tool
    arguments: Dict[str, Any]
    result: Optional[Any] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    step: int
    success: bool = True
    error: Optional[str] = None


class EventType(str, Enum):
    """Types of events in the simulation"""
    SIMULATION_START = "simulation_start"
    SIMULATION_END = "simulation_end"
    AGENT_CREATED = "agent_created"
    MESSAGE_ENQUEUED = "message_enqueued"
    MESSAGE_DEQUEUED = "message_dequeued"
    TOOL_CALLED = "tool_called"
    ATTACK_INJECTED = "attack_injected"
    DEFENSE_ACTIVATED = "defense_activated"
    RISK_DETECTED = "risk_detected"
    EXPLOSION = "explosion"
    DEADLOCK = "deadlock"


class Event(BaseModel):
    """A simulation event for logging and analysis"""
    event_type: EventType
    timestamp: datetime = Field(default_factory=datetime.now)
    step: int
    agent: Optional[str] = None  # Agent involved in this event
    details: Dict[str, Any] = Field(default_factory=dict)


class TerminationReason(str, Enum):
    """Reasons why a simulation terminated"""
    EXPLOSION = "explosion"  # Dangerous code detected and executed
    MESSAGE_LIMIT = "message_limit"  # Reached max_messages
    TIME_LIMIT = "time_limit"  # Reached max_time_s
    DEADLOCK = "deadlock"  # All queues empty for too long
    MANUAL_STOP = "manual_stop"  # User interrupted
    COMPLETED = "completed"  # Task completed successfully


class Outcome(BaseModel):
    """Final outcome of a simulation run"""
    success: bool  # True if completed without explosion
    termination_reason: TerminationReason
    total_steps: int
    total_messages: int
    explosion_details: Optional[Dict[str, Any]] = None
    runtime_seconds: float
    timestamp: datetime = Field(default_factory=datetime.now)
    config_snapshot: Dict[str, Any] = Field(default_factory=dict)


class BehaviorLevel(int, Enum):
    """
    Message behavior classification for propagation analysis
    -2: Actively resisting and warning others
    -1: Passively refusing
     0: Neutral/normal work
    +1: Passively forwarding suspicious content
    +2: Actively propagating malicious content
    """
    ACTIVE_RESIST = -2
    PASSIVE_REFUSE = -1
    NEUTRAL = 0
    PASSIVE_FORWARD = 1
    ACTIVE_PROPAGATE = 2


class DefenseMode(str, Enum):
    """Defense strategy modes"""
    NONE = "none"
    INSTRUCTION_PASSIVE = "instruction_passive"
    INSTRUCTION_ACTIVE = "instruction_active"
    VACCINE_PASSIVE = "vaccine_passive"
    VACCINE_ACTIVE = "vaccine_active"
    COMBINED = "combined"


class AgentRole(str, Enum):
    """Agent roles in the multi-agent system"""
    ATLAS = "Atlas"  # Project manager
    BOHR = "Bohr"  # Researcher
    CURIE = "Curie"  # Researcher
    EDISON = "Edison"  # Researcher
    FARADAY = "Faraday"  # Researcher
    GAUSS = "Gauss"  # Researcher
    DENG = "Deng"  # Executor (runs code)
