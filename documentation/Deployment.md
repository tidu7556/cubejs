# Deploy Streamlit App to Streamlit Cloud - Complete Guide

This guide walks you through deploying your Streamlit app to the cloud so anyone can access it on the internet.

## Prerequisites

Before you deploy, make sure:
- ✓ Your code is working perfectly on your computer
- ✓ All your code is pushed to GitHub (see [Git Push Guideline](./PushCode.md))
- ✓ Your GitHub account is ready to connect

## Part 1: Deploy Using the Deploy Button

### Step 1: Run Your App Locally

Before deploying, make sure your app works perfectly on your computer.

In your terminal, run:

```
streamlit run app.py
```

(Replace `app.py` with your main app filename if different)

Test all your features to make sure everything works. Once you're satisfied, continue to the next step.

### Step 2: Click the Deploy Button

In your Streamlit app running locally, look at the **top-right corner** of the browser window.

You'll see a Deploy button (grey color). Click it.

![Deploy Button](./images/deploy_button.png)

This will open the Streamlit deployment page. Choose the free plan (of course)

![Deploy Plan](./images/deply-plan.png)

### Step 3: Sign In to Streamlit Community Cloud

If you're not already signed in:

1. Go to https://streamlit.io/cloud (or click the deploy button which opens this)
2. Click **"Sign up"** or **"Sign in"**
3. **Connect your GitHub account**:
   - Click "GitHub" as your sign-in option
   - Click "Authorize streamlit" when GitHub asks
   - This allows Streamlit Cloud to access your GitHub repositories

**Note**: If you don't have a GitHub account yet, create one at https://github.com first.

Once signed in, you'll see the deployment form.

![Deploy Form](./images/deploy-settings.png)

### Step 4: Select Your Repository

In the Streamlit Cloud deployment page:

1. **Repository**: Select your GitHub repository containing your Streamlit app
   - It will show your username and repository name (example: `yourname/my-streamlit-app`)

2. **Branch**: Select `main` (this is your main branch where your code is)

3. **Main file path**: Enter the name of your main app file
   - Usually `app.py`
   - If your file is in a subfolder, use: `subfolder/app.py`

### Step 5: Set Your App URL

Under "App URL," you'll see a field to customize your app's web address.

**This is your public URL** that people will use to access your app.

Enter a name you want for your app:
- Examples: `my-awesome-app`, `data-analyzer`, `chatbot-demo`
- Use lowercase letters, numbers, and hyphens only (no spaces)
- The full URL will be: `https://your-name-here.streamlit.app`

**⚠️ IMPORTANT**: Remember this URL! You'll need it to set up Google Authentication redirect URI.

For Google Auth, your redirect URI will be:
```
https://your-name-here.streamlit.app/oauth2callback
```

Write this down or copy it somewhere safe.

### Step 6: Add Secrets (Click Advanced Settings)

Now you need to add your sensitive information securely. Scroll down and click **"Advanced settings"**.

#### Add Your MongoDB Connection String

In the **"Secrets"** text area, paste your secrets in TOML format.

**First, add your MONGO_URI**:

```toml
MONGO_URI = "mongodb+srv://username:password@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
```

**Important**: Add these suffixes to your connection string:
- `&ssl=true&ssl_cert_reqs=CERT_NONE`

This tells MongoDB to use a secure connection. Your full string should end with these parameters.

#### Add Your Google Authentication Secrets

Next, add your Google Auth configuration. Copy your entire `.streamlit/secrets.toml` content and paste it.

Your secrets should look like this:

```toml
MONGO_URI = "mongodb+srv://username:password@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"

[auth]
redirect_uri = "https://your-name-here.streamlit.app/oauth2callback"
cookie_secret = "your-random-secret-key"
client_id = "123456789-abcdefg.apps.googleusercontent.com"
client_secret = "GOCSPX-1234567890abcdefgh"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

⚠️ **CRITICAL**: 
- Replace `your-name-here` in redirect_uri with the app URL you chose in Step 5
- Keep all other values exactly as they are
- Never share these secrets with anyone

![Deploy Advanced Settings](./images/deploy-advanced-settings.png)

### Step 7: Update Google Cloud Console

Before clicking deploy, you need to add your deployment URL to Google Cloud.

1. Go to https://console.cloud.google.com/auth/overview
2. Select your project (the one you set up for Google Auth)
3. Click on your Client
5. Under **"Authorized JavaScript origins,"** add:
   - `https://your-name-here.streamlit.app`
