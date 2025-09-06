        #!/bin/bash
        # Example runner: loads .env and runs the daily brief once
        set -a
        . ./.env
        set +a
        python - <<'PY'
from AI_Project.agent import AIProjectAgent
ag = AIProjectAgent()
print(ag.handle_command('daily_brief'))
PY
