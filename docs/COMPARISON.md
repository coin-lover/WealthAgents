# TradingAgents vs WealthAgents: Framework Comparison

## Origin

WealthAgents is directly inspired by [TradingAgents](https://github.com/tauricresearch/tradingagents), a multi-agent LLM financial trading framework. We adapted the same architectural patterns to a new domain: **personal wealth management**.

## What We Kept

### 1. Multi-Agent Decomposition
TradingAgents breaks trading into specialized roles (Fundamentals, Sentiment, Technical, News analysts). WealthAgents uses the same pattern:
- **Income Analyst** ↔ Fundamentals Analyst
- **Expense Analyst** ↔ New (cash flow focus)
- **Asset/Liability Analyst** ↔ New (balance sheet focus)
- **Goal Analyst** ↔ New (goal feasibility)
- **Risk Profile Analyst** ↔ Risk Management Team (adapted)

### 2. Researcher Debate
TradingAgents has Bullish and Bearish researchers debate stock prospects. WealthAgents preserves this:
- **Optimistic Researcher** ↔ Bullish Researcher
- **Cautious Researcher** ↔ Bearish Researcher
- Both produce structured arguments with confidence scores
- A synthesizer resolves the debate

### 3. Structured Outputs
TradingAgents uses Pydantic models for agent outputs. WealthAgents expands this:
- Every agent produces a typed Pydantic model
- State is fully serializable
- Type safety across the pipeline

### 4. LangGraph Integration
TradingAgents uses LangGraph for orchestration. WealthAgents provides:
- Sequential executor (no dependencies needed)
- LangGraph adapter for parallel execution
- Same checkpoint and persistence patterns

### 5. Risk Management
TradingAgents has a Risk Management Team. WealthAgents adapts this:
- **Risk Manager** stress tests personal plans
- Scenarios: job loss, market crash, emergency expense, rate spike
- Guardrails and vulnerability identification

## What We Changed

### 1. The "Asset" Being Analyzed
| | TradingAgents | WealthAgents |
|---|---|---|
| **Input** | Stock ticker + market data | User profile + financial data |
| **Output** | Buy/Hold/Sell decision | Comprehensive wealth plan |
| **Time horizon** | Days to weeks | Years to decades |
| **Unit of value** | Price per share | Net worth, goal achievement |

### 2. The Decision Layer
TradingAgents ends with a Portfolio Manager making trade decisions. WealthAgents ends with a **Mentor Persona**:
- The mentor doesn't change the math; they reinterpret it
- Voice, philosophy, and behavioral coaching are first-class features
- Users can switch mentors to see different perspectives

### 3. The Planning Team
TradingAgents has a Trader who proposes trades. WealthAgents has a **Planning Team**:
- **Strategist**: drafts the wealth plan (emergency fund, debt, allocation)
- **Risk Manager**: stress tests the plan
- **Tax & Efficiency Analyst**: optimizes taxes and fees

This is more complex than a single trader because personal finance has more dimensions than a single trade.

### 4. Persistence Model
TradingAgents evaluates a ticker once per session. WealthAgents maintains a **living state**:
- WealthState is versioned and persisted
- Monthly re-evaluation cycles
- Decision log tracks plan evolution
- Diff-based updates (only re-run changed dimensions)

### 5. Compliance Requirements
TradingAgents is research-only. WealthAgents faces higher regulatory exposure:
- Educational framing on all outputs
- No trade execution
- Jurisdiction-aware tax rules
- Forbidden topics per mentor (no stock picks)

## Code Structure Comparison

### TradingAgents
```
tradingagents/
├── agents/
│   ├── analysts.py      # Fundamentals, Sentiment, Technical, News
│   ├── researchers.py   # Bullish, Bearish
│   └── decision.py      # Trader, Portfolio Manager
├── state.py             # TradingState
└── graph.py             # LangGraph workflow
```

### WealthAgents
```
wealthagents/
├── agents/
│   ├── analysts.py      # Income, Expense, Asset, Goal, Risk
│   ├── researchers.py   # Optimistic, Cautious
│   └── planning.py      # Strategist, Risk Manager, Tax Analyst
├── mentors/
│   ├── base.py          # MentorPersona base class
│   ├── personalities.py # Buffett, Bogle, Lynch, etc.
│   └── registry.py      # MentorRegistry
├── state.py             # WealthState (expanded)
├── graph.py             # Sequential + LangGraph adapters
└── core.py              # User-facing API
```

## Key Innovation: The Mentor Layer

The biggest departure from TradingAgents is the **Mentor Persona system**:

1. **Config-driven personas**: Each mentor is a YAML-like config (philosophy, voice, rules)
2. **Plan reinterpretation**: Same underlying plan, different voice and emphasis
3. **Behavioral coaching**: Mentors teach users how to behave, not just what to buy
4. **Suitability scoring**: Each mentor evaluates how well they fit the user
5. **Council mode**: Multiple mentors can debate and user picks the synthesis

This would be like if TradingAgents let you pick whether Buffett, Soros, or Druckenmiller managed your portfolio, and each one explained the same market data through their own lens.

## When to Use Which

| Scenario | Use TradingAgents | Use WealthAgents |
|----------|-------------------|------------------|
| Analyzing a stock | ✅ | ❌ |
| Building a personal budget | ❌ | ✅ |
| Evaluating market sentiment | ✅ | ❌ |
| Planning for retirement | ❌ | ✅ |
| Backtesting a strategy | ✅ | ✅ (adapted) |
| Behavioral coaching | ❌ | ✅ |
| Tax optimization | ❌ | ✅ |

## Future Convergence

The frameworks could converge in interesting ways:
1. **TradingAgents for execution**: WealthAgents generates the plan, TradingAgents manages the portfolio
2. **Shared analyst infrastructure**: Fundamentals analyst could evaluate user's employer stock
3. **Unified state**: A single state object tracking both personal wealth and investment portfolio
4. **Mentor overlay on TradingAgents**: Buffett persona could interpret trading signals
