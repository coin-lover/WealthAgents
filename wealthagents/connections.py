"""Account connection logic for WealthAgents.

Simple rule: Plaid for supported countries, manual entry for everything else.
"""

from typing import List, Optional

from wealthagents.state import UserProfile


# Plaid-supported countries as of 2025
# Source: https://plaid.com/global/
PLAID_SUPPORTED_COUNTRIES: List[str] = [
    # North America
    "US",  # United States
    "CA",  # Canada
    # United Kingdom
    "GB",  # United Kingdom
    # Europe (18 countries)
    "AT",  # Austria
    "BE",  # Belgium
    "DK",  # Denmark
    "EE",  # Estonia
    "FI",  # Finland
    "FR",  # France
    "DE",  # Germany
    "IE",  # Ireland
    "IT",  # Italy
    "LV",  # Latvia
    "LT",  # Lithuania
    "NL",  # Netherlands
    "NO",  # Norway
    "PL",  # Poland
    "PT",  # Portugal
    "ES",  # Spain
    "SE",  # Sweden
]


def is_plaid_supported(country_code: str) -> bool:
    """Check if a country is supported by Plaid.
    
    Args:
        country_code: ISO 3166-1 alpha-2 country code (e.g., "US", "GB", "DE")
        
    Returns:
        True if Plaid supports automatic account connections in this country.
    """
    if not country_code:
        return False
    return country_code.upper() in PLAID_SUPPORTED_COUNTRIES


def get_connection_mode(user_profile: UserProfile) -> str:
    """Determine the account connection mode for a user.
    
    Returns:
        "plaid_auto" if Plaid is available in the user's country.
        "manual_input" if the user must enter data manually.
    """
    country = (user_profile.location_country or "").upper()
    if is_plaid_supported(country):
        return "plaid_auto"
    return "manual_input"


def get_connection_mode_for_country(country_code: str) -> str:
    """Determine connection mode for a given country code.
    
    Args:
        country_code: ISO 3166-1 alpha-2 country code
        
    Returns:
        "plaid_auto" or "manual_input"
    """
    if is_plaid_supported(country_code):
        return "plaid_auto"
    return "manual_input"


def get_supported_countries() -> List[str]:
    """Return the full list of Plaid-supported country codes."""
    return PLAID_SUPPORTED_COUNTRIES.copy()


def get_supported_countries_text() -> str:
    """Return a human-readable list of supported countries."""
    country_names = {
        "US": "United States",
        "CA": "Canada",
        "GB": "United Kingdom",
        "AT": "Austria",
        "BE": "Belgium",
        "DK": "Denmark",
        "EE": "Estonia",
        "FI": "Finland",
        "FR": "France",
        "DE": "Germany",
        "IE": "Ireland",
        "IT": "Italy",
        "LV": "Latvia",
        "LT": "Lithuania",
        "NL": "Netherlands",
        "NO": "Norway",
        "PL": "Poland",
        "PT": "Portugal",
        "ES": "Spain",
        "SE": "Sweden",
    }
    return ", ".join(f"{code} ({country_names.get(code, code)})" for code in PLAID_SUPPORTED_COUNTRIES)


