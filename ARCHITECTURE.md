# 🤖 Agent Architecture Deep Dive

## System Overview

The Multi-Agent Game Tester uses a coordinated multi-agent system where each agent has a specific responsibility in the testing pipeline.

```
┌─────────────────────────────────────────────────────────────────┐
│                     OrchestratorAgent                            │
│  (Master Coordinator - Orchestrates entire workflow)             │
└────┬───────────────────────────────────────────────────┬─────────┘
     │                                                   │
     ▼                                                   ▼
┌──────────────────┐                          ┌─────────────────────┐
│ PlannerAgent     │                          │ GameInteraction     │
│                  │                          │                     │
│ Generates 20+    │  ─────────────────────▶ │ - Opens game        │
│ test cases       │                          │ - Captures screenshots
│                  │                          │ - Records artifacts │
└──────────────────┘                          └─────────────────────┘
                                                       ▲
     ┌───────────────────────────────────────┐        │
     │            RankerAgent                │        │
     │                                       │        │
     │ Ranks and selects                     │        │
     │ Top 10 test cases                     │        │
     │                                       │        │
     └───────────────────┬───────────────────┘        │
                         │                            │
         ┌───────────────┴────────────────┐           │
         │                                │           │
         ▼                                ▼           │
   ┌──────────────────┐          ┌──────────────────┐ │
   │ ExecutorAgent-1  │          │ ExecutorAgent-2  │ │
   │                  │          │                  │ │
   │ Executes tests   │          │ Executes tests   │ │
   │ & artifacts      │          │ & artifacts      │─┘
   └────────┬─────────┘          └────────┬─────────┘
            │                             │
            └──────────────┬──────────────┘
                          │
                          ▼
                   ┌──────────────────┐
                   │ AnalyzerAgent    │
                   │                  │
                   │ - Validates      │
                   │ - Cross-checks   │
                   │ - Generates      │
                   │   verdicts       │
                   └────────┬─────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │ ReportGenerator  │
                   │                  │
                   │ Creates JSON     │
                   │ report with      │
                   │ all details      │
                   └──────────────────┘
```

## Workflow Execution

### Phase 1: PLANNING (PlannerAgent)
```
Input: Game URL
│
├─ Analyze game requirements
├─ Generate test templates
├─ Create 20+ test cases with:
│  ├─ Test ID
│  ├─ Description
│  ├─ Priority (High/Medium/Low)
│  ├─ Type (UI, Functional, Stress)
│  └─ Expected results
│
Output: List of 20+ test cases
```

### Phase 2: RANKING (RankerAgent)
```
Input: 20+ test cases

Scoring Algorithm:
┌─────────────────┐
│ Priority        │ High: +100, Medium: +50, Low: +25
├─────────────────┤
│ Type            │ Functional: +30, UI: +20, Other: +10
├─────────────────┤
│ Complexity      │ Edge cases/Errors: +20
├─────────────────┤
│ Total Score     │ Sum of all categories
└─────────────────┘

Output: Top 10 tests sorted by score
```

### Phase 3: EXECUTION (ExecutorAgents - Parallel)
```
ExecutorAgent-1          ExecutorAgent-2
│                        │
├─ Test 1 → Screenshot   ├─ Test 6 → Screenshot
├─ Test 2 → DOM SNAP     ├─ Test 7 → DOM SNAP
├─ Test 3 → Console      ├─ Test 8 → Console
├─ Test 4 → Screenshot   ├─ Test 9 → Screenshot
├─ Test 5 → DOM SNAP     ├─ Test 10 → DOM SNAP
│                        │
└─ Results              └─ Results
   │                      │
   └──────────┬───────────┘
              │
        (Artifact Pool)
```

### Phase 4: VALIDATION (AnalyzerAgent)
```
Input: All test results

Validation Checks:
├─ Repeatability
│  └─ Run same test multiple times
│     └─ Results consistent? (Yes/No)
│
├─ Cross-Agent Consistency
│  └─ Do different executors agree?
│     └─ Same result? (Yes/No)
│
├─ Evidence Quality
│  └─ Sufficient artifacts captured?
│     └─ Screenshots + DOM + Logs? (Yes/No)
│
└─ Verdict Determination
   ├─ PASSED - Test succeeded consistently
   ├─ FAILED - Test failed consistently
   └─ FLAKY - Test result varies

Output: Validated results with confidence scores
```

