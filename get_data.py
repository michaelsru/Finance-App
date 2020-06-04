from financials_loader import FinancialsLoader

msft_fl = FinancialsLoader("MSFT")

msft_fl.load_balance_sheet()
print(msft_fl.balance_sheet)

msft_fl.load_cashflow()
print(msft_fl.cashflow)

msft_fl.load_income_statement()
print(msft_fl.income_statement)

msft_fl.load_key_ratios()
print(msft_fl.key_ratios)
