# AI Customer Support Chatbot

An interactive AI chatbot prototype built using Python, Streamlit, and Natural Language Processing (NLP).

## Features
- Interactive chat interface
- Futuristic background and custom UI
- Keyword-based responses for account, order, delivery, refund, payment, and support questions
- Machine-learning intent classification using TF-IDF and Logistic Regression
- Saved model and vectorizer for prediction

## Technologies Used
- Python
- Streamlit
- Scikit-learn
- TF-IDF
- Logistic Regression
- Joblib

## Project Structure
```text
AI Customer Support Chatbot/
├── Data/
├── notebooks/
│   ├── app.py
│   └── customer_support_chatbot.ipynb
├── outputs/
│   ├── intent_model.pkl
│   └── tfidf_vectorizer.pkl
├── chatbot_bg.png.png
├── intent-corpus-enrich-limit-20.json
├── README.md
└── requirements.txt
```

## Run Locally
1. Install the required packages:
   `pip install -r requirements.txt`
2. Start the Streamlit app:
   `streamlit run notebooks/app.py`

## Note
This is a learning prototype. Common customer-support questions are handled using keyword-based rules, while other messages can use the saved intent classifier. The saved classifier was trained on the available intent dataset, which includes game/voice-assistant intents; it has not been trained specifically on a customer-support dataset.