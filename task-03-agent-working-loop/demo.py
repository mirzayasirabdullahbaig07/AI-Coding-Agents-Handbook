from pathlib import Path
from agent_loop import ScriptedModel, run_loop

print("Agent loop on the Task Tracker 'Done filter' bug (model = scripted stand-in)\n")
for s in run_loop(ScriptedModel(), Path(__file__).parent / "workspace"):
    print(f"{s.n:02d} {s.phase:<8} {s.text}")
