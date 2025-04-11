import logging
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.llms import OpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from fpdf import FPDF
import streamlit as st
import warnings
warnings.filterwarnings("ignore", message="cmap value too big/small")

# 環境変数読み込み
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# モデル準備
llm = ChatOpenAI(
    model_name="openai/gpt-3.5-turbo",
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1",
)

# Web検索ツール定義
search_tool = DuckDuckGoSearchRun()

# ツールとLLMの準備
tools = [
    Tool(
        name="Web Search",
        func=search_tool.run,
        description="最新の情報を取得したいときに使う"
    )
]

# エージェントの初期化
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

# ログの設定
logging.basicConfig(
    filename=r"C:\Autoreport\report_output\search_log.txt",
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
)

# Web検索とAI要約のログ記録
def log_search(query, result):
    logging.info(f"検索クエリ: {query}")
    logging.info(f"検索結果: {result}")

# PDF保存のための関数（IPAex明朝フォント使用）
def save_pdf(content, save_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # IPAex明朝フォントを追加
    font_path = r"C:/Autoreport/fonts/ipaexm.ttf"
    pdf.add_font('IPAexMincho', '', font_path, uni=True)

    # タイトル
    pdf.set_font("IPAexMincho", '', 16)
    pdf.cell(200, 10, txt="AIレポート", ln=True, align='C')

    # 本文
    pdf.set_font('IPAexMincho', '', 12)
    pdf.multi_cell(0, 10, content)

    # 保存先
    pdf.output(save_path)
    print(f"✅ PDFレポートが {save_path} に保存されました！")

# 要約を生成し、400字以内になるように確認・再試行する関数
def generate_summary_with_retry(topic, max_retries=3):
    retries = 0
    while retries < max_retries:
        # Web検索と要約実行
        response = agent.run(
            f"""
            次のトピックについてWeb検索を行い、日本語で要約してください。

            【トピック】：{topic}

            要件：
            - 必ず **300文字以上400文字以内** に収めてください。
            - **Markdown形式**で出力してください（例：`### タイトル` や `- 箇条書き` など）。
            - 不要な挨拶や前置きは入れず、**要約本文のみ**を書いてください。
            - 出力の最後に **「文字数：○○字」** と記載してください。
            - **文字数が400字を超えないようにしてください。**
            """
        )

        # 文字数チェック
        if len(response) <= 400:
            return response  # 400字以内であればそのまま返す
        else:
            retries += 1
            # 再試行するメッセージを表示
            print(f"文字数が400字を超えているため、再試行します。試行回数: {retries}")
            # プロンプトに再度要約を依頼（文字数を守るように）
            response = agent.run(
                f"""
                次のトピックについてWeb検索を行い、日本語で要約してください。

                【トピック】：{topic}

                要件：
                - 必ず **300文字以上400文字以内** に収めてください。
                - **Markdown形式**で出力してください（例：`### タイトル` や `- 箇条書き` など）。
                - 不要な挨拶や前置きは入れず、**要約本文のみ**を書いてください。
                - 出力の最後に **「文字数：○○字」** と記載してください。
                - **文字数が400字を超えないようにしてください。**
                - もし400字を超える場合は再試行して、必ず制限内で収めるようにしてください。
                """
            )

    return response  # 最大試行回数に達した場合も最終的に返す

# Streamlit UI部分
st.title("AIレポート生成ツール")
topic = st.text_input("トピックを入力してください：", "2025年のAIトレンド")

if st.button("レポート生成"):
    # Web検索と要約実行（再試行対応）
    response = generate_summary_with_retry(topic)

    # レポートをMarkdown形式で表示
    st.subheader("生成されたレポート")
    st.write(response)
    
    # 保存先設定
    md_save_path = r"C:\Autoreport\report_output\report.md"
    pdf_save_path = r"C:\Autoreport\report_output\report.pdf"

    # フォルダがない場合に作成
    os.makedirs(os.path.dirname(md_save_path), exist_ok=True)
    os.makedirs(os.path.dirname(pdf_save_path), exist_ok=True)

    # Markdown形式で保存
    with open(md_save_path, "w", encoding="utf-8") as f:
        f.write(response)
    print(f"✅ レポートが {md_save_path} に保存されました！")

    # PDF形式で保存
    save_pdf(response, pdf_save_path)

    # ダウンロードボタン（PDFファイル）
    with open(pdf_save_path, "rb") as f:
        st.download_button("PDFで保存", data=f, file_name="report.pdf", mime="application/pdf")
