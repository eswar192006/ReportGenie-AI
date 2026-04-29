# ReportGenie AI: Automated KPI Reporter

ReportGenie AI is a business analytics application for teams that generate weekly and monthly reports from structured CSV data. Instead of manually calculating metrics and drafting narrative summaries, the system uses an LLM plus approved KPI and chart tools to produce a complete, data-driven business report.

## Overview

ReportGenie AI combines a Python FastAPI backend, a React + Tailwind frontend, and an LLM-powered insights layer to turn CSV sales and performance data into actionable reports.

## Key Features

- Drag-and-drop CSV upload for quick dataset exploration
- Automatic schema detection and preview table
- Hybrid schema detection with heuristic profiling and optional local-LLM schema assist
- KPI engine for revenue, growth, averages, trends, and anomaly flags
- Interactive charts for line, bar, and pie visualizations
- LLM-driven report generation that uses tool outputs as the basis for insights
- Story mode with narrative sections that guide report readers
- Tool-aware AI chat panel for follow-up questions on analyzed datasets
- Shareable live report links and downloadable insights JSON

## Use Cases and Scenarios

- Scenario: weekly sales review
  - Import the latest store sales CSV, automatically compute revenue, growth, category mix, and anomalies, then generate a narrative summary for leadership.
- Scenario: product launch performance
  - Analyze launch-period sales data, compare category performance, surface key wins and risks, and create a concise report for marketing and product teams.
- Scenario: regional performance monitoring
  - Upload region-level sales data, generate trend charts and KPIs, and deliver a scenario-based narrative for regional sales managers.
- Scenario: executive summary creation
  - Convert raw CSV data into a polished report with charts, insights, and follow-up Q&A capability.

## Architecture

- Backend: FastAPI, Pandas, Plotly
- Frontend: React, Tailwind CSS, Framer Motion, Vite
- AI layer: Ollama-compatible tool-augmented LLM with graceful fallback mode
- Tool pattern: `calculate_kpis(data)` and `generate_chart(data, type)`
- MCP layer: JSON-RPC tool discovery and invocation for `initialize`, `tools/list`, and `tools/call`

## Project Structure

- `app/main.py` - FastAPI app and static frontend serving
- `app/routes/report.py` - analysis, chat, sample, and report APIs
- `services/csv_service.py` - schema detection, preview generation, CSV normalization
- `services/kpi_service.py` - KPI and anomaly engine
- `services/chart_service.py` - tool-based chart generation and Plotly payloads
- `services/llm_service.py` - AI orchestration prompts, agent decisions, and fallbacks
- `services/tool_service.py` - approved KPI/chart tool implementations
- `services/mcp_service.py` - MCP-style JSON-RPC tool server and client helpers
- `services/report_service.py` - persistent live-report storage
- `frontend/` - React + Tailwind + Framer Motion app
- `outputs/reports/` - saved live report payloads

## Setup

### Backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
npm run build
cd ..
```

## Optional Ollama Setup

InsightForge AI works without Ollama by falling back to deterministic insight copy, but the premium AI insight and chat layers improve when Ollama is running.

```bash
ollama pull mistral:latest
ollama serve
```

Optional environment variables:

- `OLLAMA_HOST` defaults to `http://localhost:11434`
- `OLLAMA_MODEL` defaults to `mistral:latest`
- `OLLAMA_TIMEOUT_SECONDS` defaults to `20`
- `SCHEMA_LLM_ASSIST` defaults to `1` and enables local-LLM help for unfamiliar CSV schemas
- `SCHEMA_LLM_CONFIDENCE_THRESHOLD` defaults to `1.35` and controls when schema assist kicks in

## Run

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open in your browser:

```text
http://localhost:8000
```

## API Endpoints

- `POST /api/analyze` - upload a CSV and build the full InsightForge AI report payload
- `POST /api/chat` - ask follow-up questions against a saved report
- `GET /api/reports/{report_id}` - reopen a saved live report
- `GET /api/sample` - fetch the sample dataset path
- `GET /api/tools` - inspect the available analytics tools
- `POST /api/mcp` - MCP JSON-RPC endpoint for tool discovery and tool calls

## Verification Completed

- Frontend production build succeeds with Vite
- FastAPI imports correctly
- Sample CSV analysis succeeds and returns KPI, chart, story, and shareable report data
- Chat endpoint succeeds in fallback mode when Ollama is unavailable

## Production Deployment

ReportGenie AI is ready for production deployment. See [DEPLOYMENT.md](DEPLOYMENT.md) for complete instructions.

### Quick Start (Vercel + Railway)

1. **Deploy Frontend to Vercel**
   ```bash
   git push
   ```
   Frontend automatically deploys to your Vercel account.

2. **Deploy Backend to Railway**
   - Connect your GitHub repo at https://railway.app
   - Railway auto-deploys and provides a public URL

3. **Connect Frontend to Backend**
   - In Vercel dashboard, add environment variable:
   ```
   VITE_API_URL=https://your-railway-backend-url.railway.app
   ```

4. **Redeploy frontend** to pick up the new environment variable.

### Docker Support

Deploy with Docker:
```bash
docker build -t reportgenie-ai .
docker run -p 8000:8000 reportgenie-ai
```

Or with docker-compose:
```bash
docker-compose up
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions and alternative hosting platforms (Render, Heroku, etc.).
