#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import json
import logging
from Parametres import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




# -------------------------------
# Configuration du logging
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger("ScrapPronote")

# -------------------------------
# Fonction d'attente d'un élément
# -------------------------------
def wait_for_element(driver, by, selector, wait_time=20):
    """Attend la présence d'un élément sur la page."""
    try:
        return WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((by, selector))
        )
    except TimeoutException:
        logger.warning("Timeout lors de l'attente de l'élément : %s", selector)
        return None

# -------------------------------
# Classe de connexion à Pronote
# -------------------------------
class ScrapPronote:
    def __init__(self):
        self.USERNAME = identifiant_pronote
        self.PASSWORD = mot_de_passe_pronote
        self.URL_LOGIN = url_page_de_connexion_pronote + url_pronote
        self.WAIT_TIME = 20

    def login(self, driver):
        logger.info("Accès à la page de connexion Pronote...")
        driver.get(self.URL_LOGIN)

        email_field = wait_for_element(driver, By.NAME, "email", self.WAIT_TIME)
        password_field = wait_for_element(driver, By.NAME, "password", self.WAIT_TIME)

        if not email_field or not password_field:
            raise Exception("Les champs de connexion ne sont pas accessibles.")

        email_field.send_keys(self.USERNAME)
        password_field.send_keys(self.PASSWORD)
        password_field.send_keys(Keys.RETURN)
        logger.info("Formulaire de connexion soumis.")

        # Attendre que la page d'accueil s'affiche (exemple avec une liste de cours)
        if not wait_for_element(driver, By.CSS_SELECTOR, "ul.liste-cours", self.WAIT_TIME):
            raise Exception("La page d'accueil Pronote ne semble pas chargée correctement.")
        logger.info("Connexion réussie, page d'accueil chargée.")

# -------------------------------
# Fonctions d'extraction des données
# -------------------------------
def parse_schedule(soup):
    """Extrait le planning depuis la section 'liste-cours'."""
    schedule = []
    ul = soup.find("ul", class_="liste-cours")
    if ul:
        for li in ul.find_all("li", class_="flex-contain", recursive=False):
            # Récupérer le texte caché qui contient l'heure et la matière
            sr_text = li.find("span", class_="sr-only").get_text(strip=True) if li.find("span", class_="sr-only") else ""
            # Exemple attendu : "de 8h30 à 10h25 ED.PHYSIQUE & SPORT."
            match = re.search(r"de\s+(\d{1,2}h\d{2})\s+à\s+(\d{1,2}h\d{2})\s+(.*)", sr_text)
            if match:
                start_time = match.group(1)
                end_time = match.group(2)
                subject_text = match.group(3)
            else:
                start_time = end_time = subject_text = ""
            # Récupération des informations dans la liste des cours
            container = li.find("ul", class_="container-cours")
            items = [item.get_text(strip=True) for item in container.find_all("li")] if container else []
            teacher = items[1] if len(items) > 1 else ""
            room = items[2] if len(items) > 2 else ""
            status = items[3] if len(items) > 3 else ""
            # Récupération de la couleur dans le style du trait-matiere
            trait = li.find("div", class_="trait-matiere")
            color = ""
            if trait and trait.has_attr("style"):
                style = trait["style"]
                m = re.search(r"background-color\s*:\s*([^;]+)", style)
                if m:
                    color = m.group(1).strip()
            schedule.append({
                "start_time": start_time,
                "end_time": end_time,
                "subject": subject_text,
                "teacher": teacher,
                "room": room,
                "status": status,
                "color": color
            })
    return schedule

def parse_homework(soup):
    """Extrait les devoirs depuis la section correspondante."""
    homework_list = []
    container = soup.find("div", id="id_96")
    if container:
        li_items = container.find_all("li")
        for li in li_items:
            subject_el = li.find("span", class_="titre-matiere")
            status_el = li.find("div", class_="text", recursive=True)
            desc_el = li.find("div", class_="description")
            date_el = li.find_parent("li", attrs={"aria-labelledby": True})
            date_text = ""
            if date_el and date_el.find("h3"):
                date_text = date_el.find("h3").get_text(strip=True)
            homework_list.append({
                "subject": subject_el.get_text(strip=True) if subject_el else "",
                "status": status_el.get_text(strip=True) if status_el else "",
                "description": desc_el.get_text(strip=True) if desc_el else "",
                "date": date_text
            })
    return homework_list

