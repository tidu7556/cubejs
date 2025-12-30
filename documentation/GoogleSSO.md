# Complete Guide: Google Authentication SSO in Streamlit

This guide shows you how to set up Google Authentication (SSO) in your Streamlit app with two configurations: one for local development and one for deployment.

**Reference**: Based on Streamlit's official Google Auth Platform documentation [link](https://docs.streamlit.io/develop/tutorials/authentication/google)

## Part 1: Google Cloud Setup (Required for Both Local and Deployment)

Before you can use Google Authentication, you need to set up a Google Cloud project and create OAuth credentials.

### Step 1: Create a Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Sign in with your Google account
3. In the top-left corner, click "Select a Project" or "My First Project"
4. Click "New Project"
5. Enter a project name (example: "my-streamlit-app")
6. Click "Create"
7. Wait for the project to be created (about 1-2 minutes)

### Step 2: Configure Your Consent Screen

The consent screen is what users see when they log in with Google.

1. Go to the Google Auth Platform: https://console.cloud.google.com/
2. Sign in to Google
3. In the upper-left corner, select your project
4. In the left navigation menu, select **"Branding"**
5. Fill in the required information for your application's consent screen:
   - **App name**: Give your app a name (example: "My Streamlit App")
   - **Authorized domain**: Enter `example.com` (Google's standard for development and Streamlit Community Cloud)
   - **User support email**: Enter your email address
   - **Developer contact information**: Enter your email address
6. At the bottom of the page, select **"SAVE"**

### Step 3: Configure Your Audience

1. In the left navigation menu, select **"Audience"**
2. Below "OAuth user cap" → "Test users," select **"ADD USERS"**
3. Enter the email address for a personal Google account (use the email you'll test with)
4. Select **"SAVE"**

**Important**: When your app is in "Testing" status, only these email addresses can log in. Later, when you're ready to publish, you'll return here and change the status to "Published" to allow anyone to sign up.

### Step 4: Configure Your Client

1. In the left navigation menu, select **"Clients"**
2. At the top of the client list, select **"CREATE CLIENT"**
3. For the application type, select **"Web application"**
4. Enter a unique name for your application (example: "Streamlit App Client")
   - This name is used internally and not shown to users
5. Skip "Authorized JavaScript origins" (leave it blank)
6. Under **"Authorized redirect URIs,"** select **"ADD URI"**
7. Enter your app's URL with the pathname `oauth2callback`:
   - **For local development**: `http://localhost:8501/oauth2callback`
   - If you use a different port, change 8501 to match your port
8. **Optional**: Add additional authorized redirect URIs for future deployment
   - For example, if deploying on Streamlit Cloud: `https://my-app.streamlit.app/oauth2callback`
   - Ensure each URL includes the `oauth2callback` pathname
9. At the bottom of the screen, select **"CREATE"**

You now have a client in Google Cloud ready to authenticate your users.

### Step 5: Gather Your Application Details

1. From the clients page, select your new client
2. You'll see two important values:
   - **Client ID** (looks like: `123456789-abcdefg.apps.googleusercontent.com`)
   - **Client secret** (looks like: `GOCSPX-1234567890abcdefgh`)
3. **Copy these values** into a text editor or password manager with labels so you don't mix them up

**Server Metadata URL**: For Google Auth, use this URL (it's the same for all applications):
```
https://accounts.google.com/.well-known/openid-configuration
```

## Part 2: Local Development Setup

Now you'll set up Google Auth to work on your computer.

### Step 1: Install Required Libraries

In your terminal, run:

```
pip install streamlit authlib
```

### Step 2: Create `.streamlit/secrets.toml` ⚠️ CRITICAL STEP

⚠️ **READ THIS CAREFULLY - MUST FOLLOW EXACTLY**

You MUST create a file at `.streamlit/secrets.toml` in your project. The structure and naming MUST be exactly as shown below, or Google Authentication will NOT work.

#### Folder Structure (Must Match Exactly)

```
your-project-folder/
├── .streamlit/
│   └── secrets.toml
├── app.py
├── .env
└── .gitignore
```

- Create a folder named `.streamlit` (with a dot at the start)
- Inside that folder, create a file named `secrets.toml` (exactly this name)
- The file extension MUST be `.toml` (not `.txt` or anything else)

#### File Content (Follow Pattern Strictly)

Open `.streamlit/secrets.toml` and paste this EXACT content:

```toml
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "your-random-secret-key-here"
client_id = "your-client-id.apps.googleusercontent.com"
client_secret = "your-client-secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

⚠️ **DO NOT CHANGE THE SECTION NAMES** - They must be exactly:
- `[auth]` (not `[AUTH]` or `[Auth]`)

#### Replace These Values Only

Only replace the values shown below (keep everything else exactly the same):

1. **`your-random-secret-key-here`** → Replace with any random string, like:
   - `abcd1234efgh5678ijkl9012`
   - `my-secret-key-2024`
   - Or generate one: https://tools.ietf.org/html/rfc4648

2. **`your-client-id.apps.googleusercontent.com`** → Replace with your FULL Client ID from Google Cloud (it will look like: `123456789-abcdefg.apps.googleusercontent.com`)

3. **`your-client-secret`** → Replace with your Client Secret from Google Cloud

#### Verify Your File is Correct

Your secrets.toml should look like this (with YOUR values):

```toml
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "my-secret-key-xyz123"
client_id = "123456789-abcdefg.apps.googleusercontent.com"
client_secret = "GOCSPX-1234567890abcdefgh"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

#### Add to .gitignore

Make ABSOLUTELY SURE this file is protected. Add it to `.gitignore`:

```
.streamlit/secrets.toml
```

Your `.gitignore` should now have:
```
.env
client_secret.json
.streamlit/secrets.toml
```

### Step 3: Create Your Streamlit App with Google Auth

Create a file called `app.py`:

```python
import streamlit as st

st.set_page_config(page_title="My App", layout="wide")

# Check if user is logged in
if not st.user.is_logged_in:
    # Show login button
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown("## Please log in to continue")
        if st.button("🔐 Log in with Google", use_container_width=True):
            st.login("google")
    st.stop()

# User is logged in - show the app
st.markdown(f"## Welcome, {st.user.name}! 👋")
st.write(f"Email: {st.user.email}")

if st.button("Log out"):
    st.logout()

# Your app content goes here
st.write("This is your protected app content!")
st.write("Only logged-in users can see this.")
```

### Step 4: Run Your App Locally

In your terminal, run:

```
streamlit run app.py
```

Your app will open at `http://localhost:8501`. Click the login button and sign in with your Google account. You should be able to log in if:
- Your email is in the test users list
- Your credentials file has the correct Client ID and Client Secret

## Part 3: Deployment Setup (Going Live)

When you're ready to deploy your app to the internet, you need to make two changes:

### Change 1: Update the Redirect URI in Your Secrets

Your deployed app will have a different URL than `localhost`. For example, if you're deploying on Streamlit Cloud:

Your app URL will be something like: `https://my-awesome-app.streamlit.app`

Update your secrets.toml redirect URI:

```toml
[auth]
redirect_uri = "https://my-awesome-app.streamlit.app/oauth2callback"
```

(Replace `my-awesome-app` with your actual app name)

**For Streamlit Cloud**: Go to your app settings and set this in the "Secrets" section instead of a local file.

**For other hosting platforms**: Update the secrets on your hosting platform's secrets/environment variables section.

### Change 2: Add the New URL to Google Cloud

You can add additional authorized redirect URIs in Google Cloud if you know a URL you will use in the future.

1. Go back to Google Cloud Console
2. Go to "APIs & Services" → "Credentials"
3. Click on your OAuth 2.0 client
4. Update "Authorized JavaScript origins":
   - Keep `http://localhost:8501` (for local testing)
   - Add your deployment URL (example: `https://my-awesome-app.streamlit.app`)
5. Update "Authorized redirect URIs":
   - Keep `http://localhost:8501/oauth2callback` (for local testing)
   - Add your deployment redirect URI (example: `https://my-awesome-app.streamlit.app/oauth2callback`)
6. Click "Save"

### Deployment Checklist

Before deploying, make sure:

- ✓ Your redirect URI in secrets.toml matches your actual app URL
- ✓ Your app URL is added to Google Cloud authorized URIs
- ✓ Your Client ID and Client Secret are in your hosting platform's secrets
- ✓ Your `.gitignore` includes `client_secret.json` and `.streamlit/secrets.toml`
- ✓ Your `.env` file is also protected by `.gitignore`

## Complete App Example

Here's a more complete example with protected pages:

```python
import streamlit as st

st.set_page_config(page_title="My Protected App", layout="wide")

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Check authentication
if not st.user.is_logged_in:
    # Login page
    st.markdown("# 🔐 Secure Application")
    st.markdown("Please log in with your Google account to continue.")
    
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("Log in with Google", use_container_width=True, key="login"):
            st.login("google")
    st.stop()

# User is authenticated - show main app
st.sidebar.markdown(f"Logged in as: **{st.user.name}**")
st.sidebar.markdown(f"Email: `{st.user.email}`")

if st.sidebar.button("Log out", key="logout"):
    st.logout()

# Navigation
page = st.sidebar.radio("Navigate", ["Home", "Dashboard", "Settings"])

if page == "Home":
    st.markdown("# Welcome! 👋")
    st.write(f"Hello, {st.user.name}!")
    st.write("This app is protected with Google Authentication.")

elif page == "Dashboard":
    st.markdown("# Dashboard")
    st.write("Your protected dashboard content here.")
    st.bar_chart({"data": [1, 5, 2, 6, 2, 1]})

elif page == "Settings":
    st.markdown("# Settings")
    st.write(f"User ID: {st.user.sub}")
    st.write(f"Email: {st.user.email}")
    st.write(f"Email verified: {st.user.get('email_verified', 'N/A')}")
```

## Common Issues and Solutions

### "Invalid Redirect URI"

**Problem**: Google is rejecting your redirect URI.

**Solutions**:
- Make sure your redirect URI matches exactly (http vs https, including `/oauth2callback`)
- Add the exact URL to Google Cloud's authorized redirect URIs
- Clear your browser cookies and try again

### "Client ID not found"

**Problem**: Streamlit can't find your Google credentials.

**Solutions**:
- Check that your Client ID is correct in secrets.toml
- Make sure you're using the full Client ID (including `.apps.googleusercontent.com`)
- Restart your Streamlit app after changing secrets

### "User not authorized"

**Problem**: You can see the login button, but login fails.

**Solutions**:
- Make sure your email is in the test users list in Google Cloud Console
- Your app is still in "Testing" mode—only test users can log in
- Once you're ready to go live, change the app status to "Published" in Google Cloud Console

### "Secrets not loading on deployed app"

**Problem**: Works locally but fails after deployment.

**Solutions**:
- Make sure you've added your secrets to your hosting platform
- For Streamlit Cloud, add them in the "Advanced settings" → "Secrets" section
- Redeploy your app after adding secrets
- Make sure the secret names match exactly (case-sensitive)

## Summary: Local vs Deployment Changes

**Just two things change when you deploy:**

1. **In secrets.toml**: Change `redirect_uri` from `http://localhost:8501/oauth2callback` to your app's actual URL
2. **In Google Cloud Console**: Add your app's URL to both "Authorized JavaScript origins" and "Authorized redirect URIs"

Everything else stays the same!