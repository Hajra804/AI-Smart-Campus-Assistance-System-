
# Smart Campus AI Decision Support and Automation System
# Project Overview

The Smart Campus AI Decision Support and Automation System is an integrated AI platform designed to process structured campus service requests through the appropriate artificial intelligence pipeline. Depending on the type of request, the system utilizes Artificial Neural Networks (ANN), a Logic-Based Knowledge Base, Constraint Satisfaction Problem (CSP) scheduling, and Search algorithms to generate a unified and intelligent response.

---

# Project Modules

| Module                             | File                                    | Marks |
| ---------------------------------- | --------------------------------------- | ----: |
| Input Validation and Preprocessing | `modules/preprocessing.py`              |    10 |
| ANN-Based Priority Prediction      | `modules/ann_priority.py`               |    20 |
| Logic and Knowledge Base           | `modules/logic_kb.py`                   |    20 |
| CSP-Based Scheduler                | `modules/csp_scheduler.py`              |    15 |
| Search and Navigation              | `modules/search_navigation.py`          |    15 |
| Response Integration               | `modules/final_response.py` + `main.py` |    10 |

---

# Running the Project

Execute the project using:

```bash
python main.py
```

The command-line interface will guide the user through a series of prompts based on the selected request type.

---

# Supported Request Types

1. **Navigation_Only**
   Finds the shortest campus route using BFS for unweighted graphs and A* for weighted graphs.

2. **Eligibility_Check**
   Evaluates eligibility using a First-Order Logic (FOL) knowledge base with forward chaining.

3. **Booking_or_Scheduling**
   Allocates available rooms or time slots using CSP backtracking after validating eligibility.

4. **Urgent_Service_Request**
   Predicts request priority using ANN, verifies eligibility, and schedules the service.

5. **Full_Service_Request**
   Executes the complete AI pipeline, including priority prediction, eligibility verification, scheduling, and navigation.

---

# Processing Pipeline

```
Navigation_Only:
Preprocessing → Router → Search → Final Response

Eligibility_Check:
Preprocessing → Router → Logic/Knowledge Base → Final Response

Booking_or_Scheduling:
Preprocessing → Router → Logic/Knowledge Base → CSP Scheduler → (Optional Search) → Final Response

Urgent_Service_Request:
Preprocessing → Router → ANN → Logic/Knowledge Base → CSP Scheduler → (Optional Search) → Final Response

Full_Service_Request:
Preprocessing → Router → ANN → Logic/Knowledge Base → CSP Scheduler → Search → Final Response
```

---

# ANN Architecture

The priority prediction module consists of two neural network models:

* **Perceptron (Binary Classification):** Determines whether a request is **Urgent** or **Not Urgent**.
* **Multilayer Perceptron (MLP):** Classifies requests into one of four priority levels:

  * Low
  * Normal
  * High
  * Urgent

### Feature Vector

The models use the following input features:

```
[Role, Request Type, Severity, Time Sensitivity,
Crowd Level, Distance, Eligibility]
```

---

# Search Algorithms

### Implemented for System Operation

* Breadth-First Search (BFS)
* A* Search
* Uniform Cost Search (UCS)

### Implemented for Academic Comparison

* Depth-First Search (DFS)
* Depth-Limited Search (DLS)
* Iterative Deepening Search (IDS)
* Bidirectional Breadth-First Search
* Greedy Best-First Search
* Recursive Best-First Search (RBFS)

---

# Campus Locations

The navigation module includes the following campus locations:

* Main_Gate
* Parking
* Admin_Block
* Student_Services
* Exam_Hall
* Seminar_Room
* Library
* AI_Lab
* Science_Block
* Cafeteria
* Hostel
* Medical_Center
* Bus_Stop

---

# Example Command-Line Session

```text
Enter Name: Ali
Enter Role (student / instructor / staff): student
Enter choice (number or name): 5
Enter Category: 1
Enter Current Location: Hostel
Enter Preferred Slot (1-4): 2
Enter Severity (1-10): 8
Enter Time Sensitivity (1-10): 9
Enter Crowd Level (1-10): 5
Enter Description Note: Need urgent help before practical evaluation
```

### Sample Output

The generated response may include:

* Predicted request priority
* Eligibility verification
* Assigned room or time slot
* Recommended campus route

---

# Project Structure

```text
smart_campus/
├── main.py                      # Project entry point
├── README.md
└── modules/
    ├── __init__.py
    ├── preprocessing.py         # Input validation and normalization
    ├── router.py                # Pipeline selection
    ├── ann_priority.py          # Perceptron and MLP implementation
    ├── logic_kb.py              # FOL knowledge base with forward chaining
    ├── csp_scheduler.py         # CSP-based scheduling using backtracking
    ├── search_navigation.py     # Search algorithms for navigation
    └── final_response.py        # Final response generation and integration
```
