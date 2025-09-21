import os
import tempfile
from src.license_metric import find_license_metadata, calculate_license_score


def test_spdx_license():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a fake Python file with SPDX license header
        file_path = os.path.join(tmpdir, "dummy.py")
        with open(file_path, "w") as f:
            f.write("# SPDX-License-Identifier: MIT\n")

        result = find_license_metadata(tmpdir)
        score = calculate_license_score(result["spdx_licenses"],
                                        result["readme_license"])

        assert result["spdx_licenses"] == ["MIT"]
        assert result["readme_license"] == []   # no README
        assert score == 1.0


def test_readme_license():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a fake README with License section
        readme_path = os.path.join(tmpdir, "README.md")
        with open(readme_path, "w") as f:
            f.write("#License\nIt is licensed under the Apache-2.0 license.\n")

        result = find_license_metadata(tmpdir)
        score = calculate_license_score(result["spdx_licenses"],
                                        result["readme_license"])

        assert result["readme_license"] == ["Apache-2.0"]
        assert score == 1.0


def test_no_license():
    with tempfile.TemporaryDirectory() as tmpdir:
        # No license info
        result = find_license_metadata(tmpdir)
        score = calculate_license_score(result["spdx_licenses"],
                                        result["readme_license"])

        assert result["spdx_licenses"] == []
        assert result["readme_license"] == []
        assert score == 0.0
