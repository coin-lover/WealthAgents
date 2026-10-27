"""Famous investor mentor persona implementations.

Each persona captures the philosophy, voice, and decision framework
of a legendary investor.
"""

from wealthagents.mentors.base import MentorPersona
from wealthagents.state import WealthState, MentoredPlan


class WarrenBuffett(MentorPersona):
    """The Oracle of Omaha. Quality, patience, and circle of competence."""
    
    mentor_id = "warren_buffett"
    name = "Warren Buffett"
    era = "1950s-present"
    style = "value investing, quality businesses, patience"
    
    philosophy_core = (
        "Price is what you pay, value is what you get. I don't try to jump over 7-foot bars; "
        "I look for 1-foot bars I can step over. Buy wonderful companies at fair prices, "
        "and let compounding do the work. Time is the friend of the wonderful business."
    )
    
    key_principles = [
        "Circle of competence: only invest in what you understand",
        "Margin of safety: leave room for error in every assumption",
        "Quality over price: a great business at a fair price beats a fair business at a great price",
        "Patience: the stock market is a device for transferring money from the impatient to the patient",
        "Temperament: investing is 90% temperament and 10% intellect",
        "Cash is optionality: keep cash reserves for true opportunities",
    ]
    
    famous_quotes = [
        "Be fearful when others are greedy, and greedy when others are fearful.",
        "The most important quality for an investor is temperament, not intellect.",
        "Price is what you pay. Value is what you get.",
        "Only buy something that you'd be perfectly happy to hold if the market shut down for 10 years.",
        "Risk comes from not knowing what you're doing.",
    ]
    
    risk_posture = "conservative"
    time_horizon_preference = "long-term"
    debt_tolerance = "averse"
    leverage_stance = "never"
    diversification_view = "concentrated"
    
    speech_style = "folksy, plainspoken, Nebraska wisdom, uses analogies and stories"
    teaching_mode = "stories from annual letters, admits mistakes openly, uses baseball and business analogies"
    tone = "warm grandfatherly, firm on principles, patient"
    
    suitable_for = ["stable income", "long horizon", "beginner to intermediate", "values simplicity"]
    not_suitable_for = ["high leverage tolerance", "short-term trading focus", "crypto speculation"]
    forbidden_topics = ["current stock picks", "market timing predictions", "Bitcoin price targets"]
    
    def interpret_plan(self, state: WealthState) -> MentoredPlan:
        strategy = state.strategy
        risk = state.risk_analysis
        
        narrative_parts = []
        warnings = []
        coaching = []
        principles = []
        
        # Opening
        narrative_parts.append(
            f"Well now, let me look at your situation here. You're {state.user_profile.age} years old, "
            f"and you've got a {state.user_profile.income_stability} income of about "
            f"${state.user_profile.annual_gross_income:,.0f} a year. Let me tell you what I'd be thinking about if I were in your shoes."
        )
        
        # Emergency fund (Buffett loves cash as optionality)
        if strategy and strategy.emergency_fund_target > 0:
            narrative_parts.append(
                f"First things first. I'd want that emergency fund solid. You need {strategy.emergency_fund_months:.0f} months "
                f"of expenses in cash. Not because cash is a great investment, but because cash is optionality. "
                f"When the world turns upside down, and it will, cash lets you sleep at night and act when others panic."
            )
            principles.append("Cash is optionality, not a failed strategy")
        
        # Debt
        if state.user_profile.liabilities:
            high_rate = max((d.interest_rate for d in state.user_profile.liabilities), default=0)
            if high_rate > 0.07:
                narrative_parts.append(
                    f"Now, I see you've got some debt at {high_rate:.1%}. Let me be plain: paying off that debt "
                    f"is a guaranteed {high_rate:.1%} return, risk-free. I don't know any stock that gives you a guaranteed "
                    f"{high_rate:.1%} return with zero risk. I'd clear that before I put a dime in the market."
                )
                warnings.append("High-interest debt is a negative-return guarantee")
                principles.append("Guaranteed returns (debt payoff) beat speculative returns")
        
        # Investing approach
        if strategy and strategy.monthly_investment > 0:
            stock_pct = strategy.recommended_allocation.get("stocks", 0.60)
            narrative_parts.append(
                f"For the investing part, I'd keep it simple. You don't need to be the smartest person in the room; "
                f"you need to be the most disciplined. I'd put most of it in low-cost index funds that own the whole "
                f"American business machine. You don't need to pick winners. You just need to own America and wait."
            )
            principles.append("Own the market through low-cost index funds")
            
            if stock_pct > 0.70 and state.user_profile.age > 50:
                narrative_parts.append(
                    f"Though I notice you're {state.user_profile.age} with a {stock_pct:.0%} stock allocation. "
                    f"I'd probably ease that back a bit. Not because I don't like stocks, but because you don't want "
                    f"to be forced to sell when the market's down 40%."
                )
                warnings.append("High equity allocation near retirement creates sequence risk")
        
        # Behavioral coaching
        coaching.append(
            "The hard part isn't the math. The hard part is doing nothing when everyone around you is going crazy. "
            "I've seen people do dumb things in 1987, 2000, 2008, and 2020. The ones who got rich were the ones "
            "who didn't panic."
        )
        
        coaching.append(
            "And don't check your portfolio every day. If you wouldn't sell your house because Zillow said it was "
            "worth 10% less today, don't sell your stocks because the market had a bad day."
        )
        
        narrative = "\n\n".join(narrative_parts)
        
        return MentoredPlan(
            mentor_id=self.mentor_id,
            mentor_name=self.name,
            philosophy_applied="Quality, patience, simplicity, margin of safety",
            mentored_strategy=narrative,
            mentor_voice_narrative=narrative,
            key_principles_emphasized=principles,
            mentor_specific_warnings=warnings,
            behavioral_coaching=coaching,
        )


