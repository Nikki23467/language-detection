# 🌐 Language Detection App

A Streamlit web application that detects the language of the input text using the **Google Gemini API**. The app includes a secure login and registration system, allowing users to interact safely and privately.

## 🚀 Features

- 🔐 **Secure Authentication**: Login and registration functionality with SHA256-hashed passwords stored in a local JSON file.
- 🌍 **Language Detection**: Uses Google's Gemini API to identify the language of any given text.
- 🧠 **AI Integration**: Prompts Gemini with natural language queries for robust, accurate responses.
- ✅ **User Feedback**: Visual feedback using Streamlit's user interface components.
- 📄 **Environment Configuration**: Secure API key handling using `.env` files.

> 📝 **Note:** Due to how Streamlit session state and rerun handling works, you may need to **click the Login or Logout button twice** to fully transition between states.
> Try it out here: https://language-detection-nikhilesh.streamlit.app/
