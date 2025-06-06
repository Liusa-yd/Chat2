"""
main.py - 自助式数据分析（数据分析智能体）

Author: 骆昊
Version: 0.1
"""
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from langchain.memory import ConversationBufferMemory

from utils import dataframe_agent,get_ai_response


def create_chart(input_data, chart_type):
    """生成统计图表"""
    df_data = pd.DataFrame(
        data={
            "x": input_data["columns"],
            "y": input_data["data"]
        }
    )
    df_data.set_index("x", inplace=True)
    if chart_type == "bar":
        st.bar_chart(df_data)
    elif chart_type == "line":
        plt.plot(df_data.index, df_data["y"], marker="o", linestyle="--")
        plt.ylim(0, df_data["y"].max() * 1.1)
        plt.title("xxxxxxxxxxx")
        st.pyplot(plt.gcf())
        # st.line_chart(df_data)


# st.title("千锋互联数据分析智能体")
# option = st.radio("请选择数据文件类型:", ("Excel", "CSV"))
# file_type = "xlsx" if option == "Excel" else "csv"
# data = st.file_uploader(f"上传你的{option}数据文件", type=file_type)
# if data:
#     if file_type == "xlsx":
#         st.session_state["df"] = pd.read_excel(data, sheet_name='data')
#     else:
#         st.session_state["df"] = pd.read_csv(data)
#     with st.expander("原始数据"):
#         st.dataframe(st.session_state["df"])
#
# query = st.text_area(
#     "请输入你关于以上数据集的问题或数据可视化需求：",
#     disabled="df" not in st.session_state
# )
# button = st.button("生成回答")
#
# if button and "df" not in st.session_state:
#     st.info("请先上传数据文件")
#     st.stop()
# if query:
#     with st.spinner("AI正在思考中，请稍等..."):
#         result = dataframe_agent(st.session_state["df"], query)
#         if "answer" in result:
#             st.write(result["answer"])
#         if "table" in result:
#             st.table(pd.DataFrame(result["table"]["data"],
#                                   columns=result["table"]["columns"]))
#         if "bar" in result:
#             create_chart(result["bar"], "bar")
#         if "line" in result:
#             create_chart(result["line"], "line")
#
#
# if 'messages' not in st.session_state:
#     st.session_state['messages'] = [{'role': 'ai', 'content': '你好主人，我是你的AI助手，我叫小美。'}]
#     st.session_state['memory'] = ConversationBufferMemory(return_messages=True)
#
# for message in st.session_state['messages']:
#     role, content = message['role'], message['content']
#     st.chat_message(role).write(content)
#
# user_input = st.chat_input()
# if user_input:
#     st.chat_message('human').write(user_input)
#     st.session_state['messages'].append({'role': 'human', 'content': user_input})
#     with st.spinner('AI正在思考，请等待……'):
#         resp_from_ai = get_ai_response(user_input)
#         st.session_state['history'] = resp_from_ai
#         st.chat_message('ai').write(resp_from_ai)
#         st.session_state['messages'].append({'role': 'ai', 'content': resp_from_ai})


# ... (前面的导入和初始代码保持不变)

st.title("千锋互联数据分析智能体")

# 添加功能选择器
function_choice = st.radio(
    "请选择要使用的功能:",
    ("数据分析智能体", "通用AI聊天"),
    horizontal=True
)

if function_choice == "数据分析智能体":
    # 数据分析功能部分
    option = st.radio("请选择数据文件类型:", ("Excel", "CSV"), horizontal=True)
    file_type = "xlsx" if option == "Excel" else "csv"
    data = st.file_uploader(f"上传你的{option}数据文件", type=file_type)

    if data:
        if file_type == "xlsx":
            st.session_state["df"] = pd.read_excel(data, sheet_name='data')
        else:
            st.session_state["df"] = pd.read_csv(data)
        with st.expander("原始数据"):
            st.dataframe(st.session_state["df"])

    query = st.text_area(
        "请输入你关于以上数据集的问题或数据可视化需求：",
        disabled="df" not in st.session_state
    )
    button = st.button("生成回答")

    if button and "df" not in st.session_state:
        st.info("请先上传数据文件")
        st.stop()
    if query:
        with st.spinner("AI正在思考中，请稍等..."):
            result = dataframe_agent(st.session_state["df"], query)
            if "answer" in result:
                st.write(result["answer"])
            if "table" in result:
                st.table(pd.DataFrame(result["table"]["data"],
                                      columns=result["table"]["columns"]))
            if "bar" in result:
                create_chart(result["bar"], "bar")
            if "line" in result:
                create_chart(result["line"], "line")

else:
    # 通用聊天功能部分
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [{'role': 'ai', 'content': '你好主人，我是你的AI助手，我叫小美。'}]
        st.session_state['memory'] = ConversationBufferMemory(return_messages=True)

    for message in st.session_state['messages']:
        role, content = message['role'], message['content']
        st.chat_message(role).write(content)

    user_input = st.chat_input()
    if user_input:
        st.chat_message('human').write(user_input)
        st.session_state['messages'].append({'role': 'human', 'content': user_input})
        with st.spinner('AI正在思考，请等待……'):
            resp_from_ai = get_ai_response(user_input)
            st.session_state['history'] = resp_from_ai
            st.chat_message('ai').write(resp_from_ai)
            st.session_state['messages'].append({'role': 'ai', 'content': resp_from_ai})