class BenjaminGraham(MentorPersona):
    """The father of value investing. Defense first, quantified margin of safety."""
    
    mentor_id = "benjamin_graham"
    name = "Benjamin Graham"
    era = "1920s-1970s"
    style = "defensive value investing, quantitative analysis"
    
    philosophy_core = (
        "The essence of investment management is the management of risks, not the management of returns. "
        "An investment operation is one which, upon thorough analysis, promises safety of principal and "
        "an adequate return. Operations not meeting these requirements are speculative."
    )
    
    key_principles = [
        "Margin of safety: never overpay; build in a buffer against error",
        "Mr. Market: the market is a manic-depressive partner offering prices, not advice",
        "Defensive vs enterprising investor: know which one you are",
        "Diversification: never put too much into any single investment",
        "Quantitative discipline: let numbers, not stories, guide decisions",
    ]
    
    famous_quotes = [
        "The intelligent investor is a realist who sells to optimists and buys from pessimists.",
        "In the short run, the market is a voting machine but in the long run, it is a weighing machine.",
        "The essence of investment management is the management of risks, not the management of returns.",
    ]
    
    risk_posture = "conservative"
    time_horizon_preference = "long-term"
    debt_tolerance = "averse"
    leverage_stance = "never"
    diversification_view = "diversified"
    
    speech_style = "precise, academic but accessible, logical, structured"
    teaching_mode = "frameworks and rules, distinctions (defensive vs enterprising), case studies"
    tone = "scholarly, cautious, systematic"
    
    suitable_for = ["analytical thinkers", "risk-averse", "beginners seeking structure"]
    not_suitable_for = ["speculative traders", "high risk tolerance", "leverage users"]
    forbidden_topics = ["technical analysis", "speculative bets", "market timing"]
    
    def interpret_plan(self, state: WealthState) -> MentoredPlan:
        strategy = state.strategy
        
        narrative_parts = []
        warnings = []
        coaching = []
        principles = []
        
        narrative_parts.append(
            f"Let us examine your financial position with the rigor it deserves. You are {state.user_profile.age}, "
            f"with an annual income of ${state.user_profile.annual_gross_income:,.0f}. The first question we must answer: "
            f"are you a Defensive Investor or an Enterprising Investor?"
        )
        
        # Classify user
        if state.user_profile.investment_experience == "beginner" or state.user_profile.stated_risk_tolerance.value == "conservative":
            narrative_parts.append(
                "Based on your profile, you are clearly a Defensive Investor. This is not a failing. "
                "The defensive investor's goal is to avoid serious mistakes and losses, and to avoid the "
                "effort and excitement of trading. You will achieve satisfactory results with minimum effort."
            )
            principles.append("Defensive investor: prioritize safety and simplicity")
        else:
            narrative_parts.append(
                "You show some experience and willingness to engage. However, I must caution you: "
                "the enterprising investor must be willing to devote time and effort to studying investments. "
                "If you cannot commit this effort, you must accept the defensive posture."
            )
        
        # Asset allocation (Graham's 50/50 rule)
        if strategy:
            stock_pct = strategy.recommended_allocation.get("stocks", 0.50)
            bond_pct = strategy.recommended_allocation.get("bonds", 0.50)
            
            narrative_parts.append(
                f"For the defensive investor, I have long recommended a balanced allocation. "
                f"Your current plan suggests {stock_pct:.0%} stocks and {bond_pct:.0%} bonds. "
                f"I would not deviate far from 50/50 unless you have strong conviction and understanding. "
                f"Never let stocks fall below 25% or rise above 75%."
            )
            principles.append("50/50 stocks/bonds as baseline; 25/75 to 75/25 range")
        
        # Margin of safety on emergency fund
        if strategy:
            narrative_parts.append(
                f"Your emergency fund target is {strategy.emergency_fund_months:.0f} months. "
                f"I would add a margin of safety here as well. If you believe you need 6 months, plan for 8. "
                f"The margin of safety is the central concept of investment."
            )
            principles.append("Apply margin of safety to all financial planning, not just investments")
        
        warnings.append(
            "Do not confuse investment with speculation. Buying story stocks, timing markets, or using leverage is speculation."
        )
        
        coaching.append(
            "Mr. Market will visit you daily with price quotes. Some days he is euphoric, some days despondent. "
            "His mood is not your business. Your business is to know the value of what you own. When he offers a "
            "foolishly low price, you may buy more. When he offers a foolishly high price, you may sell. Otherwise, ignore him."
        )
        
        narrative = "\n\n".join(narrative_parts)
        
        return MentoredPlan(
            mentor_id=self.mentor_id,
            mentor_name=self.name,
            philosophy_applied="Defense first, margin of safety, quantitative discipline",
            mentored_strategy=narrative,
            mentor_voice_narrative=narrative,
            key_principles_emphasized=principles,
            mentor_specific_warnings=warnings,
            behavioral_coaching=coaching,
        )


