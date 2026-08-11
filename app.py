# 将原本的 import requests 替换为：
from curl_cffi import requests

# ... 前面代码保持不变 ...

if st.button("开始抓取页面元数据"):
    with st.spinner("正在请求页面..."):
        try:
            # impersonate="chrome110" 会模拟真实 Chrome 浏览器的 TLS/JA3 指纹
            response = requests.get(
                target_url, 
                impersonate="chrome110", 
                timeout=15
            )
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
        except Exception as e:
            st.error(f"页面抓取失败: {e}")
