# Project Progress Report

## Completed Work

### ✅ Paper Understanding & Design Documentation
- Created detailed [Paper Core Logic Analysis](论文核心逻辑分析.md)
- Understood "security tax" concept: trade-off between security and cooperation ability
- Clarified experimental design: 7 Agents, social propagation, two defense strategies
- Understood evaluation metrics: Robustness (explosion rate) and Cooperation (acceptance rate)

### ✅ Project Initialization (Step 0)
1. **Directory Structure**: Complete creation of src/, data/, configs/, outputs/, and all directories
2. **Project Configuration**:
   - [pyproject.toml](pyproject.toml): Python project configuration with all dependencies
   - [README.md](README.md): Complete project documentation
   - [.env.example](.env.example): Environment variable template

3. **Configuration Files**:
   - [configs/llm.yaml](configs/llm.yaml): LLM model configuration
   - [configs/sim.yaml](configs/sim.yaml): Simulation parameter configuration
   - [configs/defense_matrix.yaml](configs/defense_matrix.yaml): Defense strategy matrix
   - [configs/experiments.yaml](configs/experiments.yaml): Batch experiment run configuration

4. **Data Files**:
   - [data/attacks/jailbreak_prompts.jsonl](data/attacks/jailbreak_prompts.jsonl): 12 malicious prompts
   - [data/vaccines/passive.jsonl](data/vaccines/passive.jsonl): Passive vaccine examples
   - [data/vaccines/active.jsonl](data/vaccines/active.jsonl): Active vaccine examples
   - [data/harmless/weird_but_safe.jsonl](data/harmless/weird_but_safe.jsonl): Weird but harmless instructions
   - [data/tasks/lab_task_mof.json](data/tasks/lab_task_mof.json): Initial task (MOF optimization)

### ✅ Core Data Structures (Step 1 partial)
- [src/common/types.py](src/common/types.py): Defined all core data types
  - Message, Event, ToolCall, Outcome, etc.
  - Enum types: MessageRole, EventType, TerminationReason, etc.
  - BehaviorLevel (danger level classification from -2 to +2)
  
- [src/common/utils.py](src/common/utils.py): Utility functions
  - Random seed setting, timestamp, JSONL read/write, etc.
  
- [src/common/constants.py](src/common/constants.py): Global constants
  - Agent name list, dangerous chemical combinations, attack configuration, etc.
  
- [src/common/logging.py](src/common/logging.py): Logging system
  - SimulationLogger class, unified management of event/message/tool call logs

## Next Steps

### 🔄 In Progress (Step 1)
Continue implementing tool interfaces:
- src/tools/messaging.py - send_message tool
- src/tools/run_code.py - run_code tool (with risk detection)
- src/tools/risk_rules.py - Dangerous rule detection
- src/tools/langchain_adapters.py - LangChain tool wrapping

### 📋 Pending Tasks

#### Step 2-3: Agent Core
- LLM factory and prompt construction system
- AgentRuntime main loop
- Message queue and memory management

#### Step 4-5: Multi-Agent Collaboration
- Agent factory (create 7 Agents)
- Message routing (agents_by_name dictionary)
- Parallel scheduler (asyncio workers)

#### Step 6-8: Attack & Logging
- Improve log tracking system
- Attack injection timing control (after 2nd message)
- Attack target selection (random, exclude Atlas/Deng)

#### Step 9-10: Defense Mechanisms
- Instruction defense (system prompt append)
- Memory vaccines (memory prepend)
- Passive/Active two-level implementation

#### Step 11-12: Evaluation & Visualization
- Robustness evaluation (explosion rate)
- Cooperation evaluation (acceptance rate)
- Propagation graph generation (HTML/PNG)

#### Step 13: Testing & Validation
- Unit tests
- Integration tests
- Paper result reproduction validation

## Technical Points

### Key Design Decisions
1. **Independent State Management**: Each Agent has independent queue and memory instances
2. **Message Propagation**: Routing through agents_by_name dictionary, no shared state
3. **Risk Determination**: Detect dangerous chemical substance keyword combinations
4. **Attack Timing**: Global counter dequeued_count control
5. **Reproducibility**: All random operations use seed

### Data Flow
```
Initial task → Atlas queue
  ↓
Atlas processes and dispatches → Other Agent queues (via send_message)
  ↓
After 2nd message processed → Attack injection to random Agent
  ↓
Multi-hop propagation → Messages forwarded between Agents
  ↓
Finally reaches Deng → run_code → Risk determination
  ↓
Explosion/Normal end → Record outcomes.json
```

## Project Quality Metrics

- [x] Complete type annotations (Pydantic models)
- [x] Comprehensive documentation (README + design docs + core logic analysis)
- [x] Structured configuration management (YAML configs)
- [x] Reproducible experiment setup (seed control)
- [ ] Unit test coverage
- [ ] Performance optimization (async concurrency)
- [ ] Code style checking (black, ruff)

## Estimated Remaining Work

- Step 1 remaining (tool interfaces): 2-3 hours
- Step 2-3 (Agent core): 4-5 hours
- Step 4-5 (Multi-Agent + scheduling): 3-4 hours
- Step 6-8 (Logging + attack): 2-3 hours
- Step 9-10 (Defense): 2-3 hours
- Step 11-12 (Evaluation): 3-4 hours
- Step 13 (Testing): 2-3 hours

**Total Estimate**: 18-25 hours coding + debugging time

## Dependency Check

Main dependencies to install:
```bash
pip install langchain langchain-openai langchain-community
pip install pydantic pyyaml jinja2 aiofiles python-dotenv
pip install pytest pytest-asyncio  # Development dependencies
```

Recommend installing in virtual environment:
```bash
cd /home/severin/Codelib/SKKU
source venv/bin/activate
pip install -e .
```
