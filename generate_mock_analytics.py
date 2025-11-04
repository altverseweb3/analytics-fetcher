#!/usr/bin/env python3
"""
Generate realistic dummy analytics data for dApp analytics.
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Configuration
DAYS_BACK = 30
CHAINS = ["Ethereum", "Polygon", "Arbitrum", "Solana", "Optimism", "Base"]
PROTOCOLS = {
    "swap": ["Uniswap", "SushiSwap", "Curve", "Balancer", "0x"],
    "lending": ["AaveV3", "CompoundV3", "MorphoBlue"],
    "earn": ["etherFi", "Lido", "MakerDAO", "Yearn"],
}
MARKETS = {
    "Polygon": ["AaveV3Polygon", "CompoundPolygon"],
    "Ethereum": ["AaveV3Ethereum", "CompoundEthereum"],
    "Arbitrum": ["AaveV3Arbitrum", "CompoundArbitrum"],
    "Solana": ["SolendSolana"],
    "Optimism": ["AaveV3Optimism"],
}


def generate_daily_user_stats(days: int) -> List[Dict[str, Any]]:
    """Generate daily user statistics with realistic patterns."""
    data = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        day_of_week = (datetime.now() - timedelta(days=i)).weekday()
        weekend_factor = 0.6 if day_of_week >= 5 else 1.0

        new_users = max(0, int(random.randint(2, 8) * weekend_factor))
        active_users = max(new_users, int(random.randint(5, 25) * weekend_factor))

        data.append(
            {
                "period_start": date,
                "new_users": new_users,
                "active_users": active_users,
            }
        )
    return data


def generate_daily_activity_stats(days: int) -> List[Dict[str, Any]]:
    """Generate daily activity statistics."""
    data = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        day_of_week = (datetime.now() - timedelta(days=i)).weekday()
        weekend_factor = 0.7 if day_of_week >= 5 else 1.0

        swaps = max(0, int(random.randint(5, 30) * weekend_factor))
        lending = max(0, int(random.randint(1, 10) * weekend_factor))
        earn = max(0, int(random.randint(2, 15) * weekend_factor))
        total_tx = swaps + lending + earn
        active_users = max(1, int(random.randint(3, 15) * weekend_factor))

        data.append(
            {
                "period_start": date,
                "total_transactions": total_tx,
                "swap_count": swaps,
                "lending_count": lending,
                "earn_count": earn,
                "dapp_entrances": random.randint(20, 100),
                "active_users": active_users,
                "transactions_per_active_user": (
                    total_tx // active_users if active_users > 0 else 0
                ),
            }
        )
    return data


def generate_daily_swap_stats(days: int) -> List[Dict[str, Any]]:
    """Generate daily swap statistics."""
    data = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        day_of_week = (datetime.now() - timedelta(days=i)).weekday()
        weekend_factor = 0.7 if day_of_week >= 5 else 1.0

        total_swaps = max(0, int(random.randint(5, 30) * weekend_factor))
        routes = generate_swap_routes(total_swaps)

        cross_chain = 0
        same_chain = 0
        for route, count in routes.items():
            chain1, chain2 = route.split(",")
            if chain1 == chain2:
                same_chain += count
            else:
                cross_chain += count

        data.append(
            {
                "period_start": date,
                "total_swap_count": total_swaps,
                "swap_routes": routes,
                "cross_chain_count": cross_chain,
                "same_chain_count": same_chain,
            }
        )
    return data


def generate_daily_lending_stats(days: int) -> List[Dict[str, Any]]:
    """Generate daily lending statistics."""
    data = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        day_of_week = (datetime.now() - timedelta(days=i)).weekday()
        weekend_factor = 0.7 if day_of_week >= 5 else 1.0

        has_lending = random.random() > 0.5
        if has_lending:
            total_lending = max(1, int(random.randint(1, 10) * weekend_factor))
            breakdown = generate_lending_breakdown(total_lending)
        else:
            total_lending = 0
            breakdown = []

        data.append(
            {
                "period_start": date,
                "total_lending_count": total_lending,
                "breakdown": breakdown,
            }
        )
    return data


def generate_daily_earn_stats(days: int) -> List[Dict[str, Any]]:
    """Generate daily earn statistics."""
    data = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        day_of_week = (datetime.now() - timedelta(days=i)).weekday()
        weekend_factor = 0.7 if day_of_week >= 5 else 1.0

        has_earn = random.random() > 0.5
        if has_earn:
            total_earn = max(1, int(random.randint(2, 15) * weekend_factor))
            by_chain = {
                chain: random.randint(1, 5)
                for chain in random.sample(CHAINS, k=min(3, len(CHAINS)))
            }
            by_protocol = {
                protocol: random.randint(1, 5)
                for protocol in random.sample(
                    PROTOCOLS["earn"], k=min(2, len(PROTOCOLS["earn"]))
                )
            }
            by_chain_protocol = {
                f"{chain}#{protocol}": random.randint(1, 3)
                for chain in random.sample(CHAINS, k=1)
                for protocol in random.sample(PROTOCOLS["earn"], k=1)
            }
        else:
            total_earn = 0
            by_chain = {}
            by_protocol = {}
            by_chain_protocol = {}

        data.append(
            {
                "period_start": date,
                "total_earn_count": total_earn,
                "by_chain": by_chain,
                "by_protocol": by_protocol,
                "by_chain_protocol": by_chain_protocol,
            }
        )
    return data


def generate_swap_routes(count: int) -> Dict[str, int]:
    """Generate realistic swap routes, including same-chain."""
    if count == 0:
        return {}
    routes = {}
    for _ in range(count):
        # ~30% chance of same-chain swap
        if random.random() < 0.3:
            chain = random.choice(CHAINS)
            chain1, chain2 = chain, chain
        else:
            chain1, chain2 = random.sample(CHAINS, 2)
        route = f"{chain1.lower()},{chain2.lower()}"
        routes[route] = routes.get(route, 0) + 1
    return routes


def generate_lending_breakdown(count: int = None) -> List[Dict[str, Any]]:
    """Generate lending activity breakdown by chain and market."""
    if count is None:
        count = random.randint(1, 5)

    breakdown = []
    available_chains = [c for c in CHAINS if c in MARKETS]

    for _ in range(count):
        chain = random.choice(available_chains)
        market = random.choice(MARKETS[chain])
        breakdown.append(
            {
                "chain": chain,
                "market": market,
                "count": random.randint(1, 5),
            }
        )
    return breakdown


def generate_periodic_stats(period_type: str, days: int) -> Dict[str, Any]:
    """Generate periodic statistics for a given period type."""
    if period_type == "daily":
        user_stats = generate_daily_user_stats(days)
        activity_stats = generate_daily_activity_stats(days)
        swap_stats = generate_daily_swap_stats(days)
        lending_stats = generate_daily_lending_stats(days)
        earn_stats = generate_daily_earn_stats(days)

    elif period_type == "weekly":
        weeks = 54
        user_stats = []
        activity_stats = []
        swap_data = []
        lending_data = []
        earn_data = []

        for i in range(weeks):
            current_date = datetime.now()
            days_since_monday = current_date.weekday()
            monday = current_date - timedelta(days=days_since_monday)
            period_date = monday - timedelta(weeks=i)
            period_str = period_date.strftime("%Y-%m-%d")

            # Aggregate daily stats for this week
            new_users = sum(random.randint(2, 8) for _ in range(7))
            active_users = sum(random.randint(5, 25) for _ in range(7))

            user_stats.append(
                {
                    "period_start": period_str,
                    "new_users": new_users,
                    "active_users": active_users,
                }
            )

            swaps = sum(random.randint(5, 30) for _ in range(7))
            lending = sum(random.randint(1, 10) for _ in range(7))
            earn = sum(random.randint(2, 15) for _ in range(7))
            total_tx = swaps + lending + earn
            active_u = max(1, active_users)

            activity_stats.append(
                {
                    "period_start": period_str,
                    "total_transactions": total_tx,
                    "swap_count": swaps,
                    "lending_count": lending,
                    "earn_count": earn,
                    "dapp_entrances": random.randint(140, 700),
                    "active_users": active_u,
                    "transactions_per_active_user": total_tx // active_u,
                }
            )

            swap_routes = generate_swap_routes(swaps)
            cross_chain = 0
            same_chain = 0
            for route, count in swap_routes.items():
                chain1, chain2 = route.split(",")
                if chain1 == chain2:
                    same_chain += count
                else:
                    cross_chain += count
            swap_data.append(
                {
                    "period_start": period_str,
                    "total_swap_count": swaps,
                    "swap_routes": swap_routes,
                    "cross_chain_count": cross_chain,
                    "same_chain_count": same_chain,
                }
            )

            lending_data.append(
                {
                    "period_start": period_str,
                    "total_lending_count": lending,
                    "breakdown": (
                        generate_lending_breakdown(min(3, lending))
                        if lending > 0
                        else []
                    ),
                }
            )

            by_chain = (
                {
                    chain: random.randint(1, 10)
                    for chain in random.sample(CHAINS, k=min(3, len(CHAINS)))
                }
                if earn > 0
                else {}
            )
            by_protocol = (
                {
                    protocol: random.randint(1, 10)
                    for protocol in random.sample(
                        PROTOCOLS["earn"], k=min(2, len(PROTOCOLS["earn"]))
                    )
                }
                if earn > 0
                else {}
            )
            by_chain_protocol = (
                {
                    f"{chain}#{protocol}": random.randint(1, 5)
                    for chain in random.sample(CHAINS, k=1)
                    for protocol in random.sample(PROTOCOLS["earn"], k=1)
                }
                if earn > 0
                else {}
            )

            earn_data.append(
                {
                    "period_start": period_str,
                    "total_earn_count": earn,
                    "by_chain": by_chain,
                    "by_protocol": by_protocol,
                    "by_chain_protocol": by_chain_protocol,
                }
            )

        swap_stats = swap_data
        lending_stats = lending_data
        earn_stats = earn_data

    else:  # monthly
        months = 24
        user_stats = []
        activity_stats = []
        swap_data = []
        lending_data = []
        earn_data = []

        current_month = datetime.now().replace(day=1)

        for i in range(months):
            if i == 0:
                period_date = current_month
            else:
                # Go back to previous month
                period_date = (
                    current_month.replace(day=1) - timedelta(days=i * 30)
                ).replace(day=1)

            period_str = period_date.strftime("%Y-%m-%d")

            new_users = sum(random.randint(2, 8) for _ in range(30))
            active_users = sum(random.randint(5, 25) for _ in range(30))

            user_stats.append(
                {
                    "period_start": period_str,
                    "new_users": new_users,
                    "active_users": active_users,
                }
            )

            swaps = sum(random.randint(5, 30) for _ in range(30))
            lending = sum(random.randint(1, 10) for _ in range(30))
            earn = sum(random.randint(2, 15) for _ in range(30))
            total_tx = swaps + lending + earn
            active_u = max(1, active_users)

            activity_stats.append(
                {
                    "period_start": period_str,
                    "total_transactions": total_tx,
                    "swap_count": swaps,
                    "lending_count": lending,
                    "earn_count": earn,
                    "dapp_entrances": random.randint(600, 3000),
                    "active_users": active_u,
                    "transactions_per_active_user": total_tx // active_u,
                }
            )

            swap_routes = generate_swap_routes(swaps)
            cross_chain = 0
            same_chain = 0
            for route, count in swap_routes.items():
                chain1, chain2 = route.split(",")
                if chain1 == chain2:
                    same_chain += count
                else:
                    cross_chain += count
            swap_data.append(
                {
                    "period_start": period_str,
                    "total_swap_count": swaps,
                    "swap_routes": swap_routes,
                    "cross_chain_count": cross_chain,
                    "same_chain_count": same_chain,
                }
            )

            lending_data.append(
                {
                    "period_start": period_str,
                    "total_lending_count": lending,
                    "breakdown": (
                        generate_lending_breakdown(min(5, lending))
                        if lending > 0
                        else []
                    ),
                }
            )

            by_chain = (
                {
                    chain: random.randint(5, 20)
                    for chain in random.sample(CHAINS, k=min(4, len(CHAINS)))
                }
                if earn > 0
                else {}
            )
            by_protocol = (
                {
                    protocol: random.randint(5, 20)
                    for protocol in random.sample(
                        PROTOCOLS["earn"], k=min(3, len(PROTOCOLS["earn"]))
                    )
                }
                if earn > 0
                else {}
            )
            by_chain_protocol = (
                {
                    f"{chain}#{protocol}": random.randint(2, 10)
                    for chain in random.sample(CHAINS, k=2)
                    for protocol in random.sample(PROTOCOLS["earn"], k=1)
                }
                if earn > 0
                else {}
            )

            earn_data.append(
                {
                    "period_start": period_str,
                    "total_earn_count": earn,
                    "by_chain": by_chain,
                    "by_protocol": by_protocol,
                    "by_chain_protocol": by_chain_protocol,
                }
            )

        swap_stats = swap_data
        lending_stats = lending_data
        earn_stats = earn_data

    return {
        "periodic_user_stats": user_stats,
        "periodic_activity_stats": activity_stats,
        "periodic_swap_stats": swap_stats,
        "periodic_lending_stats": lending_stats,
        "periodic_earn_stats": earn_stats,
    }


def generate_analytics_data(days: int = DAYS_BACK) -> Dict[str, Any]:
    """Generate complete analytics data structure."""

    # Calculate totals from daily data
    daily_user_stats = generate_daily_user_stats(days)
    daily_activity_stats = generate_daily_activity_stats(days)
    daily_swap_stats = generate_daily_swap_stats(days)
    daily_lending_stats = generate_daily_lending_stats(days)

    total_users = sum(d["new_users"] for d in daily_user_stats)
    total_swaps = sum(d["total_swap_count"] for d in daily_swap_stats)
    total_lending = sum(d["total_lending_count"] for d in daily_lending_stats)
    total_earn = sum(d["earn_count"] for d in daily_activity_stats)
    total_transactions = sum(d["total_transactions"] for d in daily_activity_stats)
    total_entrances = sum(d["dapp_entrances"] for d in daily_activity_stats)

    # Generate swap routes for totals
    swap_routes = {}
    for day_stats in daily_swap_stats:
        for route, count in day_stats["swap_routes"].items():
            swap_routes[route] = swap_routes.get(route, 0) + count

    cross_chain_total = 0
    same_chain_total = 0
    for route, count in swap_routes.items():
        chain1, chain2 = route.split(",")
        if chain1 == chain2:
            same_chain_total += count
        else:
            cross_chain_total += count

    # Generate lending breakdown for totals
    all_lending_breakdowns = []
    for day_stats in daily_lending_stats:
        all_lending_breakdowns.extend(day_stats["breakdown"])

    # Aggregate lending by chain and market
    lending_breakdown = {}
    for item in all_lending_breakdowns:
        key = (item["chain"], item["market"])
        if key not in lending_breakdown:
            lending_breakdown[key] = {
                "chain": item["chain"],
                "market": item["market"],
                "count": 0,
            }
        lending_breakdown[key]["count"] += item["count"]

    return {
        "total_users": {"total_users": total_users},
        "total_activity_stats": {
            "total_transactions": total_transactions,
            "swap_count": total_swaps,
            "lending_count": total_lending,
            "earn_count": total_earn,
            "dapp_entrances": total_entrances,
            "total_users": total_users,
        },
        "total_swap_stats": {
            "total_swap_count": total_swaps,
            "swap_routes": swap_routes,
            "cross_chain_count": cross_chain_total,
            "same_chain_count": same_chain_total,
        },
        "total_lending_stats": {
            "total_lending_count": total_lending,
            "breakdown": list(lending_breakdown.values()),
        },
        "total_earn_stats": {
            "total_earn_count": total_earn,
            "by_chain": {
                chain: random.randint(10, 50)
                for chain in random.sample(CHAINS, k=min(4, len(CHAINS)))
            },
            "by_protocol": {
                protocol: random.randint(10, 50)
                for protocol in random.sample(
                    PROTOCOLS["earn"], k=min(3, len(PROTOCOLS["earn"]))
                )
            },
            "by_chain_protocol": {
                f"{chain}#{protocol}": random.randint(5, 20)
                for chain in random.sample(CHAINS, k=2)
                for protocol in random.sample(PROTOCOLS["earn"], k=1)
            },
        },
        "periodic_stats": {
            "daily": generate_periodic_stats("daily", days),
            "weekly": generate_periodic_stats("weekly", days),
            "monthly": generate_periodic_stats("monthly", days),
        },
    }


def main():
    """Main entry point."""
    analytics_data = generate_analytics_data()

    # Write to file
    output_file = "mock_analytics.json"
    with open(output_file, "w") as f:
        json.dump(analytics_data, f, indent=2)

    print(f"✓ Generated realistic analytics data: {output_file}")
    print(f"  - {DAYS_BACK} days of data")
    print(f"  - Total users: {analytics_data['total_users']['total_users']}")
    print(
        f"  - Total transactions: {analytics_data['total_activity_stats']['total_transactions']}"
    )


if __name__ == "__main__":
    main()
