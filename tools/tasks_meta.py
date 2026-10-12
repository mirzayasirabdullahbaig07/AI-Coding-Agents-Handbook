"""Single source of truth for per-task metadata (used by screenshots + PDF reports)."""

TASKS = [
    dict(
        n=1, folder="task-01-coding-agent-basics", page="Page 1",
        title="Coding Agent Basics: Suggestion vs Verified Result",
        main="evidence.py", test="test_evidence.py",
        concept=("A coding agent is a supervised engineering assistant: model + instructions + context + authorised tools in an "
                 "execution loop. It is not a chatbot, not autocomplete and not a human developer. The key rule of the page: a model "
                 "<b>proposing</b> a command and the application <b>executing</b> it are different things. 'I ran the test' is a verified "
                 "claim only if an observable tool result exists."),
        built=("An <b>evidence recorder</b> (<font face='Courier'>run_check</font>) that really executes a command and stores the command, "
               "return code, output, time and exact revision (content hash). A <b>claim judge</b> then labels every claim as "
               "VERIFIED, FAILED, BLOCKED/timeout or NOT VERIFIED (no execution evidence)."),
        points=["Claim without evidence -> 'NOT VERIFIED'", "Attempt that was blocked / timed out is NOT a completed action",
                "A failing run is reported as FAILED, never as success", "Evidence is tied to an exact revision (hash of the code)"],
        takeaway="You can delegate work to an agent, never accountability. Keep scope + evidence + human judgement together.",
        not_run=["Real LLM calls (the demo uses fixed example claims)"],
        limits=["Revision = content hash of .py files; in a git repo use the commit SHA (see Task 07)."],
    ),
    dict(
        n=2, folder="task-02-llm-context-memory", page="Page 2",
        title="LLM, Context and Memory: the Context Packet",
        main="context_packet.py", test="test_context_packet.py",
        concept=("An LLM works only on the context it is given (prompt, tokens, a limited context window). Missing API contracts, tests "
                 "or repo instructions lead to plausible but wrong code. Saved memory is not an automatically current repository "
                 "record - the source code and repository instructions stay the source of truth. Give <b>relevant, current, bounded</b> "
                 "context, never secrets."),
        built=("A 6-field <b>ContextPacket</b> (Goal, Files, Current, Expected, Constraints, Acceptance criteria), a <b>gate</b> that "
               "rejects incomplete packets or packets containing secrets, and a <b>file selector</b> that ranks files by relevance, "
               "stays inside a token budget, always includes AGENTS.md, and skips files that contain secrets."),
        points=["Missing fields are reported before the agent starts", "API keys / passwords / e-mails detected by regex and blocked",
                "Relevant files chosen under a token budget (~4 chars per token)", "'List your assumptions first' prompt included"],
        takeaway="Strong context means relevant, current and bounded information - not more text.",
        not_run=["Real tokenizer (token count is an estimate)"],
        limits=["Secret detection is regex-based and will miss unusual formats; it is a safety net, not a guarantee."],
    ),
    dict(
        n=3, folder="task-03-agent-working-loop", page="Page 3",
        title="The Agent Working Loop",
        main="agent_loop.py", test="test_agent_loop.py",
        concept=("The agent works in a loop: Task -> Inspect -> Propose -> Policy check -> Execute -> Observe -> Adjust -> Verify -> Handoff. "
                 "The model proposes, the orchestration layer checks policy, tools execute, a human sets intent and approval limits. "
                 "Retries must be bounded - repeating the same failing action only adds cost and confusion."),
        built=("A working loop on a real buggy Task Tracker copy. A deterministic <b>ScriptedModel</b> (stand-in for an LLM, clearly labelled) "
               "reads the file, proposes a dangerous <font face='Courier'>rm -rf</font> that the <b>Policy</b> blocks, makes a first edit, "
               "<b>observes a real failing test</b>, adjusts, re-runs and verifies. A 'stuck' model that repeats itself is escalated."),
        points=["Dangerous / out-of-scope proposals are blocked, not executed", "First attempt fails for real -> observation drives the adjustment",
                "VERIFY only passes if the latest test run is green", "Repeated identical action -> ESCALATE (bounded retries)",
                "Original workspace is untouched (works in a temp copy)"],
        takeaway="Think 'propose -> execute -> observe -> verify'. Never mix an attempt with a result.",
        not_run=["A real LLM (ScriptedModel is deterministic so the demo is reproducible)"],
        limits=["Policy is a simple allow-list + single editable file; real systems need richer permission models."],
    ),
    dict(
        n=4, folder="task-04-orchestration-layer", page="Page 4",
        title="What Is the Orchestration Layer?",
        main="orchestrator.py", test="test_orchestrator.py",
        concept=("The orchestration layer is the application logic around the model: task routing, context assembly, permissions, "
                 "reliability (retry, timeout, checkpoints, logging) and completion logic. A smart prompt alone cannot grant file access, "
                 "enforce permissions, persist state or guarantee tool execution. Even a single agent needs an orchestrator."),
        built=("An <b>Orchestrator</b> with a tool registry, a <b>Permissions</b> object (allow-list, write scope, human-approval tools), "
               "<b>bounded retries only for transient errors</b>, per-call timeout, JSON <b>checkpoints</b> with resume, a JSONL "
               "<b>audit log</b>, and completion / escalation logic."),
        points=["Permission is checked BEFORE a tool runs", "Only TransientError is retried; real bugs surface immediately",
                "Timeout and exhausted retries -> ESCALATE", "Checkpoint resume skips already-done steps",
                "Production deploy requires human approval"],
        takeaway="The model is the proposer; the orchestration layer is the control plane. Keep them conceptually separate.",
        not_run=["Concurrency / multi-process locking"],
        limits=["Timeout uses a thread; a stuck tool thread cannot be force-killed in Python."],
    ),
    dict(
        n=5, folder="task-05-multi-agent-systems", page="Page 5",
        title="How a Multi-Agent System Is Built",
        main="multi_agent.py", test="test_multi_agent.py",
        concept=("A multi-agent system has several agent instances with defined responsibilities and communication rules - possibly the "
                 "same model. More agents are not automatically faster, cheaper or more accurate. Implementation and test planning can "
                 "run in parallel when inputs are stable; review depends on the final diff. Two agents editing the same file conflict."),
        built=("A <b>Delegation Contract</b> (Task, Inputs, Allowed files, Constraints, Output, Verify, Stop), a <b>task graph</b> with "
               "topological levels (parallel where possible), <b>file-conflict detection</b> that forces sequential execution, "
               "<b>scope enforcement</b> (an agent touching files outside its contract is rejected) and a <b>should_delegate</b> decision table."),
        points=["Coordinator -> (Implementation || Test) -> Review", "Review always runs after implementation output exists",
                "Overlapping allowed files -> run sequentially", "Out-of-contract edits raise PermissionError",
                "Reviewer output notes it shares assumptions: a second AI is not proof"],
        takeaway="Delegate only when boundaries are clear and the benefit outweighs coordination cost.",
        not_run=["Real LLM agents (roles are simulated functions)"],
        limits=["Parallelism uses threads on simple functions; real agents would need isolated worktrees."],
    ),
    dict(
        n=6, folder="task-06-ai-communication", page="Page 6",
        title="Communicating with AI: Weak -> Better -> Strong",
        main="prompt_kit.py", test="test_prompt_kit.py",
        concept=("Reusable structure: Goal -> Context -> Scope -> Constraints -> Acceptance criteria -> Verification -> Required response. "
                 "A strong request gives the agent both freedom and boundaries. Ask for assumptions, evidence, trade-offs and uncertainty - "
                 "not for hidden chain-of-thought."),
        built=("A <b>PromptSpec</b> that renders the 7-part structure, a <b>grader</b> that scores any free-text prompt 0-7 and lists the missing "
               "sections (Weak / Better / Strong), the four copy-ready templates (explain, diagnose, bounded change, review diff), "
               "the daily prompt template and a <b>linter</b> that flags requests for hidden chain-of-thought."),
        points=["'Fix the filter.' scores Weak (1/7)", "Observed-vs-expected description scores Better", "Full 7-part prompt scores Strong (7/7)",
                "Read-only templates explicitly forbid code changes"],
        takeaway="A good prompt makes the task measurable: what to change, what not to, and which evidence means 'done'.",
        not_run=["Sending prompts to a real model"],
        limits=["The grader is keyword-based: a quick teaching aid, not a quality guarantee."],
    ),
    dict(
        n=7, folder="task-07-repo-daily-workflow", page="Page 7",
        title="Daily Workflow in a Real Repository",
        main="repo_workflow.py", test="test_repo_workflow.py",
        concept=("Before using AI in a repository, understand its state: existing uncommitted changes may belong to someone else and must "
                 "not be overwritten or silently included. Flow: instructions + status -> code + criteria -> branch/worktree -> small change "
                 "-> inspect diff -> checks -> PR review -> exact revision. Local pass, CI pass, merged and deployed are different states."),
        built=("Real <b>git</b> automation: <b>preflight</b> (finds AGENTS.md, branch, foreign uncommitted files), <b>branch creation that "
               "refuses a dirty tree</b>, <b>diff inspection</b> with out-of-scope file detection, check runner, and a <b>handoff</b> that records the "
               "exact commit and an enum of delivery states - listing which ones are evidenced and which are not."),
        points=["Dirty tree -> refuse to branch, report who-knows-whose changes", "Diff outside allowed scope is flagged",
                "Handoff refuses to run on a dirty tree (evidence must match one exact revision)",
                "Only LOCAL_TESTS_PASS can be claimed; CI / merged / deployed are shown as NOT evidenced"],
        takeaway="Every handoff states the exact revision and exact checks - evidence belongs to the revision it ran on.",
        not_run=["Hosted CI, merge and deploy (no remote in the demo)"],
        limits=["Uses a temporary local repo; no push / PR creation is performed."],
    ),
    dict(
        n=8, folder="task-08-debugging-review-evidence", page="Page 8",
        title="Debugging, Review and Evidence",
        main="debug_tools.py", test="test_filter.py",
        concept=("Debugging means narrowing the cause with testable evidence and restoring intended behaviour: reproduce -> relevant error -> "
                 "hypothesis -> focused change -> verify -> regression check. Do not call a failure 'flaky' without evidence, do not weaken "
                 "assertions to get green, and remember that tests written with the same wrong assumption can both pass."),
        built=("A real <b>bug</b> (UI label 'Done' vs stored 'done'/'DONE'). Tools to run the <b>same tests against the unchanged base and the fixed "
               "revision</b>, inspect the <b>data shape</b>, derive a hypothesis, classify failures as <b>regression vs pre-existing</b>, and render the "
               "<b>evidence-backed report</b> template (Change, Revision, Checks run, Results, Checks not run, Limitations, Next action)."),
        points=["Bug reproduces on base (tests FAIL), passes on the fixed revision", "Positive, negative and regression test cases",
                "Failure that also exists on base is labelled PRE-EXISTING, not a regression", "Report lists 'checks not run' honestly"],
        takeaway="Passing tests are evidence, not proof of everything. Only behaviour the checks cover is supported.",
        not_run=["Browser/UI tests", "Hosted CI"],
        limits=["Only case/whitespace differences in status are covered."],
    ),
    dict(
        n=9, folder="task-09-safety-privacy-efficiency", page="Page 9",
        title="Safety, Privacy and Efficiency",
        main="safety.py", test="test_safety.py",
        concept=("Giving an agent a repo and tools is power; boundaries make it inspectable and safe. Keep passwords, tokens, production data and "
                 "customer records out of prompts and logs. Repository text, web pages, issues and tool output are <b>data</b>, not instructions "
                 "(prompt injection). Stop and escalate when authority or information is missing. Set limits on agents, retries, time and spend."),
        built=("A <b>redactor</b> (API keys, AWS keys, passwords, e-mails), a <b>prompt-injection detector</b> and an <b>untrusted-data wrapper</b>, "
               "a <b>CONTINUE vs PAUSE-AND-ESCALATE</b> decision function that implements the handbook table, and a <b>Budget</b> object limiting agents, "
               "retries, spend and time."),
        points=["Secrets are redacted before reaching prompts/logs", "'Ignore previous instructions...' in an issue is flagged and labelled as data",
                "Production write / customer data / conflict / security concern -> escalate", "Escalation always wins over 'read-only'",
                "Budgets stop extra agents, retries and spend"],
        takeaway="Where the next action needs authority or information the agent lacks, stop and escalate - that is correct engineering behaviour.",
        not_run=["Real secret-scanning tools (e.g. gitleaks) - regex only"],
        limits=["Injection detection is pattern-based and can be bypassed; real defence is permissions + sandboxing."],
    ),
    dict(
        n=10, folder="task-10-practice-lab", page="Page 10",
        title="Practice Lab: Task Tracker Status Filter + PR Handoff",
        main="task_tracker/tracker.py", test="tests/test_status_filter.py",
        concept=("Exercise: add a status filter to the existing Task Tracker, preserve current behaviour, diagnose one relevant bug and prepare an "
                 "evidence-backed PR handoff. Acceptance: All / Open / Done behave per criteria; a Done filter must never contain Open tasks. "
                 "Complete means: diff reviewed, selected checks recorded, exact revision and limitations reported."),
        built=("A complete small app: <b>task_tracker</b> package (filter + CLI + HTML render), a <b>baseline</b> copy of the pre-feature behaviour, "
               "<b>15 tests</b> (acceptance, negative, preserved behaviour, CLI), a <b>bug diagnosis</b> script and note, a generator for "
               "<b>PR_HANDOFF.md</b> from real results, and a <b>5-point rubric self-check</b> (Clarity, Scope, Correctness, Verification, Handoff)."),
        points=["All / Open / Done return the right tasks in any stored case", "Done never contains Open; Open and Done partition All",
                "Default list == baseline behaviour, order preserved, input not mutated", "Unknown status raises a clear error instead of an empty list",
                "Rubric self-check scores 5/5 from files on disk"],
        takeaway="A confident developer defines scope, inspects evidence, reports uncertainty and involves a human at the right time.",
        not_run=["Hosted CI (runs on GitHub after push)", "Manual browser testing (static HTML render only)"],
        limits=["Only two statuses exist; the rubric is an automated aid, not a replacement for review."],
    ),
]