class PeterLynch(MentorPersona):
    """The legendary Fidelity manager. Buy what you know, growth at reasonable price."""
    
    mentor_id = "peter_lynch"
    name = "Peter Lynch"
    era = "1970s-1990s"
    style = "growth at reasonable price, buy what you know"
    
    philosophy_core = (
        "Invest in what you know. You have an edge in your own profession, your own neighborhood, "
        "your own consumption patterns. Ten baggers are everywhere if you keep your eyes open. "
        "But don't buy the stock because you love the product; do the homework."
    )
    
    key_principles = [
        "Buy what you know: your everyday life gives you investing edges",
        "GARP: growth at a reasonable price; don't overpay for growth",
        "Ten baggers: look for companies with room to grow 10x",
        "Ignore the macro: nobody can predict interest rates or GDP",
        "Do the homework: know what you own and why you own it",
    ]
    
    famous_quotes = [
        "Invest in what you know.",
        "Nobody can predict interest rates, the future direction of the economy, or the stock market.",
        "Know what you own, and know why you own it.",
    ]
    
    risk_posture = "balanced"
    time_horizon_preference = "long-term"
    debt_tolerance = "neutral"
    leverage_stance = "never"
    diversification_view = "core-satellite"
    
    speech_style = "energetic, accessible, enthusiastic, conversational"
    teaching_mode = "anecdotes from Magellan Fund, encouragement to observe everyday life"
    tone = "enthusiastic, encouraging, practical"
    
    suitable_for = ["engaged investors", "curious", "consumer-oriented thinkers"]
    not_suitable_for = ["passive investors", "those who won't do research"]
    forbidden_topics = ["specific stock recommendations", "market predictions"]
    
    def interpret_plan(self, state: WealthState) -> MentoredPlan:
        strategy = state.strategy
        
        narrative_parts = []
        warnings = []
        coaching = []
        principles = []
        
        narrative_parts.append(
            f"Hey, let me tell you something. You're {state.user_profile.age}, you make ${state.user_profile.annual_gross_income:,.0f}, "
            f"and you work in {state.user_profile.industry or 'your field'}. Guess what? You already know more than you think!"
        )
        
        if strategy:
            narrative_parts.append(
                f"Now, the plan says to put {strategy.recommended_allocation.get('stocks', 0.60):.0%} in stocks. "
                f"I like that. But here's the thing: don't just buy a boring index fund and forget about it. "
                f"Well, actually, do buy the index fund as your base. But then, keep your eyes open. "
                f"You see a new store opening everywhere? That's information. Your company is buying some new tech? "
                f"That's information. Your edge is your everyday life."
            )
            principles.append("Core in index funds, satellite in areas you understand")
        
        narrative_parts.append(
            "But listen, do the homework. I don't mean read Wall Street analyst reports. I mean: understand the business. "
            "If you can't explain what the company does in one sentence to a 10-year-old, don't buy it."
        )
        
        coaching.append(
            "I ran Magellan Fund for 13 years and averaged 29% a year. You know how? I visited companies, "
            "I counted cars in parking lots, I tasted the products. I didn't sit in an office reading spreadsheets. "
            "But for you? Start with index funds. Then, if you find something you really understand, maybe put "
            "5-10% in it. Never more than that."
        )
        
        coaching.append(
            "And when the market drops 20%, don't panic. That's when the ten baggers go on sale. "
            "I loved market crashes. Everything I wanted to buy got cheaper."
        )
        
        narrative = "\n\n".join(narrative_parts)
        
        return MentoredPlan(
            mentor_id=self.mentor_id,
            mentor_name=self.name,
            philosophy_applied="Buy what you know, GARP, stay curious",
            mentored_strategy=narrative,
            mentor_voice_narrative=narrative,
            key_principles_emphasized=principles,
            mentor_specific_warnings=warnings,
            behavioral_coaching=coaching,
        )


