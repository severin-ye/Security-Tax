"""Parallel scheduler for running multiple agents concurrently"""

import asyncio
from typing import Dict, Callable, Optional
from src.agents.runtime.agent_runtime import AgentRuntime
from src.common.logging import SimulationLogger


class ParallelScheduler:
    """
    Scheduler for running multiple agents in parallel using asyncio
    """
    
    def __init__(
        self,
        agents: Dict[str, AgentRuntime],
        logger: SimulationLogger,
        step_counter: Dict[str, int]
    ):
        """
        Initialize scheduler
        
        Args:
            agents: Dictionary of agent name -> AgentRuntime
            logger: Simulation logger
            step_counter: Shared step counter
        """
        self.agents = agents
        self.logger = logger
        self.step_counter = step_counter
        
        self.worker_tasks = []
        self.is_running = False
    
    async def agent_worker(
        self,
        agent: AgentRuntime,
        should_stop
    ) -> None:
        """
        Worker coroutine for a single agent
        
        Args:
            agent: AgentRuntime instance
            should_stop: Async function or regular function that returns True when worker should stop
        """
        agent.is_running = True
        
        while True:
            # Check stop condition (support both sync and async)
            if asyncio.iscoroutinefunction(should_stop):
                stop = await should_stop()
            else:
                stop = should_stop()
            
            if stop:
                break
            
            try:
                # Try to process one message
                processed = await agent.step(self.step_counter["current_step"])
                
                if not processed:
                    # Queue was empty, sleep briefly
                    await asyncio.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"Worker error for {agent.name}: {e}")
                await asyncio.sleep(0.5)
        
        agent.is_running = False
        self.logger.info(f"Agent {agent.name} worker stopped")
    
    async def run(
        self,
        should_stop,
        max_time: Optional[float] = None
    ) -> None:
        """
        Run all agent workers in parallel
        
        Args:
            should_stop: Async function or regular function that returns True when simulation should stop
            max_time: Optional maximum time in seconds
        """
        self.is_running = True
        
        # Create worker tasks for each agent
        self.worker_tasks = [
            asyncio.create_task(self.agent_worker(agent, should_stop))
            for agent in self.agents.values()
        ]
        
        self.logger.info(f"Started {len(self.worker_tasks)} agent workers")
        
        # Wait for all workers to complete or timeout
        try:
            if max_time:
                await asyncio.wait_for(
                    asyncio.gather(*self.worker_tasks, return_exceptions=True),
                    timeout=max_time
                )
            else:
                await asyncio.gather(*self.worker_tasks, return_exceptions=True)
        
        except asyncio.TimeoutError:
            self.logger.warning(f"Scheduler timed out after {max_time}s")
        
        finally:
            self.is_running = False
            self.logger.info("All agent workers completed")
    
    def stop(self) -> None:
        """Stop all workers"""
        for task in self.worker_tasks:
            if not task.done():
                task.cancel()
        
        self.is_running = False