def parse_notes(soup):
    """Extrait les notes depuis la section 'liste-clickable'."""
    notes = []
    ul = soup.find("ul", class_="liste-clickable")
    if ul:
        for li in ul.find_all("li", recursive=False):
            a = li.find("a", class_="wrapper-link")
            if a:
                subject_el = a.find("h3")
                date_el = a.find("div", class_="infos-conteneur").find("span", class_="date") if a.find("div", class_="infos-conteneur") else None
                eval_container = a.find("div", class_="evaluations-conteneur")
                evaluations = []
                if eval_container:
                    for span in eval_container.find_all("span", recursive=True):
                        title = span.get("title", "").strip()
                        style = span.get("style", "")
                        color = ""
                        m = re.search(r"background-color\s*:\s*([^;]+)", style)
                        if m:
                            color = m.group(1).strip()
                        evaluations.append({
                            "title": title,
                            "color": color,
                            "text": span.get_text(strip=True)
                        })
                notes.append({
                    "subject": subject_el.get_text(strip=True) if subject_el else "",
                    "date": date_el.get_text(strip=True) if date_el else "",
                    "evaluations": evaluations
                })
    return notes

def time_to_minutes(t):
    """Convertit un temps au format '8h30' en minutes."""
    try:
        parts = t.split("h")
        if len(parts) == 2:
            hours = int(parts[0])
            minutes = int(parts[1])
            return hours * 60 + minutes
    except Exception:
        pass
    return 0

def update_schedule_status(input_file):
    """
    Modifie les valeurs vides du champ "status" dans la section "schedule"
    et met à jour le fichier d'entrée avec les données modifiées.
    """
    # Ouvre le fichier d'entrée en mode lecture
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Vérifie s'il y a une section "schedule" et modifie le champ "status"
    if "schedule" in data:
        for item in data["schedule"]:
            if not item.get("status"):
                item["status"] = "Normal"

    # Ouvre le fichier d'entrée en mode écriture pour mettre à jour les données
    with open(input_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Le fichier '{input_file}' a été mis à jour avec succès.")


def main():
    # Configuration du driver Firefox en mode headless

    options = Options()
    options.headless = True  # Assurez-vous que cette ligne est bien présente
    options.set_preference("dom.disable_open_during_load", True)  # Désactive les popups
    options.set_preference("browser.download.folderList",2)  # Force les téléchargements à être effectués dans un dossier prédéfini
    options.set_preference("browser.download.manager.showWhenStarting",False)  # Masque l'écran de démarrage du téléchargement
    gecko_path = chemin_driver_firefox
    service = Service(gecko_path)
    driver = webdriver.Firefox(service=service, options=options)
    scrap = ScrapPronote()

    try:
        # Connexion à Pronote via Selenium
        scrap.login(driver)


        # Récupérer le code HTML dynamique (avec page_source)
        html = driver.page_source

        # Parser le HTML avec BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        # Optionnel : supprimer les balises <script>
        for script in soup.find_all("script"):
            script.decompose()
        # Sauvegarder le HTML nettoyé dans un fichier
        with open("donnés/code_html_pronote_sans_script.html", "w", encoding="utf-8") as f:
            f.write(str(soup))
        logger.info("Le code HTML dynamique a été récupéré et enregistré dans 'code_html_pronote_sans_script.html'.")

        # Extraction des données
        schedule = parse_schedule(soup)
        homework = parse_homework(soup)
        notes = parse_notes(soup)

        # Trier le planning par heure de début
        schedule.sort(key=lambda x: time_to_minutes(x.get("start_time", "")))

        data = {
            "schedule": schedule,
            "homework": homework,
            "notes": notes
        }

        # Sauvegarder les données extraites dans un fichier JSON
        with open("donnés/extracted_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info("Les données ont été extraites et sauvegardées dans 'extracted_data.json'.")
        print(json.dumps(data, ensure_ascii=False, indent=4))


        # Mettre à jour le champ "status" dans "schedule" après extraction
        update_schedule_status("donnés/extracted_data.json")


    except Exception as e:
        logger.error("Une erreur s'est produite : %s", e)
    finally:
        driver.quit()
        logger.info("Driver fermé.")

if __name__ == "__main__":
    main()
