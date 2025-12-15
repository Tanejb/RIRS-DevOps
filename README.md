# To-Do App - DevOps Project

Full-stack To-Do aplikacija z Flask backendom in React frontendom.

## Struktura projekta

```
app/
├── backend/          # Flask backend aplikacija
│   ├── app.py       # Glavna Flask aplikacija
│   ├── models.py    # MongoDB povezava in modeli
│   ├── routes/      # API route handlers
│   └── requirements.txt
└── frontend/        # React frontend aplikacija
    ├── src/
    └── package.json
```

## Nastavitev

### Backend

1. Namesti odvisnosti:
```bash
cd app/backend
pip install -r requirements.txt
```

2. Ustvari `.env` datoteko v `app/backend/` z:
```
JWT_SECRET_KEY=your-secret-key
MONGODB_URI=mongodb+srv://...
DATABASE_NAME=todoapp
```

3. Zaženi backend:
```bash
cd app/backend
python app.py
```

### Frontend

1. Namesti odvisnosti:
```bash
cd app/frontend
npm install
```

2. Zaženi frontend:
```bash
npm start
```

## GitHub Secrets (za CI/CD)

Za avtomatizirano testiranje v GitHub Actions moraš nastaviti naslednje secrets v repozitoriju:

1. Odpri repozitorij na GitHubu
2. Pojdi v **Settings** → **Secrets and variables** → **Actions**
3. Dodaj naslednje secrets:
   - `JWT_SECRET_KEY` - Secret key za JWT tokenje
   - `MONGODB_URI` - MongoDB connection string
   - `DATABASE_NAME` (opcijsko) - Ime baze podatkov (privzeto: `todoapp`)
   - `DOCKER_USERNAME` - Docker Hub uporabniško ime
   - `DOCKER_PASSWORD` - Docker Hub geslo ali access token

**Opomba:** Za lokalni razvoj še vedno uporabljaj `.env` datoteko v `app/backend/`.

## Docker

Projekt vključuje Dockerfile-e za oba dela aplikacije:

### Backend Docker Image
```bash
cd app/backend
docker build -t rirs-todo-backend .
docker run -p 5000:5000 --env-file .env rirs-todo-backend
```

### Frontend Docker Image
```bash
cd app/frontend
docker build -t rirs-todo-frontend .
docker run -p 80:80 rirs-todo-frontend
```

Docker slike se avtomatsko gradijo in pushajo na Docker Hub ob vsakem push-u na glavne veje.

## CI/CD

Projekt uporablja GitHub Actions za avtomatizirano:
- **Testiranje:**
  - Backend testi (12 testov) z coverage poročilom
  - Frontend testi (8 testov) z coverage poročilom
- **Gradnja:**
  - Backend build artefakt
  - Frontend build artefakt (React production build)
- **Docker:**
  - Gradnja Docker slik za backend in frontend
  - Push na Docker Hub (`<username>/rirs-todo-backend:latest`, `<username>/rirs-todo-frontend:latest`)
- **Caching:**
  - npm cache za frontend odvisnosti
  - pip cache za Python odvisnosti

Workflow se zažene ob:
- Push na `master`, `pre-production`, `production`, ali `feature/*` veje
- Pull request na glavne veje

## GitHub Flow

Projekt uporablja GitHub Flow z naslednjimi vejami:
- `master` - glavna razvojna veja
- `pre-production` - pre-produkcijska veja
- `production` - produkcijska veja
- `feature/*` - kratkoživeče veje za nove funkcionalnosti

