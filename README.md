# AccessiHub Backend

Backend service for **AccessiHub**, an accessibility analyzer platform.  
Built with **Flask**, it scans websites for **WCAG compliance issues**, processes HTML, and generates structured reports via REST APIs for the frontend dashboard.

---

## 🚀 Features
- REST API to analyze any given website URL
- Detects common accessibility issues (missing `alt`, heading structure, titles)
- Generates structured JSON reports (future: PDF/Excel exports)
- Built with Python & Flask for scalability
- Designed to integrate with the React frontend (`accessihub-frontend`)

---

## 🛠️ Tech Stack
- **Python 3.x**
- **Flask** – REST API framework
- **Requests / BeautifulSoup** – HTML fetching & parsing
- **JSON** – Report output

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/accessihub-backend.git
cd accessihub-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows

# Install dependencies
pip install -r requirements.txt
