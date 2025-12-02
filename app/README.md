# To-Do App Backend

Flask backend za to-do aplikacijo z uporabniško avtentifikacijo.

## Nastavitev

1. Namesti dependencies:
```bash
pip install -r requirements.txt
```

2. Ustvari `.env` datoteko z naslednjo vsebino:
```
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/todoapp?retryWrites=true&w=majority
```

3. Zaženi aplikacijo:
```bash
python app.py
```

## API Endpoints

### Avtentifikacija
- `POST /api/auth/register` - Registracija uporabnika
- `POST /api/auth/login` - Prijava uporabnika
- `GET /api/auth/profile` - Profil uporabnika (zahteva JWT token)

### To-Do elementi
- `GET /api/todos/` - Pridobi vse to-do elemente (zahteva JWT token)
- `POST /api/todos/` - Ustvari nov to-do element (zahteva JWT token)
- `PUT /api/todos/<id>` - Posodobi to-do element (zahteva JWT token)
- `DELETE /api/todos/<id>` - Izbriši to-do element (zahteva JWT token)
- `PATCH /api/todos/<id>/toggle` - Preklopi status to-do elementa (zahteva JWT token)

## Testiranje

Uporabi Postman ali curl za testiranje API-jev. Ne pozabi dodati JWT token v Authorization header:
```
Authorization: Bearer <your-jwt-token>
```
