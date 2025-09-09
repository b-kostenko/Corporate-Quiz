

Create migrations:
```bash
alembic revision --autogenerate -m "initial user models"
```

Apply migrations:
```bash
alembic upgrade head
```