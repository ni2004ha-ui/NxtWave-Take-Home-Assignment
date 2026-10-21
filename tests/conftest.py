"""Safety rails: tests must never spend money, read the real .env, or touch real memory/output files."""
import os
import tempfile

_tmp = tempfile.mkdtemp()
os.environ.pop("ANTHROPIC_API_KEY", None)            # subprocesses inherit "no key"
os.environ["AGENT_NO_DOTENV"] = "1"                  # ...and are told not to read .env
os.environ["MEMORY_PATH"] = os.path.join(_tmp, "store.json")
os.environ["CANDIDATES_PATH"] = os.path.join(_tmp, "candidate_checks.yaml")
