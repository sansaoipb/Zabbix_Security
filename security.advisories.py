#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Criador: Sansão - Especialista Infraestrutura
Data: 07/04/2025
"""

import sys
import json
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


zbx_server = sys.argv[1]
fileName = sys.argv[2]
timeOut = 20

current_year = int(time.strftime("%Y"))
check_previous_year = 0 # 0 = somente ano atual / 4 = verifica 5 anos atras

servico = Service(ChromeDriverManager().install())
chrome_options = Options()
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless') 
driver = webdriver.Chrome(service=servico, options=chrome_options)


def save_json(filename, data):
    try:
        with open(filename, 'w', encoding='utf-8') as Json:
            json.dump(data, Json, ensure_ascii=False, indent=2)
    except (OSError, IOError) as e:
        print(f"Erro ao salvar o arquivo {filename}: {e}")


def main():
    try:
        resultado = requests.post(f'{zbx_server}/api_jsonrpc.php',
                                  headers={'Content-type': 'application/json'},
                                  verify=False,
                                  data=json.dumps(
                                      {"jsonrpc": "2.0","method": "apiinfo.version","params": [],"id": 1}
                                  ))
        zbx_version = json.loads(resultado.content)
        if 'result' in zbx_version:
            zbx_version = zbx_version["result"][:3]

        complement = f"refinementList%5Bversions%5D%5B0%5D={float(zbx_version)}"
        for num, i in enumerate(range(check_previous_year, -1, -1)):  # Itera do ano mais antigo para o mais novo
            year = current_year - i
            complement += f"&refinementList%5Bpublished_year%5D%5B{num}%5D={year}"

        driver.get(f"https://www.zabbix.com/br/security_advisories?{complement}")

        WebDriverWait(driver, timeOut).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ais-Hits-item"))
        )

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        cve_list = {"last_updated": {"secs": 0.0}, "reports": []}
        table_rows = soup.find_all("li", class_="ais-Hits-item")
        for row in table_rows:
            cveref = row.find("small").text.strip()
            synopsis = row.find("h2", class_="entry-title").text.strip()
            score = row.find("div", class_="cvss_score").text.strip()
            description = row.find("th", string="Description:").find_next("td").text.strip()
            vectors = row.find("th", string="Known Attack Vectors:").find_next("td").text.strip()
            resolution = row.find("th", string="Resolution:").find_next("td").text.strip()
            workaround = row.find("th", string="Workarounds:").find_next("td").text.strip()
            acknowledgement = row.find("th", string="Acknowledgements:").find_next("td").text.strip()
            publish_date = row.find("div", class_="entry-author-content").text.strip()

            components = [comp.text.strip() for comp in row.find("th", string="Component").find_next("td").find_all("span")]
            affected_versions = [div.text.strip() for div in row.find("span", class_="cvss_versions_affected").find_all("div")]
            fixed_versions = [div.text.strip() for div in row.find("span", class_="cvss_versions_fixed").find_all("div")]

            affected_version_list = [
                {"affected": ver, "fixed": fixed_versions[idx] if idx < len(fixed_versions) else "-"}
                for idx, ver in enumerate(affected_versions)
            ]

            Components = []
            for compts in components:
                if compts:
                    if "," in compts:
                        continue
                    elif ", " in compts:
                        compts = compts.split(", ")
                    else:
                        compts = compts.strip().split()

                    Components += compts

            Score = float(score) if score.replace('.', '', 1).isdigit() else score
            score, severity = Score.split()
            cve_data = {
                "publish_date": publish_date,
                "zbxref": synopsis,
                "cveref": cveref,
                "score_full": Score,
                "score": score,
                "severity": severity,
                "synopsis": synopsis,
                "description": description,
                "vectors": vectors,
                "resolution": resolution,
                "workaround": workaround,
                "acknowledgement": acknowledgement,
                "components": ", ".join(list(filter(None, set(Components)))),
                "affected_version": affected_version_list
            }

            cve_list["reports"].append(cve_data)

        cve_list["last_updated"]["secs"] = time.time()
        save_json(fileName, cve_list)

    finally:
        driver.quit()


if __name__ == '__main__':
    main()
