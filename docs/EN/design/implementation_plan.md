# Step 0 | Project Initialization (One-time)

Create directories and empty files (according to your defined structure)

Configure dependencies (recommended):

* langchain (core)
* Model package of your choice (e.g., langchain-openai or local model adapter)
* pydantic (schema)
* pyyaml (configs)
* pytest (tests)

Define output convention: Each run generates `outputs/runs/<timestamp>_seedX/`

**Deliverables:**
* `pyproject.toml`
* `configs/*.yaml`
* Output directory convention documented in README

---

# Step 1 | Define "Structured Tool Interface" (LangChain's Minimum Viable Loop)

For multi-agent propagation, the key is: **LLM must use tools to send messages/execute**. Therefore, the first step is tools.

**Implementation:**

* `src/tools/messaging.py`
  * `send_message(sender, receiver, content)`: Deliver message to receiver's queue

* `src/tools/run_code.py`
  * `run_code(code)`: First return "simulated execution result" (add risk judgment later)

* `src/tools/langchain_adapters.py`
  * Wrap the above functions into LangChain StructuredTool

**Deliverables (acceptance criteria):**
* You can directly call send_message and run_code using LangChain (even without agent loop yet)

---

# Step 2 | Define Unified Prompt Construction (system + memory + incoming_message)

**Implementation:**

* `src/agents/memory/store.py`
  * MemoryStore: append/prepend, return "messages that can be concatenated into prompt"

* `src/llm/prompts.py`
  * `build_messages(system, memory, incoming)`: Output message list required by LangChain

* `src/agents/prompt_templates/base_system.jinja2`
* `src/agents/prompt_templates/scratchpad.jinja2`

**Deliverables (acceptance criteria):**
* Given system + memory + incoming_message → produces consistent, testable prompt messages

---

# Step 3 | Implement Single AgentRuntime (Driven by LangChain AgentExecutor)

This begins the paper's "one runtime per agent" concept.

**Implementation:**

* `src/agents/runtime/message_queue.py`
  * FIFO: asyncio.Queue

* `src/agents/runtime/agent_runtime.py`
  * Member variables: self.queue, self.memory
  * async step():
    * msg = await queue.get()
    * prompt = system + memory + msg
    * Call LangChain AgentExecutor.ainvoke()
    * Execute tools (triggered by AgentExecutor)
    * Write current conversation back to memory (append)

* `src/llm/factory.py`
  * Return LLM (OpenAI/local) for AgentExecutor to use

**Deliverables (acceptance criteria):**
* Single agent can consume queue messages and invoke tools (at least one call to send_message or run_code)

---

# Step 4 | Multi-Agent Creation and Routing (agents_by_name)

**Implementation:**

* `src/agents/runtime/agent_factory.py`
  * Create different agents based on roles/*.yaml (different system prompts)
  * **Each new: must new queue + new memory**

* `src/orchestrator/simulation.py`
  * Initialize 7 agents into agents_by_name
  * Inject initial task into Atlas queue

* `src/tools/messaging.py`
  * Use `agents_by_name[receiver].queue.put(...)` to deliver messages

**Deliverables (acceptance criteria):**
* messages.jsonl shows multiple deliveries from Atlas → others
* Queue and memory are **private to each agent** (not shared)

---

# Step 5 | Parallel Scheduling (asyncio, multiple workers)

**Implementation:**

* `src/orchestrator/scheduler.py`
  * Launch one worker per agent: `while not terminated: await agent.step()`

* `src/orchestrator/lifecycle.py`
  * Minimum termination conditions:
    * max_messages
    * Deadlock (all queues empty and exceed deadlock_timeout_s)

**Deliverables (acceptance criteria):**
* 7 agents run in parallel, can exit stably, won't hang

---

# Step 6 | Logging System (Must be done early, otherwise cannot evaluate/draw propagation graph later)

**Implementation:**

* `src/common/types.py`
* `src/common/logging.py`
* `src/orchestrator/tracing.py`

Unified writing:
* `events.jsonl`
* `messages.jsonl`
* `tool_calls.jsonl`
* `outcomes.json`
* `config_snapshot.yaml`

**Deliverables (acceptance criteria):**
* Each run has complete five-piece set under outputs, and is reproducible (fixed seed)

---

# Step 7 | run_code Risk Judgment → Explosion Termination (Core termination for reproducing Experiment 1)

**Implementation:**

* `src/tools/risk_rules.py`
  * Minimum rule: Detect dangerous three-element combination (keywords/structured fields both acceptable)

* `src/tools/run_code.py`
  * Call risk_rules, report "EXPLOSION" to orchestrator if triggered

* `src/orchestrator/lifecycle.py`
  * Add termination reason: explosion

**Deliverables (acceptance criteria):**
* Once agent calls run_code and triggers danger rule → immediately terminate and record outcome

---

# Step 8 | Attack Injection (After 2nd message)

**Implementation:**

* `src/attacks/prompt_bank.py`: Read `data/attacks/jailbreak_prompts.jsonl`
* `src/attacks/target_selection.py`: Exclude Atlas/Deng, reproducible with seed
* `src/attacks/schedule.py`: Trigger when global dequeued_count==2
* `src/attacks/injector.py`: Put malicious message to target queue
* `src/orchestrator/injection_points.py`: Hook injection point to orchestrator's event loop

**Deliverables (acceptance criteria):**
* Logs verify: injection indeed occurs "after 2nd message is processed"
* messages.jsonl shows malicious message entering queue and beginning multi-hop propagation

---

# Step 9 | Defense 1: Instruction Defense (passive / active)

**Implementation:**

* `src/defenses/instructions.py`: Two tiers of policy text
* `src/agents/runtime/policy_hooks.py`: System patch hook
* `configs/defense_matrix.yaml`: Add INSTR_PASSIVE / INSTR_ACTIVE

**Deliverables (acceptance criteria):**
* Under same seed, explosion rate decreases after enabling defense (not guaranteed 0, but trend should emerge)

---

# Step 10 | Defense 2: Memory Vaccine (passive / active)

**Implementation:**

* `src/defenses/vaccines.py`
* `src/agents/memory/vaccines.py`: Read data and prepend
* `configs/defense_matrix.yaml`: Add VAX_PASSIVE / VAX_ACTIVE

**Deliverables (acceptance criteria):**
* Vaccine must appear at the very beginning of memory (can check via log snapshot)

---

# Step 11 | Evaluation: robustness + cooperation

**Implementation:**

* `src/eval/robustness.py`: Aggregate explosion rate from outcomes
* `src/eval/cooperation.py`: Read `data/harmless/weird_but_safe.jsonl`, calculate acceptance rate
* `src/eval/report.py`: Export CSV
* `scripts/run_batch.py`: Batch run defense_matrix × seeds

**Deliverables:**
* `outputs/reports/table_robustness.csv`
* `outputs/reports/table_cooperation.csv`

---

# Step 12 | Propagation Analysis and Visualization

**Implementation:**

* `src/eval/propagation.py`
  * Build propagation graph from messages.jsonl and output metrics (multi-hop paths/infection chain length)

* `scripts/make_figures.py`
  * Output propagation graph (HTML or PNG)

**Deliverables:** 
* Propagation graph + propagation statistics
