<div align="center">

# 🔬 ResearchMind

### **A multi-agent AI research assistant that turns a topic into a researched, written, and critiqued report.**

**[🚀 Open the live app](https://researchmind-3dfclx17n-sakshampachauri558-2538.vercel.app/)**

<br>

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/Agents-LangChain-1C3C3C)
![Deployment](https://img.shields.io/badge/Deployed%20on-Vercel-000000?logo=vercel&logoColor=white)

</div>

---

## **✨ Overview**

ResearchMind takes a topic you enter and coordinates **four AI research stages**
to deliver a detailed report:

1. **Search** — finds recent web results with Tavily.
2. **Read** — selects a relevant result and extracts useful page content.
3. **Write** — creates a structured report with an introduction, key findings,
   conclusion, and sources.
4. **Critique** — independently reviews the report and returns a score,
   strengths, and areas to improve.

The interface shows each stage as it runs, presents the report and agent
outputs, and lets you **download the report as Markdown**.

> **Live demo:** [Open ResearchMind directly on Vercel](https://researchmind-3dfclx17n-sakshampachauri558-2538.vercel.app/).
> **Access note:** The current Vercel deployment may require authorization if
> deployment protection is enabled. A project owner can change this in the
> Vercel project's **Settings → Deployment Protection**.

## **🧰 Technology**

| **Component** | **Technology** | **Purpose** |
|---|---|---|
| Web interface | HTML, CSS, JavaScript | Responsive research UI and streaming progress |
| Web application | [FastAPI](https://fastapi.tiangolo.com/) | Serves the UI and research API |
| AI orchestration | [LangChain](https://www.langchain.com/) | Connects agents, tools, prompts, and model calls |
| Language model | [Mistral AI](https://mistral.ai/) | Powers web research, report writing, and critique |
| Web search | [Tavily](https://tavily.com/) | Finds relevant web pages and search snippets |
| Page extraction | [Requests](https://requests.readthedocs.io/), [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), [lxml](https://lxml.de/) | Fetches pages and extracts readable content |
| Hosting | [Vercel](https://vercel.com/) | Deploys the FastAPI application |

## **🔗 Services and API links**

The app uses these external services:

- **Mistral API** — [Documentation](https://docs.mistral.ai/) · [API keys](https://console.mistral.ai/api-keys/)
- **Tavily Search API** — [Documentation](https://docs.tavily.com/) · [API keys](https://app.tavily.com/home)
- **LangChain** — [Documentation](https://docs.langchain.com/oss/python/langchain/overview)
- **Vercel** — [Python runtime documentation](https://vercel.com/docs/functions/runtimes/python) · [FastAPI deployment guide](https://vercel.com/docs/frameworks/backend/fastapi)

**The application does not require users to visit or edit `vercel.json` to try
the live website.** Open the live app link above and enter a research topic.
API credentials are stored in the server environment, not in the browser.

## **🖥️ Run locally**

### **Requirements**

- **Python 3.12 or later**
- A **Mistral API key**
- A **Tavily API key**

### **1. Install the project**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

### **2. Configure API credentials**

Open `.env` and add your own keys:

```dotenv
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
MISTRAL_MODEL=ministral-14b-latest
```

`MISTRAL_MODEL` is optional. The default, **`ministral-14b-latest`**, was
selected for the configured Mistral account. If you change it, use a model
available to your account.

### **3. Start the app**

```powershell
uvicorn app:app --reload
```

Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

## **☁️ Deploy your own copy to Vercel**

1. Create or import your GitHub repository in **[Vercel](https://vercel.com/)**.
2. In **Project Settings → Environment Variables**, add:
   - **`MISTRAL_API_KEY`**
   - **`TAVILY_API_KEY`**
   - **`MISTRAL_MODEL`** (optional; defaults to `ministral-14b-latest`)
3. Select the environments you need and **redeploy** after setting or changing
   variables.

Vercel detects the FastAPI app in `app.py`. The included `vercel.json` contains
deployment configuration; it is not needed to open or use the live demo.

### **Publish the source on GitHub**

Create an empty **public** GitHub repository, then run these commands from the
project folder (replace the placeholders with your repository details):

```powershell
git add .
git commit -m "Prepare ResearchMind for public release"
git branch -M main
git remote add origin https://github.com/<YOUR-USERNAME>/<YOUR-REPOSITORY>.git
git push -u origin main
```

**Never commit your `.env` file or paste real API keys into GitHub.** The
repository ignores `.env`; `.env.example` contains blank placeholders for
local setup.

## **🔌 API reference**

The backend exposes these endpoints:

### **`GET /api/health`**

Returns a small status response when the app is running:

```json
{
  "status": "ok"
}
```

### **`POST /api/research`**

Starts the research pipeline. The topic must contain **1–200 characters**.

**Request:**

```json
{
  "topic": "Recent advances in renewable energy storage"
}
```

**Response:** a **Server-Sent Events (SSE)** stream with progress and stage
results. Events use `step` and `status` fields; the final successful event has
`"step": "complete"`. If a provider or pipeline step fails, the stream reports
an error event.

## **📁 Project structure**

```text
.
├── agents.py          # Mistral model, search and reader agents, writer and critic
├── app.py             # FastAPI app, health check, and streaming research endpoint
├── pipeline.py        # Reusable four-stage research workflow
├── tools.py           # Tavily search and webpage scraping tools
├── public/
│   └── index.html     # Browser interface
├── requirements.txt   # Python dependencies
├── vercel.json        # Vercel deployment configuration
└── .env.example       # Blank environment-variable template
```

## **🔐 Privacy and usage**

- **API keys stay on the server.** Keep them in `.env` locally and in Vercel
  Environment Variables when deployed.
- Each research run calls **Mistral** and **Tavily** and uses the quotas or
  billing associated with those accounts.
- Research depends on third-party model availability, search results, and
  website access. Generated answers should be checked against their sources.
- Making a Vercel deployment public allows visitors to submit research
  requests using the owner's configured API accounts. **Consider this before
  changing deployment protection.**
