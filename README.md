
# UsedFinder – MVP template

Questo repository contiene un prototipo completo (crawler → matcher → notifiche → API) per un portale di annunci dell’usato.

1. Copia `.env.example` in `.env` e compila le variabili.
2. `docker compose up --build`
3. POST `/search` con `{"term":"vespa 125"}` su `localhost:8000`.
