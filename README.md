# Smart Campus AI Decision Support and Automation System
## AL2002 – Artificial Intelligence Lab (Spring 2026)
### National University of Computing & Emerging Sciences (NUCES)
**Lab Instructor:** Muzaffar Abbas | **Department:** Computer Science

---

## Project Overview

A unified AI-based smart campus platform that routes structured user requests through
the correct AI pipeline (ANN → Logic/KB → CSP → Search) and produces a single coherent
final response.

---

## Module Summary

| Module | File | Marks |
|--------|------|-------|
| Input & Preprocessing | `modules/preprocessing.py` | 10 |
| ANN Priority Prediction | `modules/ann_priority.py` | 20 |
| Logic / Knowledge Base | `modules/logic_kb.py` | 20 |
| CSP Scheduler | `modules/csp_scheduler.py` | 15 |
| Search & Navigation | `modules/search_navigation.py` | 15 |
| Final Response & Integration | `modules/final_response.py` + `main.py` | 10 |

---

## How to Run

```
python main.py
```

Follow the CLI prompts. The system will ask for fields one by one based on request type.

---

## Supported Request Types

1. **Navigation_Only** — Campus route finding (BFS for unweighted, A* for weighted)
2. **Eligibility_Check** — FOL query answered via forward-chaining knowledge base
3. **Booking_or_Scheduling** — Slot/room assignment using CSP backtracking
4. **Urgent_Service_Request** — ANN priority prediction + validation + scheduling
5. **Full_Service_Request** — Complete pipeline: ANN → Logic → CSP → Search

---

## Pipeline by Request Type

```
Navigation_Only:       Preprocessing → Router → Search → Final Response
Eligibility_Check:     Preprocessing → Router → Logic/KB → Final Response
Booking_Scheduling:    Preprocessing → Router → Logic/KB → CSP → [Search] → Final Response
Urgent_Service:        Preprocessing → Router → ANN → Logic/KB → CSP → [Search] → Final Response
Full_Service:          Preprocessing → Router → ANN → Logic/KB → CSP → Search → Final Response
```

---

## ANN Architecture

- **Perceptron** (binary): `urgent` vs `not_urgent`  
- **MLP** (multiclass): `low` / `normal` / `high` / `urgent`  
- Feature vector: `[Role, RequestType, Severity, TimeSensitivity, CrowdLevel, Distance, Eligibility]`

---

## Search Algorithms

**Operational:** BFS (unweighted), A* (weighted + heuristic), UCS (weighted fallback)  
**Academic/Comparison:** DFS, DLS, IDS, Bidirectional BFS, Greedy Best-First, RBFS

---

## Campus Nodes

Main_Gate, Parking, Admin_Block, Student_Services, Exam_Hall, Seminar_Room,
Library, AI_Lab, Science_Block, Cafeteria, Hostel, Medical_Center, Bus_Stop

---

## Example CLI Session

```
Enter Name: Ali
Enter Role (student / instructor / staff): student
Enter choice (number or name): 5          ← Full_Service_Request
Enter Category: 1                          ← AI_Lab_Support
Enter Current Location: Hostel
Enter Preferred Slot (1-4): 2
Enter Severity (1-10): 8
Enter Time Sensitivity (1-10): 9
Enter Crowd Level (1-10): 5
Enter Description Note: Need urgent help before practical evaluation
```

Output includes: priority prediction, eligibility confirmation, slot/room assignment, campus route.

---

## File Structure

```
smart_campus/
├── main.py                      ← Entry point
├── README.md
└── modules/
    ├── __init__.py
    ├── preprocessing.py         ← Input validation & normalization
    ├── router.py                ← Pipeline selection
    ├── ann_priority.py          ← Perceptron + MLP
    ├── logic_kb.py              ← FOL knowledge base + forward chaining
    ├── csp_scheduler.py         ← CSP backtracking scheduler
    ├── search_navigation.py     ← 9 search algorithms
    └── final_response.py        ← Output aggregation layer
```
