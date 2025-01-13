import json
from runner import run_spiders_async
from Tweeter import Tweeter
from twisted.internet import reactor
class Scrubber():
    def __init__(self):
        pass

    def save_results_to_json(self, results, output_file):

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

    def main(self, keyword):
        spiders_config = [
            {
                "class": Tweeter,
                "settings": {
                    "DOWNLOAD_DELAY": 3.0,
                    "CONCURRENT_REQUESTS": 1,
                },
                "kwargs": {
                    "keyword": keyword,
                },
            },
            {
                "class": Tweeter,
                "settings": {
                    "DOWNLOAD_DELAY": 5.0,
                    "CONCURRENT_REQUESTS": 1,
                },
                "kwargs": {
                    "keyword": keyword,
                },
            },
        ]

        # Run spiders and get the result
        results = run_spiders_async(spiders_config)

        if isinstance(results, list) and results:
            print(f"Spider returned {len(results)} items.")
            output_file = "results.json"
            self.save_results_to_json(results, output_file)
            print(f"Results saved to {output_file}")
            return results
        else:
            print("All spiders failed or no results were scraped.")


