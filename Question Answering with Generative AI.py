from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

class MarketingContentGenerator:

    def __init__(self, model_name="mixtral-8x7b-32768", temperature=0.7, groq_api_key="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"):
        self.model_name = model_name
        self.temperature = temperature
        self.groq_api_key = groq_api_key 

        self.chat = ChatGroq(temperature=self.temperature, groq_api_key=self.groq_api_key, model_name=self.model_name)

    def generate_marketing_content(self, topic, format, emotion=None):
        loader = WebBaseLoader("https://www.espn.com/")  
        data = loader.load()
        data = data[0].page_content

        system_prompt = self._build_system_prompt(format, emotion)
        human_prompt = f"data = <{data}>"

        prompt = ChatPromptTemplate.from_messages([("system", system_prompt),("human",human_prompt)])
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


marketing_generator = MarketingContentGenerator()

linkedin_post = marketing_generator.generate_marketing_content(
    topic="Generative AI", format="linkedin_post", emotion="excited"
)

print(linkedin_post)

blog_intro = marketing_generator.generate_marketing_content(
    topic="AI in Healthcare", format="blog_intro", emotion="informative"
)

print(blog_intro)
