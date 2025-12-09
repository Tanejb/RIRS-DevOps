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

## GitHub Flow

Projekt uporablja GitHub Flow z naslednjimi vejami:
- `master` - glavna razvojna veja
- `pre-production` - pre-produkcijska veja
- `production` - produkcijska veja
- `feature/*` - kratkoživeče veje za nove funkcionalnosti

