# Nasdaq Futures Risk Calculator

A simple command-line Python tool for calculating trade risk on Nasdaq futures for a **$50,000 evaluation account**. The script is designed around a $2,000 max drawdown, a $48,000 fail level, and a $53,000 profit target.

## What It Does

This calculator helps you estimate risk before placing a trade. It supports both **Micro Nasdaq futures (MNQ)** and **E-mini Nasdaq futures (NQ)**.

The script calculates:

- Remaining drawdown before failing the account
- Profit still needed to reach the target
- Stop distance in points and ticks
- Target distance in points and ticks
- Risk per contract
- Profit per contract
- Recommended contract size based on your max risk
- Number of similar losses before reaching the fail level
- Number of similar wins needed to hit the profit target
- Warnings when risk is too high or trade levels appear incorrect

## Account Settings

The script uses these default evaluation account settings:

| Setting | Value |
|---|---:|
| Starting balance | `$50,000` |
| Max drawdown | `$2,000` |
| Fail level | `$48,000` |
| Profit target | `$53,000` |
| Profit needed | `$3,000` |
| Default max risk per trade | `$200` |

## Supported Contracts

| Contract | Dollars Per Point | Tick Size | Dollars Per Tick |
|---|---:|---:|---:|
| MNQ | `$2.00` | `0.25` | `$0.50` |
| NQ | `$20.00` | `0.25` | `$5.00` |

## Requirements

- Python 3.10 or newer
- No external packages required

The script only uses Python’s built-in `dataclasses` module.

## How to Run

1. Save the script as:

```bash
nasdaq_risk_calculator.py
```

2. Run it from your terminal:

```bash
python3 nasdaq_risk_calculator.py
```

On Windows, you may need to use:

```bash
python nasdaq_risk_calculator.py
```

## Inputs

When you run the script, it will ask for:

| Input | Description |
|---|---|
| Current account balance | Your current evaluation account balance |
| Contract | Choose `MNQ` or `NQ` |
| Direction | Choose `LONG` or `SHORT` |
| Entry price | Your planned entry price |
| Stop loss price | Your planned stop price |
| Target price | Your planned take-profit price |
| Max dollar risk per trade | Your max risk for the trade, default is `$200` |

## Example

Example inputs:

```text
Current account balance: 50000
Contract (MNQ/NQ): MNQ
Direction (LONG/SHORT): LONG
Entry price: 18500
Stop loss price: 18480
Target price: 18560
Max dollar risk per trade [200.0]: 200
```

Example meaning:

- You are trading MNQ.
- You are taking a long trade.
- Your entry is `18,500`.
- Your stop is `18,480`, which is `20` points of risk.
- MNQ is worth `$2` per point, so one contract risks `$40`.
- With a `$200` max risk, the calculator may recommend up to `5` contracts.

## Warnings

The script will show warnings when:

- The stop appears to be on the wrong side of the entry
- The target appears to be on the wrong side of the entry
- The account is already at or below the fail level
- Risk per contract is zero
- One contract risks too much of the remaining drawdown
- One losing trade could put the account close to the fail level

## Notes

This tool is for planning and risk awareness only. It does not place trades, connect to a broker, or guarantee passing an evaluation account. Always verify your account rules with your prop firm or broker before trading.

## File Structure

```text
nasdaq_risk_calculator.py   # Main calculator script
README.md                   # Project documentation
```

