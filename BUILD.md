# Getting Started

This guide covers everything needed to go from a fresh clone to running notebooks.

## Prerequisites

- Python 3.11 or later — check with `python --version`
- API keys for [OpenAI](https://platform.openai.com/api-keys) and [Tavily](https://app.tavily.com)

## 1. Create and activate a virtual environment

```bash
# Create the environment (one-time)
python -m venv .venv

# Activate — Linux / macOS
source .venv/bin/activate

# Activate — Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Activate — Windows (cmd.exe)
.venv\Scripts\activate.bat
```

You should see `(.venv)` in your terminal prompt after activation.

## 2. Install dependencies

```bash
pip install -e .
```

The `-e` flag installs the project in editable mode so the `shared/` utilities are importable from any notebook without path tricks.

## 3. Configure API keys

```bash
cp .env.example .env
```

Open `.env` and fill in your keys:

```
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
```

The `ANTHROPIC_API_KEY` line is optional — only Lectures 1–3 use OpenAI and Tavily.

## 4. Register the virtual environment as a Jupyter kernel

```bash
python -m ipykernel install --user --name ai-agents --display-name "AI Agents Course"
```

This makes the kernel available inside VS Code, JupyterLab, and classic Notebook.

## 5. Open a notebook

**VS Code**
1. Open any `lectureN_*/notebookN.ipynb` file.
2. Click "Select Kernel" in the top-right corner and choose **AI Agents Course**.

**JupyterLab / classic Notebook**
```bash
jupyter lab
# or
jupyter notebook
```
Navigate to the lecture folder and open the notebook. Select the **AI Agents Course** kernel from the *Kernel* menu if it is not already active.

## Lecture order

| Notebook | Topic |
|----------|-------|
| [lecture1_minimal_loop/notebook1.ipynb](lecture1_minimal_loop/notebook1.ipynb) | Minimal agent loop — raw OpenAI, no frameworks |
| [lecture2_memory_rag/notebook2.ipynb](lecture2_memory_rag/notebook2.ipynb) | Memory and RAG with Chroma |
| [lecture3_graphs_planning/notebook3.ipynb](lecture3_graphs_planning/notebook3.ipynb) | Graphs and planning with LangGraph + Tavily |
| [lecture4_multi_agent/notebook4.ipynb](lecture4_multi_agent/notebook4.ipynb) | Multi-agent systems |

Run notebooks from top to bottom — each cell builds on the previous one.

## Deactivating the environment

When you are done, deactivate with:

```bash
deactivate
```

## Troubleshooting

**`ModuleNotFoundError: No module named 'shared'`**
Re-run `pip install -e .` with the virtual environment active.

**Kernel not appearing in VS Code**
Re-run the `ipykernel install` command, then reload the VS Code window (`Ctrl+Shift+P` → "Developer: Reload Window").

**API key not found at runtime**
Make sure `.env` exists (not just `.env.example`) and the virtual environment is active when you start Jupyter.
