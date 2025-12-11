from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def connect_to_browser():
    print("🔌 Connecting to open chrome tab...")
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=options)
    return driver