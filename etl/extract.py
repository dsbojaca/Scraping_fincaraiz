from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

def extract_properties(driver, wait_time=2, n=10):
    wait = WebDriverWait(driver, wait_time)
    accions = ActionChains(driver)

    driver.get("https://www.fincaraiz.com.co/apartamentos/arriendos/bogota/")
    time.sleep(3)

    # Cerrar pop-up
    try:
        driver.execute_script("window.scrollBy(0, 300);")
        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.ESCAPE)
    except:
        print("No se encontró el modal de cierre.")

    # Filtro: menor precio
    try:
        driver.find_element(By.CSS_SELECTOR, "button.order-filter-btn:nth-child(1)").click()
        menor_precio_opcion = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Menor precio']"))
        )
        accions.move_to_element(menor_precio_opcion).click().perform()
        time.sleep(2)
    except:
        print("No se pudieron aplicar los filtros.")

    # Scrapeo
    try:
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "listingCard")))
        first_cards = driver.find_elements(By.CLASS_NAME, "listingCard")[:n]
        data = []

        for i, card in enumerate(first_cards):
            try:
                precio = card.find_element(By.CLASS_NAME, "lc-price").text
            except:
                precio = "No disponible"

            try:
                tipologia = card.find_element(By.CLASS_NAME, "lc-typologyTag").text
            except:
                tipologia = "No disponible"

            try:
                arrendador = card.find_element(By.CLASS_NAME, "publisher").text
            except:
                arrendador = "No disponible"

            data.append({
                "Precio": precio,
                "Tipología": tipologia,
                "Arrendador": arrendador
            })

        return data

    except:
        print("No se obtuvieron las tarjetas de propiedades.")
        return []