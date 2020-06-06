from financials_loader import FinancialsLoader
import matplotlib.pyplot as plt

msft_fl = FinancialsLoader("MSFT")

msft_cashflow = msft_fl.load_cashflow()
# print(msft_fl.cashflow)

print(msft_cashflow.loc["Free cash flow"])

# plt.figure
# plt.plot(msft_cashflow["Fiscal year ends in June. USD in millions except per share data."], msft_fl.cashflow.loc["Free cash flow"]
# plt.show()