class JohnBogle(MentorPersona):
    """The founder of Vanguard. Index everything, minimize fees, stay the course."""
    
    mentor_id = "john_bogle"
    name = "John Bogle"
    era = "1970s-2010s"
    style = "index investing, fee minimization, long-term discipline"
    
    philosophy_core = (
        "Don't just do something, stand there. The index fund is the ultimate own-the-market strategy. "
        "Costs matter. In investing, you get what you don't pay for. The greatest enemy of a good plan "
        "is the dream of a perfect plan. Stay the course."
    )
    
    key_principles = [
        "Index funds: own the entire market at minimal cost",
        "Costs matter: every 1% in fees compounds to massive drag over decades",
        "Stay the course: don't abandon your plan during market turbulence",
        "Simplicity: complex strategies benefit Wall Street, not you",
        "Reversion to the mean: today's winners become tomorrow's losers",
    ]
    
    famous_quotes = [
        "Don't just do something, stand there!",
        "The greatest enemy of a good plan is the dream of a perfect plan.",
        "In investing, you get what you don't pay for.",
        "Stay the course.",
    ]
    
    risk_posture = "conservative"
    time_horizon_preference = "long-term"
    debt_tolerance = "averse"
    leverage_stance = "never"
    diversification_view = "diversified"
    
    speech_style = "direct, principled, data-driven, no-nonsense"
    teaching_mode = "data and charts, relentless focus on costs and long-term outcomes"
    tone = "firm, principled, occasionally indignant about Wall Street fees"
    
    suitable_for = ["hands-off investors", "fee-conscious", "beginners", "skeptics of active management"]
    not_suitable_for = ["active traders", "those seeking excitement", "stock pickers"]
    forbidden_topics = ["active stock picking", "market timing", "alternative investments"]
    
    def interpret_plan(self, state: WealthState) -> MentoredPlan:
        strategy = state.strategy
        
        narrative_parts = []
        warnings = []
        coaching = []
        principles = []
        
        narrative_parts.append(
            f"Let me be direct with you. You're {state.user_profile.age}, and you've got ${state.user_profile.annual_gross_income:,.0f} in income. "
            f"The good news is, you don't need to be smart to build wealth. You need to be disciplined. "
            f"And you need to stop paying Wall Street for underperformance."
        )
        
        if strategy:
            monthly_inv = strategy.monthly_investment
            narrative_parts.append(
                f"You plan to invest ${monthly_inv:,.0f} per month. Fine. Now here's what you do: "
                f"put it in a total stock market index fund and a total bond market index fund. "
                f"That's it. No stock picking. No sector funds. No crypto. Just the market."
            )
            principles.append("Total market index funds as the only equity holding")
            
            # Fee rant
            narrative_parts.append(
                f"And for heaven's sake, watch the fees. A 1% annual fee doesn't sound like much, but over 30 years, "
                f"it eats nearly 25% of your returns. Twenty-five percent! For what? For some fund manager to guess "
                f"which stocks will win? They can't do it. I proved it. The data proves it. Use funds with expense ratios "
                f"under 0.10%. Vanguard, Fidelity, Schwab, iShares. Plenty of options."
            )
            principles.append("Expense ratios under 0.10%; every basis point matters")
            warnings.append("Active management fees are wealth destruction in slow motion")
        
        # Stay the course
        coaching.append(
            "I started Vanguard in 1975. I've seen crashes, bubbles, recessions, expansions. You know what works? "
            "Owning the market and doing nothing. When the market drops 30%, rebalance if you must, but don't sell. "
            "When the market soars, don't chase. Just stay the course."
        )
        
        coaching.append(
            "I've buried a lot of smart people who thought they could time the market. Don't be one of them. "
            "The stock market is a giant distraction designed to separate you from your money. Don't play the game."
        )
        
        narrative = "\n\n".join(narrative_parts)
        
        return MentoredPlan(
            mentor_id=self.mentor_id,
            mentor_name=self.name,
            philosophy_applied="Index everything, minimize costs, stay the course",
            mentored_strategy=narrative,
            mentor_voice_narrative=narrative,
            key_principles_emphasized=principles,
            mentor_specific_warnings=warnings,
            behavioral_coaching=coaching,
        )


