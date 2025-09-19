# URL Classifier 
import re
from typing import List, Dict


def classify_url(url: str) -> str:
    if re.match(r"^https?://huggingface\.co/datasets/", url):
        return "DATASET"
    elif re.match(r"^https?://huggingface\.co/", url):
        return "MODEL"
    elif re.match(r"^https?://github\.com/", url):
        return "CODE"
    elif url == "":
        return "EMPTY"
    else:
        return "UNKNOWN"


def parse_url_file(filepath: str) -> List[Dict[str, str]]:
    results = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line_result = {}
                urls = line.strip().split(',')
                for url in urls:
                    url = url.strip()
                    classification = classify_url(url)
                    line_result[url] = classification
                results.append(line_result)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    return results


if __name__ == "__main__":
    urls = parse_url_file("urls.txt")
    for entry in urls:
        print(entry)