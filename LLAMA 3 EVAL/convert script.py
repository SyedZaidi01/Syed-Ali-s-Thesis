

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Path to the folder containing HTML files
input_folder = "nvbench chart"
output_folder = "svg_outputs"

# Path to ChromeDriver
chrome_driver_path = "cd /usr/local/bin/Google"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

def extract_svg_from_html(html_file, output_file):
    # Initialize Selenium WebDriver
    service = Service(chrome_driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Load the HTML file in the browser
        driver.get(f"file://{os.path.abspath(html_file)}")
        
        # Wait for Vega-Lite to render the SVG
        driver.implicitly_wait(5)
        
        # Extract the page source and parse the SVG
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        svg = soup.find("svg")
        
        if svg:
            # Save the SVG content to the output file
            with open(output_file, "w") as file:
                file.write(str(svg))
            print(f"SVG saved to {output_file}")
        else:
            print(f"No SVG found in {html_file}")
    finally:
        driver.quit()

# Process all HTML files in the folder
def convert_html_to_svgs():
    html_files = [f for f in os.listdir(input_folder) if f.endswith('.html')]
    
    if not html_files:
        print("No HTML files found in the folder.")
        return

    for html_file in html_files:
        input_path = os.path.join(input_folder, html_file)
        output_file = os.path.join(output_folder, os.path.splitext(html_file)[0] + ".svg")
        extract_svg_from_html(input_path, output_file)

    print("All HTML files have been processed and converted to SVGs.")

# Run the script
convert_html_to_svgs()
