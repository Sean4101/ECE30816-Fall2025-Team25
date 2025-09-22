import os
import re
from typing import Dict, List, Optional


SPDX_LICENSES = {
    "MIT",
    "Apache-2.0",
    "GPL-3.0",
    "BSD-3-Clause",
    "BSD-2-Clause",
    "LGPL-2.1",
    "LGPL-3.0",
    "MPL-2.0",
    "AGPL-3.0",
}

COMPATIBLE_LICENSES = {"mit", "bsd", "apache-2.0", "lgpl-2.1"}
NON_COMPATIBLE_LICENSES = {"gpl", "gpl-3.0", "agpl", "cc-by-nc"}


def check_spdx_in_file(filepath: str) -> Optional[str]:
    """Check a source file for an SPDX-License-Identifier tag."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                match = re.search(
                    r"SPDX-License-Identifier:\s*([A-Za-z0-9\.\-]+)", line
                )
                if match:
                    license_id = match.group(1)
                    return license_id if license_id in SPDX_LICENSES else None
    except Exception:
        pass
    return None


def check_readme_license_section(readme_path: str) -> Optional[str]:
    """Check README file for a 'License' section."""
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(
                r"(?i)^#+\s*license\s*$([\s\S]+?)(?=^#+|\Z)",
                content,
                re.MULTILINE,
            )
            if match:
                section = match.group(1)
                for lic in SPDX_LICENSES:
                    if lic.lower() in section.lower():
                        return lic
    except Exception:
        pass
    return None


def find_license_metadata(src_dir: str) -> Dict[str, List[str]]:
    """Search source files and README for license information."""
    spdx_found = set()

    # Scan source files
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith((".py", ".js", ".cpp", ".c", ".h")):
                lic = check_spdx_in_file(os.path.join(root, file))
                if lic:
                    spdx_found.add(lic)

    # Scan README
    readme_license = []
    for file in os.listdir(src_dir):
        if file.lower().startswith("readme"):
            lic = check_readme_license_section(os.path.join(src_dir, file))
            if lic:
                readme_license.append(lic)
            break

    return {
        "spdx_licenses": list(spdx_found),
        "readme_license": readme_license,
    }


def calculate_license_score(licenses: List[str],
                            readme_license: List[str]) -> float:
    """Convert license findings into a numeric metric score."""
    all_licenses = [lic.lower() for lic in licenses + readme_license]

    if not all_licenses:
        return 0.0

    for lic in all_licenses:
        if lic in COMPATIBLE_LICENSES:
            return 1.0
        if lic in NON_COMPATIBLE_LICENSES:
            return 0.0

    return 0.5  # custom/unclear license


if __name__ == "__main__":
    src_dir = os.path.dirname(__file__)
    result = find_license_metadata(src_dir)
    score = calculate_license_score(
        result["spdx_licenses"], result["readme_license"]
    )

    print("SPDX Licenses found:", result["spdx_licenses"])
    print("README License section:", result["readme_license"])
    print("License Metric Score:", score)
