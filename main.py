import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
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
driver.get("https://wpstarterpack.com/category/wordpress-plugins/page/5/?per_page=20&orderby=popularity")
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

# Esperar os elementos de produto aparecerem
product_sections = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "section.product.type-product"))
)

i = 0

# Loop para processar produtos e páginas
while True:
    print("Processando produtos na página atual...")
    
    # Captura os produtos da página
    try:
        product_sections = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "section.product.type-product"))
        )
    except Exception as e:
        print(f"Erro ao carregar produtos na página: {e}")
        break

    if i < 20:  # Limitar a 20 produtos
        # Processar os produtos da página
        try:
            product = product_sections[i]
            product_link = product.find_element(By.CSS_SELECTOR, "a")
            product_link.click()
            print(f"Produto {i + 1} aberto com sucesso!")

            try:
                download_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.button.product-download-button"))
                )
                download_button.click()
                print(f"Download do produto {i + 1} iniciado!")
            except Exception as e:
                print(f"Erro ao iniciar o download do produto {i + 1}: {e}")
            
            time.sleep(random.uniform(2, 3))
            driver.back()
            time.sleep(random.uniform(1, 2))
        except Exception as e:
            print(f"Erro ao processar o produto {i + 1}: {e}")
        
        i += 1  # Incrementar o contador de produtos

    else:
        # Avançar para a próxima página
        try:
            next_page_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.next.page-numbers"))
            )
            next_page_button.click()
            print("Indo para a próxima página...")
            time.sleep(random.uniform(3, 4))
            i = 0  # Resetar o contador de produtos
        except Exception as e:
            print(f"Erro ao clicar no botão 'Next page': {e}. Encerrando o processo.")
            break

print("Processo concluído!")
driver.quit()