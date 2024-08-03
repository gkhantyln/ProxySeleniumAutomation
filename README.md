# ProxySeleniumAutomation
This project provides a way to automate proxy configuration and scrape a website's content using Selenium and Python.

## Contents

- `main.py`: The main Python script containing proxy settings and Selenium WebDriver configuration.
- `proxy.txt`: A text file containing proxy information (format: `ip:port:username:password`).
- `chromedriver.exe`: ChromeDriver executable file (if included).

## Requirements

- Python 3.x
- `selenium` Python library
- ChromeDriver browser driver
- Proxy information (in `proxy.txt`)

## Installation

1. Clone this repository:

   ```sh
   git clone https://github.com/gkhantyln/ProxySeleniumAutomation.git
   cd ProxySeleniumAutomation

2. Install the required Python packages:

```sh 
pip install selenium
```

3. Add your proxy information to the proxy.txt file. The file format should be `ip:port:username:password.`

Include the `chromedriver.exe` file in the project or place it in an appropriate directory, and update the driver_path variable in the `main.py` script.

## Usage
1. Run the Python script:
```sh 
python main.py
```
2. The script will start a web browser with the configured proxy settings and navigate to the specified website, printing the page source.

## License
This project is licensed under the MIT License.

## Contact
For any questions regarding the project, you can contact me

This `README.md` file provides a clear overview of the project, including its contents, installation instructions, usage, and licensing information.