### Phase 5: REPORTING (ReportGenerator)
```
Input: Validated test results

Generate Report with:
├─ Summary Statistics
│  ├─ Tests generated/selected/executed
│  ├─ Pass/fail counts
│  └─ Success rate percentage
│
├─ Detailed Test Results
│  ├─ Individual test status
│  ├─ Verdicts
│  ├─ Evidence/artifacts
│  └─ Validation details
│
├─ Cross-Agent Analysis
│  ├─ Consistency scores
│  ├─ Agreed-upon results
│  └─ Anomalies detected
│
├─ Verdicts
│  ├─ Overall verdict (PASS/FAIL/WARNING)
│  ├─ Issue count
│  └─ Recommendation
│
└─ Final Report (JSON with 50+ fields)

Output: Comprehensive JSON report saved to disk
```

## Agent Responsibilities

| Agent | Input | Process | Output |
|-------|-------|---------|--------|
| **PlannerAgent** | Game URL | Template-based + Edge case analysis | 20+ test cases with metadata |
| **RankerAgent** | Test cases | Score each test, sort by importance | Top 10 ranked tests |
| **ExecutorAgent** | Test + URL | Execute action, capture artifacts | Test result with evidence |
| **AnalyzerAgent** | All results | Cross-validation, consistency check | Validated results with verdicts |
| **OrchestratorAgent** | Game URL | Coordinate all agents | Complete workflow result |

## Data Flow

```
Game URL
   │
   ▼
[Planning] → Test Cases (20+)
   │
   ▼
[Ranking] → Selected Tests (10)
   │
   ▼
[Execution] ─────┬────── ExecutorAgent-1: Results
                 └────── ExecutorAgent-2: Results
   │
   ▼
[Analysis] → Validated Results (with verdicts & scores)
   │
   ▼
[Reporting] → JSON Report with all details
   │
   ▼
Report saved to: reports/report_YYYYMMDD_HHMMSS.json
```

## Key Features

### 1. Intelligent Test Generation
- Template-based approach for consistency
- Edge case detection
- Priority-based importance assessment

### 2. Smart Selection
- Scoring algorithm considering multiple factors
- Prioritizes critical tests
- Balances breadth and depth

### 3. Parallel Execution
- Multiple ExecutorAgents work simultaneously
- Efficient resource utilization
- Faster total execution time

### 4. Comprehensive Validation
- Repeatability checks (consistency over time)
- Cross-agent validation (multiple perspectives)
- Evidence quality assessment
- Confidence scoring

### 5. Rich Reporting
- Structured JSON format
- Detailed verdict justification
- Actionable recommendations
- Complete artifact traceability

## Scalability

The architecture supports:
- **More test cases**: Simple configuration change
- **More executors**: Add ExecutorAgent instances
- **Multiple games**: Change game URL input
- **Custom validation logic**: Extend AnalyzerAgent

## Error Handling

Each agent includes:
- Input validation
- Graceful degradation
- Error logging
- Fallback behaviors

## Performance

```
Planning:     ~30 seconds
Ranking:      ~5 seconds
Execution:    ~1-2 minutes (parallel)
Analysis:     ~30 seconds
Total:        ~3 minutes for 10 tests
```

## Example: Test Case Flow

```
Test: "Click button 'submit'"

[PlannerAgent] Creates:
├─ test_id: "test_1"
├─ description: "Click button 'submit' and verify"
├─ priority: "high"
├─ type: "ui_interaction"
└─ expected_result: "Button responds correctly"

[RankerAgent] Scores:
├─ Priority: +100 (high)
├─ Type: +20 (UI)
├─ Complexity: 0
└─ Total Score: 120

[ExecutorAgent] Executes:
├─ Actions: Click submit button
├─ Captures: Screenshot of result
├─ Records: DOM state after click
├─ Logs: Any console messages
└─ Status: "passed"

[AnalyzerAgent] Validates:
├─ Repeatability: "repeatable" (same result each run)
├─ Consistency: "consistent" (all agents agree)
├─ Evidence: "sufficient" (all artifacts captured)
└─ Verdict: "PASSED"

[ReportGenerator] Documents:
├─ Result with full metadata
├─ Links to artifacts
├─ Validation confidence: 95%
└─ No issues found
```

---

**This architecture ensures robust, thorough, and trustworthy game testing!**