6. Under **"Authorized redirect URIs,"** add:
   - `https://your-name-here.streamlit.app/oauth2callback`
7. Click **"Save"**


![Google Oauth Add URL](./images/google-settings.png)

Now your deployment URL is authorized in Google Cloud.

### Step 8: Deploy!

Once everything is set up:

1. Review all your settings one more time:
   - ✓ Correct repository selected
   - ✓ Branch is `main`
   - ✓ App URL is what you decided
   - ✓ MONGO_URI has `ssl=true&ssl_cert_reqs=CERT_NONE`
   - ✓ Google Auth secrets are correct with updated redirect_uri
   - ✓ URL is added to Google Cloud

2. Click the **"Deploy!"** button

Streamlit will now:
- Clone your GitHub repository
- Install your dependencies
- Start your app
- Make it available at your chosen URL

You should see "Your app is running!" or similar message. This usually takes 1-3 minutes.

## Part 3: Verify Your Deployment

### Check If Your App is Running

1. Go to your app URL: `https://your-name-here.streamlit.app`
2. You should see your app loading

### Test Your Features

1. Test all major features of your app
2. Try logging in with Google Auth
3. Make sure MongoDB is connecting and saving/retrieving data

Fix the issue in your local code, push to GitHub, and Streamlit will automatically redeploy.

## Part 4: Making Updates After Deployment

Your app will automatically update whenever you push changes to GitHub.

### To Update Your App

1. Make changes to your code locally
2. Test locally with `streamlit run app.py`
3. Push to GitHub:
   ```
   git add .
   git commit -m "Update: describe your changes"
   git push
   ```
4. Streamlit will automatically detect the change and redeploy
5. Wait 1-2 minutes for the deployment to complete

You don't need to re-enter secrets or settings—they're saved automatically.

## Deployment Workflow Summary

```
Local Development
       ↓
Push Code to GitHub
       ↓
Click Deploy Button
       ↓
Connect GitHub Account
       ↓
Select Repository & Branch
       ↓
Set App URL
       ↓
Add Secrets (MONGO_URI + Google Auth)
       ↓
Update Google Cloud with New URL
       ↓
Click Deploy!
       ↓
Your App is Live! 🎉
```

## Troubleshooting: Common Deployment Issues

### "Repository Not Found"

**Problem**: Streamlit can't find your GitHub repository.

**Solutions**:
- Make sure your GitHub account is connected to Streamlit
- Make sure your code is actually on GitHub
- Refresh the page and try again
- Check that your repository is public

### "No module named 'X'"

**Problem**: Your app needs a library that's not installed.

**Solution**:
- Create a `requirements.txt` file in your project root
- List all libraries you need (one per line):
  ```
  streamlit
  pymongo
  authlib
  python-dotenv
  ```
- Push to GitHub
- Streamlit will automatically install them on redeploy

### "MongoDB Connection Failed"

**Problem**: Your MONGO_URI isn't working in the cloud.

**Solutions**:
- Verify `ssl=true&ssl_cert_reqs=CERT_NONE` is in your MONGO_URI
- Check your MongoDB cluster is running
- Verify your IP whitelist on MongoDB Atlas allows all IPs (0.0.0.0/0)
- Test the connection string locally first

### "Invalid Redirect URI" (Google Auth Error)

**Problem**: Users can't log in with Google.

**Solutions**:
- Check your redirect_uri in secrets matches your app URL exactly
- Verify your app URL is added to Google Cloud authorized URIs
- Make sure you added both:
  - Authorized JavaScript origin: `https://your-app.streamlit.app`
  - Authorized redirect URI: `https://your-app.streamlit.app/oauth2callback`

### "App is Stuck on Loading"

**Problem**: Your app keeps loading but never finishes.

**Solution**:
- Click the "⋯" menu on your app
- Select "Reboot app"
- Check the logs for errors
- Fix errors locally and push to GitHub

![App Reboot](./images/app-reboot.png)

## You've Done It!

Your app is now live on the internet! 🎉

You can share the URL with anyone, and they can use your app just like a real website. Every time you push code to GitHub, your app automatically updates.