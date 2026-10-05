from fastapi import FastAPI
from app.invoice.routes import router as invoice_router

app = FastAPI(
    title="IntelliFlow AI",
    description="AI-Powered Business Automation Platform",
    version="1.0.0"
)


# Register Invoice Router
app.include_router(invoice_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
