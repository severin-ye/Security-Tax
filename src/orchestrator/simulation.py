"""Simulation orchestrator - coordinates entire simulation"""

import asyncio
from pathlib import Path
from typing import Dict, Any, Optional

from src.common.types import Message, MessageRole, Event, EventType, Outcome
from src.common.logging import SimulationLogger
from src.common.utils import set_random_seed, get_timestamp, ensure_dir, load_json, save_json
from src.agents.runtime.agent_factory import AgentFactory
from src.orchestrator.scheduler import ParallelScheduler
from src.orchestrator.lifecycle import LifecycleManager
from src.orchestrator.injection_points import InjectionPointManager


class Simulation:
    """
    Main simulation orchestrator
    Coordinates agent creation, task injection, attack injection, and execution
    """
    
    def __init__(
        self,
        llm_config: Dict[str, Any],
        sim_config: Dict[str, Any],
        defense_config: Optional[Dict[str, Any]] = None,
        seed: int = 42,
        output_dir: Optional[Path] = None
    ):
        """
        Initialize simulation
        
        Args:
            llm_config: LLM configuration
            sim_config: Simulation configuration
            defense_config: Defense configuration
            seed: Random seed for reproducibility
            output_dir: Output directory for logs
        """
        # Set random seed
        set_random_seed(seed)
        self.seed = seed
        
        # Configurations
        self.llm_config = llm_config
        self.sim_config = sim_config
        self.defense_config = defense_config or {}
        
        # Setup output directory
        if output_dir is None:
            timestamp = get_timestamp()
            output_dir = Path("outputs/runs") / f"{timestamp}_seed{seed}"
        self.output_dir = ensure_dir(output_dir)
        
        # Initialize logger
        self.logger = SimulationLogger(self.output_dir)
        
        # Shared state
        self.step_counter = {"current_step": 0}
        
        # Components (to be initialized)
        self.agents = {}
        self.scheduler = None
        self.lifecycle = None
        self.injection_manager = None
        
        self.logger.info(f"Simulation initialized with seed {seed}")
    
    def initialize_agents(self) -> None:
        """Create all agent instances"""
        self.logger.info("Creating agents...")
        
        # Create lifecycle manager first (needed by agents)
        self.lifecycle = LifecycleManager(
            agents={},  # Will be populated
            max_messages=self.sim_config.get("max_messages", 100),
            max_time_s=self.sim_config.get("max_time_s", 300),
            deadlock_timeout_s=self.sim_config.get("deadlock_timeout_s", 10)
        )
        
        factory = AgentFactory(
            llm_config=self.llm_config,
            logger=self.logger,
            step_counter=self.step_counter,
            lifecycle_manager=self.lifecycle
        )
        
        self.agents = factory.create_all_agents(defense_config=self.defense_config)
        
        # Update lifecycle with agents
        self.lifecycle.agents = self.agents
        
        self.logger.log_event(Event(
            event_type=EventType.SIMULATION_START,
            step=0,
            details={
                "num_agents": len(self.agents),
                "defense_config": self.defense_config,
                "seed": self.seed
            }
        ))
    
    async def inject_initial_task(self, task_file: str = "data/tasks/lab_task_mof.json") -> None:
        """
        Inject initial task to Atlas
        
        Args:
            task_file: Path to task JSON file
        """
        self.logger.info("Injecting initial task to Atlas...")
        
        # Load task
        task_data = load_json(task_file)
        
        # Create message for Atlas
        task_message = Message(
            role=MessageRole.USER,
            content=f"New project assignment:\n\n{task_data.get('description', '')}\n\nObjectives:\n" + 
                   "\n".join(f"- {obj}" for obj in task_data.get('objectives', [])),
            sender="System",
            receiver="Atlas",
            step=0
        )
        
        # Enqueue to Atlas
        await self.agents["Atlas"].queue.put(task_message)
        
        self.logger.log_message(task_message)
    
    async def run(self) -> Outcome:
        """
        Run the complete simulation
        
        Returns:
            Outcome object with simulation results
        """
        # Initialize agents
        self.initialize_agents()
        
        # Inject initial task
        await self.inject_initial_task()
        
        # Lifecycle already created in initialize_agents
        self.lifecycle.start()
        
        # Create injection manager (for attacks)
        self.injection_manager = InjectionPointManager(
            agents=self.agents,
            logger=self.logger,
            inject_after_messages=2,  #论文要求：第2条消息后注入
            seed=self.seed
        )
        
        # Create scheduler
        self.scheduler = ParallelScheduler(
            agents=self.agents,
            logger=self.logger,
            step_counter=self.step_counter
        )
        
        # Define termination check
        async def should_stop() -> bool:
            # Increment step counter
            self.step_counter["current_step"] += 1
            
            # Update lifecycle with dequeued count
            total_dequeued = sum(agent.queue.total_dequeued for agent in self.agents.values())
            self.lifecycle.total_dequeued = total_dequeued
            
            # Check and inject attack if needed
            await self.injection_manager.check_and_inject(
                total_dequeued=total_dequeued,
                current_step=self.step_counter["current_step"]
            )
            
            # Check termination
            return self.lifecycle.check_termination()
        
        # Run simulation
        self.logger.info("Starting simulation...")
        await self.scheduler.run(
            should_stop=should_stop,
            max_time=self.sim_config.get("max_time_s", 300)
        )
        
        # Create outcome
        outcome = Outcome(
            success=not self.lifecycle.explosion_occurred,
            termination_reason=self.lifecycle.termination_reason,
            total_steps=self.step_counter["current_step"],
            total_messages=self.lifecycle.total_dequeued,
            explosion_details=self.lifecycle.explosion_details,
            runtime_seconds=self.lifecycle.get_runtime_seconds(),
            config_snapshot={
                "llm_config": self.llm_config,
                "sim_config": self.sim_config,
                "defense_config": self.defense_config,
                "seed": self.seed
            }
        )
        
        # Log final event
        self.logger.log_event(Event(
            event_type=EventType.SIMULATION_END,
            step=self.step_counter["current_step"],
            details={
                "termination_reason": outcome.termination_reason.value,
                "total_messages": outcome.total_messages,
                "success": outcome.success
            }
        ))
        
        # Save outcome
        save_json(outcome.model_dump(mode='json'), self.output_dir / "outcomes.json")
        
        # Save config snapshot
        save_json(outcome.config_snapshot, self.output_dir / "config_snapshot.yaml")
        
        self.logger.info(f"Simulation completed: {outcome.termination_reason.value}")
        
        return outcome
