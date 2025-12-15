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

**Opomba:** Za lokalni razvoj še vedno uporabljaj `.env` datoteko v `app/backend/`.

## CI/CD

Projekt uporablja GitHub Actions za avtomatizirano testiranje:
- Backend testi (12 testov) z coverage poročilom
- Frontend testi (8 testov) z coverage poročilom
- Coverage artefakti so shranjeni v Actions zavihku

Workflow se zažene ob:
- Push na `master`, `pre-production`, `production`, ali `feature/*` veje
- Pull request na glavne veje

## GitHub Flow

Projekt uporablja GitHub Flow z naslednjimi vejami:
- `master` - glavna razvojna veja
- `pre-production` - pre-produkcijska veja
- `production` - produkcijska veja
- `feature/*` - kratkoživeče veje za nove funkcionalnosti

