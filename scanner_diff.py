#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys
from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple


class VulnerabilityScanner:
    """Scan container images with Trivy and Grype, then compare results."""

    def __init__(self, images: List[str]):
        self.images = images
        self.results = []

    def scan_with_trivy(self, image: str) -> Dict:
        """Scan image with Trivy and return JSON results."""
        print(f"[Trivy] Scanning {image}...", file=sys.stderr)
        try:
            result = subprocess.run(
                ["trivy", "image", "--format", "json", "--quiet", image],
                capture_output=True,
                text=True,
            )
            # Trivy returns non-zero when vulnerabilities are found, but still outputs valid JSON
            if result.stdout:
                return json.loads(result.stdout)
            print(f"[Trivy] No output for {image}: {result.stderr}", file=sys.stderr)
            return {}
        except json.JSONDecodeError as e:
            print(f"[Trivy] Error parsing JSON for {image}: {e}", file=sys.stderr)
            return {}

    def scan_with_grype(self, image: str) -> Dict:
        """Scan image with Grype and return JSON results."""
        print(f"[Grype] Scanning {image}...", file=sys.stderr)
        try:
            result = subprocess.run(
                ["grype", image, "-o", "json", "-q"],
                capture_output=True,
                text=True,
            )
            # Grype may return non-zero when vulnerabilities are found
            if result.stdout:
                return json.loads(result.stdout)
            print(f"[Grype] No output for {image}: {result.stderr}", file=sys.stderr)
            return {}
        except json.JSONDecodeError as e:
            print(f"[Grype] Error parsing JSON for {image}: {e}", file=sys.stderr)
            return {}

    def extract_trivy_vulns(
        self, trivy_data: Dict
    ) -> Tuple[Set[Tuple[str, str]], Dict[str, int]]:
        """Extract vulnerability IDs, packages, and severity counts from Trivy results."""
        vulns = set()
        severity_counts = Counter()

        if not trivy_data:
            return vulns, dict(severity_counts)

        for result in trivy_data.get("Results", []):
            for vuln in result.get("Vulnerabilities", []):
                vuln_id = vuln.get("VulnerabilityID", "")
                pkg_name = vuln.get("PkgName", "")
                severity = vuln.get("Severity", "UNKNOWN").upper()

                if vuln_id and pkg_name:
                    vulns.add((vuln_id, pkg_name))
                    severity_counts[severity] += 1

        return vulns, dict(severity_counts)

    def extract_grype_vulns(
        self, grype_data: Dict
    ) -> Tuple[Set[Tuple[str, str]], Dict[str, int]]:
        """Extract vulnerability IDs, packages, and severity counts from Grype results."""
        vulns = set()
        severity_counts = Counter()

        if not grype_data:
            return vulns, dict(severity_counts)

        for match in grype_data.get("matches", []):
            vuln_id = match.get("vulnerability", {}).get("id", "")
            pkg_name = match.get("artifact", {}).get("name", "")
            severity = match.get("vulnerability", {}).get("severity", "Unknown").upper()

            if vuln_id and pkg_name:
                vulns.add((vuln_id, pkg_name))
                severity_counts[severity] += 1

        return vulns, dict(severity_counts)

    def compare_results(
        self,
        image: str,
        trivy_vulns: Set,
        grype_vulns: Set,
        trivy_severity: Dict,
        grype_severity: Dict,
    ) -> Dict:
        """Compare Trivy and Grype results for an image."""
        only_trivy = trivy_vulns - grype_vulns
        only_grype = grype_vulns - trivy_vulns
        both = trivy_vulns & grype_vulns

        return {
            "image": image,
            "trivy": {"total": len(trivy_vulns), "severity": trivy_severity},
            "grype": {"total": len(grype_vulns), "severity": grype_severity},
            "comparison": {
                "common_count": len(both),
                "only_trivy_count": len(only_trivy),
                "only_grype_count": len(only_grype),
            },
            "details": {
                "only_trivy": sorted(list(only_trivy)),
                "only_grype": sorted(list(only_grype)),
                "common": sorted(list(both)),
            },
        }

    def scan_all(self):
        """Scan all images and aggregate results."""
        for image in self.images:
            print(f"\n{'=' * 60}", file=sys.stderr)
            print(f"Processing: {image}", file=sys.stderr)
            print(f"{'=' * 60}", file=sys.stderr)

            trivy_data = self.scan_with_trivy(image)
            grype_data = self.scan_with_grype(image)

            trivy_vulns, trivy_severity = self.extract_trivy_vulns(trivy_data)
            grype_vulns, grype_severity = self.extract_grype_vulns(grype_data)

            comparison = self.compare_results(
                image, trivy_vulns, grype_vulns, trivy_severity, grype_severity
            )
            self.results.append(comparison)

    def generate_report(self) -> Dict:
        """Generate aggregate report across all images."""
        total_trivy_severity = Counter()
        total_grype_severity = Counter()
        total_trivy = 0
        total_grype = 0
        total_common = 0
        total_only_trivy = 0
        total_only_grype = 0

        for result in self.results:
            total_trivy += result["trivy"]["total"]
            total_grype += result["grype"]["total"]
            total_common += result["comparison"]["common_count"]
            total_only_trivy += result["comparison"]["only_trivy_count"]
            total_only_grype += result["comparison"]["only_grype_count"]

            for severity, count in result["trivy"]["severity"].items():
                total_trivy_severity[severity] += count
            for severity, count in result["grype"]["severity"].items():
                total_grype_severity[severity] += count

        return {
            "summary": {
                "images_scanned": len(self.images),
                "trivy": {
                    "total_findings": total_trivy,
                    "severity": dict(total_trivy_severity),
                },
                "grype": {
                    "total_findings": total_grype,
                    "severity": dict(total_grype_severity),
                },
                "comparison": {
                    "common_findings": total_common,
                    "only_trivy": total_only_trivy,
                    "only_grype": total_only_grype,
                },
            },
            "per_image": self.results,
        }

    def print_summary(self):
        """Print per-image breakdown and cumulative summary to stdout."""
        report = self.generate_report()

        # Per-image breakdown
        for result in self.results:
            print(f"{result['image']}:")
            trivy_sev = result["trivy"]["severity"]
            grype_sev = result["grype"]["severity"]
            print(f"  Trivy:  {result['trivy']['total']:3d}  (C:{trivy_sev.get('CRITICAL', 0)} H:{trivy_sev.get('HIGH', 0)} M:{trivy_sev.get('MEDIUM', 0)} L:{trivy_sev.get('LOW', 0)})")
            print(f"  Grype:  {result['grype']['total']:3d}  (C:{grype_sev.get('CRITICAL', 0)} H:{grype_sev.get('HIGH', 0)} M:{grype_sev.get('MEDIUM', 0)} L:{grype_sev.get('LOW', 0)})")
            print()

        # Cumulative summary
        print("=" * 50)
        print("CUMULATIVE TOTAL")
        print("=" * 50)
        print()
        print("Trivy:")
        print(f"  Total: {report['summary']['trivy']['total_findings']}")
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            count = report["summary"]["trivy"]["severity"].get(severity, 0)
            print(f"  {severity}: {count}")

        print()
        print("Grype:")
        print(f"  Total: {report['summary']['grype']['total_findings']}")
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            count = report["summary"]["grype"]["severity"].get(severity, 0)
            print(f"  {severity}: {count}")


def main():
    parser = argparse.ArgumentParser(
        description="Compare Trivy and Grype vulnerability scan results across multiple container images"
    )
    parser.add_argument(
        "images",
        nargs="+",
        help="Container images to scan (e.g., nginx:latest ubuntu:22.04)",
    )
    parser.add_argument(
        "-o", "--output", help="Output JSON file", default=None
    )
    parser.add_argument(
        "--json", action="store_true", help="Output JSON to stdout instead of summary"
    )

    args = parser.parse_args()

    scanner = VulnerabilityScanner(args.images)
    scanner.scan_all()

    report = scanner.generate_report()

    if args.output:
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\nResults written to: {args.output}", file=sys.stderr)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        scanner.print_summary()


if __name__ == "__main__":
    main()
