# WealthAgents Architecture

## Design Philosophy

WealthAgents adapts the proven multi-agent pattern from [TradingAgents](https://github.com/tauricresearch/tradingagents) to personal wealth management. Where TradingAgents analyzes market securities, WealthAgents analyzes **human financial lives**.

The core insight: personal finance decisions are just as complex as trading decisions, involving multiple dimensions (income, expenses, assets, goals, risk) that benefit from specialized analysis and structured debate.

## From TradingAgents to WealthAgents

| TradingAgents | WealthAgents | Analogy |
|--------------|--------------|---------|
| Stock ticker | User profile | The "asset" being analyzed |
| Market data | Financial profile | Input data |
| Analyst Team | Wealth Analyst Team | Parallel evaluation |
| Bull/Bear researchers | Optimistic/Cautious researchers | Debate & balance |
| Trader | Strategist | Proposes concrete actions |
| Risk Management Team | Risk Manager | Stress tests |
| Portfolio Manager | Mentor Persona | Final voice & philosophy |
| Execution | Action Items | Concrete next steps |

## State Machine

The framework uses a persistent `WealthState` that evolves over time:

```
UserProfile → Analyst Team → Debate → Planning → Mentor → MentoredPlan
                ↑                                              ↓
                └──────────── Monthly Re-evaluation ←──────────┘
```

Key design decisions:
- **Immutable versions**: Each evaluation creates a new version with a decision log entry
- **Partial state**: The system works with incomplete data; missing fields use sensible defaults
- **Error resilience**: Individual agent failures don't crash the pipeline

## Agent Communication

Agents communicate through structured Pydantic models, not raw text. This ensures:
- Type safety across the pipeline
- Consistent output parsing
- Easy serialization for persistence
- Clear contracts between agents

```python
# Analyst outputs are structured models
income_analysis: IncomeAnalysis = IncomeAnalyst().run(state)
# Contains: income_score, stability_rating, growth_trajectory, risks, recommendations
```

## The Mentor Layer

The mentor layer is WealthAgents' key differentiator. It works by:

1. **Persona as Config**: Each mentor is a configuration object, not a fine-tuned model
2. **Prompt Injection**: The mentor's philosophy, voice, and rules are injected into the LLM prompt
3. **Plan Reinterpretation**: The mentor rewrites the planning team's output in their voice
4. **Behavioral Coaching**: Mentors provide ongoing behavioral guidance

This design means:
- New mentors can be added without model retraining
- Mentors can be switched instantly
- The same underlying plan gets different interpretations
- Users can run "mentor council mode" for multiple perspectives

## Graph Structure

### Sequential Version (Default)
```
[Entry] → Analysts → Debate → Planning → Mentor → [Exit]
```

### LangGraph Version (Parallel Analysts)
```
[Entry] → [Parallel: Income, Expense, Asset, Goal, Risk] → Debate → Planning → Mentor → [Exit]
```

The LangGraph version uses:
- **Parallel node execution** for the Analyst Team
- **Conditional edges** for error handling
- **Checkpoint persistence** for long-running evaluations
- **State updates** that merge outputs from parallel branches

## Data Flow

```
UserProfile
    ├── IncomeAnalyst → IncomeAnalysis
    ├── ExpenseAnalyst → ExpenseAnalysis
    ├── AssetLiabilityAnalyst → AssetAnalysis
    ├── GoalAnalyst → GoalAnalysis
    └── RiskProfileAnalyst → RiskAnalysis
              ↓
        DebateResult (optimistic + cautious + synthesis)
              ↓
        Strategist → WealthStrategy
        RiskManager → RiskAssessment
        TaxEfficiencyAnalyst → TaxPlan
              ↓
        MentorPersona → MentoredPlan
              ↓
        PlanDecision (logged to history)
```

## Extensibility

### Adding a New Analyst

1. Subclass `BaseWealthAgent`
2. Define output model (Pydantic BaseModel)
3. Add field to `WealthState`
4. Add node to graph

### Adding a New Mentor

1. Subclass `MentorPersona`
2. Define philosophy, voice, and decision rules
3. Implement `interpret_plan()`
4. Register in `MentorRegistry`

### Adding a New Stress Test

1. Add method to `RiskManager`
2. Add scenario to `stress_test_results` dict
3. Add guardrail if test fails

## Persistence

WealthState is fully serializable:
- Pydantic models serialize to JSON
- Decision log provides audit trail
- Versioning supports plan comparison over time

Recommended: Store in PostgreSQL with JSONB columns, or document DB (MongoDB, Firestore).

## Compliance Architecture

WealthAgents includes compliance guardrails:

1. **Educational Framing**: All outputs labeled as educational, not advice
2. **Disclaimer Injection**: Every plan includes mandatory disclaimers
3. **No Execution**: Framework has no trade execution capabilities
4. **Jurisdiction Awareness**: Tax rules adapt to user location
5. **Forbidden Topics**: Each mentor has forbidden topics (e.g., no stock picks)

```python
# Compliance check in mentor interpretation
if "current stock picks" in mentor.forbidden_topics:
    plan = filter_stock_picks(plan)
```

## Performance Considerations

- **Analyst Team**: Parallel execution reduces latency by ~60%
- **Caching**: User profiles change slowly; cache analysis results
- **Incremental Updates**: Monthly re-eval only re-runs changed dimensions
- **Lazy Evaluation**: Tax analysis only runs if tax-relevant assets exist
