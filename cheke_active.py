import time
import re
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def process_and_scrape_gstins():
    # 1. Read GSTIN lines from your text file line by line
    gstin_list = []
    try:
        with open("GST_NUMBER.txt", "r", encoding="utf-8") as f:
            for line in f:
                line_text = line.strip()
                # Skip header decorative rows or empty spaces
                if not line_text or "===" in line_text:
                    continue
                # Match strict GST number format rules
                if re.match(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9A-Z]{1}Z[0-9A-Z]{1}$', line_text.upper()):
                    gstin_list.append(line_text.upper())
    except FileNotFoundError:
        print("Error: GST_NUMBER.txt file not found.")
        return

    if not gstin_list:
        print("No valid GSTIN IDs found in the file to process.")
        return

    excel_file = "VERIFIED_GST_DATA.xlsx"
    all_records = []

    # 2. Configure Chrome with your exact User-Agent string specification
    print("Launching Stealth Chrome Browser...")
    options = uc.ChromeOptions()
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = uc.Chrome(options=options, use_subprocess=True)
    driver.maximize_window()
    
    # 3. Navigate to url target and perform your requested 4 second static hold wait
    print("Navigating to GST Portal...")
    driver.get("https://services.gst.gov.in/services/searchtp")
    time.sleep(4)
    
    wait = WebDriverWait(driver, 20)

    try:
        for index, gstin in enumerate(gstin_list, start=1):
            print(f"\n[{index}/{len(gstin_list)}] Current ID target -> {gstin}")
            
            # Step A: Wait until the input field box name="for_gstin" appears completely
            gstin_box = wait.until(EC.presence_of_element_located((By.NAME, "for_gstin")))
            
            # Populate text field
            gstin_box.clear()
            gstin_box.send_keys(gstin)
            
            # Step B: Wait until the specific captcha entry field ID "fo-captcha" appears on screen layout
            wait.until(EC.presence_of_element_located((By.ID, "fo-captcha")))
            print(f"--> [Success] {gstin} written inside input lane successfully.")
            
            # Step C: HUMAN HANDSHAKE PAUSE 
            # This completely stalls the loop code. You can click 'fa-refresh' as many times as you like,
            # type the code into your browser screen window, and click 'Submit/Search' manually.
            print("\n======================= ACTION REQUIRED =======================")
            print("1. (Optional) Feel free to click the reload icon (fa-refresh) if needed.")
            print("2. Type the visual CAPTCHA image details.")
            print("3. CLICK THE SUBMIT/SEARCH BUTTON IN YOUR CHROME WINDOW.")
            print("4. ONCE RESULTS COMPILATION LOADS ON SCREEN, press [ENTER] here in this terminal...")
            input("===============================================================")

            print("Extracting dynamic results blocks from active viewport layouts...")
            time.sleep(1) # Tiny safety buffer for values to settle inside target elements
            
            # Step D: Target every single structural div tag matching class="col-sm-4 col-xs-12"
            div_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'col-sm-4') and contains(@class, 'col-xs-12')]")
            
            if div_elements:
                record_data = {"GSTIN": gstin}
                
                for div in div_elements:
                    try:
                        # Grab all paragraph structural blocks inside the layout column block context
                        p_tags = div.find_elements(By.TAG_NAME, "p")
                        
                        # Ensure there is a tracking title <p> (e.g. Legal Name) and a target value string data row <p>
                        if len(p_tags) >= 2:
                            header_text = p_tags[0].text.strip()
                            value_text = p_tags[1].text.strip() # Isolates pure string text (e.g., "A BT LIMITED")
                            
                            if header_text:
                                record_data[header_text] = value_text
                    except Exception:
                        continue
                
                all_records.append(record_data)
                print(f"✅ Extracted data points mapped directly into dataset entries.")
            else:
                print("❌ No matching text fields detected inside layout. Recording fallback check.")
                all_records.append({"GSTIN": gstin, "Status": "DATA ROW FETCH OMISSION"})

            # Step E: Save data rows incrementally to the Excel spreadsheet layout
            df = pd.DataFrame(all_records)
            df.to_excel(excel_file, index=False)
            
            # Step F: Native Refresh Strategy
            # Explicitly reload URL at end of cycle to serve a clean slate empty form for the next record
            print("Preparing fresh template grid layer execution tracks...")
            driver.get("https://services.gst.gov.in/services/searchtp")
            time.sleep(4) # Match original 4 seconds hold rule specification parameter

    except Exception as e:
        print(f"\nProcessing system pipeline dropped operation tracks: {e}")
        
    finally:
        print(f"\nFinal tracking operations concluded layout data saves. Check: {excel_file}")
        driver.quit()

if __name__ == "__main__":
    process_and_scrape_gstins()
