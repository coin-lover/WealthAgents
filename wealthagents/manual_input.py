"""Guided manual input for users in non-Plaid countries.

Provides structured forms, smart defaults, and validation
for users who must enter their financial data manually.
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass

from wealthagents.state import UserProfile, Asset, Debt, Goal, AssetType, DebtType
from wealthagents.connections import AccountConnectionManager


@dataclass
class InputSection:
    """A section of the manual input form."""
    title: str
    description: str
    fields: List[Dict[str, Any]]
    is_required: bool = True


class ManualInputGuide:
    """Generates a guided manual input experience based on user country.
    
    This class returns form configuration that a frontend can render.
    It does not render UI itself; it provides the structure and validation.
    """
    
    def __init__(self, user_profile: UserProfile):
        self.user_profile = user_profile
        self.country = (user_profile.location_country or "US").upper()
        self.currency = user_profile.currency or "USD"
    
    def get_form_sections(self) -> List[InputSection]:
        """Get the ordered list of form sections for this user."""
        return [
            self._income_section(),
            self._expenses_section(),
            self._assets_section(),
            self._liabilities_section(),
            self._goals_section(),
        ]
    
    def _income_section(self) -> InputSection:
        return InputSection(
            title="Income",
            description="Let's start with how much you earn.",
            fields=[
                {
                    "name": "annual_gross_income",
                    "label": f"Annual Gross Income ({self.currency})",
                    "type": "number",
                    "placeholder": f"e.g., 80000",
                    "required": True,
                    "help": "Your pre-tax annual salary before any deductions",
                },
                {
                    "name": "monthly_net_income",
                    "label": f"Monthly Net Income ({self.currency})",
                    "type": "number",
                    "placeholder": f"e.g., 5200",
                    "required": False,
                    "help": "What hits your bank account each month after taxes",
                },
                {
                    "name": "employment_status",
                    "label": "Employment Status",
                    "type": "select",
                    "options": ["employed", "self-employed", "unemployed", "retired"],
                    "required": True,
                },
                {
                    "name": "income_stability",
                    "label": "How stable is your income?",
                    "type": "select",
                    "options": ["stable", "moderate", "unstable"],
                    "required": True,
                },
            ],
        )
    
    def _expenses_section(self) -> InputSection:
        return InputSection(
            title="Monthly Expenses",
            description="How much do you spend each month? A rough estimate is fine.",
            fields=[
                {
                    "name": "monthly_expenses",
                    "label": f"Total Monthly Expenses ({self.currency})",
                    "type": "number",
                    "placeholder": f"e.g., 4000",
                    "required": True,
                    "help": "Include rent, food, transport, subscriptions, everything",
                },
                {
                    "name": "housing_expense",
                    "label": f"Housing (rent/mortgage) ({self.currency})",
                    "type": "number",
                    "placeholder": f"e.g., 1500",
                    "required": False,
                },
                {
                    "name": "debt_payments",
                    "label": f"Total Debt Payments ({self.currency})",
                    "type": "number",
                    "placeholder": f"e.g., 500",
                    "required": False,
                    "help": "Minimum payments on all loans and credit cards",
                },
            ],
        )
    
    def _assets_section(self) -> InputSection:
        suggested_types = self._get_country_asset_types()
        
        return InputSection(
            title="Assets",
            description="What do you own? Include everything from checking accounts to property.",
            fields=[
                {
                    "name": "assets",
                    "label": "Your Assets",
                    "type": "repeatable_group",
                    "group_fields": [
                        {"name": "name", "label": "Account Name", "type": "text", "placeholder": "e.g., Chase Checking"},
                        {"name": "asset_type", "label": "Type", "type": "select", "options": suggested_types},
                        {"name": "value", "label": f"Current Value ({self.currency})", "type": "number"},
                        {"name": "cost_basis", "label": f"Cost Basis (if investment) ({self.currency})", "type": "number", "required": False},
                    ],
                    "required": True,
                    "help": "Add all bank accounts, investments, retirement accounts, property",
                },
            ],
        )
    
    def _liabilities_section(self) -> InputSection:
        return InputSection(
            title="Liabilities",
            description="What do you owe? Mortgages, student loans, credit cards.",
            fields=[
                {
                    "name": "liabilities",
                    "label": "Your Debts",
                    "type": "repeatable_group",
                    "group_fields": [
                        {"name": "name", "label": "Debt Name", "type": "text", "placeholder": "e.g., Student Loan"},
                        {"name": "debt_type", "label": "Type", "type": "select", 
                         "options": ["credit_card", "student_loan", "mortgage", "auto_loan", "personal_loan", "other"]},
                        {"name": "balance", "label": f"Current Balance ({self.currency})", "type": "number"},
                        {"name": "interest_rate", "label": "Interest Rate (%)", "type": "number", "step": 0.01},
                        {"name": "minimum_payment", "label": f"Minimum Monthly Payment ({self.currency})", "type": "number"},
                    ],
                    "required": False,
                    "help": "It's important to be honest here. We use this to optimize your debt payoff.",
                },
            ],
        )
    
    def _goals_section(self) -> InputSection:
        return InputSection(
            title="Goals",
            description="What are you saving for? We'll check if your plan can get you there.",
            fields=[
                {
                    "name": "goals",
                    "label": "Your Financial Goals",
                    "type": "repeatable_group",
                    "group_fields": [
                        {"name": "name", "label": "Goal Name", "type": "text", "placeholder": "e.g., Buy a House"},
                        {"name": "category", "label": "Category", "type": "select",
                         "options": ["emergency_fund", "debt_payoff", "home_purchase", "retirement", "education", "short_term", "other"]},
                        {"name": "target_amount", "label": f"Target Amount ({self.currency})", "type": "number"},
                        {"name": "current_amount", "label": f"Saved So Far ({self.currency})", "type": "number", "default": 0},
                        {"name": "timeline_months", "label": "Months to Goal", "type": "number"},
                        {"name": "priority", "label": "Priority", "type": "select", 
                         "options": ["critical", "high", "medium", "low"], "default": "medium"},
                    ],
                    "required": True,
                },
            ],
        )
    
    def _get_country_asset_types(self) -> List[str]:
        """Get asset type suggestions tailored to the user's country."""
        base = ["cash", "checking", "savings", "brokerage", "real_estate", "crypto", "other"]
        
        country_retirement = {
            "US": ["retirement_401k", "retirement_ira", "retirement_roth"],
            "CA": ["retirement_401k"],  # RRSP mapped broadly
            "GB": ["retirement_ira"],   # SIPP mapped broadly
            "AU": ["retirement_401k"],  # Superannuation mapped broadly
            "DE": ["retirement_ira"],   # Riester/Rurup mapped broadly
            "FR": ["retirement_ira"],   # PER mapped broadly
        }
        
        extra = country_retirement.get(self.country, [])
        return extra + base
    
    def get_smart_defaults(self) -> Dict[str, Any]:
        """Provide smart defaults based on country and demographics."""
        defaults = {
            "currency": self.currency,
            "suggested_emergency_fund_months": 6 if self.user_profile.dependents > 0 else 3,
            "suggested_retirement_age": 65,
        }
        
        # Country-specific retirement accounts
        if self.country == "US":
            defaults["retirement_accounts"] = ["401(k)", "Traditional IRA", "Roth IRA", "HSA"]
        elif self.country == "GB":
            defaults["retirement_accounts"] = ["SIPP", "ISA", "LISA"]
        elif self.country == "CA":
            defaults["retirement_accounts"] = ["RRSP", "TFSA"]
        elif self.country == "AU":
            defaults["retirement_accounts"] = ["Superannuation"]
        elif self.country == "DE":
            defaults["retirement_accounts"] = ["Riester-Rente", "Rurup-Rente"]
        else:
            defaults["retirement_accounts"] = ["Workplace Pension", "Personal Pension"]
        
        return defaults
    
    def validate_input(self, data: dict) -> List[str]:
        """Validate manually submitted form data.
        
        Returns a list of error messages. Empty list means valid.
        """
        errors = []
        
        # Income validation
        income = data.get("annual_gross_income", 0)
        if income <= 0:
            errors.append("Annual income must be greater than zero.")
        if income > 10_000_000:
            errors.append("Annual income seems unusually high. Please verify.")
        
        # Expense validation
        expenses = data.get("monthly_expenses", 0)
        net_income = data.get("monthly_net_income") or (income * 0.75 / 12)
        
        if expenses > net_income * 1.5:
            errors.append("Your monthly expenses are much higher than your net income. Please double-check.")
        if expenses < 100 and net_income > 2000:
            errors.append("Your expenses seem too low for your income level. Please verify.")
        
        # Asset validation
        assets = data.get("assets", [])
        if not assets:
            errors.append("Please add at least one asset (e.g., a checking account).")
        
        for asset in assets:
            if asset.get("value", 0) < 0:
                errors.append(f"Asset '{asset.get('name')}' cannot have a negative value.")
        
        # Liability validation
        liabilities = data.get("liabilities", [])
        for debt in liabilities:
            rate = debt.get("interest_rate", 0)
            if rate > 1.0:
                errors.append(f"Interest rate on '{debt.get('name')}' should be entered as a decimal (e.g., 0.05 for 5%), not {rate}.")
            if rate > 0.50:
                errors.append(f"Interest rate on '{debt.get('name')}' seems extremely high ({rate:.0%}). Please verify.")
        
        # Net worth sanity check
        total_assets = sum(a.get("value", 0) for a in assets)
        total_debt = sum(d.get("balance", 0) for d in liabilities)
        
        if total_debt > total_assets * 5 and total_assets > 0:
            errors.append("Your total debt is more than 5x your total assets. Please review your entries.")
        
        # Goal validation
        goals = data.get("goals", [])
        for goal in goals:
            target = goal.get("target_amount", 0)
            current = goal.get("current_amount", 0)
            if target <= 0:
                errors.append(f"Goal '{goal.get('name')}' must have a positive target amount.")
            if current > target:
                errors.append(f"Goal '{goal.get('name')}' current amount exceeds the target. Please adjust.")
        
        return errors
    
    def build_user_profile(self, form_data: dict) -> UserProfile:
        """Convert validated form data into a UserProfile.
        
        This is the main method called after the user submits the manual form.
        """
        # Parse assets
        assets = []
        for a in form_data.get("assets", []):
            assets.append(Asset(
                name=a.get("name", "Unnamed Asset"),
                asset_type=a.get("asset_type", "other"),
                value=float(a.get("value", 0)),
                cost_basis=float(a.get("cost_basis")) if a.get("cost_basis") else None,
            ))
        
        # Parse liabilities
        liabilities = []
        for d in form_data.get("liabilities", []):
            rate = d.get("interest_rate", 0)
            if rate > 1:
                rate = rate / 100
            liabilities.append(Debt(
                name=d.get("name", "Unnamed Debt"),
                debt_type=d.get("debt_type", "other"),
                balance=float(d.get("balance", 0)),
                interest_rate=float(rate),
                minimum_payment=float(d.get("minimum_payment", 0)),
            ))
        
        # Parse goals
        goals = []
        for g in form_data.get("goals", []):
            goals.append(Goal(
                name=g.get("name", "Unnamed Goal"),
                category=g.get("category", "other"),
                target_amount=float(g.get("target_amount", 0)),
                current_amount=float(g.get("current_amount", 0)),
                timeline_months=int(g.get("timeline_months", 60)) if g.get("timeline_months") else None,
                priority=g.get("priority", "medium"),
            ))
        
        # Update profile
        self.user_profile.annual_gross_income = float(form_data.get("annual_gross_income", 0))
        self.user_profile.monthly_net_income = float(form_data.get("monthly_net_income", 0)) if form_data.get("monthly_net_income") else None
        self.user_profile.employment_status = form_data.get("employment_status", "employed")
        self.user_profile.income_stability = form_data.get("income_stability", "stable")
        self.user_profile.monthly_expenses = float(form_data.get("monthly_expenses", 0))
        self.user_profile.assets = assets
        self.user_profile.liabilities = liabilities
        self.user_profile.goals = goals
        
        # Calculate derived fields
        if self.user_profile.monthly_net_income:
            savings = self.user_profile.monthly_net_income - self.user_profile.monthly_expenses
            self.user_profile.current_monthly_savings = max(0, savings)
        
        liquid = sum(a.value for a in assets if a.asset_type in ["cash", "checking", "savings"])
        if self.user_profile.monthly_expenses > 0:
            self.user_profile.current_emergency_fund_months = liquid / self.user_profile.monthly_expenses
        
        return self.user_profile


def get_manual_input_guide(user_profile: UserProfile) -> ManualInputGuide:
    """Factory function to create a manual input guide for a user."""
    return ManualInputGuide(user_profile)
