# WealthAgents

**Multi-Agent LLM Financial Planning Framework**

[![Python](https://img.shields.io/badge/python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Framework: LangGraph](https://img.shields.io/badge/framework-LangGraph-1C3C3C)](https://github.com/langchain-ai/langgraph)
[![Tests](https://img.shields.io/badge/tests-8%20passing-brightgreen)](tests/)

A multi-agent AI framework for personal wealth evaluation, planning, and mentorship. Modeled after [TradingAgents](https://github.com/TauricResearch/TradingAgents), WealthAgents decomposes complex personal finance decisions into specialized agent roles that collaboratively evaluate a user's financial life and generate personalized wealth plans — then reinterpret them through the voice of a legendary investor mentor.

## Table of Contents

- [Core Philosophy](#core-philosophy)
- [Why WealthAgents?](#why-wealthagents)
- [Architecture](#architecture)
- [Agent Teams](#agent-teams)
- [Investor Mentor Roster](#investor-mentor-roster)
- [Quick Start](#quick-start)
- [Running Locally](#running-locally)
- [LLM Integration](#llm-integration)
- [Account Connections](#account-connections)
- [State Schema](#state-schema)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [Compliance & Safety](#compliance--safety)
- [License](#license)

## Core Philosophy

> "The best investment you can make is in yourself." — Warren Buffett

WealthAgents treats **personal wealth as the primary asset** to be analyzed, debated, and optimized. Instead of analyzing stocks, our agents analyze:

- Income stability and career trajectory (human capital)
- Spending patterns and cash flow dynamics
- Asset allocation and liability management
- Goal alignment and time horizons
- Risk capacity vs. risk willingness

Then, a chosen **investor mentor persona** reinterprets the plan through their philosophy, voice, and decision framework.

## Why WealthAgents?

Traditional robo-advisors give you a number. Financial advisors give you a pitch. WealthAgents gives you a **team**:

- 🧠 **Five specialist analysts** evaluate your finances in parallel — income, expenses, assets, goals, and risk — each with its own lens and output schema.
- ⚔️ **Adversarial debate** between optimistic and cautious researchers stress-tests every conclusion before it becomes a recommendation.
- 🛡️ **Built-in risk management** — every plan is stress-tested against market crashes and job loss scenarios.
- 🎭 **Mentor personas** — the final plan is filtered through Buffett's patience, Graham's defense-first discipline, or Bogle's index simplicity.
- 🌍 **Jurisdiction-aware** — Plaid auto-sync where supported, guided manual input everywhere else.
- 🔄 **Living state** — plans persist and re-evaluate monthly, with a full decision log.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        WEALTHAGENTS FRAMEWORK                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐           │
│   │   Intake     │────▶│ Analyst Team │────▶│   Debate     │           │
│   │   (User Data)│     │  (Parallel)  │     │  (Bull/Bear) │           │
│   └──────────────┘     └──────────────┘     └──────────────┘           │
│                              │                    │                     │
│                              │                    ▼                     │
│                              │            ┌──────────────┐              │
│                              └───────────▶│ Wealth State │              │
│                                           │  (Persisted) │              │
│                                           └──────────────┘              │
│                                                  │                      │
│                                                  ▼                      │
│                                         ┌──────────────┐                │
│                                         │  Plan Team   │                │
│                                         │  (Sequential)│                │
│                                         └──────────────┘                │
│                                                │                        │
│   ┌──────────────┐     ┌──────────────┐       ▼                        │
│   │   Mentor     │◀────│  Plan Output │  ┌──────────────┐             │
│   │   Persona    │     │ + Rationale  │  │ Risk Manager │             │
│   │  (User Pick) │     │ + Dissent    │  └──────────────┘             │
│   └──────────────┘     └──────────────┘                               │
│          │                                                              │
│          ▼                                                              │
│   ┌──────────────┐                                                      │
│   │  Mentored    │                                                      │
│   │  Wealth Plan │                                                      │
│   └──────────────┘                                                      │
│          │                                                              │
│          ▼                                                              │
│   ┌──────────────┐     ┌──────────────┐                                │
│   │   Monthly    │◀────│  Decision    │                                │
│   │  Re-eval     │     │    Log       │                                │
│   └──────────────┘     └──────────────┘                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Agent Teams

### Analyst Team (Parallel Execution)

Five specialized analysts simultaneously evaluate different dimensions of the user's financial life:

| Agent | Focus | Key Output |
|-------|-------|------------|
| **Income Analyst** | Salary, side income, stability, trajectory | Income Score, Growth Trajectory |
| **Expense & Cashflow Analyst** | Spending patterns, savings rate, fixed costs | Cash Flow Map, Burn Rate |
| **Asset & Liability Analyst** | Net worth, debt, illiquid assets, equity comp | Balance Sheet, Debt Health |
| **Goal Analyst** | Time-stamped goals, priority ranking, feasibility | Goal Timeline, Funding Gap |
| **Risk Profile Analyst** | Capacity vs. willingness, dependants, job cyclicality | Risk Matrix, Stress Events |

### Researcher Team (Debate)

Two researchers debate the wealth plan:

- **Optimistic Researcher** — argues for growth, compounding, and the opportunity cost of idle cash
- **Cautious Researcher** — argues for resilience, sequence-of-returns risk, and plan fragility

### Planning Team (Sequential)

- **Strategist** — drafts the plan (emergency fund, debt payoff, asset allocation)
- **Risk Manager** — stress tests (-30% market, 6 months unemployed)
- **Tax & Efficiency Analyst** — account ordering, tax-advantaged vehicles, fee minimization

### Mentor Layer

A user-selected investor persona reinterprets the plan — maintaining the investor's philosophy, voice, and decision rules, teaching through stories and analogies, and providing behavioral coaching.

## Investor Mentor Roster

| Mentor | Philosophy | Best For |
|--------|-----------|----------|
| **Warren Buffett** | Quality, margin of safety, patience | Stable income, long horizon |
| **Benjamin Graham** | Defense first, quantified safety | Conservative, risk-averse |
| **Peter Lynch** | Buy what you know, GARP | Engaged, curious investors |
| **John Bogle** | Index everything, minimize fees | Hands-off, systematic |
| **Ray Dalio** | All-weather, risk parity | Sophisticated diversification |
| **Cathie Wood** | Disruptive innovation | High risk tolerance |
| **Paul Tudor Jones** | Macro awareness, trend defense | Active, tactical |

## Quick Start

**Requirements:** Python 3.10+

```bash
git clone https://github.com/coin-lover/WealthAgents.git
cd WealthAgents
pip install -e .
```

```python
from wealthagents import WealthAgents
from wealthagents.state import UserProfile, Asset, Debt, Goal

# Create a user profile
profile = UserProfile(
    user_id="user_001",
    age=32,
    annual_gross_income=120000,
    monthly_expenses=5000,
    location_country="US",   # ISO country code
    currency="USD",
    assets=[
        Asset(name="Emergency Fund", asset_type="savings", value=30000),
        Asset(name="401(k)", asset_type="retirement_401k", value=80000),
        Asset(name="Brokerage", asset_type="brokerage", value=25000),
    ],
    liabilities=[
        Debt(name="Student Loans", debt_type="student_loan", balance=40000,
             interest_rate=0.045, minimum_payment=400),
        Debt(name="Mortgage", debt_type="mortgage", balance=300000,
             interest_rate=0.035, minimum_payment=1800),
    ],
    goals=[
        Goal(name="Emergency Fund", category="emergency_fund", target_amount=30000,
             current_amount=30000, timeline_months=12, priority="critical"),
        Goal(name="House Down Payment", category="home_purchase", target_amount=100000,
             current_amount=15000, timeline_months=60, priority="high"),
        Goal(name="Retirement", category="retirement", target_amount=2000000,
             current_amount=80000, timeline_months=360, priority="high"),
    ],
)

# Initialize with a mentor
agent = WealthAgents(user_profile=profile, mentor="warren_buffett")

# Check account connection mode
print(agent.connection_mode)           # "plaid_auto" or "manual_input"
print(agent.get_connection_message())  # User-facing guidance

# Generate wealth plan
plan = agent.evaluate()
print(agent.get_plan_summary())

# Switch mentors and compare perspectives
plan_bogle = agent.with_mentor("john_bogle").evaluate()
```

See [`examples/basic_usage.py`](examples/basic_usage.py) for a complete runnable example.

## Running Locally

```bash
# 1. Clone and enter the project
git clone https://github.com/coin-lover/WealthAgents.git
cd WealthAgents

# 2. Create a virtual environment (keeps dependencies isolated)
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install (add [llm] if you plan to use MiniMax)
pip install -e "."
# pip install -e ".[llm]"       # includes the OpenAI client for MiniMax

# 4. Run the example
python examples/basic_usage.py

# 5. Run the tests
pytest tests/ -q
```

No API key is required — the framework runs in **heuristic mode** by default. Add an LLM (below) to make the mentor narratives richer.

## LLM Integration

The framework follows the TradingAgents pattern — **tools compute, LLMs reason**. When an LLM is configured, every layer of the pipeline is AI-powered:

| Layer | What the LLM does |
|-------|-------------------|
| **5 Analysts** | Rewrite risks/recommendations with user-specific reasoning (numeric scores stay deterministic) |
| **Researcher Debate** | A real 3-step debate: bullish thesis → bearish rebuttal → neutral judge synthesis |
| **Strategist** | Rewrites the strategy summary in plain language (all numbers stay computed) |
| **Mentor** | Writes the final letter in the investor's authentic voice |

If the LLM is unavailable or a request fails, every layer silently falls back to heuristic mode — the framework never breaks.

WealthAgents follows the [TradingAgents](https://github.com/TauricResearch/TradingAgents) provider convention — set **one** API-key environment variable and the framework auto-detects the provider.

**Supported providers** (`pip install "wealthagents[llm]"` first — installs the OpenAI + Anthropic clients):

| Provider | Env var | Default model |
|----------|---------|---------------|
| OpenAI (GPT) | `OPENAI_API_KEY` | `gpt-4o-mini` |
| Google (Gemini) | `GOOGLE_API_KEY` | `gemini-2.5-flash` |
| Anthropic (Claude) | `ANTHROPIC_API_KEY` | `claude-sonnet-4-5` |
| xAI (Grok) | `XAI_API_KEY` | `grok-4` |
| DeepSeek | `DEEPSEEK_API_KEY` | `deepseek-chat` |
| Qwen (international) | `DASHSCOPE_API_KEY` | `qwen-plus` |
| Qwen (China) | `DASHSCOPE_CN_API_KEY` | `qwen-plus` |
| GLM via Z.AI (international) | `ZHIPU_API_KEY` | `glm-4.5` |
| GLM via BigModel (China) | `ZHIPU_CN_API_KEY` | `glm-4.5` |
| MiniMax (global) | `MINIMAX_API_KEY` | `MiniMax-M2` |
| MiniMax (China) | `MINIMAX_CN_API_KEY` | `MiniMax-M2` |
| OpenRouter | `OPENROUTER_API_KEY` | `openai/gpt-4o-mini` |
| Mistral | `MISTRAL_API_KEY` | `mistral-large-latest` |
| Kimi (Moonshot) | `MOONSHOT_API_KEY` | `moonshot-v1-8k` |
| Groq | `GROQ_API_KEY` | `llama-3.3-70b-versatile` |
| NVIDIA NIM | `NVIDIA_API_KEY` | `nvidia/llama-3.3-70b-instruct` |

Every provider except Anthropic uses the OpenAI-compatible chat API; Anthropic uses its native SDK. Any other OpenAI-compatible endpoint (e.g., local Ollama) works via `LLMClient` with an explicit `base_url`.

**Usage:**

```python
from wealthagents import WealthAgents, get_llm

# Auto-detect: picks the first provider with an env-var key set
llm = get_llm()

# Or be explicit (provider name, optional model override):
llm = get_llm("deepseek")
llm = get_llm("openai", model="gpt-4o")

agent = WealthAgents(user_profile=profile, mentor="warren_buffett", llm=llm)
state = agent.evaluate()
print(state.mentored_plan.mentor_voice_narrative)

# Shortcut: pass the provider name directly
agent = WealthAgents(user_profile=profile, mentor="warren_buffett", llm="anthropic")
```

The mentor's system prompt (philosophy, principles, voice, decision rules) is injected automatically — each of the 7 mentors speaks distinctly. Works with `with_mentor()` and `compare_mentors()` too. See [`examples/minimax_usage.py`](examples/minimax_usage.py) (identical flow for every provider).

The mentor's system prompt (philosophy, principles, voice, decision rules) is injected automatically — each of the 7 mentors speaks distinctly. Works with `with_mentor()` and `compare_mentors()` too. See [`examples/minimax_usage.py`](examples/minimax_usage.py).

Design note: quantitative fields (income scores, savings rates, allocations, stress tests) are always computed by deterministic tools — following TradingAgents' separation of data tools from LLM reasoning. The LLM never invents numbers.

## Account Connections

WealthAgents uses a simple rule: **Plaid for supported countries, manual input for everything else.**

### Plaid-Supported Countries (20 total)

**North America**: United States, Canada · **United Kingdom**: Great Britain · **Europe**: Austria, Belgium, Denmark, Estonia, Finland, France, Germany, Ireland, Italy, Latvia, Lithuania, Netherlands, Norway, Poland, Portugal, Spain, Sweden

**For supported countries** — users connect bank accounts via Plaid Link; assets, liabilities, and transactions sync automatically; monthly refresh keeps the plan current.

**For all other countries** — users enter data through a guided manual form with smart country-tailored defaults and real-time validation, and can update anytime.

```python
from wealthagents import is_plaid_supported

is_plaid_supported("US")  # True
is_plaid_supported("GB")  # True
is_plaid_supported("AU")  # False -> manual input
is_plaid_supported("JP")  # False -> manual input
is_plaid_supported("BR")  # False -> manual input
```

See [`docs/ACCOUNT_CONNECTIONS.md`](docs/ACCOUNT_CONNECTIONS.md) for full details.

## State Schema

The framework uses a persistent `WealthState` object that evolves over time:

```python
class WealthState:
    user_id: str
    version: int
    timestamp: datetime

    # Analyst outputs
    income_analysis: IncomeAnalysis
    expense_analysis: ExpenseAnalysis
    asset_analysis: AssetAnalysis
    goal_analysis: GoalAnalysis
    risk_analysis: RiskAnalysis

    # Debate outputs
    optimistic_view: ResearchView
    cautious_view: ResearchView

    # Plan outputs
    strategy: WealthStrategy
    risk_assessment: RiskAssessment
    tax_plan: TaxPlan

    # Mentor interpretation
    mentor_id: str
    mentored_plan: MentoredPlan

    # Historical
    decision_log: List[PlanDecision]
```

## Project Structure

```
wealthagents/
├── core.py            # WealthAgents orchestration entry point
├── graph.py           # LangGraph workflow definition
├── state.py           # WealthState & typed data models
├── connections.py     # Plaid/manual input country logic
├── manual_input.py    # Guided manual data entry
├── agents/
│   ├── base.py        # Shared agent primitives
│   ├── analysts.py    # 5 parallel analyst agents
│   ├── researchers.py # Bull/bear debate team
│   └── planning.py    # Strategist, Risk Manager, Tax Analyst
└── mentors/
    ├── base.py
    ├── personalities.py
    └── registry.py    # Mentor persona registry
```

## Roadmap

- [ ] Live Plaid Link integration (currently country-detection logic only)
- [x] LLM-backed agent reasoning — TradingAgents-style wiring: analysts, live debate, strategist summary, mentor narratives (MiniMax)
- [ ] Web UI for plan visualization
- [ ] More mentor personas (Charlie Munger, Howard Marks, …)
- [ ] Backtesting of plan recommendations against historical scenarios

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for details.

## Compliance & Safety

WealthAgents is designed as an **educational and planning framework**, not a licensed financial advisory service:

- All outputs include disclaimers
- No trade execution capabilities
- Jurisdiction-aware rule filters
- Encrypted user data handling
- Educational framing on all recommendations

## License

[MIT](LICENSE)
