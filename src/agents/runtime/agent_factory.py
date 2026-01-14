"""Factory for creating agent instances with proper configuration"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional

from src.agents.runtime.agent_runtime import AgentRuntime
from src.agents.memory.vaccines import inject_vaccine
from src.common.logging import SimulationLogger
from src.llm.factory import create_llm
from src.tools.messaging import MessagingTool, create_send_message_function
from src.tools.run_code import CodeExecutionTool, create_run_code_function
from src.tools.langchain_adapters import create_agent_tools


class AgentFactory:
    """Factory for creating configured agent instances"""
    
    def __init__(
        self,
        llm_config: Dict[str, Any],
        logger: SimulationLogger,
        step_counter: Dict[str, int],
        lifecycle_manager=None
    ):
        """
        Initialize agent factory
        
        Args:
            llm_config: LLM configuration
            logger: Simulation logger
            step_counter: Shared step counter
            lifecycle_manager: Optional lifecycle manager for explosion reporting
        """
        self.llm_config = llm_config
        self.logger = logger
        self.step_counter = step_counter
        self.lifecycle_manager = lifecycle_manager
        
        # Create shared tools
        self.messaging_tool = None  # Will be set after agents are created
        self.code_tool = CodeExecutionTool(
            enable_execution=False,
            lifecycle_manager=lifecycle_manager
        )  # Simulation mode
        
        # Role configurations
        self.roles_dir = Path(__file__).parent.parent / "roles"
    
    def load_role_config(self, agent_name: str) -> Dict[str, Any]:
        """
        Load role configuration from YAML file
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            Role configuration dict
        """
        config_file = self.roles_dir / f"{agent_name.lower()}.yaml"
        
        if not config_file.exists():
            raise FileNotFoundError(f"Role config not found: {config_file}")
        
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def create_agent(
        self,
        agent_name: str,
        agents_registry: Dict[str, AgentRuntime],
        defense_config: Optional[Dict[str, Any]] = None
    ) -> AgentRuntime:
        """
        Create a single agent instance
        
        Args:
            agent_name: Name of the agent
            agents_registry: Registry of all agents (for messaging)
            defense_config: Optional defense configuration
            
        Returns:
            Configured AgentRuntime instance
        """
        # Load role configuration
        role_config = self.load_role_config(agent_name)
        
        # Create LLM instance
        llm = create_llm(
            provider=self.llm_config.get("provider", "openai"),
            model=self.llm_config.get("model", "gpt-4"),
            temperature=self.llm_config.get("temperature", 0.7),
            max_tokens=self.llm_config.get("max_tokens", 2000)
        )
        
        # Create messaging function for this agent
        if not self.messaging_tool:
            self.messaging_tool = MessagingTool(agents_registry, self.logger)
        
        send_message_func = create_send_message_function(
            self.messaging_tool,
            sender=agent_name,
            step_counter=self.step_counter
        )
        
        # Create run_code function if agent can run code
        run_code_func = None
        if role_config.get("can_run_code", False):
            run_code_func = create_run_code_function(
                self.code_tool,
                caller=agent_name,
                step_counter=self.step_counter
            )
        
        # Determine agent role type
        if agent_name == "Atlas":
            role_type = "manager"
        elif agent_name == "Deng":
            role_type = "executor"
        else:
            role_type = "researcher"
        
        # Create LangChain tools
        tools = create_agent_tools(
            send_message_func=send_message_func,
            run_code_func=run_code_func,
            agent_role=role_type
        )
        
        # Create agent runtime
        agent = AgentRuntime(
            name=agent_name,
            role_config=role_config,
            llm=llm,
            tools=tools,
            logger=self.logger,
            defense_config=defense_config
        )
        
        # Apply vaccine defense if configured
        if defense_config and defense_config.get("vaccine_defense"):
            vaccine_config = defense_config["vaccine_defense"]
            vaccine_mode = vaccine_config.get("mode")
            
            if vaccine_mode:
                inject_vaccine(agent.memory, vaccine_type=vaccine_mode)
                self.logger.info(f"Injected {vaccine_mode} vaccine into {agent_name}")
        
        return agent
    
    def create_all_agents(
        self,
        defense_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, AgentRuntime]:
        """
        Create all 7 agents
        
        Args:
            defense_config: Optional defense configuration to apply to all agents
            
        Returns:
            Dictionary mapping agent names to AgentRuntime instances
        """
        agent_names = ["Atlas", "Bohr", "Curie", "Edison", "Faraday", "Gauss", "Deng"]
        
        # First pass: create registry structure
        agents_registry: Dict[str, AgentRuntime] = {}
        
        # Second pass: create agents
        for name in agent_names:
            agent = self.create_agent(name, agents_registry, defense_config)
            agents_registry[name] = agent
            self.logger.info(f"Created agent: {name}")
        
        # Update messaging tool with complete registry
        self.messaging_tool = MessagingTool(agents_registry)
        
        return agents_registry
