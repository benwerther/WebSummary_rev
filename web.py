import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Streamlit 앱 제목 설정
st.title("뉴스 기사 요약 블로그 생성기")

# 사용자로부터 여러 개의 URL 입력 받기
st.write("최대 10개의 뉴스 기사 URL을 입력하세요. 각 URL은 새 줄로 구분됩니다:")
urls_input = st.text_area("URL 입력", height=200)

if st.button("요약하기"):
    if urls_input:
        # 로딩 메시지 표시
        with st.spinner("뉴스 기사를 분석 중입니다..."):
            # URL 리스트 생성
            urls = [url.strip() for url in urls_input.strip().split('\n') if url.strip()][:10]

            # 성공적으로 로드된 기사들을 저장할 리스트
            successful_docs = []
            failed_urls = []

            # 각 URL에 대해 개별적으로 처리
            for url in urls:
                try:
                    loader = WebBaseLoader(url)
                    data = loader.load()
                    # 불필요한 공백 제거
                    content = data[0].page_content.strip()
                    successful_docs.append({'url': url, 'content': content})
                except Exception as e:
                    failed_urls.append(url)

            if successful_docs:
                # 모든 뉴스 기사의 내용을 합침
                combined_content = ""
                for doc in successful_docs:
                    combined_content += f"기사 원본 링크: {doc['url']}\n\n{doc['content']}\n\n"

                # Groq LLM 초기화
                llm = ChatGroq(
                    model="llama-3.1-70b-versatile",
                )

                # 메시지 준비
                messages = [
                    (
                        "system",
                        "You are a professional blogger. Summarize the following news articles into a cohesive blog post with sections on 'World Economy' and 'AI Industry'. Use markdown formatting with headers, bullet points, and include the original article links. Make the content engaging and suitable for publishing on a blog.",
                    ),
                    ("human", combined_content),
                ]

                # LLM 호출
                ai_msg = llm.invoke(messages)

                # 결과 표시
                st.subheader("블로그 요약 결과:")
                st.markdown(ai_msg.content)
            else:
                st.error("유효한 기사를 로드하지 못했습니다. 입력된 URL을 확인해주세요.")

            if failed_urls:
                st.warning(f"다음 URL에서 기사를 로드하지 못했습니다:\n" + "\n".join(failed_urls))
    else:
        st.warning("URL을 입력해주세요.")
