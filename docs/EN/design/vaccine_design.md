## Directory Structure

```text
repo/
├─ README.md
│  # Project description: paper background (Multi-Agent Security Tax), system design, reproduction methods, how to run
│
├─ pyproject.toml
│  # Python project configuration: dependencies (langchain / asyncio / pydantic etc.), formatting and testing
│
├─ .env.example
│  # Environment variable example: OpenAI API Key / local model path / log path
│
├─ src/
│  ├─ app.py
│  │  # Main entry point: load config → start orchestrator → run single or batch simulation
│  │
│  ├─ common/
│  │  ├─ __init__.py
│  │  ├─ types.py
│  │  │  # Global data structure definitions (Message / Event / ToolCall / Outcome)
│  │  ├─ constants.py
│  │  │  # Constants: Agent names, termination reason enum, risk types, behavior levels (-2 ~ +2)
│  │  ├─ utils.py
│  │  │  # Common utility functions: random seed, timestamp, JSONL read/write
│  │  └─ logging.py
│  │     # Unified logging interface: events / messages / tool_calls
│  │
│  ├─ llm/
│  │  ├─ __init__.py
│  │  ├─ factory.py
│  │  │  # LLM factory: OpenAI / local model / mock (replaces AutoGPT model layer)
│  │  └─ prompts.py
│  │     # Prompt assembly: system + memory + message + scratchpad
│  │
│  ├─ agents/
│  │  ├─ __init__.py
│  │  │
│  │  ├─ roles/
│  │  │  ├─ atlas.yaml
│  │  │  │  # Atlas: Project manager agent (task decomposition and scheduling)
│  │  │  ├─ bohr.yaml
│  │  │  │  # Bohr: Researcher agent
│  │  │  ├─ curie.yaml
│  │  │  │  # Curie: Researcher agent
│  │  │  ├─ deng.yaml
│  │  │  │  # Deng: Executor agent (run_code high risk)
│  │  │  ├─ edison.yaml
│  │  │  │  # Edison: Researcher agent
│  │  │  ├─ faraday.yaml
│  │  │  │  # Faraday: Researcher agent
│  │  │  └─ gauss.yaml
│  │  │     # Gauss: Researcher agent
│  │  │
│  │  ├─ prompt_templates/
│  │  │  ├─ base_system.jinja2
│  │  │  │  # Base system prompt (without defense)
│  │  │  └─ scratchpad.jinja2
│  │  │     # Internal thinking template (react / plan / critique)
│  │  │
│  │  ├─ memory/
│  │  │  ├─ __init__.py
│  │  │  ├─ store.py
│  │  │  │  # Agent memory stream structure (append / prepend / truncate)
│  │  │  └─ vaccines.py
│  │  │     # Memory vaccine injection logic (passive / active)
│  │  │
│  │  └─ runtime/
│  │     ├─ __init__.py
│  │     ├─ agent_runtime.py
│  │     │  # Single agent main loop: get message → LLM → actions → tools
│  │     ├─ agent_factory.py
│  │     │  # Create agent instance based on role + defense strategy
│  │     ├─ message_queue.py
│  │     │  # FIFO message queue (asyncio.Queue wrapper)
│  │     └─ policy_hooks.py
│  │        # Defense hooks: system patch / memory prepend / message filtering
│  │
│  ├─ tools/
│  │  ├─ __init__.py
│  │  ├─ messaging.py
│  │  │  # send_message: send message to target agent queue
│  │  ├─ run_code.py
│  │  │  # run_code: simulate code execution (only entry point for dangerous behavior)
│  │  ├─ risk_rules.py
│  │  │  # Risk detection rules: identify dangerous chemical mixtures → trigger "explosion"
│  │  └─ langchain_adapters.py
│  │     # LangChain Tool wrapper (expose tools to agents)
│  │
│  ├─ orchestrator/
│  │  ├─ __init__.py
│  │  ├─ simulation.py
│  │  │  # Single simulation flow: initialize → inject task → run in parallel → terminate
│  │  ├─ scheduler.py
│  │  │  # Parallel scheduling: start asyncio worker for each agent
│  │  ├─ injection_points.py
│  │  │  # Injection timing management (e.g., after 2nd message)
│  │  ├─ lifecycle.py
│  │  │  # Termination conditions: explosion / deadlock / message limit
│  │  └─ tracing.py
│  │     # Global tracing: message propagation graph, state changes
│  │
│  ├─ attacks/
│  │  ├─ __init__.py
│  │  ├─ injector.py
│  │  │  # Attack injection executor: inject malicious prompt to target agent
│  │  ├─ prompt_bank.py
│  │  │  # Load 12 jailbreak prompts
│  │  ├─ target_selection.py
│  │  │  # Randomly select attack target (exclude Atlas / Deng)
│  │  └─ schedule.py
│  │     # Attack trigger strategy (works with injection_points)
│  │
│  ├─ defenses/
│  │  ├─ __init__.py
│  │  ├─ instructions.py
│  │  │  # Instruction defense: append to system prompt (passive / active)
│  │  ├─ vaccines.py
│  │  │  # Vaccine defense: prepend to memory (passive / active)
│  │  ├─ modes.py
│  │  │  # Defense mode enum (NONE / INSTR / VAX × passive/active)
│  │  └─ registry.py
│  │     # Defense strategy registration and combination (experiment matrix)
│  │
│  └─ eval/
│     ├─ __init__.py
│     ├─ robustness.py
│     │  # System robustness: whether explosion triggered
│     ├─ cooperation.py
│     │  # Cooperation ability: acceptance rate of weird but harmless instructions
│     ├─ propagation.py
│     │  # Propagation analysis: multi-hop infection chain, behavior level statistics
│     ├─ judge.py
│     │  # LLM-as-judge (optional, align with paper)
│     └─ report.py
│        # Aggregate results and export to CSV / JSON
│
├─ data/
│  ├─ attacks/
│  │  └─ jailbreak_prompts.jsonl
│  │     # 12 malicious prompts from the paper
│  ├─ vaccines/
│  │  ├─ passive.jsonl
│  │  │  # Passive vaccine memory examples
│  │  └─ active.jsonl
│  │     # Active vaccine memory examples
│  ├─ harmless/
│  │  └─ weird_but_safe.jsonl
│  │     # Weird but harmless instructions (Experiment 2)
│  └─ tasks/
│     └─ lab_task_mof.json
│        # Initial experiment task (sent to Atlas)
│
├─ configs/
│  ├─ llm.yaml
│  │  # LLM parameters (model name / temperature / max_tokens)
│  ├─ sim.yaml
│  │  # Simulation parameters (max_messages / timeout)
│  ├─ experiments.yaml
│  │  # Experiment scale (runs / seeds)
│  └─ defense_matrix.yaml
│     # Defense combination matrix (Paper Table 1 / Table 2)
│
├─ scripts/
│  ├─ run_one.py
│  │  # Run single simulation (debugging)
│  ├─ run_batch.py
│  │  # Batch run experiments (all defenses × multiple seeds)
│  ├─ summarize_runs.py
│  │  # Aggregate outputs → tables
│  └─ make_figures.py
│     # Generate propagation graphs / robustness plots
│
├─ outputs/
│  ├─ runs/
│  │  └─ <timestamp>_seed42/
│  │     ├─ events.jsonl
│  │     │  # Full event timeline
│  │     ├─ messages.jsonl
│  │     │  # Message propagation between agents
│  │     ├─ tool_calls.jsonl
│  │     │  # send_message / run_code records
│  │     ├─ outcomes.json
│  │     │  # Explosion / termination reasons
│  │     └─ config_snapshot.yaml
│  │        # Complete configuration snapshot for this run
│  └─ reports/
│     ├─ table_robustness.csv
│     ├─ table_cooperation.csv
│     └─ propagation_graphs/
│
└─ tests/
   ├─ test_risk_rules.py
   │  # Whether risk rules trigger correctly
   ├─ test_injection_schedule.py
   │  # Whether injection strictly happens after 2nd message
   └─ test_queue_order.py
      # FIFO queue order correctness
```