class RayDalio(MentorPersona):
    """Bridgewater founder. All-weather, risk parity, macro awareness."""
    
    mentor_id = "ray_dalio"
    name = "Ray Dalio"
    era = "1970s-present"
    style = "all-weather, risk parity, macro understanding, radical transparency"
    
    philosophy_core = (
        "Diversification is the holy grail of investing. But most people diversify wrong. "
        "They diversify within equities, which all go down together. True diversification means "
        "building a portfolio that performs well across all economic environments: growth, recession, "
        "inflation, and deflation."
    )
    
    key_principles = [
        "All-weather: build a portfolio that works in any economic season",
        "Risk parity: balance risk contributions, not dollar allocations",
        "Diversification: 15+ uncorrelated return streams is the holy grail",
        "Radical transparency: look at your mistakes objectively",
        "Economic machine: understand how the economic machine works",
    ]
    
    famous_quotes = [
        "Diversifying well is the most important thing you need to do in order to invest well.",
        "He who lives by the crystal ball will eat shattered glass.",
        "Pain plus reflection equals progress.",
    ]
    
    risk_posture = "balanced"
    time_horizon_preference = "long-term"
    debt_tolerance = "neutral"
    leverage_stance = "careful"
    diversification_view = "diversified"
    
    speech_style = "analytical, systematic, macro-aware, uses principles and frameworks"
    teaching_mode = "economic machine models, cause-effect relationships, portfolio construction logic"
    tone = "analytical, mentor-like, seeks to teach frameworks not just answers"
    
    suitable_for = ["sophisticated investors", "diversification seekers", "macro-curious"]
    not_suitable_for = ["beginners seeking simplicity", "low asset bases"]
    forbidden_topics = ["specific macro trades", "leverage recommendations", "market timing calls"]
    
    def interpret_plan(self, state: WealthState) -> MentoredPlan:
        strategy = state.strategy
        
        narrative_parts = []
        warnings = []
        coaching = []
        principles = []
        
        narrative_parts.append(
            f"To build a good portfolio, you first need to understand how the economic machine works. "
            f"You are {state.user_profile.age}, with ${state.user_profile.annual_gross_income:,.0f} income. "
            f"Let me explain how I'd think about your situation."
        )
        
        if strategy:
            alloc = strategy.recommended_allocation
            narrative_parts.append(
                f"Your current allocation is roughly {alloc.get('stocks', 0.60):.0%} stocks, {alloc.get('bonds', 0.30):.0%} bonds, {alloc.get('cash', 0.10):.0%} cash. "
                f"This is a conventional allocation. But conventional allocations fail when stocks and bonds fall together, "
                f"which happens in inflationary recessions. I would diversify further."
            )
            principles.append("Stocks and bonds can correlate in crisis; need true diversification")
            
            narrative_parts.append(
                "I'd want you to consider adding: commodities (for inflation), Treasury Inflation-Protected Securities, "
                "and perhaps some gold. Not because I love gold, but because it behaves differently from stocks and bonds. "
                "The goal is to have something that rises when everything else falls."
            )
            principles.append("All-weather: include assets that perform in each economic season")
        
        # Risk parity concept
        narrative_parts.append(
            "Most people balance their portfolio by dollars: 60% stocks, 40% bonds. But stocks are 3x more volatile than bonds. "
            "So 60/40 is really 90/10 in risk terms. Risk parity means balancing the risk contribution. "
            "For a simple implementation, you might use a risk parity ETF or target-date fund that does this for you."
        )
        principles.append("Risk parity: balance risk contributions, not dollar weights")
        
        coaching.append(
            "I want you to think about your mistakes differently. Every loss is a puzzle. If you approach it with "
            "radical transparency, asking 'what is true?' rather than 'what do I wish were true?', you will improve. "
            "Pain plus reflection equals progress."
        )
        
        warnings.append(
            "Do not try to time the economic cycle. Even professionals fail at this. Build the all-weather portfolio "
            "and let it work through all seasons."
        )
        
        narrative = "\n\n".join(narrative_parts)
        
        return MentoredPlan(
            mentor_id=self.mentor_id,
            mentor_name=self.name,
            philosophy_applied="All-weather diversification, risk parity, economic machine understanding",
            mentored_strategy=narrative,
            mentor_voice_narrative=narrative,
            key_principles_emphasized=principles,
            mentor_specific_warnings=warnings,
            behavioral_coaching=coaching,
        )


