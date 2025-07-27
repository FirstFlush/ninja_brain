from ninja import Router
from django.http import HttpRequest

router = Router()

@router.post("/predict")
def predict(request: HttpRequest, text: str):
    return {"entities": []} 