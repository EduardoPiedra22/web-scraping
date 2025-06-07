from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from openpyxl.workbook import Workbook
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36")  # Run in headless mode
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts
    )
# URL de la pagina web a scrapiar
driver.get('https://hevy.com/login?postLoginPath=%2Fexercise')

user= ""  # Correo
password = ""  #Clave

# Obtener Inputs 
input_user = driver.find_element(By.XPATH, '//input[@class="sc-1f1e1ba1-2 bTgnVe"]') 
input_password = driver.find_element(By.XPATH, '//input[@label="Password"]')

# Asignar correo y clave a los inputs
input_user.send_keys(user)
input_password.send_keys(password)

# Obtener el boton de inicio de session 
button = driver.find_element(By.XPATH, '//button[@type="submit"]')
# Click
button.click()

# esperar a que cargue toda la web
sleep(20)

# Obtener los Div que se necesita y que contiene un patron
contenedores = driver.find_elements(By.XPATH,'//div[contains(@class, "sc-5cfead32-0")]' )

data = []

# Iterar los contenedores
for contenedor in contenedores:
    try:
        # Obtener la informacion necesaria desde los contenedores que se esta iterando
        nombres_ejericicios = contenedor.find_element(By.XPATH, './/div[contains(@class, "sc-5cfead32-2")]//p[contains(@class, "sc-8f93c0b5-8")]').text
        

        nombres_musculos = contenedor.find_element(
            By.XPATH, 
            './/div[contains(@class, "sc-42fff1f3-0")]//p[contains(@class, "sc-8f93c0b5-9")]'
        ).text
        imagenes = contenedor.find_element(
            By.XPATH, 
            './/div[contains(@class, "sc-5cfead32-1")]//img[contains(@class, "sc-6d8eac73-0")]'
        ).get_attribute("src")
        
        # Verificamos si desde cada contenedor se logro extraer los campos necesarios
        if nombres_ejericicios and nombres_musculos and imagenes:
            
            # Agregamos a la lista
           data.append({
               'Ejercicios': nombres_ejericicios,
               'Musculos': nombres_musculos,
               "Url_Imagen": imagenes
               })
    except NoSuchElementException:
        # En caso de que no este la informacion completa en el contenedor lo saltamos
        continue
    
df = pd.DataFrame(data)


try:
    # Intentamos Guardar los datos en excel usango el motor Openpyxl
    df.to_excel('ejercicios_hevy.xlsx', index=False, engine='openpyxl')
    print("\nArchivo 'ejercicios_hevy.xlsx' guardado correctamente!")
except Exception as e:
        print(f"\nError al guardar el archivo: {str(e)}")
            # Alternativa sin openpyxl
        df.to_csv('ejercicios_hevy.csv', index=False, encoding='utf-8')
        print("Datos guardados en CSV como alternativa")
driver.quit()  # Cerrar el navegador