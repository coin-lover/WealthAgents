# WealthAgents Roadmap

## MVP (Current)
- [x] Core framework architecture
- [x] 5 Analyst agents (Income, Expense, Asset, Goal, Risk)
- [x] 2 Researcher agents (Optimistic, Cautious) with debate synthesis
- [x] 3 Planning agents (Strategist, Risk Manager, Tax Analyst)
- [x] 7 Investor mentor personas (Buffett, Graham, Lynch, Bogle, Dalio, Wood, PTJ)
- [x] Sequential execution engine
- [x] Structured state schema with versioning
- [x] Basic example and tests

## V1.0 (Next)
- [ ] **LangGraph Integration**: True parallel analyst execution with checkpointing
- [ ] **LLM Backend**: Integrate OpenAI/Anthropic for richer narrative generation
- [ ] **Web API**: FastAPI backend with REST endpoints
- [ ] **Database Persistence**: PostgreSQL/MongoDB for state storage
- [ ] **Authentication**: User accounts and profile management
- [ ] **Monthly Re-evaluation**: Automated scheduled plan updates
- [ ] **Decision Log UI**: Visual timeline of plan changes
- [ ] **Mentor Chat**: Interactive Q&A with chosen mentor
- [ ] **Export**: PDF plan generation
- [ ] **Compliance Layer**: Jurisdiction-aware disclaimers and rule filtering

## V2.0 (Future)
- [ ] **Account Connections**: Plaid integration for live data
- [ ] **Advanced Tax Modeling**: State-specific tax rules, AMT, capital gains
- [ ] **Monte Carlo Simulations**: Probabilistic goal achievement
- [ ] **Scenario Builder**: User-defined what-if scenarios
- [ ] **Mentor Council Mode**: Multiple mentors debate simultaneously
- [ ] **Community Features**: Anonymous plan benchmarking
- [ ] **Mobile App**: React Native companion
- [ ] **AI Coaching**: Proactive nudges based on spending patterns
- [ ] **Integration with TradingAgents**: Portfolio execution layer

## V3.0 (Vision)
- [ ] **Global Support**: Multi-currency, multi-jurisdiction
- [ ] **Institutional Tier**: Family office features
- [ ] **Custom Mentors**: Users create their own mentor personas
- [ ] **Real-time Monitoring**: Live net worth tracking
- [ ] **Generational Planning**: Multi-generational wealth transfer
- [ ] **AI Negotiator**: Automated bill negotiation, rate optimization
- [ ] **Open Source Ecosystem**: Plugin marketplace for new analysts

## Contributing

We welcome contributions in these priority areas:
1. **New Analysts**: Healthcare cost analyst, college savings analyst, estate planning analyst
2. **New Mentors**: Localized mentors (e.g., Li Ka-shing for Asian markets)
3. **LangGraph Migration**: Convert sequential execution to true parallel graph
4. **Data Sources**: Integrate real market data, cost-of-living APIs
5. **Testing**: More comprehensive test coverage, property-based tests
