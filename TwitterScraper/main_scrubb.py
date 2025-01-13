import json

from runner import run_spiders_async
from Tweeter  import Tweeter


def save_results_to_json(results, output_file):
    """
    Save the results to a JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

def on_success(results):
    """
    Callback for a successful spider run.
    """
    if results:
        print(f"Spider returned {len(results)} items.")
        output_file = "results.json"
        save_results_to_json(results, output_file)
        print(f"Results saved to {output_file}")
    else:
        print("No results were scraped.")

def on_failure(failure):
    """
    Callback for handling errors during spider runs.
    """

    print("All spiders failed.")
    print(failure)

if __name__ == "__main__":
    spiders_config = [
        {
            "class": Tweeter,
            "settings": {
                "DOWNLOAD_DELAY": 3.0,
                "CONCURRENT_REQUESTS": 1,
            },
            "kwargs": {
                "keyword": "Trump",
                "since": "2025-01-01",
                "until": "2025-01-05"

            },
        },
        {
            "class": Tweeter,
            "settings": {
                "DOWNLOAD_DELAY": 5.0,
                "CONCURRENT_REQUESTS": 1,
            },
            "kwargs": {
                "keyword": "Biden",
                "since": "2025-01-06",
                "until": "2025-01-09"
            },
        },

    ]

    # Run spiders and handle the result
    run_spiders_async(spiders_config, callback=on_success, errback=on_failure)
