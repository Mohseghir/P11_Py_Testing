import pytest
from server import app

# Création d'une fixture 'test_client' pour les tests Flask
@pytest.fixture
def test_client():
    # Utilisation d'un contexte 'with' pour gérer automatiquement la fermeture du test_client après utilisation
    with app.test_client() as test_client:
        # Fournit le test_client de test aux tests qui l'utilisent
        yield test_client
        # nettoyage apres exe (contrairement à return)

