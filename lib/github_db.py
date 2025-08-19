# lib/github_db.py
from __future__ import annotations
import base64, json
import requests
from dataclasses import dataclass

@dataclass
class GitConfig:
    token: str
    repo: str
    branch: str
    path: str

API = "https://api.github.com"

class GitHubDB:
    def __init__(self, cfg: GitConfig):
        self.cfg = cfg
        self._sha_cache = None

    def _headers(self):
        return {"Authorization": f"Bearer {self.cfg.token}", "Accept": "application/vnd.github+json"}

    def read_json(self):
        url = f"{API}/repos/{self.cfg.repo}/contents/{self.cfg.path}?ref={self.cfg.branch}"
        r = requests.get(url, headers=self._headers())
        r.raise_for_status()
        data = r.json()
        self._sha_cache = data.get("sha")
        import base64
        content = base64.b64decode(data["content"]).decode("utf-8")
        return json.loads(content) if content.strip() else []

    def write_json(self, obj: dict|list, message: str):
        url = f"{API}/repos/{self.cfg.repo}/contents/{self.cfg.path}"
        content_b64 = base64.b64encode(json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8")).decode("utf-8")
        payload = {
            "message": message,
            "content": content_b64,
            "branch": self.cfg.branch,
        }
        if self._sha_cache:
            payload["sha"] = self._sha_cache
        r = requests.put(url, headers=self._headers(), json=payload)
        r.raise_for_status()
        self._sha_cache = r.json()["content"]["sha"]
        return True
