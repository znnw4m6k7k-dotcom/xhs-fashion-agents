# Codex Agent Bundle Installation

When a user asks Codex to install this repository:

1. Read this file and `README.md`.
2. Inspect `scripts/install_agents.py` before executing it.
3. Run `python3 scripts/install_agents.py`.
4. Run `python3 scripts/install_agents.py --check` and require both agents to pass.
5. Read `docs/使用说明-中文.md`.
6. In the same chat, give the user a Chinese manual that includes:
   - both installed absolute paths;
   - the check result;
   - the responsibility boundary of each Agent;
   - one first-call example for each Agent;
   - the reminder that a new Codex conversation may be needed to refresh the Agent list.
7. Do not claim that the orchestration Skill, image generation, RedBeacon, Feishu, Ego, or any account login was installed by this bundle.
