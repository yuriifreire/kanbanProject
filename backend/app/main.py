from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import board, column, card

# Cria todas as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="Kanban Board API",
    description="API completa para gerenciamento de quadro Kanban",
    version="1.0.0",
    contact={
        "name": "Yuri Freire",
        "email": "yuriifreire@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Configura CORS (para desenvolvimento)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, substitua por seus domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui todas as rotas
app.include_router(board.router)
app.include_router(column.router)
app.include_router(card.router)

# Rota de health check
@app.get("/health", tags=["Health Check"])
async def health_check():
    return {
        "status": "healthy",
        "message": "Kanban API is running",
        "version": app.version
    }

# Rota raiz com documentação
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Bem-vindo à API de Quadro Kanban",
        "documentation": [
            {
                "description": "Documentação interativa (Swagger UI)",
                "url": "/docs"
            },
            {
                "description": "Documentação alternativa (ReDoc)",
                "url": "/redoc"
            },
            {
                "description": "Health Check",
                "url": "/health"
            }
        ],
        "endpoints": {
            "boards": "/boards",
            "columns": "/columns",
            "cards": "/cards"
        }
    }