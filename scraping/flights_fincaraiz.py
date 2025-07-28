#Importaciones de Inicio del Bot
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager

#Importaciones de herramientas de scraping
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
#Configuracion del navegador 
options = FirefoxOptions()
options.add_argument("--start-maximized") 
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options = options)


#Inicio de la pagina 
driver.get("https://www.fincaraiz.com.co/apartamentos/arriendos/bogota/")
accions= ActionChains(driver)
time.sleep(3)  
wait = WebDriverWait(driver, 2)

#Cerrar pop-ups si aparecen
try: 
    driver.execute_script("window.scrollBy(0, 300);")
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.ESCAPE)
    
except:
    print("No se encontró el modal de cierre.")


#Establecer los filtros por precio principales
try: 
    driver.find_element(By.CSS_SELECTOR, "button.order-filter-btn:nth-child(1)").click()
    menor_precio_opcion = wait.until(
    EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Menor precio']"))
    )
    ActionChains(driver).move_to_element(menor_precio_opcion).click().perform()
    time.sleep(2)  # Esperar a que se aplique el filtro
except:
    print("no se pudieron hacer los filtros iniciales de precio.")


#Primera interaccion para obtencion de las propiedades mas economicas
try:
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "listingCard")))
    first_cards= driver.find_elements(By.CLASS_NAME, "listingCard")[:10]
    data=[]

    for i, card in enumerate(first_cards):
        try:
            precio= card.find_element(By.CLASS_NAME, "lc-price").text
        except:
            precio= "No disponible"
        
        try:
            tipologia= card.find_element(By.CLASS_NAME, "lc-typologyTag").text
        except:
            tipologia= "No disponible"

        try:
            arrendador= card.find_element(By.CLASS_NAME, "publisher").text
        except:
            arrendador= "No disponible"


        data.append({
            "Precio": precio,
            "Tipología": tipologia,
            "Arrendador": arrendador
        })

        print(f"\n📌 Propiedad {i+1}")
        print(f"💰 Precio: {precio}")
        print(f"🏠 Tipología: {tipologia}")
        print(f"📍 Arrendador: {arrendador}")

        df= pd.DataFrame(data)
        df.to_csv("Propiedades_FincaRaiz.csv", index=False)
except:
    print("no se obtenieron las tarjetas de las propiedades.")






input("Presiona Enter para cerrar navegador...")
driver.quit()