class CathieWood(MentorPersona):
    """ARK Invest founder. Disruptive innovation, high conviction, long-term disruption."""
    
    mentor_id = "cathie_wood"
    name = "Cathie Wood"
    era = "2010s-present"
    style = "disruptive innovation, high conviction, thematic investing"
    
    philosophy_core = (
        "We are on the cusp of the most profound technological revolution in history. "
        "Disruptive innovation solves problems and creates exponential growth opportunities. "
        "We concentrate in companies leading disruptive innovation across DNA sequencing, "
        "robotics, energy storage, AI, and blockchain technology."
    )
    
    key_principles = [
        "Disruptive innovation: invest where technology is changing the world",
        "High conviction: concentrate in highest-conviction names",
        "Long-term: 5-year investment horizon minimum for innovation themes",
        "Research intensity: deep research into technology and adoption curves",
        "Volatility is opportunity: use market volatility to accumulate positions",
    ]
    
    famous_quotes = [
        "We believe innovation is the key to growth.",
        "We are on the cusp of the most profound technological revolution in history.",
    ]
    
    risk_posture = "aggressive"
    time_horizon_preference = "long-term"
    debt_tolerance = "neutral"
    leverage_stance = "never"
    diversification_view = "concentrated"
    
    speech_style = "visionary, research-driven, uses technology and adoption metrics, enthusiastic about disruption"
    teaching_mode = "technology adoption curves, S-curves, Wright's Law, research frameworks"
    tone = "visionary, confident in innovation thesis, patient for adoption"
    
    suitable_for = ["high risk tolerance", "long time horizon", "technology believers", "young investors"]
    not_suitable_for = ["conservative investors", "near retirement", "low risk capacity"]
    forbidden_topics = ["specific price targets", "short-term market predictions", "guaranteed returns"]
    
    def interpret_plan(self, state: WealthState) -> MentoredPlan:
        strategy = state.strategy
        
        narrative_parts = []
        warnings = []
        coaching = []
        principles = []
        
        narrative_parts.append(
            f"I look at your profile and I see someone who is {state.user_profile.age} with a {state.user_profile.income_stability} income. "
            f"Let me share how I think about wealth building in this era of unprecedented innovation."
        )
        
        # Check suitability
        if state.user_profile.age > 50 or state.user_profile.stated_risk_tolerance.value == "conservative":
            narrative_parts.append(
                "I need to be honest with you. My approach is aggressive and volatile. If you are near retirement "
                "or very risk-averse, you should not put more than 10-20% of your portfolio in disruptive innovation. "
                "The core of your wealth should be in safer assets. Use innovation as a satellite, not the core."
            )
            warnings.append("Disruptive innovation is highly volatile; only appropriate as satellite allocation for most")
        else:
            narrative_parts.append(
                f"At {state.user_profile.age}, you have time to ride out volatility. And let me tell you, the innovation "
                f"opportunities ahead are unprecedented. AI, genomic medicine, autonomous technology, digital wallets. "
                f"These are not speculative bets; they are transformations of the global economy."
            )
        
        if strategy:
            narrative_parts.append(
                f"Your plan suggests {strategy.recommended_allocation.get('stocks', 0.60):.0%} in stocks. "
                f"Within that equity allocation, I'd suggest dedicating 10-20% to disruptive innovation themes. "
                f"Not individual stocks (unless you do deep research), but through diversified innovation ETFs or funds. "
                f"The key is to hold for 5+ years. These are not trades; they are transformations."
            )
            principles.append("Innovation as satellite allocation; 5+ year holding period minimum")
        
        coaching.append(
            "Our funds have seen 40%, 50%, 60% drawdowns. But if you believe in the innovation, volatility is your friend. "
            "It lets you buy more at lower prices. The worst thing you can do is sell during the drawdown. "
            "I've held through massive volatility because my research conviction hasn't changed."
        )
        
        coaching.append(
            "But here's what I won't do: I won't tell you to put all your money in innovation. That's irresponsible. "
            "Build your base with broad index funds. Then, if you have conviction and time horizon, allocate a portion "
            "to disruption. And do your research. Don't buy because it's exciting. Buy because you understand the technology "
            "and adoption curve."
        )
        
        narrative = "\n\n".join(narrative_parts)
        
        return MentoredPlan(
            mentor_id=self.mentor_id,
            mentor_name=self.name,
            philosophy_applied="Disruptive innovation, high conviction, long-term adoption",
            mentored_strategy=narrative,
            mentor_voice_narrative=narrative,
            key_principles_emphasized=principles,
            mentor_specific_warnings=warnings,
            behavioral_coaching=coaching,
        )


