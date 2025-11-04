import os
import sys
import json
import requests
from requests.exceptions import RequestException

API_KEY = os.environ.get("ANALYTICS_API_KEY")
BASE_URL = os.environ.get("ALTVERSE_API_URL")

PERIODIC_JOBS = [
    {"period_type": "daily", "limit": 30},
    {"period_type": "weekly", "limit": 54},
    {"period_type": "monthly", "limit": 24},
]


def make_request(session, url, query_payload):
    """
    Helper function to make a POST request to the analytics endpoint.
    """
    try:
        response = session.post(url, json=query_payload)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        # Return the JSON data
        return response.json()

    except RequestException as e:
        print(
            f"Error for query '{query_payload.get('queryType')}': {e}", file=sys.stderr
        )
        if hasattr(e, "response") and e.response is not None:
            try:
                # Try to print the error message from the API
                print(f"API Error: {e.response.json()}", file=sys.stderr)
            except json.JSONDecodeError:
                print(f"API Error: {e.response.text}", file=sys.stderr)
        return {"error": str(e)}


def fetch_all_analytics():
    """
    Main function to fetch all metrics and save them to a JSON file.
    """
    if not API_KEY or not BASE_URL:
        print(
            "Error: ANALYTICS_API_KEY and ALTVERSE_API_URL environment variables must be set.",
            file=sys.stderr,
        )
        sys.exit(1)

    analytics_endpoint = f"{BASE_URL.rstrip('/')}/analytics"

    headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}

    # This dictionary will hold ALL collected data
    all_metrics = {}

    with requests.Session() as session:
        session.headers.update(headers)

        print(f"Hitting endpoint: {analytics_endpoint}\n")

        # These are run only once.
        print("--- Fetching All-Time (Total) Stats ---")

        total_queries_to_run = [
            ("total_users", {"queryType": "total_users"}),
            ("total_activity_stats", {"queryType": "total_activity_stats"}),
            ("total_swap_stats", {"queryType": "total_swap_stats"}),
            ("total_lending_stats", {"queryType": "total_lending_stats"}),
            ("total_earn_stats", {"queryType": "total_earn_stats"}),
        ]

        for name, payload in total_queries_to_run:
            print(f"Fetching {name}...")
            all_metrics[name] = make_request(session, analytics_endpoint, payload)

        all_metrics["periodic_stats"] = {}

        for job in PERIODIC_JOBS:
            period_type = job["period_type"]
            limit = job["limit"]

            print(f"\n--- Fetching {period_type.upper()} stats (limit={limit}) ---")

            current_period_results = {}

            # Define all periodic query types
            periodic_query_types = [
                "periodic_user_stats",
                "periodic_activity_stats",
                "periodic_swap_stats",
                "periodic_lending_stats",
                "periodic_earn_stats",
            ]

            for query_type in periodic_query_types:
                payload = {
                    "queryType": query_type,
                    "period_type": period_type,
                    "limit": limit,
                }
                print(f"Fetching {query_type}...")
                current_period_results[query_type] = make_request(
                    session, analytics_endpoint, payload
                )

            # Store all results for this period_type
            all_metrics["periodic_stats"][period_type] = current_period_results

    output_filename = "analytics.json"
    try:
        with open(output_filename, "w") as f:
            json.dump(all_metrics, f, indent=2)
        print(f"\nSuccess! All metrics saved to {output_filename}")

    except IOError as e:
        print(
            f"\nError: Could not write to file {output_filename}: {e}",
            file=sys.stderr,
        )


if __name__ == "__main__":
    fetch_all_analytics()
