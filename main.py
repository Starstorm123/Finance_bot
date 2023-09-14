import openai
import streamlit as st
from gnewsclient import gnewsclient

# Initialize the GPT-3 API
openai.api_key = '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'

# Initialize the GNewsClient with the desired parameters
news_client = gnewsclient.NewsClient(language='en', location='IN')  # Adjust parameters as needed

def get_news():
    news_articles = news_client.get_news()
    return news_articles

def chat_with_bot(user_input, chat_history):
    # Determine if the user's query is related to financial news
    if "financial news" in user_input.lower():
        # Use the GNewsClient to fetch financial news
        news_query = user_input.replace("financial news", "").strip()
        news_articles = get_news()  # Removed the query parameter
        response = "Financial News Bot: Here are the latest financial news articles related to '{}':\n".format(news_query)
        for idx, article in enumerate(news_articles[:4], 1):
            response += "\n{}. Title: {}".format(idx, article['title'])
            response += "\n   Source: {}".format(article['link'])
            
    else:
        # Use the OpenAI chatbot for other queries
        conversation = [
            {"role": "system", "content": "You are a finance and news assistant."},
            {"role": "user", "content": user_input},
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            max_tokens=50,  # Adjust the max_tokens value to limit response length
        )['choices'][0]['message']['content']
    
    # Add the user's message and bot's response to the chat history
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "bot", "content": response})
    
    return chat_history

def main():
    st.title("Finance and News ChatBot")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("You:")
    
    if st.button("Send"):
        st.session_state.chat_history = chat_with_bot(user_input, st.session_state.chat_history)

    # Display the chat history with the most recent message at the top
    for message in reversed(st.session_state.chat_history):
        st.chat_message(message["role"]).write(message["content"])

if __name__ == "__main__":
    main()
