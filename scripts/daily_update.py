"""Rewrite the DAILY-UPDATE block of README.md with a quote, concept and tip of the day.

Selection is deterministic by date, so re-running on the same day gives the same output.
"""

from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"
START = "<!-- DAILY-UPDATE:START -->"
END = "<!-- DAILY-UPDATE:END -->"

QUOTES = [
    ("Risk comes from not knowing what you're doing.", "Warren Buffett"),
    ("In the short run, the market is a voting machine but in the long run, it is a weighing machine.", "Benjamin Graham"),
    ("The four most dangerous words in investing are: 'this time it's different.'", "Sir John Templeton"),
    ("All models are wrong, but some are useful.", "George E. P. Box"),
    ("Diversification is the only free lunch in finance.", "Harry Markowitz (attributed)"),
    ("The market can remain irrational longer than you can remain solvent.", "John Maynard Keynes (attributed)"),
    ("In God we trust. All others must bring data.", "W. Edwards Deming (attributed)"),
    ("Know what you own, and know why you own it.", "Peter Lynch"),
    ("The stock market is filled with individuals who know the price of everything, but the value of nothing.", "Philip Fisher"),
    ("It's not whether you're right or wrong, but how much money you make when you're right and how much you lose when you're wrong.", "George Soros"),
    ("The individual investor should act consistently as an investor and not as a speculator.", "Benjamin Graham"),
    ("Price is what you pay. Value is what you get.", "Warren Buffett"),
]

CONCEPTS = [
    ("Sharpe Ratio", "excess return per unit of total volatility; the default yardstick for risk-adjusted performance."),
    ("Sortino Ratio", "like Sharpe, but penalizes only downside volatility."),
    ("Value at Risk (VaR)", "the loss threshold not exceeded with a given confidence over a given horizon."),
    ("Expected Shortfall (CVaR)", "the average loss in the tail beyond VaR; coherent, unlike VaR."),
    ("GARCH(1,1)", "models volatility clustering: today's variance depends on yesterday's shock and yesterday's variance."),
    ("Hierarchical Risk Parity", "clusters assets by correlation and allocates risk top-down, avoiding the covariance inversion that makes Markowitz unstable."),
    ("Kelly Criterion", "the bet size that maximizes long-run log wealth; most practitioners use a fraction of it."),
    ("Maximum Drawdown", "the largest peak-to-trough loss; the number investors actually feel."),
    ("Beta", "sensitivity of an asset's returns to the market's returns."),
    ("Modified Duration", "approximate % price change of a bond for a 1% change in yield."),
    ("Convexity", "the curvature of the price-yield relationship; second-order correction to duration."),
    ("Nelson-Siegel-Svensson", "a parametric yield-curve model with level, slope and two curvature factors."),
    ("Implied Volatility", "the volatility that makes an option-pricing model match the market price."),
    ("Volatility Risk Premium", "implied volatility tends to exceed realized volatility; option sellers are paid for bearing it."),
    ("Cointegration", "a stationary linear combination of non-stationary series; the basis of pairs trading."),
    ("Mean Reversion", "the tendency of a series to drift back toward a long-run average."),
    ("Risk Parity", "weights assets so each contributes equally to total portfolio risk."),
    ("Information Ratio", "active return over tracking error; Sharpe for benchmark-relative managers."),
    ("Ledoit-Wolf Shrinkage", "pulls the sample covariance matrix toward a structured target to cut estimation error."),
    ("Walk-Forward Analysis", "re-fit on a rolling window, test on the next unseen slice; repeat."),
]

TIPS = [
    "Always backtest out-of-sample. In-sample Sharpe ratios lie.",
    "Include transaction costs and slippage before you trust any backtest.",
    "Beware look-ahead bias: only use data that was available at decision time.",
    "Survivorship bias inflates returns. Include delisted assets.",
    "Log returns add over time; simple returns add across assets.",
    "Annualize volatility with sqrt(252) for daily data, not 252.",
    "Shrink your covariance matrix before optimizing.",
    "If a strategy only works with one parameter set, it doesn't work.",
    "Version your data, not just your code.",
    "Plot the equity curve. Summary stats hide regime changes.",
    "Set a random seed so your simulations are reproducible.",
    "Correlations go to one in a crisis. Stress-test for it.",
]


def progress_bar(fraction: float, width: int = 20) -> str:
    filled = round(fraction * width)
    return "▓" * filled + "░" * (width - filled)


def build_block(now: dt.datetime) -> str:
    day = now.timetuple().tm_yday
    start = dt.datetime(now.year, 1, 1, tzinfo=dt.timezone.utc)
    end = dt.datetime(now.year + 1, 1, 1, tzinfo=dt.timezone.utc)
    frac = (now - start) / (end - start)

    quote, author = QUOTES[day % len(QUOTES)]
    concept, definition = CONCEPTS[day % len(CONCEPTS)]
    tip = TIPS[day % len(TIPS)]

    return f"""{START}
### Daily Dose of Quant 📈

<div align="center">

> *"{quote}"*
> — **{author}**

</div>

| | |
|---|---|
| **Year Progress** | `{progress_bar(frac)}` {frac * 100:.1f}% of {now.year} |
| **Concept of the Day** | **{concept}** — {definition} |
| **Today's Tip** | {tip} |
| **Last Updated** | {now.strftime('%B %d, %Y %H:%M')} UTC |
{END}"""


def main() -> None:
    text = README.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if not pattern.search(text):
        raise SystemExit("DAILY-UPDATE markers not found in README.md")
    new_block = build_block(dt.datetime.now(dt.timezone.utc))
    README.write_text(pattern.sub(lambda _: new_block, text), encoding="utf-8")


if __name__ == "__main__":
    main()
