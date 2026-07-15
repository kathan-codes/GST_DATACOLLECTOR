# 🚛 GST Transport Verifier

A Python automation tool that scrapes Transport GSTINs from a public website and verifies them through the official GST Portal. Verified GST details are exported to an Excel file.

## ✨ Features

* Scrape Transport GST Numbers
* Extract only valid GSTINs
* Save webpage HTML for debugging
* Verify GSTINs on the GST Portal
* Manual CAPTCHA support
* Export verified data to Excel

---

## 📂 Project Structure

```
.
├── get_text.py              # Scrape GST numbers
├── cheke_active.py          # Verify GST details
├── GST_NUMBER.txt           # Extracted GSTINs
├── DATA.txt                 # Raw webpage HTML
├── VERIFIED_GST_DATA.xlsx   # Verified GST data
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Prerequisites

* Python 3.10 or later
* Google Chrome

### Install Dependencies

Clone the repository and install the required Python packages:

```bash
pip install -r requirements.txt
```

The project uses the following libraries:

* `requests`
* `beautifulsoup4`
* `pandas`
* `selenium`
* `undetected-chromedriver`
* `openpyxl`

If you don't have a `requirements.txt` file, you can install them manually:

```bash
pip install requests beautifulsoup4 pandas selenium undetected-chromedriver openpyxl
```


## 🚀 Usage

### 1. Extract GST Numbers

```bash
python get_text.py
```

Creates:

* `GST_NUMBER.txt`
* `DATA.txt`

### 2. Verify GST Details

```bash
python cheke_active.py
```

For each GST number:

1. Solve the CAPTCHA.
2. Click **Search**.
3. Press **Enter** in the terminal.

After processing, all verified records are saved in:

```
VERIFIED_GST_DATA.xlsx
```

---

## 🔄 Workflow

```
Website
   │
   ▼
get_text.py
   │
   ▼
GST_NUMBER.txt
   │
   ▼
cheke_active.py
   │
   ▼
GST Portal
   │
   ▼
VERIFIED_GST_DATA.xlsx
```

---

## 🛠️ Built With

* Python
* Requests
* BeautifulSoup
* Selenium
* Undetected ChromeDriver
* Pandas
* OpenPyXL

---

## ⚠️ Notes

* CAPTCHA must be solved manually.
* An internet connection is required.
* If the GST Portal changes its layout, the scraper may need updates.

---

## 📄 License

This project is intended for educational and research purposes only.
