# Application de scraping local

Cette application web Flask permet de lancer un scraping simple sur un site public en fournissant une URL et un sélecteur CSS.

## Installation

1. Créez un environnement virtuel Python (optionnel mais recommandé).
2. Installez les dépendances :

```bash
pip install -r requirements.txt
```

## Utilisation

1. Lancez le serveur :

```bash
python app.py
```

2. Ouvrez votre navigateur sur `http://localhost:5000`.
3. Saisissez l'URL à analyser et un sélecteur CSS (par défaut `p`). Les éléments trouvés sont affichés avec leur texte et leur HTML.
4. En cas de sélecteur invalide ou d'absence de résultats, un message d'erreur clair est affiché dans l'interface.

### Test rapide

Pour vérifier rapidement que l'application fonctionne, vous pouvez utiliser `https://example.com` avec le sélecteur `p`, qui retournera les paragraphes visibles de la page de test par défaut du web.

## Remarques

- L'application ajoute un en-tête User-Agent basique pour limiter les blocages.
- Vérifiez que le scraping du site ciblé est autorisé (robots.txt, conditions d'utilisation).
