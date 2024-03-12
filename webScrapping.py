from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import csv

from webdriver_manager.chrome import ChromeDriverManager

from time import sleep

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts
)

# Navegar a la página de inicio de sesión de Twitter
driver.get('https://twitter.com/login')

hashtag = 'Queretaro'

# Cambiar al iframe si es necesario
try:
    iframe = driver.find_element(By.XPATH, '//iframe[@title="Twitter login"]')
    driver.switch_to.frame(iframe)
except:
    pass

# Buscar el campo de entrada del nombre de usuario
username_field = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="text"][autocomplete="username"]'))
)

# Ingresar el nombre de usuario
username_field.send_keys("SoyAziel")

# Buscar el botón "Siguiente" y hacer clic en él
login_button = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Siguiente")]'))
)
login_button.click()

# Encontrar el campo de contraseña
password_input = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, '//input[@autocomplete="current-password"]'))
)
# Completar el campo de contraseña con tu valor deseado
password_input.send_keys("HailSatan2028")
sleep(2)
password_input.send_keys(Keys.ENTER)

WebDriverWait(driver, 3).until(
    EC.url_contains('https://twitter.com/home')
)

# Navegar a la página de búsqueda de Twitter para el hashtag dado
driver.get(f'https://twitter.com/hashtag/{hashtag}?lang=en')
sleep(3)

# Obtener la altura actual de la ventana del navegador
last_height = driver.execute_script("return document.body.scrollHeight")
# Desplazarse hacia abajo un máximo de 7 veces
scroll_count = 0
max_scroll_count = 5

tweet_texts = []  # Lista para almacenar los textos de los tweets

while scroll_count < max_scroll_count:
    # Desplazarse hacia abajo
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Esperar un breve tiempo para que la página se cargue después de desplazarse
    sleep(2)
    
    # Encontrar los elementos <div> con el atributo data-testid="tweetText"
    div_elements = driver.find_elements("xpath", '//div[@data-testid="tweetText"]')
    
    # Recorrer los elementos y agregar los textos a la lista
    for div_element in div_elements:
        tweet_texts.append(div_element.text)
    
    # Incrementar el contador de desplazamiento
    scroll_count += 1

#Borrar twits duplicados
tweet_texts = list(set(tweet_texts))  # Eliminar duplicados
print(tweet_texts)  # Imprimir la lista sin duplicados

with open("infoTweet.csv", "a", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)

    #Escribe el encabezado en el archivo CSV
    writer.writerow(["Fecha", "Tweet"])

    #Obtiene la fecha de hoy
    today = date.today()

    #Escribir cada tweet en una nueva fila junto con la fecha de hoy

    for tweet_text in tweet_texts:
        writer.writerow([today, tweet_text])
#Mostrar los textos de los tweets

# Añadir un tiempo de espera para que la página se cargue completamente
sleep(5)
# Puedes continuar con el resto de tu automatización aquí