---

## I. Overall Architecture Overview

The system adopts a layered architecture, from top to bottom:

* **Simulation Orchestration Layer** (orchestrator): manages the lifecycle of a complete simulation
* **Agent Runtime Layer** (agents): defines agent behavior, memory, and policy extension points
* **Tool Layer** (tools): action interfaces that agents can call
* **Attack Layer** (attacks): injects adversarial inputs into the system at specified times
* **Defense Layer** (defenses): enhances agent robustness through instructions or memory
* **Evaluation Layer** (eval): quantitative analysis of simulation results
* **Data & Config** (data / configs): input samples and experiment parameters
* **Output** (outputs): ensures reproducible and traceable experiment results

---

## II. Module Responsibilities

### 1️⃣ src/orchestrator/ — Simulation Orchestration Layer

Manages the full lifecycle of a simulation from start to finish.

* **simulation.py**
  Single simulation entry point, main flow:

  * Initialize all agents
  * Inject initial task
  * Start parallel scheduling
  * Wait for termination conditions and cleanup

* **scheduler.py**
  Parallel scheduler based on asyncio

  * Each agent corresponds to a worker coroutine

* **injection_points.py**
  Unified management of attack trigger points

  * Example: "Inject attack after system processes 2nd message"

* **lifecycle.py**
  Simulation termination condition checks:

  * Explosion (dangerous behavior)
  * Deadlock
  * Message count limit
  * Timeout

