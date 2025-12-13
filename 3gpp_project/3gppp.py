import os
import glob
import yaml
import json
import logging
import requests
import datetime
from pythonjsonlogger import jsonlogger


class APIResponseError(Exception):
    def __init__(self, message, status_code, payload=None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload


def setup_logging():
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.INFO)

    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(message)s %(exception_code)s'
    )

    file_handler = logging.FileHandler('project.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger

logger = setup_logging()


class RobustClient:
    def fetch_spec(self, url):
        try:
            response = requests.get(url, timeout=10)
            if 400 <= response.status_code < 600:
                raise APIResponseError(
                    "HTTP Error",
                    response.status_code,
                    response.text
                )
            return response.text
        except requests.RequestException as e:
            logger.error(
                "Network failure",
                extra={"exception_code": "NETWORK_ERROR"}
            )
            return None

def analyze_apis():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    specs_dir = os.path.join(base_dir, "specs")
    files = glob.glob(os.path.join(specs_dir, "*.yaml"))

    if not files:
        logger.error(
            "No YAML files found",
            extra={"exception_code": "NO_FILES"}
        )
        return

    stats = {
        "total_endpoints": 0,
        "methods": {},
        "auth_methods": set(),
        "codes": {},
        "missing_responses": 0,
        "files_processed": 0
    }

    metadata = []

    logger.info(
        "Analysis started",
        extra={"exception_code": "NONE"}
    )

    for file_path in files:
        try:
            with open(file_path, "r") as f:
                data = yaml.safe_load(f)

            stats["files_processed"] += 1

          
            api_info = {
                "file": os.path.basename(file_path),
                "title": data.get("info", {}).get("title"),
                "version": data.get("info", {}).get("version"),
                "description": data.get("info", {}).get("description"),
                "servers": [s.get("url") for s in data.get("servers", [])],
                "tags": [t.get("name") for t in data.get("tags", [])],
                "endpoints": []
            }

            global_security = data.get("security", [])

            for path, methods in data.get("paths", {}).items():
                for method, details in methods.items():
                    if method.lower() not in ["get", "post", "put", "patch", "delete"]:
                        continue

                    stats["total_endpoints"] += 1
                    stats["methods"][method.upper()] = stats["methods"].get(method.upper(), 0) + 1

                    # --- Auth ---
                    endpoint_security = details.get("security", global_security)
                    auth_used = []
                    if endpoint_security:
                        for rule in endpoint_security:
                            for scheme in rule:
                                auth_used.append(scheme)
                                stats["auth_methods"].add(scheme)
                    else:
                        auth_used.append("None")

                    responses = details.get("responses", {})
                    if not responses:
                        stats["missing_responses"] += 1

                    for code in responses:
                        stats["codes"][code] = stats["codes"].get(code, 0) + 1

                    api_info["endpoints"].append({
                        "path": path,
                        "method": method.upper(),
                        "auth": auth_used,
                        "response_codes": list(responses.keys())
                    })

            metadata.append(api_info)

            logger.info(
                "File parsed successfully",
                extra={"exception_code": "NONE"}
            )

        except Exception as e:
            logger.error(
                "Parsing failed",
                extra={"exception_code": "YAML_PARSE_ERROR"}
            )

   
    covered = stats["total_endpoints"] - stats["missing_responses"]
    coverage = round((covered / stats["total_endpoints"]) * 100, 2)

    with open("metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    summary = {
        "files_processed": stats["files_processed"],
        "total_endpoints": stats["total_endpoints"],
        "http_methods": stats["methods"],
        "auth_methods": list(stats["auth_methods"]),
        "response_codes": list(stats["codes"].keys()),
        "missing_response_endpoints": stats["missing_responses"],
        "coverage_percentage": coverage
    }

    with open("summary.json", "w") as f:
        json.dump(summary, f, indent=2)

 
    with open("README.md", "a") as f:
        f.write(
            f"\n## Run Summary ({datetime.datetime.now()})\n"
            f"- Total Endpoints: {stats['total_endpoints']}\n"
            f"- Coverage: {coverage}%\n"
        )

    logger.info(
        "Summary generation completed",
        extra={"exception_code": "NONE"}
    )

if __name__ == "__main__":
    analyze_apis()