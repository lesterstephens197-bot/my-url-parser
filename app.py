import streamlit as st
from urllib.parse import urlparse, parse_qs
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="URL 参数与元数据解析器", page_icon="🔗", layout="wide")

st.title("🔗 URL 参数与页面元数据抓取工具")
st.write("输入任意链接，提取 URL Query 参数及网页 Open Graph / Meta 元数据。")

input_url = st.text_input("请输入目标 URL:", placeholder="https://example.com/page?utm_source=google&id=123")

if input_url:
    target_url = input_url if input_url.startswith(("http://", "https://")) else "https://" + input_url

    parsed_url = urlparse(target_url)
    query_params = parse_qs(parsed_url.query)

    st.subheader("📌 1. URL 基础结构与 Query 参数")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**域名 (Host):** `{parsed_url.netloc}`")
        st.write(f"**路径 (Path):** `{parsed_url.path}`")
    with col2:
        st.write(f"**协议 (Scheme):** `{parsed_url.scheme}`")
        st.write(f"**锚点 (Fragment):** `{parsed_url.fragment}`")

    if query_params:
        param_data = [{"参数名 (Key)": k, "参数值 (Value)": ", ".join(v)} for k, v in query_params.items()]
        st.markdown("##### 提取到的 Query 参数")
        st.dataframe(pd.DataFrame(param_data), use_container_width=True)
    else:
        st.info("该链接中未包含 Query 参数。")

    st.divider()

    st.subheader("🌐 2. 页面 Meta 与 Open Graph 详细参数")
    if st.button("开始抓取页面元数据"):
        with st.spinner("正在请求页面..."):
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
                }
                response = requests.get(target_url, headers=headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, "html.parser")
                page_title = soup.title.string.strip() if soup.title and soup.title.string else "未获取到标题"
                
                meta_data = []
                for tag in soup.find_all("meta"):
                    name = tag.get("name") or tag.get("property")
                    content = tag.get("content")
                    if name and content:
                        meta_data.append({"属性 (Name/Property)": name, "内容 (Content)": content})

                st.success("抓取成功！")
                st.write(f"**页面 Title:** {page_title}")
                if meta_data:
                    st.dataframe(pd.DataFrame(meta_data), use_container_width=True)
                else:
                    st.warning("未在页面中找到有效的 Meta 标签。")
            except requests.exceptions.RequestException as e:
                st.error(f"页面抓取失败: {e}")
