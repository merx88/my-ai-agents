from __future__ import annotations

import os
import re
import shutil
import subprocess
from typing import Callable, List, Optional, Tuple


def _ensure_wrangler_available() -> None:
    if shutil.which("wrangler") is None:
        raise RuntimeError("wrangler CLI not found. Install with: npm i -g wrangler")


def _require_env(var: str) -> str:
    val = os.environ.get(var)
    if not val:
        raise RuntimeError(f"Missing env: {var}")
    return val


def _run(cmd: List[str], cwd: Optional[str] = None) -> Tuple[int, str, str]:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def _project_exists(project_name: str) -> bool:
    code, out, err = _run(["wrangler", "pages", "project", "list"])
    if code != 0:
        raise RuntimeError(f"Failed to list projects\n{err or out}")
    return any(project_name in line for line in out.splitlines())


def _create_project(project_name: str, production_branch: str = "main") -> None:
    code, out, err = _run(
        [
            "wrangler",
            "pages",
            "project",
            "create",
            project_name,
            f"--production-branch={production_branch}",
        ]
    )
    if code != 0:
        raise RuntimeError(
            f"Failed to create Pages project '{project_name}'\n"
            f"STDERR:\n{err}\nSTDOUT:\n{out}"
        )


def _deploy_pages(
    project_name: str, site_dir: str, branch: str = "main"
) -> Tuple[Optional[str], str]:
    code, out, err = _run(
        [
            "wrangler",
            "pages",
            "deploy",
            site_dir,
            f"--project-name={project_name}",
            f"--branch={branch}",
        ]
    )
    if code != 0:
        raise RuntimeError(
            f"Failed to deploy project '{project_name}' from '{site_dir}'\n"
            f"STDERR:\n{err}\nSTDOUT:\n{out}"
        )

    urls = set(re.findall(r"https?://[a-zA-Z0-9._/-]+", out))
    primary = next((u for u in urls if ".pages.dev" in u), (next(iter(urls), None)))
    return primary, out


def deploy_sites_under(
    sites_dir: str,
    image_copier: Optional[Callable[[str], None]] = None,
    account_envs_required: bool = True,
    branch: str = "main",
    report_path: str = "output/deployment_report.md",
    project_namer: Optional[Callable[[str], str]] = None,
) -> List[Tuple[str, str]]:
    """
    Deploy each symbol folder under sites_dir to Cloudflare Pages.
    Return: [(symbol, url), ...]

    - image_copier(symbol): Image copy hook before deployment (omitted if not present)
    - project_namer(symbol): Project name customization hook (default: f"{symbol.lower()}-token-site")
    """
    print("🚀 Starting deployment via Cloudflare Pages (Wrangler Direct Upload)...\n")

    _ensure_wrangler_available()
    if account_envs_required:
        _require_env("CLOUDFLARE_API_TOKEN")
        _require_env("CLOUDFLARE_ACCOUNT_ID")

    if not os.path.exists(sites_dir):
        print("⚠️ No sites found to deploy.")
        return []

    deployed: List[Tuple[str, str]] = []

    for symbol in os.listdir(sites_dir):
        site_path = os.path.join(sites_dir, symbol)
        if not os.path.isdir(site_path):
            continue

        # copy image
        if image_copier:
            image_copier(symbol)

        proj_name = (
            project_namer(symbol) if project_namer else f"{symbol.lower()}-token-site"
        )
        print(f"📦 Deploying {symbol} as Cloudflare Pages project '{proj_name}'...")

        try:
            if not _project_exists(proj_name):
                print(f"🆕 Creating Pages project '{proj_name}'...")
                _create_project(proj_name, production_branch=branch)
            else:
                print(f"✅ Pages project '{proj_name}' already exists.")

            print("🚚 Uploading files via Wrangler...")
            url, raw_out = _deploy_pages(proj_name, site_path, branch=branch)

            if url:
                deployed.append((symbol, url))
                print(f"✅ Deployed {symbol} → {url}\n")
            else:
                print("ℹ️ Deployment succeeded but URL not parsed. Raw output:")
                print(raw_out)

        except Exception as e:
            print(f"❌ Failed to deploy {symbol}")
            print(str(e))
            continue

    # save report
    if deployed:
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# 📦 Cloudflare Pages Deployment Report\n\n")
            for symbol, url in deployed:
                f.write(f"- **{symbol}** → [{url}]({url})\n")
        print(f"\n📝 Report saved to `{report_path}`")
    else:
        print("\n⚠️ No deployments were successful.")

    return deployed
