"""Build deterministic synthetic research data, an executed notebook and a Bokeh report.
No market connection and no trading account. Run from repository root.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import nbformat as nb
from nbclient import NotebookClient
from backtesting import Backtest, Strategy
from bokeh.resources import INLINE

ROOT = Path(__file__).resolve().parents[1]
np.random.seed(42)
n = 720
close = 1.10 * np.exp(np.cumsum(np.random.normal(0, 0.0007, n)))
opening = np.r_[close[0], close[:-1]]
spread = np.random.uniform(.0001, .0008, n)
data = pd.DataFrame({'Open': opening, 'High': np.maximum(opening, close)+spread,
                     'Low': np.minimum(opening, close)-spread, 'Close': close,
                     'Volume': np.random.randint(100, 1500, n)},
                    index=pd.date_range('2025-01-01', periods=n, freq='h', tz='UTC'))
data.index.name = 'timestamp'
# These continuous bars deliberately DO NOT represent a real FX calendar.
data.to_csv(ROOT/'examples/synthetic_eurusd.csv')

class DemoBreakout(Strategy):
    def init(self):
        self.high10 = self.I(lambda x: pd.Series(x).shift(1).rolling(10).max(), self.data.High)
    def next(self):
        if self.position:
            if len(self.data) - self.entered >= 24:
                self.position.close()
        elif self.data.Close[-1] > self.high10[-1]:
            price = self.data.Close[-1]
            self.buy(size=500, sl=price-.002, tp=price+.004)
            self.entered = len(self.data)

bt = Backtest(data, DemoBreakout, cash=10000, commission=.0001, spread=.0001,
              margin=1, exclusive_orders=True, finalize_trades=True)
stats = bt.run()
bt.plot(results=stats, filename=str(ROOT/'docs/software/backtest-report.html'),
        open_browser=False, resample=False)
# Make report offline rather than relying on Bokeh's CDN.
# Backtesting uses output_file/save. Inline CDN resources by replacing their script tags.
report_path = ROOT/'docs/software/backtest-report.html'
report = report_path.read_text()
import re
report = re.sub(r'<script[^>]+src="https://cdn\.bokeh\.org/[^\"]+"[^>]*>\s*</script>', '', report)
report = report.replace('</head>', INLINE.render() + '</head>')
report = report.replace('<body>', '<body><div style="padding:12px;background:#fff3c4;font:16px sans-serif">SYNTHETIC TRAINING DATA — NOT LIVE EUR/USD — NOT A VALIDATED STRATEGY</div>')
report_path.write_text('\n'.join(line.rstrip() for line in report.splitlines()) + '\n')
stats['_trades'].to_csv(ROOT/'examples/synthetic_trades.csv', index=False)
summary = {k: str(stats[k]) for k in ['Start','End','Return [%]','Max. Drawdown [%]','# Trades','Win Rate [%]']}
(ROOT/'examples/synthetic_summary.json').write_text(json.dumps(summary, indent=2))

cells = []
def md(s): cells.append(nb.v4.new_markdown_cell(s))
def code(s): cells.append(nb.v4.new_code_cell(s))
md('# ATLAS Research Lab\n**Real JupyterLab notebook, synthetic training data. No broker connection.**\nThis notebook illustrates software workflow, not performance on historical EUR/USD.\nContinuous bars include weekends: NOT a valid FX calendar. No AI edge is demonstrated.')
code("import pandas as pd\nimport numpy as np\nfrom pathlib import Path\nROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\ndata = pd.read_csv(ROOT/'examples/synthetic_eurusd.csv', index_col=0, parse_dates=True)\nprint('SYNTHETIC DATA ONLY | NO LIVE ORDERS')\nprint('Rows:', len(data), '| Timezone:', data.index.tz)\ndata.head(8)")
md('## 1. Validate OHLC and timestamps\nReject duplicates, reversed ranges, missing values and non-monotonic timestamps. This sample does not validate a real trading calendar.')
code("checks = {\n 'unique_timestamps': data.index.is_unique,\n 'ordered_timestamps': data.index.is_monotonic_increasing,\n 'no_missing_values': not data.isna().any().any(),\n 'high_covers_body': bool((data.High >= data[['Open','Close']].max(axis=1)).all()),\n 'low_covers_body': bool((data.Low <= data[['Open','Close']].min(axis=1)).all())\n}\npd.Series(checks, name='Passed')")
md('## 2. Inspect a chart before calculating signals\nCandles and indicators are examples, not a live chart.')
code("import matplotlib.pyplot as plt\nplt.rcParams['figure.figsize'] = (11, 3.5)\nax = data.Close.plot(title='Synthetic hourly EUR/USD-shaped series')\ndata.Close.rolling(20).mean().plot(ax=ax, label='SMA 20')\nax.legend(['Synthetic close', 'SMA 20']); plt.show()")
md('## 3. Reject size that exceeds a risk budget\nAccount currency USD; units EUR; fixed per-unit execution-cost assumption. Not a broker lot calculator.')
code("equity, risk_fraction = 1000, 0.0025\nentry, stop, cost = 1.1000, 1.0980, 0.0002\nbudget = equity * risk_fraction\nunits = int(min(budget/(entry-stop+cost), equity/(entry+cost)))\npd.Series({'Budget USD': budget, 'Units EUR': units, 'Notional USD': units*entry,\n 'Estimated loss USD': units*(entry-stop+cost)})")
md('## 4. Extract an event; do not execute the text\nUntrusted social content has no permission to place orders or modify risk limits.')
code("event = {\n 'event_id': 'SYNTHETIC-001',\n 'source': 'training_example',\n 'published_at': '2026-11-09T10:00:00Z',\n 'received_at': '2026-11-09T10:00:08Z',\n 'verified': False,\n 'action': 'NO_TRADE',\n 'reason': 'No primary-source confirmation'\n}\npd.Series(event)")
md('## 5. Inspect simulated results, not a profit promise\nThe HTML report is generated by Backtesting.py / Bokeh on the synthetic sample. The demonstration rule is intentionally simpler than the complete proposed strategy.')
code("import json\nsummary = json.loads((ROOT/'examples/synthetic_summary.json').read_text())\npd.Series(summary, name='Synthetic demonstration only')")
md('## 6. Review the journal and next tests\nEntries are simulated. Costs are assumptions; gaps, swaps and real execution need separate validation.')
code("trades = pd.read_csv(ROOT/'examples/synthetic_trades.csv')\ntrades[['EntryTime','ExitTime','Size','EntryPrice','ExitPrice','PnL']].head(8)")
notebook = nb.v4.new_notebook(cells=cells, metadata={'kernelspec':{'display_name':'Python 3 (ipykernel)','language':'python','name':'python3'}})
NotebookClient(notebook, timeout=120, kernel_name='python3', resources={'metadata':{'path':str(ROOT)}}).execute()
nb.write(notebook, ROOT/'notebooks/01_research_lab.ipynb')
print('Generated synthetic data, executed notebook, and offline Backtesting.py report.')
