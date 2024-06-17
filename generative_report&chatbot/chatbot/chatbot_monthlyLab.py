from langchain.agents import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI

from langchain_openai import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler

import streamlit as st
import pandas as pd
import os

from dotenv import load_dotenv
load_dotenv()


def clear_submit():
    """
    Clear the Submit Button State
    Returns:

    """
    st.session_state["submit"] = False


st.set_page_config(page_title="Monthly Lab", page_icon="💡")
st.title("💡 Monthly Lab Chatbot for GIST")

cluster_keyword_xlsx = "/Users/jaehpark/ai_pbl_1/dataset/cluster_keyword.xlsx"
ntis_all_xlsx = "/Users/jaehpark/ai_pbl_1/dataset/ntis_.xlsx"
gist_all_xlsx = "/Users/jaehpark/ai_pbl_1/dataset/gist_.xlsx"
cluster_keyword_df = pd.read_excel(cluster_keyword_xlsx)
ntis_all_df = pd.read_excel(ntis_all_xlsx)
gist_all_df = pd.read_excel(gist_all_xlsx)

df_list = [cluster_keyword_df, ntis_all_df, gist_all_df]

if "messages" not in st.session_state or st.sidebar.button("Clear conversation history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="연구비와 관련된 질문이 있으신가요?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    class StreamCallback(BaseCallbackHandler):
        def on_llm_new_token(self, token: str, **kwargs):
            print(token, end="", flush=True)

    model_base = ChatOpenAI(
        temperature=0,
        # model_name='gpt-4',
        # model_name='gpt-4o',
        model_name='gpt-4-turbo',
        streaming=True,
        callbacks=[StreamCallback()],
    )

    from langchain_experimental.agents.agent_toolkits.pandas.prompt import MULTI_DF_PREFIX
    MULTI_DF_PREFIX="""
    You are working with {num_dfs} pandas dataframes in Python named df1, df2, df3 etc. 
    The agent is capable of performing data analysis on three given dataframes contained within ‘df_list’ and answering user questions.

    The dataframes included in ‘df_list’ are as follows:
    - df1 (cluster_keyword_df): Presents the keywords represented by each of the four clusters, from cluster 0 to 3.
    - df2 (ntis_all_df): This is domestic data. It contains the Total Funding invested in the 'Optics' field, the Funding invested in specific clusters, and the Share of each cluster's Funding relative to the Total Funding by year. The unit of Funding is Korean Won (KRW).
    - df3 (gist_all_df): This is institutional (GIST) data. It contains the Total Funding invested in the 'Optics' field, the Funding invested in specific clusters, and the Share of each cluster's Funding relative to the Total Funding by year. The unit of Funding is Korean Won (KRW).

    - All questions should be answered in Korean.
    - The current year is 2024.

    - Please provide all answers with evidence related to research funding data.
    - Analyze research funding based on year-on-year changes of funding.
    - Express all amounts of research funding in Korean “원(₩)”.
    - Represent all percentages (%) without decimal points.
    - Please do not use the word "Cluster" in your answers. Instead, use the corresponding "Keyword" for each cluster.
    - Conduct the analysis of "Institution (GIST) data" based on the "Domestic data."
    - "Domestic" data refers to figures concerning the entire country, while "institution" data pertains to specific institutions within the country. Therefore, it is natural for the scale of research funding in domestic data to be significantly larger than that of institutional data. Please do not include this discrepancy in your analysis results.
    

    You should use the tools below to answer the question posed of you:
    """

    df_agent = create_pandas_dataframe_agent(
        model_base,
        df_list,
        # verbose=True,
        verbose=False,
        prefix=MULTI_DF_PREFIX,
        include_df_in_prompt=True,
        number_of_head_rows=23,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = df_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
