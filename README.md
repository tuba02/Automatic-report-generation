# AIレポート生成ツール
このプロジェクトは、最新のトピックに関するAI要約レポートを自動生成し、PDF形式で保存・ダウンロードできるStreamlitアプリです。  
Web検索結果をもとに、LangChainとOpenRouterを通じてAIがレポートを生成します。

## 機能概要
・ Web検索を活用した最新情報の収集（DuckDuckGo）
・ GPTを用いた300〜400文字のMarkdown形式要約
・ FPDF + IPAex明朝によるPDFレポート出力
・ Markdown / PDFでのローカル保存 & ダウンロード対応
・ 検索クエリと要約ログの保存（`search_log.txt`）

## 使用技術
・ Python
・ LangChain　(https://www.langchain.com/)
・ OpenRouter (GPT-3.5) (https://openrouter.ai/)
・ DuckDuckGo Search Tool　(https://python.langchain.com/docs/modules/agents/tools/integrations/ddg_search/)
・ FPDF　(https://pyfpdf.readthedocs.io/)
・ Streamlit　(https://streamlit.io/)

## フォントについて
PDF出力には日本語表示に対応した以下のフォントを使用しています：
・ フォント名：**IPAex明朝（ipaexm.ttf）**
・ 配布元：情報処理推進機構 (IPA) (https://moji.or.jp/ipafont/)
・ ライセンス：**IPAフォントライセンスv1.0**

### ライセンス条件（概要）
・ 商用・非商用問わず利用可能  
・ 再配布可能（ライセンス表記が必要）  
・ 改変後のフォントに元の名前を使うことは禁止

> 本プロジェクトでは、上記ライセンスに基づき `ipaexm.ttf` を再配布しています。詳細は [IPAフォントライセンスv1.0](https://moji.or.jp/ipafont/license/) をご確認ください。

## セットアップ方法

1. 必要ライブラリをインストール：
pip install -r requirements.txt


