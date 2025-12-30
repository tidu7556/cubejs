# Complete Project Setup Guide - All Steps in One Place

This is your master guide that brings together ALL the instructions you need to get your Streamlit project running, from initial setup to deployment.

---

## 🎯 Quick Navigation

Choose your situation:

1. **[I'm cloning this project from GitHub](#scenario-1-cloning-this-project-from-github)** → Start here
2. **[I already have code and need to complete it](#scenario-2-i-already-have-code-and-need-to-complete-it)** → Start here
3. **[I want to deploy my app to the internet](#scenario-3-deploying-your-app-to-streamlit-cloud)** → Start here

---

## Scenario 1: Cloning This Project from GitHub

If you're cloning an existing Streamlit project (like `github/airen95/finance_tracker`), follow these steps:

### Step 1: Clone the Project to Your Computer

Open your terminal and run:

```bash
git clone https://github.com/airen95/finance_tracker.git
cd finance_tracker
```

Replace the URL with your actual project URL. This downloads all the project files to your computer.

### Step 2: Install Required Libraries

The project should have a `requirements.txt` file. Install all dependencies:

```bash
pip install -r requirements.txt
```

This installs all the libraries the project needs:
- streamlit
- pymongo
- authlib
- python-dotenv
- matplotlib
- pandas
- plotly

### Step 3: Set Up MongoDB Atlas Connection

You need a database connection string. Follow the complete [**MongoDB Atlas Setup**](/documentation/MongoAtlas.md) guide:

**Reference**: Complete Guide: Setting Up MongoDB Atlas and Getting Your Connection String

**Quick Summary**:
1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account
3. Create a free cluster
4. Create database credentials (username + password)
5. Get your connection string
6. Create a `.env` file in your project root with:
   ```
   MONGO_URI=mongodb+srv://username:password@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority
   ```

**Important**: Add `MONGO_URI` to your `.env` file, and make sure `.env` is in `.gitignore`

### Step 4: Set Up Google Authentication (If the Project Uses It)

If the project includes Google login, follow the [**Google Authentication SSO Setup**](/documentation/GoogleSSO.md) guide:

**Reference**: Streamlit Google Authentication SSO Setup Guide

**Quick Summary**:
1. Go to https://console.cloud.google.com/
2. Create a new project
3. Configure the consent screen (Branding section)
4. Add your test email in Audience section
5. Create an OAuth 2.0 client for "Web application"
6. Add this authorized redirect URI: `http://localhost:8501/oauth2callback`
7. Copy your Client ID and Client Secret

Then create `.streamlit/secrets.toml`:

```toml
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "your-random-secret-key"
client_id = "your-client-id.apps.googleusercontent.com"
client_secret = "your-client-secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

**Important**: Add `.streamlit/secrets.toml` to your `.gitignore`

### Step 5: Run the Project

In your terminal, make sure you're in the project folder and run:

```bash
streamlit run app.py
```

If your main file has a different name, replace `app.py` with the correct filename.

Your app will open in your browser at `http://localhost:8501`

**You're Done!** The project is now running on your computer. 🎉

---

## Scenario 2: I Already Have Code and Need to Complete It

If you have existing code and need to set it up properly before running it, follow these steps:

### Step 1: Create a `requirements.txt` File (If Missing)

If your project doesn't have a `requirements.txt`, create one in your project root with this content:

```
streamlit>=1.40.0
authlib>=1.6.5
python-dotenv>=0.9.9
matplotlib>=3.10.7
pandas>=2.3.3
plotly>=6.5.0
pymongo>=4.15.4
```

Add or remove libraries based on what your project actually uses.

### Step 2: Install Dependencies

In your terminal, navigate to your project folder and run:

```bash
pip install -r requirements.txt
```

### Step 3: Create `.env` File with MongoDB Connection

In your project root, create a `.env` file:

```
MONGO_URI=mongodb+srv://username:password@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority
```

If you don't have a MongoDB connection string yet, follow the **MongoDB Atlas Setup** guide to create one.

### Step 4: Create `.streamlit/secrets.toml` for Google Auth (If Using It)

If your code uses Google Authentication, create the `.streamlit` folder and add `secrets.toml`:

```toml
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "your-random-secret-key"
client_id = "your-client-id.apps.googleusercontent.com"
client_secret = "your-client-secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

If you don't have Google credentials yet, follow the **Google Authentication SSO Setup** guide.

### Step 5: Update `.gitignore`

Make sure your `.gitignore` file protects sensitive files:

```
# Environment variables
.env
.env.local
.env.*.local

# Streamlit secrets
.streamlit/secrets.toml

# Python
__pycache__/
*.py[cod]
*.egg-info/

# IDE
.vscode/
.idea/
```

### Step 6: Run Your App

In your terminal, run:

```bash
streamlit run app.py
```

Replace `app.py` with your actual main file name.

Your app will open at `http://localhost:8501`

**You're Ready!** Your project is properly set up and running. 🎉

---

## Scenario 3: Deploying Your App to Streamlit Cloud 

Please read and follow this instruction [**Deploy guideline**](/documentation/Deployment.md)

### Step 9: Test Your Live App

1. Go to your app URL: e.g this is my app `https://airen95-finance-tracker-app-epjkq4.streamlit.app/`
2. Test all features
3. Try logging in with Google
4. Check MongoDB is working

**Your app is now live! 🎉** Share your URL with anyone and they can use your app.

---

## Troubleshooting Checklist

### App Won't Run Locally

- [ ] Did you install requirements? `pip install -r requirements.txt`
- [ ] Do you have `.env` with MONGO_URI?
- [ ] Do you have `.streamlit/secrets.toml` with Google Auth?
- [ ] Is the filename correct? `streamlit run app.py`

### MongoDB Connection Failed

- [ ] Is MONGO_URI correct in `.env`?
- [ ] Does it have `&ssl=true&ssl_cert_reqs=CERT_NONE` suffix?
- [ ] Is your cluster running in MongoDB Atlas?
- [ ] Is your IP whitelisted (0.0.0.0/0)?

### Google Login Not Working

- [ ] Is `.streamlit/secrets.toml` created?
- [ ] Are section names exactly `[auth]` and `[auth.google]`?
- [ ] Is your email in test users?
- [ ] Is redirect_uri correct?

### Deployment Failed

- [ ] Is code pushed to GitHub?
- [ ] Is GitHub account connected to Streamlit?
- [ ] Does `requirements.txt` exist?
- [ ] Are secrets added in Advanced settings?
- [ ] Is app URL added to Google Cloud?

---

## Project Structure (How It Should Look)

```
.
└── finance_tracker/
    ├── .streamlit/
    │   └── secrets.toml
    ├── .env
    ├── .gitignore
    ├── requirements.txt
    ├── app.py
    ├── config.py
    ├── utils.py
    ├── documentation/
    ├── hands-on/
    ├── analytics/
    │   ├── analyzer.py
    │   └── visualizer.py
    ├── database/
    │   ├── __init__.py
    │   ├── database_manager.py
    │   ├── category_models.py
    │   ├── transaction_models.py
    │   └── user_models.py
    └── views/
        ├── __init__.py
        ├── user_views.py
        ├── home_views.py
        ├── transaction_views.py
        └── category_views.py
```

---

## Quick Commands Reference

```bash
# Setup
pip install -r requirements.txt          # Install libraries
streamlit run app.py                     # Run app locally

# Git
git add .                                # Stage changes
git commit -m "message"                  # Create commit
git push                                 # Push to GitHub
git clone <url>                          # Clone a project

# Python
pip list                                 # See installed packages
pip install package_name                 # Install a package
python filename.py                       # Run Python file
```

---

## You Have Everything You Need!

You now have complete instructions for:
- ✓ Setting up MongoDB
- ✓ Configuring Google Authentication
- ✓ Running your app locally
- ✓ Deploying to the internet
- ✓ Pushing code to GitHub
- ✓ Managing secrets safely

Pick your scenario above and start building! 🚀