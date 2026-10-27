# Account Connections: Plaid + Manual Input

WealthAgents keeps account connections simple: **Plaid for supported countries, manual entry for everything else.**

## Why This Approach

- **Single integration**: One provider to maintain, one contract, one API surface
- **Plaid covers the biggest markets**: US, Canada, UK, and major EU economies
- **Manual input is sufficient elsewhere**: Users in non-Plaid markets are used to typing numbers
- **No provider fragmentation**: No routing logic, no fallback chains, no normalization across schemas
- **Lower compliance surface**: One security audit, one data processing agreement

## Plaid Supported Countries

| Country | Code | Coverage Level |
|---------|------|----------------|
| **United States** | US | Full stack (Auth, Balance, Transactions, Identity, Investments, Liabilities) |
| **Canada** | CA | Full stack |
| **United Kingdom** | GB | Full stack |
| **France** | FR | Full stack |
| **Germany** | DE | Full stack |
| **Spain** | ES | Full stack |
| **Netherlands** | NL | Full stack |
| **Ireland** | IE | Full stack |
| **Italy** | IT | Transactions, Balance |
| **Belgium** | BE | Transactions, Balance |
| **Austria** | AT | Transactions, Balance |
| **Denmark** | DK | Transactions, Balance |
| **Finland** | FI | Transactions, Balance |
| **Sweden** | SE | Transactions, Balance |
| **Norway** | NO | Transactions, Balance |
| **Poland** | PL | Transactions, Balance |
| **Portugal** | PT | Transactions, Balance |
| **Estonia** | EE | Transactions, Balance |
| **Latvia** | LV | Transactions, Balance |
| **Lithuania** | LT | Transactions, Balance, Payments |

**Total: 20 countries**

## How It Works

```
User Location
    ├── Plaid Supported? ──YES──▶ Plaid Link ──▶ Auto-sync accounts
    │                                (checking, savings, credit cards,
    │                                 investments, loans, mortgages)
    │
    └── Plaid Supported? ──NO───▶ Manual Input Form
                                      (guided step-by-step entry)
```

### For Plaid-Supported Countries

1. User clicks "Connect Accounts"
2. Plaid Link modal opens
3. User selects their bank and authenticates
4. WealthAgents receives account balances, transactions, and liability data
5. Data auto-populates the `UserProfile` (assets, liabilities, monthly expenses)
6. Monthly refresh keeps data current

### For Non-Plaid Countries

1. User sees message: "We don't yet support automatic connections in your country. Please enter your details below."
2. Guided manual entry form walks through:
   - Cash and bank accounts
   - Investment accounts
   - Credit cards and loans
   - Monthly income and expenses
   - Financial goals
3. Validation ensures numbers add up (e.g., debt payments <= monthly expenses)
4. User can update anytime via settings

## Country Detection & Routing

```python
from wealthagents.connections import is_plaid_supported, get_connection_mode

# Auto-detect from user profile
country = user_profile.location_country  # "US", "GB", "JP", etc.

if is_plaid_supported(country):
    mode = "plaid_auto"      # Show Plaid Link button
else:
    mode = "manual_input"    # Show manual entry form

# Or check by country code directly
is_plaid_supported("US")   # True
is_plaid_supported("AU")   # False (Australia -> manual)
is_plaid_supported("BR")   # False (Brazil -> manual)
is_plaid_supported("JP")   # False (Japan -> manual)
```

## Manual Input UX Guidelines

The manual entry form should be:

1. **Smart defaults**: Pre-fill based on country (e.g., 401k for US, ISA for UK, Super for AU)
2. **Progressive disclosure**: Show sections one at a time (assets first, then liabilities, then goals)
3. **Inline validation**: Real-time checks (e.g., "Your monthly expenses exceed your income")
4. **Currency awareness**: Use the user's local currency symbol and formatting
5. **Templates**: Offer common account type templates by country
6. **Import helpers**: Allow CSV upload from bank statements or spreadsheet import

### Manual Input Template by Region

| Region | Common Account Types to Suggest |
|--------|--------------------------------|
| **US / Canada** | 401(k), IRA, Roth IRA, HSA, 529, TFSA (CA), RRSP (CA) |
| **UK** | ISA (Cash/Stocks), SIPP, LISA, Premium Bonds |
| **EU** | Pension accounts, Livret A (FR), Bausparvertrag (DE) |
| **Australia** | Superannuation, SMSF |
| **Japan** | NISA, iDeCo |
| **Global** | Checking, Savings, Brokerage, Credit Card, Mortgage, Student Loan, Auto Loan |

## Data Freshness

| Connection Type | Refresh Frequency | User Action |
|-----------------|-------------------|-------------|
| **Plaid auto** | Daily background sync | None (automatic) |
| **Plaid manual** | On-demand refresh | Click "Refresh" button |
| **Manual input** | User-driven updates | Edit profile anytime |

## Future: Expanding Beyond Plaid

If and when WealthAgents expands to markets where Plaid is not viable:

1. **Australia/NZ**: Add Basiq integration (CDR-compliant)
2. **Brazil**: Add Pluggy or Belvo (Open Finance Brasil)
3. **India**: Evaluate Yodlee or local aggregators
4. **Latin America**: Evaluate Belvo for MX/CO

The architecture is designed so adding a second provider is straightforward, but **Plaid remains the primary and only provider for the foreseeable future.**

## Implementation

See `wealthagents/connections.py` for the country check and `wealthagents/manual_input.py` for the guided form logic.