class AccountConnectionManager:
    """Manages account connections for a user.
    
    This is a thin wrapper that decides whether to use Plaid
    or manual input based on the user's country.
    
    For Plaid-supported countries, this would integrate with
    the Plaid API (plaid-python SDK).
    
    For manual-input countries, this validates and stores
    user-entered financial data.
    """
    
    def __init__(self, user_profile: UserProfile):
        self.user_profile = user_profile
        self.mode = get_connection_mode(user_profile)
    
    def is_auto_sync_available(self) -> bool:
        """Check if automatic account syncing is available."""
        return self.mode == "plaid_auto"
    
    def get_connection_message(self) -> str:
        """Get the message to show the user about account connections."""
        if self.mode == "plaid_auto":
            country_name = self._country_name(self.user_profile.location_country)
            return (
                f"We support automatic account connections in {country_name}. "
                f"Link your bank accounts to keep your wealth plan up to date automatically."
            )
        else:
            country_name = self._country_name(self.user_profile.location_country)
            return (
                f"We don't yet support automatic connections in {country_name}. "
                f"Please enter your financial details below and update them anytime."
            )
    
    def _country_name(self, code: Optional[str]) -> str:
        """Simple country name lookup."""
        names = {
            "US": "the United States", "CA": "Canada", "GB": "the United Kingdom",
            "AT": "Austria", "BE": "Belgium", "DK": "Denmark", "EE": "Estonia",
            "FI": "Finland", "FR": "France", "DE": "Germany", "IE": "Ireland",
            "IT": "Italy", "LV": "Latvia", "LT": "Lithuania", "NL": "the Netherlands",
            "NO": "Norway", "PL": "Poland", "PT": "Portugal", "ES": "Spain",
            "SE": "Sweden",
        }
        return names.get((code or "").upper(), code or "your country")
    
    def validate_manual_input(self, assets: list, liabilities: list, monthly_expenses: float, monthly_income: float) -> list:
        """Validate manually entered financial data.
        
        Returns a list of validation errors (empty if valid).
        """
        errors = []
        
        if monthly_expenses > monthly_income * 1.2:
            errors.append("Your monthly expenses exceed your monthly income. Please double-check your numbers.")
        
        if monthly_expenses < monthly_income * 0.1:
            errors.append("Your expenses seem unusually low compared to your income. Please verify.")
        
        total_assets = sum(a.value for a in assets)
        total_liabilities = sum(d.balance for d in liabilities)
        
        if total_liabilities > total_assets * 2 and total_assets > 0:
            errors.append("Your debt is more than twice your assets. Please review your entries.")
        
        # Check for duplicate account names
        names = [a.name for a in assets] + [d.name for d in liabilities]
        if len(names) != len(set(names)):
            errors.append("You have duplicate account names. Please use unique names for each account.")
        
        # Check for suspicious interest rates
        for debt in liabilities:
            if debt.interest_rate > 0.50:
                errors.append(f"The interest rate on {debt.name} seems very high ({debt.interest_rate:.0%}). Please verify.")
        
        return errors
    
    def to_profile(self, assets: list, liabilities: list, monthly_expenses: float, 
                   monthly_income: float, goals: list) -> UserProfile:
        """Convert manual input data into a UserProfile."""
        profile = self.user_profile
        profile.assets = assets
        profile.liabilities = liabilities
        profile.monthly_expenses = monthly_expenses
        profile.monthly_net_income = monthly_income
        profile.goals = goals
        return profile


# ─── Plaid Integration Stub ───
# The following would be implemented when Plaid credentials are configured.
# Requires: pip install plaid-python

class PlaidIntegration:
    """Stub for Plaid API integration.
    
    To activate:
    1. Sign up at https://plaid.com
    2. Install: pip install plaid-python
    3. Set environment variables: PLAID_CLIENT_ID, PLAID_SECRET, PLAID_ENV
    4. Implement the methods below.
    """
    
    def __init__(self, client_id: str, secret: str, environment: str = "sandbox"):
        self.client_id = client_id
        self.secret = secret
        self.environment = environment
        # self.client = plaid_api.PlaidApi(...)  # Uncomment when plaid-python is installed
    
    def create_link_token(self, user_id: str, country_codes: list) -> dict:
        """Create a Plaid Link token for the user."""
        raise NotImplementedError("Plaid integration not yet configured. Install plaid-python and set credentials.")
    
    def exchange_public_token(self, public_token: str) -> str:
        """Exchange a public token for an access token."""
        raise NotImplementedError("Plaid integration not yet configured.")
    
    def get_accounts(self, access_token: str) -> list:
        """Fetch connected accounts."""
        raise NotImplementedError("Plaid integration not yet configured.")
    
    def get_transactions(self, access_token: str, start_date: str, end_date: str) -> list:
        """Fetch transactions for analysis."""
        raise NotImplementedError("Plaid integration not yet configured.")
    
    def get_liabilities(self, access_token: str) -> dict:
        """Fetch credit cards, student loans, mortgages."""
        raise NotImplementedError("Plaid integration not yet configured.")
    
    def get_investments(self, access_token: str) -> dict:
        """Fetch investment holdings."""
        raise NotImplementedError("Plaid integration not yet configured.")
