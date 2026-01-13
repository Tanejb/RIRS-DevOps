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

Docker slike se avtomatsko gradijo in pushajo na Docker Hub z različnimi tagi glede na okolje:
- **Development** (master veja): `dev` in `dev-<commit-sha>`
- **Production** (production veja): `prod` in `prod-<commit-sha>`

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
  - Push na Docker Hub z okoljskimi tagi (`dev` za Development, `prod` za Production)
- **GitHub Pages:**
  - Avtomatizirano nameščanje statične dokumentacije
- **Caching:**
  - npm cache za frontend odvisnosti
  - pip cache za Python odvisnosti

Workflow se zažene ob:
- Push na `master`, `pre-production`, `production`, ali `feature/*` veje
- Pull request na glavne veje

### GitHub Environments

Projekt uporablja GitHub Environments za ločevanje Development in Production okolij:

#### Nastavitev Environments

1. Odpri repozitorij na GitHubu
2. Pojdi v **Settings** → **Environments**
3. Ustvari dva okolja:

   **Development:**
   - Ime: `Development`
   - Protection rules: Ni potrebno (avtomatsko deployment)
   - Deployment branches: `master` veja

   **Production:**
   - Ime: `Production`
   - Protection rules: ✅ **Required reviewers** (dodaj sebe kot reviewerja)
   - Deployment branches: `production` veja
   - Wait timer: Opcijsko (lahko nastaviš časovni zamik)

#### Kako deluje:

- **Master veja** → Avtomatsko namešča Docker slike z `dev` tagom v **Development** okolje
- **Production veja** → Zahteva **ročno odobritev** pred nameščanjem Docker slik z `prod` tagom v **Production** okolje

Ko se spremembe pushajo na `production` vejo, bo GitHub Actions zahteval ročno odobritev pred izvedbo Docker build jobs. Odobritev lahko opraviš v zavihku **Actions** → izberi workflow run → **Review deployments**.

## GitHub Flow

Projekt uporablja GitHub Flow z naslednjimi vejami:
- `master` - glavna razvojna veja
- `pre-production` - pre-produkcijska veja
- `production` - produkcijska veja
- `feature/*` - kratkoživeče veje za nove funkcionalnosti

---

## Monitoring, Varnost in Optimizacija Cevovoda

Ta razdelek opisuje implementirane monitoring orodja, varnostne skeniranja in optimizacije CI/CD cevovoda.

### 📊 Datadog Integracija

**Namen:** Spremljanje metrik CI/CD procesov za identifikacijo ozkih grl in optimizacijo.

**Implementacija:**
- Integracija z GitHub Actions z uporabo `masci/datadog@v1` action
- Zbiranje metrik za vse jobe v cevovodu:
  - **Job duration** - trajanje posameznih jobov
  - **Test metrics** - število testov, coverage percentage
  - **Artifact sizes** - velikost build artifactov (backend-coverage, frontend-coverage, sonarcloud-report, backend-build, frontend-build, github-pages)
  - **Job status** - uspešnost/neuspešnost jobov

**Zbrane metrike:**
- `ci.job.duration` - trajanje jobov (tagged by job name, branch, status)
- `ci.tests.total` - skupno število testov
- `ci.coverage.percent` - coverage percentage (backend/frontend)
- `ci.artifact.size_kb` - velikost artifactov v KB
- `ci.job.status` - status joba (1 = success, 0 = failure)
- `ci.sonarcloud.quality_gate.status` - status SonarCloud Quality Gate

**Dashboard:**
- Ustvarjen custom dashboard v Datadog za vizualizacijo metrik
- Grafiki za job duration, coverage trends, artifact sizes
- Grouping po job names in branch names za primerjavo

**Zaslonski posnetek:** Datadog dashboard z metrikami CI/CD procesov

**Ugotovitve:**
- SonarCloud jobi so najdaljši (odvisni od SonarCloud API-ja)
- Build jobi so relativno hitri zaradi caching mehanizmov
- Coverage se vzdržuje nad 80% (zahteva SonarCloud Quality Gate)

---

### 🔒 GitHub Code Scanning (CodeQL)

**Namen:** Avtomatsko odkrivanje varnostnih ranljivosti v kodi.

**Implementacija:**
- Omogočen CodeQL analysis v GitHub Security tabu
- Avtomatsko skeniranje ob vsakem push in pull request
- Analiza Python in JavaScript kode

**Najdene ranljivosti:**
- **18 medium-severity opozoril** identificiranih v začetni analizi

**Odpravljene ranljivosti:**
1. ✅ **Hardcoded JWT Secret Key** - Premaknjeno v environment variable (`JWT_SECRET_KEY`)
2. ✅ **JWT Token Expiration** - Nastavljeno na 24 ur (86400 sekund)
3. ✅ **CORS Configuration** - Implementirana konfiguracija z `ALLOWED_ORIGINS` environment variable namesto wildcard (`*`)
4. ✅ **Input Validation** - Dodana validacija za:
   - Username: 3-50 znakov
   - Password: 6-128 znakov
   - Todo title: max 200 znakov
   - Todo description: max 1000 znakov
5. ✅ **Exception Handling** - Specifični exception handling za `InvalidId` v MongoDB operacijah

**Ostale ranljivosti:**
- **localStorage security issues** - Pustili kot so (sprejemljivo za to aplikacijo)
- **Information exposure through exceptions** - Pustili kot so (ni kritično za development aplikacijo)

**Zaslonski posnetek:** GitHub Security tab z CodeQL rezultati

