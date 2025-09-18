# Cyber News Dashboard

A minimal,  web app that fetches and displays cybersecurity and technology news from [NewsAPI](https://newsapi.org/).  
Built with Flask + Python + NewsAPI.  

---

## Features
- Live cybersecurity & technology headlines from NewsAPI  
- Clean and minimalist design
- Responsive layout (cards adapt to screen size)  
- Light/Dark theme toggle (I am proud of this :) .)

---

## Getting Started (Local Setup)

### 1. Clone this repository
```bash
git clone https://github.com/<your-username>/cyber-news-dashboard.git
cd cyber-news-dashboard
```

### 2. Create a virtual environment
```bash
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
# py -m venv .venv
# .venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Get your NewsAPI key
- Sign up at [https://newsapi.org/](https://newsapi.org/)  
- Copy your personal API key 

### 5. Create a `.env` file
In the project root, create a file named `.env` and add your API key:
```
NEWSAPI_KEY=your_api_key_here
```

(Make sure `.env` is listed in `.gitignore` so you don’t accidentally commit your key.)

### 6. Run the Flask app
```bash
python app.py
```

By default, the app runs at:
- http://127.0.0.1:5048  
- or another port if specified in `app.py`

