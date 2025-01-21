import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv

# Função para simular uma digitação humana com atraso aleatório
def human_typing(element, text, min_delay=0.1, max_delay=0.3):
    for character in text:
        element.send_keys(character)
        time.sleep(random.uniform(min_delay, max_delay))  # Atraso aleatório entre caracteres

# Carregar variáveis de ambiente
load_dotenv()

# Obter usuário e senha do arquivo .env
username = os.getenv("USERNAMEWP")
password = os.getenv("PASSWORD")

# Configurar o Service com o caminho do ChromeDriver
service = Service("C:/chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Abrir o navegador e acessar o wpstarterpack
driver.get("https://wpstarterpack.com/category/wordpress-plugins/")
print("Página carregada: ", driver.title)

# Esperar o ícone de login aparecer
login_icon = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "a.login"))
)

# Criar uma ação de hover no ícone de login
actions = ActionChains(driver)
actions.move_to_element(login_icon).perform()  # Realiza o hover no ícone

# Esperar os campos de login ficarem visíveis
username_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, "log"))  # Campo de usuário
)
password_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, "pwd"))  # Campo de senha
)

# Preencher o campo de usuário com digitação simulada
human_typing(username_field, username)

# Preencher o campo de senha com digitação simulada
human_typing(password_field, password)

# Clicar no botão de login com um pequeno atraso aleatório
login_submit = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.NAME, "wp-submit"))  # Botão de login
)
time.sleep(random.uniform(1, 3))  # Atraso aleatório antes de clicar
login_submit.click()

print("Login realizado com sucesso!")
time.sleep(1000)  # Opcional: aguardar para verificar se a página carregou corretamente

# Fechar o navegador
driver.quit()