**Rezultat:**
- Večina kritičnih ranljivosti odpravljena
- Koda zdaj uporablja best practices za varnost
- Testi prilagojeni novim validacijskim pravilom

---

### 🐳 Snyk Container Scanning

**Namen:** Odkrivanje ranljivosti v Docker slikah in base image-ih.

**Implementacija:**
- Integracija Snyk z GitHub repozitorijem
- Skeniranje Dockerfile datotek:
  - `app/backend/Dockerfile`
  - `app/frontend/Dockerfile`

**Rezultati skeniranja:**

**Backend Dockerfile (`app/backend/Dockerfile`):**
- **23 Low-severity ranljivosti**
- Vse ranljivosti iz base image-a (`python:3.11-slim` - Debian base)
- Primer: `glibc/libc-bin - Out-of-Bounds` (CVE-2019-1010022)
- **NO KNOWN EXPLOIT** - ni znanega eksploita za te ranljivosti

**Frontend Dockerfile (`app/frontend/Dockerfile`):**
- **0 ranljivosti**
- Uporablja Alpine Linux base image (`node:20-alpine`, `nginx:alpine`), ki je varnostno boljši

**Odprava ranljivosti:**
- Ranljivosti niso odpravljene, ker:
  1. Vse so **LOW severity** - nizka prioriteta
  2. **NO KNOWN EXPLOIT** - ni znanega eksploita
  3. Ranljivosti so v base image-ih, ki jih redno posodabljajo vzdrževalci
  4. Za development/test aplikacijo ni kritično

**Možne izboljšave (opcijsko):**
- Posodobitev na najnovejšo verzijo `python:3.11-slim`
- Prehod na Alpine verzijo (`python:3.11-alpine`) - lahko povzroči težave z nekaterimi paketi

**Zaslonski posnetek:** Snyk dashboard z rezultati skeniranja Dockerfile datotek

---

### ⚙️ Optimizacije Cevovoda

**1. Permissions Optimization (Security Best Practice)**
- Dodani eksplicitni `permissions` bloki na vse jobe
- Implementiran "principle of least privilege"
- Minimalna dovoljena dovoljenja:
  - `contents: read` - za checkout kode
  - `actions: read` - za download/upload artifacts
  - `pages: write`, `id-token: write` - samo za deploy-pages job

**Popravljeni jobi:**
- `backend-tests`, `frontend-tests`, `sonarcloud-analysis`, `sonarcloud-quality-gate`, `backend-build`, `frontend-build` - `contents: read`, `actions: read`
- `docker-backend-dev`, `docker-frontend-dev`, `docker-backend-prod`, `docker-frontend-prod` - `contents: read`
- `deploy-pages` - že imel permissions (nespremenjeno)

**2. Code Coverage Optimization**
- Dodani dodatni testi za povečanje coverage-ja nad 80%
- Pokriti edge cases in error handling scenariji
- Coverage: **92%** (nad zahtevanimi 80%)

**3. Artifact Management**
- Eksplicitno imenovanje artifactov za GitHub Pages deployment
- Rešitev problema z več artifacti z istim imenom

**4. SonarCloud Integration**
- Dodane metrike za SonarCloud job duration v Datadog
- Tracking Quality Gate status

---

### 📈 Identificirane Težave in Rešitve

**1. SonarCloud Quality Gate - Coverage Issue**
- **Problem:** Coverage pod 80% (66.7%)
- **Rešitev:** Dodani dodatni testi za input validation, edge cases, error handling
- **Rezultat:** Coverage povečan na 92%

**2. GitHub Pages Deployment Timeout**
- **Problem:** Deployment job timeouta po 11 minutah, ostane v `deployment_queued` statusu
- **Analiza:** Problem z GitHub Pages deployment queue (ne z našo konfiguracijo)
- **Rešitev:** Eksplicitno imenovanje artifacta (`name: github-pages`) za boljšo identifikacijo
- **Status:** Delno rešeno - občasno še vedno timeouta zaradi GitHub Pages queue

**3. Multiple Artifacts with Same Name**
- **Problem:** `deploy-pages` action najde več artifactov z istim imenom
- **Rešitev:** Dodan `name: github-pages` v `upload-pages-artifact` in `artifact_name: github-pages` v `deploy-pages`

**4. CodeQL Security Warnings**
- **Problem:** 18 medium-severity opozoril
- **Rešitev:** Implementirane varnostne izboljšave (JWT, CORS, input validation)
- **Rezultat:** Večina kritičnih ranljivosti odpravljena

---

### 📊 Povzetek Stanja Cevovoda

**Trenutno stanje:**
- ✅ **Testiranje:** 33 testov (12 backend, 21 frontend) - vse uspešno
- ✅ **Coverage:** 92% (backend), nad zahtevanimi 80%
- ✅ **SonarCloud:** Quality Gate prehaja
- ✅ **Docker:** Avtomatska gradnja in push na Docker Hub
- ✅ **Monitoring:** Datadog dashboard z metrikami
- ✅ **Varnost:** CodeQL in Snyk skeniranja aktivna
- ⚠️ **GitHub Pages:** Občasno timeouta (problem z GitHub queue)

**Optimizacije:**
- Caching za npm in pip dependencies
- Parallel execution kjer je možno
- Minimalna permissions za vse jobe
- Tracking metrik za identifikacijo ozkih grl

**Zaslonski posnetki:**
- Datadog dashboard z CI/CD metrikami
- GitHub Security tab z CodeQL rezultati
- Snyk dashboard z Dockerfile skeniranji
- SonarCloud Quality Gate status

