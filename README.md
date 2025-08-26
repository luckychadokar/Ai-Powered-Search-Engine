# 🧠 AI Website Backend

A scalable **Django-based backend** for powering an AI-driven web platform.  
This backend handles **user authentication, API integrations, data management, and AI-powered features** to deliver a seamless experience for the frontend.

---

## 🚀 Features
- 🔐 **User Authentication**: Secure signup, login, and logout functionality.
- 🧾 **Search & AI APIs**: Integrated with AI/ML APIs for intelligent responses.
- 🖼️ **AI Image Generation**: Supports text-to-image model integrations.
- 📜 **Search History**: Stores and retrieves user search history.
- 🗄️ **Database Support**: MySQL/PostgreSQL for robust data storage.
- 🌐 **RESTful APIs**: Provides endpoints for frontend consumption.

---

## 🛠️ Tech Stack
- **Backend Framework:** Django (Python)
- **Database:** MySQL / PostgreSQL
- **APIs:** OpenRouter API, Hugging Face API
- **Authentication:** Django Auth System
- **Other Tools:** HTML Templates, TailwindCSS (if applicable)

---


⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-website-backend.git
   cd ai-website-backend
2. Create and activate a virtual environment

    python -m venv venv
    venv\Scripts\activate   # Windows

    source venv/bin/activate # macOS/Linux

3. Install dependencies
   pip install -r requirements.txt

4. Run database migrations
   python manage.py migrate
   
5. Create a superuser (optional)
   python manage.py createsuperuser

6. Run the development server
   python manage.py runserver

API Endpoints (Example)
Endpoint	        Method	  Description
/api/auth/signup/	POST	    Register a new user
/api/auth/login/	POST	    Login user & get token
/api/search/	GET	Perform   AI-powered search
/api/image/	POST	Generate  image from text prompt

-> Contributing

1. Fork this repo.
2. Create your feature branch: git checkout -b feature-name.
3. Commit changes: git commit -m 'Add feature'.
4. Push to the branch: git push origin feature-name.
5. Open a Pull Request.

Author
Lucky Chadokar
B.Tech CSE Student | Web Developer | AI Enthusiast
