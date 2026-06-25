import pytest
from fastapi.testclient import TestClient
# On importe l'instance FastAPI depuis votre fichier principal (ajustez si votre fichier s'appelle différemment)
from main import app 

# On crée un client de test qui va simuler les requêtes HTTP
client = TestClient(app)

def test_read_history_status_code():
    """Vérifie que la route /history répond bien avec un code 200 (Succès)"""
    response = client.get("/history")
    assert response.status_code == 200

def test_read_history_format():
    """Vérifie que la route /history renvoie bien une liste (JSON)"""
    response = client.get("/history")
    assert response.status_code == 200
    # On vérifie que la réponse reçue est bien une structure de liste []
    assert isinstance(response.json(), list)