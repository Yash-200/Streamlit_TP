import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

class MarketingContentGenerator:

    def __init__(self, model_name="mixtral-8x7b-32768", temperature=0.7, groq_api_key=None):
        self.model_name = model_name
        self.temperature = temperature
        self.groq_api_key = groq_api_key

        if groq_api_key:
            self.chat = ChatGroq(temperature=self.temperature, groq_api_key=groq_api_key, model_name=self.model_name)
        else:
            st.error("Please enter your Groq API Key")

    def generate_marketing_content(self, topic, format, emotion=None, website=None):
        if not self.groq_api_key:
            return None

        # Use website URL if provided, otherwise default to ESPN
        loader = WebBaseLoader(website if website else "https://www.espn.com/")
        data = loader.load()
        data = data[0].page_content

        system_prompt = self._build_system_prompt(format, emotion)
        human_prompt = f"data = <{data}>"

        prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", human_prompt)])
        chain = prompt | self.chat
        response = chain.invoke({"topic": topic})
        return response.content

    def _build_system_prompt(self, format, emotion):
        base_prompt = f"""You are a large language model focused on generating creative marketing content.
        You can tailor your content to different formats,emojies and emotional tones.
        Here's the format: {format}
        """
        if emotion:
            base_prompt += f" Aim for a {emotion} tone.\n"
        base_prompt += "Use the provided data source to inform your content.\n"

        return base_prompt + "Question: <{topic}>,"


# Streamlit App
st.title("Marketing Content Generator")

api_key = st.text_input("Enter your Groq API Key:", type="password")  # Mask input for security
topic = st.text_input("Enter your topic:")
website = st.text_input("Enter a website URL (optional):")
format = st.selectbox("Choose a format:", ["linkedin_post", "blog_intro"])
emotion = st.selectbox("Select an emotion (optional):", ["", "excited", "informative"])

if st.button("Generate Content"):
    marketing_generator = MarketingContentGenerator(groq_api_key=api_key)
    content = marketing_generator.generate_marketing_content(topic, format, emotion, website)

    if content:
        st.write(content)
    else:
        st.warning("Please enter a valid Groq API Key")
