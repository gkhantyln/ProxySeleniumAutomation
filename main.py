import json
import random
import tempfile
import os
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class ProxyManager:
    def __init__(self, proxy_file):
        self.proxy_file = proxy_file
        self.proxy_info = self.load_random_proxy()

    def load_random_proxy(self):
        with open(self.proxy_file, 'r') as file:
            proxies = file.readlines()
        proxies = [proxy.strip() for proxy in proxies if proxy.strip()]
        return random.choice(proxies)

    def get_proxy_parts(self):
        proxy_parts = self.proxy_info.split(':')
        if len(proxy_parts) == 4:
            return proxy_parts
        else:
            raise ValueError("Proxy bilgileri ip:port:username:password formatında olmalıdır.")

class ChromeProxyExtension:
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.temp_dir = tempfile.TemporaryDirectory()

    def create_extension(self):
        proxies_extension = {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version": "22.0.0"
        }

        background_js = f"""
        var config = {{
            mode: "fixed_servers",
            rules: {{
                singleProxy: {{
                    scheme: "http",
                    host: "{self.ip}",
                    port: parseInt({self.port})
                }},
                bypassList: ["localhost"]
            }}
        }};
        chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});
        function callbackFn(details) {{
            return {{
                authCredentials: {{
                    username: "{self.username}",
                    password: "{self.password}"
                }}
            }};
        }}
        chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {{urls: ["<all_urls>"]}},
            ['blocking']
        );
        """

        manifest_path = os.path.join(self.temp_dir.name, 'manifest.json')
        background_path = os.path.join(self.temp_dir.name, 'background.js')

        with open(manifest_path, 'w') as file:
            json.dump(proxies_extension, file)

        with open(background_path, 'w') as file:
            file.write(background_js)

        zip_path = os.path.join(self.temp_dir.name, 'proxy_extension.zip')
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(manifest_path, 'manifest.json')
            zipf.write(background_path, 'background.js')

        return zip_path

class WebDriverManager:
    def __init__(self, driver_path, extension_path, website):
        self.driver_path = driver_path
        self.extension_path = extension_path
        self.website = website

    def start_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(f"--load-extension={self.extension_path}")

        chrome_service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    def fetch_website(self):
        self.driver.get(self.website)
        return self.driver.page_source

    def quit_driver(self):
        self.driver.quit()

def main():
    proxy_file = 'proxy.txt'
    driver_path = os.path.join(os.getcwd(), 'chromedriver.exe')
    website = 'https://ip.smartproxy.com/json'

    proxy_manager = ProxyManager(proxy_file)
    ip, port, username, password = proxy_manager.get_proxy_parts()

    extension_creator = ChromeProxyExtension(ip, port, username, password)
    extension_path = extension_creator.create_extension()

    web_driver_manager = WebDriverManager(driver_path, extension_path, website)
    web_driver_manager.start_driver()
    page_source = web_driver_manager.fetch_website()
    print(page_source)
    web_driver_manager.quit_driver()

if __name__ == "__main__":
    main()