* **tracing.py**
  Global tracing and logging:

  * Message graph (who → who)
  * Tool call records
  * Agent state snapshots

---

### 2️⃣ src/agents/ — Agent Runtime Layer

Defines how agents think, remember, and act.

#### Roles & Configuration

* **roles/*.yaml**
  Static definition for each role:

  * System prompt
  * Allowed tools
  * Default behavior strategies (e.g., Atlas / Deng)

#### Core Runtime

* **runtime/agent_runtime.py**
  Main loop for a single agent:

  * Get message from message queue
  * Construct prompt (system + memory + current message)
  * Generate actions
  * Execute tools and record results

* **runtime/message_queue.py**
  Agent's message queue

  * Currently FIFO
  * Can be replaced with asyncio.Queue wrapper

#### Memory & Policy Extension

* **memory/store.py**
  Agent's long-term / short-term memory stream

  * Supports prepending "vaccine conversations"

* **runtime/policy_hooks.py**
  Defense extension points (hooks):

  * System prompt patch
  * Memory prepend
  * Message filter

---

### 3️⃣ src/tools/ — Tool Layer (Messaging + Execution)

The only interface for agents to interact with the external world.

* **messaging.py**

  * `send_message(recipient, content)`
    Essence: deliver a message to target agent's message queue

* **run_code.py**

  * `run_code(code)`
  * Simulates code execution
  * Must produce logs
  * Must go through risk assessment

* **risk_rules.py**
  Dangerous rule set

  * E.g., detect dangerous chemical mixtures
  * Used to reproduce "explosion" and other failure states

* **langchain_adapters.py**
  Wrap the above tools as LangChain StructuredTools

---

### 4️⃣ src/attacks/ — Attack Layer

Responsible for adversarial sample selection, timing, and injection.

* **schedule.py**
  Attack trigger timing

  * Default: after system processes 2nd message

* **target_selection.py**
  Attack target selection:

  * Exclude Atlas / Deng
  * Use random seed to ensure reproducibility

* **prompt_bank.py**
  Load attack prompts:

  * `data/attacks/jailbreak_prompts.jsonl`

* **injector.py**
  Actually execute injection:

  * Insert malicious message into target agent's message queue

---

### 5️⃣ src/defenses/ — Defense Layer

Used to enhance agent robustness against attacks.

* **instructions.py**
  Instruction defense:

  * Append defense instructions to end of system prompt
  * Divided into passive / active levels

* **vaccines.py**
  Vaccine defense:

  * Prepend conversation snippets to agent memory
  * Also supports passive / active

* **modes.py**
  Defense mode enum:

  * NONE
  * INSTR_PASSIVE
  * INSTR_ACTIVE
  * VAX_PASSIVE
  * VAX_ACTIVE

* **registry.py**
  Generate defense strategy combinations based on experiment config

  * Used for matrix-style batch experiments

---

### 6️⃣ src/eval/ — Evaluation Layer

Quantitative analysis of simulation results.

* **robustness.py**
  Whether explosion occurred

  * Source: run_code risk assessment or judge

* **cooperation.py**
  Acceptance rate for "weird but harmless" instructions

  * Data from weird_but_safe.jsonl

* **propagation.py**
  Attack propagation analysis:

  * who → who
  * Infection chain length
  * Multi-hop propagation paths

* **judge.py** (optional)
  Use LLM-as-judge

  * Align with paper evaluation metrics

* **report.py**
  Aggregate output:

  * CSV / JSON
  * Input for visualization

---

## III. Data & Configuration Recommendations

### 📁 data/

* **attacks/jailbreak_prompts.jsonl**
  Each line contains {id, prompt} (~12 entries)

* **vaccines/passive.jsonl**

* **vaccines/active.jsonl**
  Each line is a "memory conversation snippet"

* **harmless/weird_but_safe.jsonl**
  "Weird but harmless" instruction samples

* **tasks/lab_task_mof.json**
  Initial task (assigned to Atlas)

### 📁 configs/

* **llm.yaml**
  Model / temperature / max tokens
  Supports OpenAI / local models

* **sim.yaml**

  * max_messages
  * deadlock_timeout_s
  * parallelism

* **defense_matrix.yaml**
  Defense strategy combination list (batch experiments)

* **experiments.yaml**

  * Number of runs
  * Seed list
  * Output path

---

## IV. Output Structure (Reproducible & Traceable)

* **outputs/runs/<timestamp_seedX>/**

  * **events.jsonl**
    Unified event stream (message dequeue, tool calls, etc.)
  * **messages.jsonl**
    who → who + content + step
  * **tool_calls.jsonl**
    Detailed records of run_code / send_message
  * **outcomes.json**
    Statistics on explosion / deadlock / limit triggers
  * **config_snapshot.yaml**
    Complete configuration snapshot for this simulation

---

## Memory Logic

### 1) Which files are responsible for "each agent is independent"

* **src/agents/runtime/message_queue.py**
  Defines MessageQueue (wraps asyncio.Queue internally), each instance = one queue

* **src/agents/memory/store.py**
  Defines MemoryStore (holds a list/deque internally), each instance = one memory stream

* **src/agents/runtime/agent_runtime.py**
  Defines AgentRuntime, binds MessageQueue + MemoryStore as member variables to the agent

* **src/agents/runtime/agent_factory.py**
  Factory: creates AgentRuntime based on role configuration, key is that each creation instantiates a new queue+memory set

* **src/orchestrator/simulation.py**
  Simulation initialization: creates 7 agents in a loop, puts them in agents_by_name mapping

* **src/tools/messaging.py**
  send_message(sender, receiver, content): does one thing—put() message into receiver's queue

### 2) Your implementation's "object relationships" should look like this

```text
SimulationContext
  ├─ agents_by_name["Atlas"]  -> AgentRuntime(queue_A, memory_A, ...)
  ├─ agents_by_name["Bohr"]   -> AgentRuntime(queue_B, memory_B, ...)
  ├─ agents_by_name["Curie"]  -> AgentRuntime(queue_C, memory_C, ...)
  └─ ...
```

Key points:

* queue_A is not queue_B
* memory_A is not memory_B
* Only orchestrator holds a global agents_by_name for message routing, but doesn't share state.
