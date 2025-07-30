from utils.driver import get_driver
from etl.extract import extract_properties
from etl.load import load_to_csv
from etl.transform import clean_data

def main():
    driver = get_driver()
    data_raw = extract_properties(driver, n=10)
    

    for i, item in enumerate(data_raw):
        print(f"\n📌 Propiedad {i+1}")
        print(f"💰 Precio: {item['Precio']}")
        print(f"🏠 Tipología: {item['Tipología']}")
        print(f"📍 Arrendador: {item['Arrendador']}")

    data= clean_data(data_raw)
    load_to_csv(data)
    driver.quit()

if __name__ == "__main__":
    main()