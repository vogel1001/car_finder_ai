from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.utilities import GoogleSerperAPIWrapper
import streamlit as st
import os
import json

os.environ["SERPER_API_KEY"] = "881bc0574426f66d1cc27ca439c9f386245d0a06"

st.title("Car Finder")

car_type = st.sidebar.selectbox("Car Tpe", ("Sedan", "SUV", "Coupe", "Truck", "Hatchback", "Van", "Electric"))

min_price = st.sidebar.selectbox("Min Price", ("$10,000", "$20,000", "$30,000", "$50,000", "$100,000"))

max_price = st.sidebar.selectbox("Max Price", ("$20,000", "$30,000", "$50,000", "$100,000", "$500,000"))

ranking_metric = st.sidebar.selectbox("Metric", ("Reliability", "Performance", "Off Road", "Fuel Efficienct", "Safety"))

car_year = st.sidebar.text_area(
    label="What year?",
    max_chars=4
)

if car_type and car_year:
    system_template = "You only respond in a JSON Array with snakecase keys. The values are not snakecase. Do not include a key for the JSON Array."
    human_template = "Give me a list of the top 3 {ranking_metric} {car_type} that are under {max_price} and above ${min_price} from the year {car_year}. Car names and short description."

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    chain = LLMChain(
        llm=ChatOpenAI(openai_api_key="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"),
        prompt=chat_prompt
    )

    result = chain.run({'car_type': car_type, 'max_price': max_price, 'min_price': min_price, 'car_year': car_year, 'ranking_metric': ranking_metric})

    car_array = json.loads(result)

    print(car_array)

    for car_info in car_array:
        with st.container(border=True):
            print(car_info)
            st.write(f"**{car_info['car_name']}**")

            link_end = car_info['car_name'].replace(" ", "/")

            print(f"https://www.autotrader.com/cars-for-sale/all-cars/{link_end}")

            search = GoogleSerperAPIWrapper(type="images")
            results = search.results(car_info['car_name'])
            print(results)
            st.image(results['images'][0]['imageUrl'], width=200)
            st.write(car_info['short_description'])
            st.link_button("View on Autotrader", f"https://www.autotrader.com/cars-for-sale/all-cars/{link_end}")