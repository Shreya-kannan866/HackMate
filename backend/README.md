# HackMate Backend — Person C Starter

## Run locally

You need a Postgres instance running. Easiest way if you don't have Postgres installed — run it in Docker:
```
docker run --name hackmate-db -e POSTGRES_USER=hackmate -e POSTGRES_PASSWORD=hackmate -e POSTGRES_DB=hackmate -p 5432:5432 -d postgres
```

Then:
```
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```
Then open http://localhost:8000/docs for interactive API docs.

If your team is sharing one real Postgres instance (e.g. on Render) instead of running it locally, just set `DATABASE_URL` in `.env` to that connection string instead.

## What's here
- Full [Shared] scaffolding: core/config.py, database/session.py, database/base.py, main.py
- A dummy `dependencies/auth.py` standing in for Person A's real Auth — swap it out once real JWT auth exists
- Roadmaps module fully built (model → schema → repository → service → route) as a template

## What's next (Track C, in order)
1. Copy the Roadmaps pattern to build Mock Hackathons (app/models/mock_hackathon.py, etc.)
2. Wait for Person B's `teams` table before starting Workspace models (messages/tasks/resources need team_id FK)
3. You can start `routes/websocket.py` early against a hardcoded team_id to de-risk the chat implementation
