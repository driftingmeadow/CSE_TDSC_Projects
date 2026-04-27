# CSE Projects 

## About this repository

This repository documents projects I am working on. It includes bug fixes and deployment work on an 
existing production system, system dynamics 
modelling work, and my M.Sc. thesis.

---

## Projects

### 1. JalTantra — Bug Fixes and Deployment (Contributor, not author)
**Folder:** `Jaltantra_Branch_reference/`

JalTantra is a web-based rural water network optimization tool developed and 
maintained by the TDSC Lab, IIT Bombay. It is live at 
[cse.iitb.ac.in/jaltantra](http://cse.iitb.ac.in/jaltantra).

> **Note:** JalTantra is not my project. I contributed to it as project staff.

My specific contributions:
- Identified and fixed an elevation precision bug caused by silent float-to-int 
  truncation across three layers: `map.js` (frontend), `MapNodeStruct.java` 
  (Java DTO), and `OptimizerServlet.java` (output generation)
- Configured dual-server deployment (production + testing) using systemd service 
  files, WAR-based Tomcat 9 deployment at `/opt/tomcat9`, with isolated 
  `CATALINA_HOME` and `CATALINA_BASE` to prevent library version conflicts
- Debugged 404 and 500 errors including a JSP filename mismatch 
  (`changepass.jsp` vs `changepassword.jsp`)

The files in `Jaltantra_Branch_reference/` are the specific files I worked on, 
extracted for reference. The full JalTantra codebase is maintained separately 
by the lab.

---

### 2. MGNREGA Data Pipeline
**Folder:** `MGNREGA/`

A multi-threaded data scraping and extraction pipeline for MGNREGA 
(Mahatma Gandhi National Rural Employment Guarantee Act) public data across 
Gujarat and Bihar. Built to support research on rural employment patterns and 
government scheme reach.

- Multi-threaded scraping across state and district-level data portals
- Structured extraction and storage pipeline in Python
- Designed for reproducibility and incremental data collection

---

### 3. System Dynamics — Indian Banking Sector Model
**Folder:** `System Dynamics/`

A stock-and-flow model of the Indian banking system built in Vensim, developed 
as part of my self-directed study in system dynamics modelling. Informed by 
*Money: A Zero Sum Game* and foundational system dynamics texts including 
Forrester and Meadows.

- Models deposit creation, credit flows, and reserve feedback loops
- Includes corrections for a conservation law violation where the same deposit 
  inflow was triple-counted across stock equations
- Ongoing work toward a financial markets research proposal

---

### 4. M.Sc. Thesis — LLM Evaluation for Mental Health Support
**File:** `Msc Thesis Documentation roll no.25 sakina.pdf`

**Title:** A Comparative Study of ChatGPT, Other AI Models and Human Responses 
for Optimal Support in Mental Health Care

M.Sc. Computer Science, University of Mumbai (2021–2023)

Evaluated whether LLMs can substitute for human psychologists in mental health 
support. Benchmarked five AI systems against human expert responses across 50 
clinical queries using NLTK similarity metrics and VADER sentiment analysis. 
Built a full Django web application with MySQL backend for live evaluation and 
comparison.

Key finding: ChatGPT achieved 55–70% similarity to human expert responses for 
common disorders but dropped to 21% for bipolar disorder — indicating a 
structured clinical reasoning gap that LLM training alone cannot close.

---

## Contact
**Email:** sakinahashmi990@gmail.com  
**GitHub:** [driftingmeadow](https://github.com/driftingmeadow)
