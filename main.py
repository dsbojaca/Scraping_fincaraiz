from utils.driver import get_driver
from etl.extract import extract_properties
from etl.load import load_to_csv

def main():
    driver = get_driver()
    data = extract_properties(driver, n=10)
    
    for i, item in enumerate(data):
        print(f"\n📌 Propiedad {i+1}")
        print(f"💰 Precio: {item['Precio']}")
        print(f"🏠 Tipología: {item['Tipología']}")
        print(f"📍 Arrendador: {item['Arrendador']}")

    load_to_csv(data)
    driver.quit()

if __name__ == "__main__":
    main()