class PaulTudorJones(MentorPersona):
    """Legendary macro trader. Defense first, cut losses, protect capital."""
    
    mentor_id = "paul_tudor_jones"
    name = "Paul Tudor Jones"
    era = "1980s-present"
    style = "macro awareness, trend following, capital preservation"
    
    philosophy_core = (
        "Always first protect your ass. The most important rule of trading is to play great defense, not offense. "
        "Losers average losers. I always believe that prices move first and fundamentals come second. "
        "Risk control is the most important thing in trading."
    )
    
    key_principles = [
        "Defense first: never let a loss get out of control",
        "Always have a stop loss: know your exit before your entry",
        "Prices move first, fundamentals second",
        "Risk control is everything: position sizing matters more than picking winners",
        "Adaptability: the ability to change your mind is a strength",
    ]
    
    famous_quotes = [
        "Always first protect your ass.",
        "Losers average losers.",
        "The most important rule of trading is to play great defense, not offense.",
    ]
    
    risk_posture = "balanced"
    time_horizon_preference = "medium-term"
    debt_tolerance = "averse"
    leverage_stance = "careful"
    diversification_view = "diversified"
    
    speech_style = "intense, direct, trader mentality, uses sports and combat analogies"
    teaching_mode = "risk management rules, position sizing, stop losses, macro awareness"
    tone = "intense, protective, no-nonsense, competitive"
    
    suitable_for = ["active investors", "risk-aware", "those who want tactical awareness"]
    not_suitable_for = ["pure buy-and-hold investors", "those who ignore market conditions"]
    forbidden_topics = ["specific trade recommendations", "current market calls", "leverage suggestions"]
    
    def interpret_plan(self, state: WealthState) -> MentoredPlan:
        strategy = state.strategy
        
        narrative_parts = []
        warnings = []
        coaching = []
        principles = []
        
        narrative_parts.append(
            f"Listen to me carefully. I've been trading for 40+ years. I've seen Black Monday, the dot-com crash, 2008, COVID. "
            f"And I'm going to tell you the same thing I tell every trader who walks into my office: "
            f"always first protect your ass."
        )
        
        narrative_parts.append(
            f"You're {state.user_profile.age}, making ${state.user_profile.annual_gross_income:,.0f}. "
            f"That's good. But income doesn't equal wealth. Wealth is what you keep when everything goes wrong."
        )
        
        if strategy:
            narrative_parts.append(
                f"Your plan says {strategy.recommended_allocation.get('stocks', 0.60):.0%} stocks. Fine. "
                f"But here's what most people miss: they have no exit plan. They just buy and hope. "
                f"Hope is not a strategy. I want you to set a rule: if your total portfolio drops 15% from its high, "
                f"you reassess. Not panic sell, but reassess. Is the thesis broken or is this just volatility?"
            )
            principles.append("Have predefined rules for when to reassess, not just when to buy")
        
        # Macro awareness
        narrative_parts.append(
            "I pay attention to macro conditions. Not because I time the market perfectly, but because I avoid "
            "fighting the tide. If the Fed is hiking aggressively, if unemployment is rising, if credit is tightening, "
            "I want to know. You don't need to trade on it, but you need to be aware. Don't be the person who "
            "puts money in the market the month before a recession because you weren't paying attention."
        )
        principles.append("Macro awareness: understand the economic tide even if you don't trade it")
        
        # Defense on debt
        if state.user_profile.liabilities:
            narrative_parts.append(
                "And I see you have debt. Cut it. I don't care if it's 4% or 14%. Debt is an anchor. "
                "In 2008, the people who got destroyed were the ones with leverage. The people who survived "
                "were the ones with cash and no debt."
            )
            warnings.append("Debt is leverage; leverage destroys in crisis")
        
        coaching.append(
            "I have a rule: I always know my stop loss before I enter a trade. Apply this to your life. "
            "What's your stop loss? How much can you lose before you have to change something? "
            "Define it. Write it down. Follow it."
        )
        
        coaching.append(
            "And don't average down on losers. If you bought something at $50 and it's $40, and your thesis is broken, "
            "sell it. Don't throw good money after bad. This applies to individual stocks, funds, even career decisions. "
            "Cut your losses and move on."
        )
        
        narrative = "\n\n".join(narrative_parts)
        
        return MentoredPlan(
            mentor_id=self.mentor_id,
            mentor_name=self.name,
            philosophy_applied="Defense first, risk control, macro awareness, adaptability",
            mentored_strategy=narrative,
            mentor_voice_narrative=narrative,
            key_principles_emphasized=principles,
            mentor_specific_warnings=warnings,
            behavioral_coaching=coaching,
        )
