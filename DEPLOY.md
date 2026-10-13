# 🚀 Deployment Guide — Swift Sign Group AI Assistant

This project deploys to **Vercel**. Pushing to the `main` branch on GitHub
automatically triggers a new production deployment (if the Vercel project is
connected to this repo).

## Architecture on Vercel
- **Frontend** — the static site in `frontend/` is served at the root (`/`).
- **API** — the Python serverless function in `api/chat.py` is served at `/api/chat`.
- The chat widget automatically calls `/api/chat` in production and
  `http://127.0.0.1:8000/api/chat` when running locally.

## 1) Push the code (run this in the project folder)
```bash
git push origin main
```
> A GitHub login window may appear the first time — sign in to authorize the push.

## 2) Set the API key in Vercel (REQUIRED)
The AI will NOT answer questions until the Gemini key is configured, because
`.env` files are never uploaded to Vercel.

1. Go to https://vercel.com → your project → **Settings → Environment Variables**.
2. Add:
   - **Key:** `GEMINI_API_KEY`
   - **Value:** your Google Gemini API key (from https://aistudio.google.com)
   - **Environment:** Production (and Preview, optional)
3. Click **Save**, then **Redeploy** (Deployments → ⋯ → Redeploy).

## 3) Verify
- Open your Vercel URL (e.g. `https://<project>.vercel.app`).
- Click the blue chat button (bottom-right) and ask: *"What services do you offer?"*
- Greetings reply instantly; real questions return AI answers within a few seconds.

---

## Running locally (development)
```bash
# 1. Create/activate the virtual environment and install deps
python -m venv venv
venv\Scripts\activate            # Windows
pip install -r requirements.txt

# 2. Put your key in backend\.env
echo GEMINI_API_KEY=your_key_here > backend\.env

# 3. Start the backend (serves http://127.0.0.1:8000)
start.bat                        # or: python run.py

# 4. Open the frontend
#    Open frontend/index.html in your browser
```

## Run the tests
```bash
venv\Scripts\python.exe test_app.py
```

## Automated testing (GitHub Actions)
Every push / pull request to `main` runs `.github/workflows/ci.yml`, which:
1. Installs dependencies from `requirements.txt`
2. Runs the test suite (`test_app.py`)
3. Verifies the Vercel serverless function imports correctly

You'll see a green ✅ (or red ❌) next to each commit on GitHub under the **Actions** tab.

---

## Option B: Deploy the full backend to Render
`render.yaml` defines a Render web service that hosts the **complete** FastAPI
backend (API + admin endpoints + SQLite database).

1. Go to https://dashboard.render.com → **New → Blueprint** and connect this repo.
2. Render reads `render.yaml` automatically.
3. Add the secret **`GEMINI_API_KEY`** in the Render dashboard when prompted
   (it is marked `sync: false`, so it is never stored in the repo).
4. Deploy — Render gives you a URL like `https://swiftsign-chatbot-api.onrender.com`.

To point the frontend at the Render backend instead of the local one, set this
before loading the page (e.g. in a `<script>` in `index.html` or the console):
```js
window.SWIFTSIGN_API_URL = 'https://swiftsign-chatbot-api.onrender.com/api/chat';
```

