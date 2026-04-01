 Revit-AI-Assistant
A custom pyRevit tool that integrates a local Large Language Model (Llama 3 via Ollama) directly into Autodesk Revit. Also have two more pyRevit tools to help you automate electrical calculations.

  Revit MEP Automation & AI Integration Suite

This repository contains a powerful suite of custom pyRevit tools developed in Python to automate complex MEP design tasks within Autodesk Revit. By combining my background in **Electrical & Electronics Engineering** with my Master's studies in **Computer Engineering**, I focus on building tools that move beyond traditional drafting and enable true computational BIM and secure on-site AI assistant integration.

The goal is to eliminate repetitive data handling and complex geometric analysis, allowing engineers to focus on high-level decision-making.

---

  Projects Overview

  Project 1: Electrical Load Exporter & Analyzer (Data Automation)
- Objective: Securely extract live electrical panel data from the active Revit model and export a structured analysis report.
- Problem: Manually checking and exporting dozens of panel schedules is time-consuming and prone to errors.
- Solution: A one-click tool that collects panel names, total loads, and voltage levels. It analyzes capacity status against defined limits and exports the data to a clean CSV/Excel file on the user's desktop.
- Tech Stack: Python, Revit DB API, `csv` module, `pyrevit.forms`.

  Project 2: Auto-Place Electrical Devices via Room Centroids (Geometry Automation)
- Objective: Automate the placement of repetitive devices (smoke detectors, fixtures) at the precise geometric center of rooms.
- Problem: Manually placing hundreds of identical elements in large projects takes days.
- Solution: An intelligent script that detects all defined rooms, performs spatial analysis to calculate their bounding box centroids, and uses the `doc.Create.NewFamilyInstance` API method to place elements instantly in all selected rooms.
- Tech Stack: Python, Revit Geometry API (BoundingBox), Transaction Management.

  Project 3: Secured Local BIM AI Assistant (AI & LLM Integration)
- Objective: Implement a local, secure AI assistant directly in the Revit interface for querying model data using natural language (NLP).
- Problem: Finding specific information in complex BIM models (e.g., "Which panels are overloaded?") often requires manual filtering or advanced knowledge of schedules. Standard cloud AI APIs introduce security risks.
- Solution: A custom tool featuring a dark-themed UI (Output window) that integrates a local Large Language Model (Llama 3 via Ollama) and a Retrieval-Augmented Generation (RAG) architecture. The Python script automatically extracts live model context (panel lists, loads) and injects it into the prompt. The AI analyzes this contextual data without any information leaving the local machine.
- Tech Stack: Python, Revit API, `requests` module, pyRevit UI/Output, Ollama, Llama 3.

---

  RAG Architecture (Retrieval-Augmented Generation)

Project 3 uses a powerful Retrieval-Augmented Generation (RAG) model to solve the problem of AI "hallucination" and data security in engineering workflows.

The architecture follows these steps:
1. Model Context Collection (Python): The script executes a `FilteredElementCollector` to retrieve all electrical panel instances. It parses their parameters ("Total Connected Load", "Panel Name") and builds a clean context string.
2. Context Injection: When the user enters a natural language query (e.g., "Analyze the capacity status"), the script constructs a "system prompt" that defines the AI's role and appends the live context string and user question.
3. Local LLM Query (Ollama/Llama 3):** The final prompt (Context + Question) is sent via local API request (`requests.post`) to the LLM server running on the user's machine. Llama 3 processes the request.
4. Structured Response:** The model analyzes the engineering data and returns a natural language answer. This response is displayed in the custom pyRevit output window.
   - Key Advantage: This "zero-internet" architecture ensures all sensitive project data stays local while providing a powerful NLP interface for complex engineering queries.

---

  How to Use This Repo
1. **Requirements:** Autodesk Revit 2024 or higher, [pyRevit](https://github.com/eirannejad/pyRevit) installed, [Ollama](https://ollama.com/) (for Project 3).
2. **Installation:** Add the `MyTools.extension` directory to your custom extensions path in pyRevit settings and reload.
3. **Running the AI Assistant:** Ensure Ollama with the `llama3` model is running (`ollama run llama3`). Click the AI button and prompt the model in English.

Developed by Osman Taylan Gökçen | https://www.linkedin.com/in/taylan-gokcen/

<img width="891" height="591" alt="image" src="https://github.com/user-attachments/assets/cb8b3d8f-b562-4c51-89e4-f05e798bbc49" />
