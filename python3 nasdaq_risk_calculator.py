#!/usr/bin/env python3
"""Nasdaq Futures Risk Calculator for a $50,000 evaluation account."""

from dataclasses import dataclass


ACCOUNT_START = 50_000.0
MAX_DRAWDOWN = 2_000.0
FAIL_LEVEL = 48_000.0
PROFIT_TARGET = 53_000.0
PROFIT_NEEDED = 3_000.0
DEFAULT_MAX_RISK = 200.0


@dataclass(frozen=True)
class ContractSpec:
    name: str
    dollar_per_point: float
    tick_size: float
    dollar_per_tick: float


CONTRACTS = {
    "MNQ": ContractSpec("MNQ", dollar_per_point=2.0, tick_size=0.25, dollar_per_tick=0.50),
    "NQ": ContractSpec("NQ", dollar_per_point=20.0, tick_size=0.25, dollar_per_tick=5.00),
}


def prompt_float(prompt: str, default: float | None = None) -> float:
    while True:
        suffix = f" [{default}]" if default is not None else ""
        raw = input(f"{prompt}{suffix}: ").strip()
        if raw == "" and default is not None:
            return float(default)
        try:
            return float(raw.replace(",", ""))
        except ValueError:
            print("Please enter a valid number.")


def prompt_choice(prompt: str, valid: tuple[str, ...]) -> str:
    valid_set = {v.upper() for v in valid}
    while True:
        raw = input(f"{prompt} ({'/'.join(valid)}): ").strip().upper()
        if raw in valid_set:
            return raw
        print(f"Please choose one of: {', '.join(valid)}")


def trade_directional_distance(side: str, entry: float, price: float) -> float:
    if side == "LONG":
        return price - entry
    return entry - price


def fmt_money(value: float) -> str:
    return f"${value:,.2f}"


def fmt_num(value: float) -> str:
    return f"{value:,.2f}"


def main() -> None:
    print("\nNasdaq Futures Risk Calculator")
    print("-" * 40)
    print(f"Starting balance: {fmt_money(ACCOUNT_START)}")
    print(f"Max drawdown:     {fmt_money(MAX_DRAWDOWN)}")
    print(f"Fail level:       {fmt_money(FAIL_LEVEL)}")
    print(f"Profit target:    {fmt_money(PROFIT_TARGET)}")
    print(f"Profit to pass:   {fmt_money(PROFIT_NEEDED)}")
    print("-" * 40)

    current_balance = prompt_float("Current account balance")
    contract_key = prompt_choice("Contract", ("MNQ", "NQ"))
    side = prompt_choice("Direction", ("LONG", "SHORT"))
    entry = prompt_float("Entry price")
    stop = prompt_float("Stop loss price")
    target = prompt_float("Target price")
    max_risk = prompt_float("Max dollar risk per trade", default=DEFAULT_MAX_RISK)

    contract = CONTRACTS[contract_key]
    drawdown_left = max(0.0, current_balance - FAIL_LEVEL)
    profit_left = max(0.0, PROFIT_TARGET - current_balance)

    stop_points_raw = trade_directional_distance(side, entry, stop)
    target_points_raw = trade_directional_distance(side, entry, target)

    stop_points = abs(stop_points_raw)
    target_points = abs(target_points_raw)
    stop_ticks = stop_points / contract.tick_size
    target_ticks = target_points / contract.tick_size

    risk_per_contract = stop_points * contract.dollar_per_point
    profit_per_contract = target_points * contract.dollar_per_point

    recommended_contracts = int(max_risk // risk_per_contract) if risk_per_contract > 0 else 0
    total_risk_at_recommended = recommended_contracts * risk_per_contract
    risk_pct_drawdown = (risk_per_contract / drawdown_left * 100.0) if drawdown_left > 0 else 0.0

    losses_to_fail = int(drawdown_left // risk_per_contract) if risk_per_contract > 0 else 0
    wins_to_target = int(profit_left // profit_per_contract) if profit_per_contract > 0 else 0
    if profit_per_contract > 0 and (profit_left % profit_per_contract) > 0:
        wins_to_target += 1

    warnings: list[str] = []
    if stop_points_raw >= 0:
        warnings.append("Stop appears to be on the wrong side of entry for the selected direction.")
    if target_points_raw <= 0:
        warnings.append("Target appears to be on the wrong side of entry for the selected direction.")
    if drawdown_left <= 0:
        warnings.append("Account is already at or below fail level.")
    if risk_per_contract <= 0:
        warnings.append("Risk per contract is zero; check entry/stop values.")

    if drawdown_left > 0 and risk_per_contract > 0:
        if risk_pct_drawdown >= 25:
            warnings.append("Single-contract risk is over 25% of remaining drawdown.")
        elif risk_pct_drawdown >= 15:
            warnings.append("Single-contract risk is over 15% of remaining drawdown.")
        elif risk_pct_drawdown >= 10:
            warnings.append("Single-contract risk is over 10% of remaining drawdown.")

        if (drawdown_left - risk_per_contract) <= (MAX_DRAWDOWN * 0.10):
            warnings.append("One losing trade could put the account very close to fail level.")

    print("\nResults")
    print("=" * 40)
    print(f"Current balance:                    {fmt_money(current_balance)}")
    print(f"Drawdown left before fail:          {fmt_money(drawdown_left)}")
    print(f"Profit left to target:              {fmt_money(profit_left)}")
    print(f"Contract:                           {contract.name}")
    print(f"Direction:                          {side}")
    print(f"Entry:                              {fmt_num(entry)}")
    print(f"Stop:                               {fmt_num(stop)}")
    print(f"Target:                             {fmt_num(target)}")
    print("-" * 40)
    print(f"Stop distance:                      {fmt_num(stop_points)} points ({fmt_num(stop_ticks)} ticks)")
    print(f"Target distance:                    {fmt_num(target_points)} points ({fmt_num(target_ticks)} ticks)")
    print(f"Risk per contract:                  {fmt_money(risk_per_contract)}")
    print(f"Profit per contract:                {fmt_money(profit_per_contract)}")
    print(f"Max risk per trade:                 {fmt_money(max_risk)}")
    print(f"Recommended contracts:              {recommended_contracts}")
    print(f"Risk at recommended contracts:      {fmt_money(total_risk_at_recommended)}")
    print("-" * 40)
    print(f"Similar losses to fail account:     {losses_to_fail}")
    print(f"Similar wins to hit target:         {wins_to_target}")

    print("\nWarnings")
    print("=" * 40)
    if warnings:
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("- None")


if __name__ == "__main__":
    main()
