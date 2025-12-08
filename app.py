from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import soupsieve
from urllib.parse import urlparse

app = Flask(__name__)

USER_AGENT = "Mozilla/5.0 (compatible; LocalScraper/1.0; +https://example.com)"
HEADERS = {"User-Agent": USER_AGENT}


class ScrapeError(Exception):
    """Custom error for scraping problems."""


def validate_url(url: str) -> str:
    if not url:
        raise ScrapeError("L'URL est requise.")

    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ScrapeError("Veuillez fournir une URL complète commençant par http ou https.")
    return url


def fetch_content(url: str) -> str:
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
    except requests.RequestException as exc:
        raise ScrapeError(f"Impossible de contacter le site : {exc}") from exc

    if not response.ok:
        raise ScrapeError(f"Le site a renvoyé une erreur ({response.status_code}).")

    return response.text


def extract_elements(html: str, selector: str):
    soup = BeautifulSoup(html, "html.parser")
    try:
        elements = soup.select(selector)
    except soupsieve.SelectorSyntaxError as exc:
        raise ScrapeError("Le sélecteur CSS est invalide.") from exc
    if not elements:
        raise ScrapeError("Aucun élément trouvé pour ce sélecteur.")
    return [
        {
            "html": element.prettify(),
            "text": element.get_text(strip=True),
        }
        for element in elements
    ]


@app.route("/", methods=["GET", "POST"])
def index():
    data = []
    error = None
    url = ""
    selector = ""

    if request.method == "POST":
        url = request.form.get("url", "").strip()
        selector = request.form.get("selector", "").strip() or "p"
        try:
            valid_url = validate_url(url)
            html = fetch_content(valid_url)
            data = extract_elements(html, selector)
        except ScrapeError as err:
            error = str(err)

    return render_template("index.html", data=data, error=error, url=url, selector=selector or "p")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
