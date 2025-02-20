import openai
import pandas as pd
from datetime import datetime
import os

try:
    # 優先使用本地配置
    from config_local import API_KEY, API_BASE, MODEL_NAME
except ImportError:
    # 如果本地配置不存在，使用默認配置
    from config import API_KEY, API_BASE, MODEL_NAME

class QARecorder:
    def __init__(self, api_key, api_base, model_name="gpt-3.5-turbo", output_dir="output", debug_mode=False):
        """
        初始化 QA 記錄器
        :param api_key: OpenAI API 金鑰
        :param api_base: API 基礎 URL
        :param model_name: AI 模型名稱
        :param output_dir: 輸出目錄
        :param debug_mode: 是否啟用除錯模式
        """
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=api_base,
            timeout=60
        )
        self.model_name = model_name
        self.debug_mode = debug_mode
        
        # 確保輸出目錄存在
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 設定輸出文件路徑
        self.excel_path = os.path.join(self.output_dir, "qa_records.xlsx")
        self.html_path = os.path.join(self.output_dir, "qa_records.html")

    def ask_question(self, question):
        """
        向 AI 詢問問題
        :param question: 問題內容
        :return: AI 的回答
        """
        # 如果是除錯模式，直接返回問題內容
        if self.debug_mode:
            return f"收到的問題是: \"{question}\" (This is debug mode)"

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"詳細錯誤信息: {str(e)}")
            return f"錯誤：{str(e)}"

    def save_to_excel(self, question, answer):
        """
        將問答記錄保存到 Excel 和 HTML
        :param question: 問題
        :param answer: 回答
        """
        current_date = datetime.now().strftime("%Y/%m/%d")
        
        # 為 Excel 準備純文字格式
        excel_record = pd.DataFrame({
            'Date': [current_date],
            'Question': [question],  # 保持原始格式
            'Result': [answer]       # 保持原始格式
        })

        # 為 HTML 準備格式化文字
        html_question = question.replace('\n', '<br>')
        html_answer = answer.replace('\n', '<br>')
        
        # 處理 Markdown 格式
        html_answer = (html_answer
            .replace('**', '<strong>')  # 開始粗體
            .replace('**', '</strong>')  # 結束粗體
            .replace('`', '<code>')  # 開始程式碼
            .replace('`', '</code>')  # 結束程式碼
            .replace('###', '<h3>')  # 開始標題
            .replace('\n', '</h3>', 1)  # 結束標題（只替換第一個換行）
        )
        
        # 處理程式碼區塊
        if '```' in html_answer:
            html_answer = html_answer.replace(
                '```python', '<pre><code class="language-python">'
            ).replace(
                '```', '</code></pre>'
            )

        html_record = pd.DataFrame({
            'Date': [current_date],
            'Question': [html_question],
            'Result': [html_answer]
        })

        # 保存到 Excel
        if os.path.exists(self.excel_path):
            existing_df = pd.read_excel(self.excel_path)
            updated_excel_df = pd.concat([existing_df, excel_record], ignore_index=True)
        else:
            updated_excel_df = excel_record
        
        updated_excel_df.to_excel(self.excel_path, index=False)

        # 生成 HTML
        if os.path.exists(self.excel_path):
            existing_df = pd.read_excel(self.excel_path)
            # 將所有現有記錄也轉換為 HTML 格式
            for i in range(len(existing_df)):
                if i == len(existing_df) - 1:  # 跳過最後一筆（剛剛新增的）
                    continue
                existing_df.loc[i, 'Question'] = existing_df.loc[i, 'Question'].replace('\n', '<br>')
                existing_df.loc[i, 'Result'] = existing_df.loc[i, 'Result'].replace('\n', '<br>')
            
            updated_html_df = pd.concat([existing_df, html_record], ignore_index=True)
        else:
            updated_html_df = html_record

        # 更新 CSS 樣式
        css_style = """
            body { 
                font-family: Arial, sans-serif; 
                margin: 20px; 
            }
            table { 
                border-collapse: collapse; 
                width: 100%; 
            }
            th, td { 
                padding: 12px; 
                text-align: left; 
                border: 1px solid #ddd; 
                vertical-align: top;
            }
            th { 
                background-color: #4CAF50; 
                color: white; 
            }
            tr:nth-child(even) { 
                background-color: #f2f2f2; 
            }
            tr:hover { 
                background-color: #ddd; 
            }
            .qa-container { 
                margin-bottom: 20px; 
            }
            pre {
                background-color: #f5f5f5;
                padding: 10px;
                border-radius: 4px;
                overflow-x: auto;
            }
            code {
                font-family: Consolas, Monaco, 'Courier New', monospace;
                background-color: #f5f5f5;
                padding: 2px 4px;
                border-radius: 3px;
            }
            h3 {
                color: #2c3e50;
                margin-top: 20px;
                margin-bottom: 10px;
            }
            strong {
                color: #2c3e50;
            }
        """

        html_content = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                {css_style}
            </style>
        </head>
        <body>
            <h1>QA Records</h1>
            {updated_html_df.to_html(index=False, classes='qa-table', escape=False)}
        </body>
        </html>
        """
        
        # 保存 HTML 文件
        with open(self.html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def process_input(self, input_text):
        """
        處理輸入並記錄結果
        :param input_text: 輸入的問題文本
        """
        answer = self.ask_question(input_text)
        self.save_to_excel(input_text, answer)
        return answer

    def process_text_file(self, file_path):
        """
        處理文本文件中的問題
        格式：使用 --- 作為問題分隔符，# 開頭的行作為問題標題
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                questions = content.split('---')
                
                for question in questions:
                    question = question.strip()
                    if question:  # 確保不是空白問題
                        self.process_input(question)
            return True
        except Exception as e:
            print(f"處理文件時發生錯誤: {str(e)}")
            return False

def main():
    recorder = QARecorder(API_KEY, API_BASE, MODEL_NAME)

    while True:
        print("\n=== 主選單 ===")
        print("1. 輸入問題")
        print("2. 從文本文件讀取問題")
        print("3. 退出")
        print("4. 進入除錯模式")
        
        choice = input("請選擇操作 (1-4): ")

        if choice == "4":
            print("\n=== 除錯模式 ===")
            debug_recorder = QARecorder(API_KEY, API_BASE, MODEL_NAME, debug_mode=True)
            
            while True:
                print("\n【目前處於除錯模式】")
                print("1. 輸入問題")
                print("2. 從文本文件讀取問題")
                print("3. 返回主選單")
                
                debug_choice = input("請選擇操作 (1-3): ")
                
                if debug_choice == "1":
                    question = input("請輸入您的問題: ")
                    answer = debug_recorder.process_input(question)
                    print(f"\n回答: {answer}")

                elif debug_choice == "2":
                    file_path = os.path.join(os.path.dirname(__file__), "input_questions.txt")
                    if not os.path.exists(file_path):
                        print(f"錯誤：找不到文件 {file_path}")
                        print("請確保文件存在並使用正確的格式")
                        continue

                    debug_recorder.process_text_file(file_path)
                    print("文件處理完成！")

                elif debug_choice == "3":
                    print("返回主選單")
                    break

                else:
                    print("無效的選擇，請重試")

        elif choice == "1":
            question = input("請輸入您的問題: ")
            answer = recorder.process_input(question)
            print(f"\n回答: {answer}")

        elif choice == "2":
            file_path = os.path.join(os.path.dirname(__file__), "input_questions.txt")
            if not os.path.exists(file_path):
                print(f"錯誤：找不到文件 {file_path}")
                print("請確保文件存在並使用正確的格式")
                continue

            recorder.process_text_file(file_path)
            print("文件處理完成！")

        elif choice == "3":
            print("程序結束")
            break

        else:
            print("無效的選擇，請重試")

if __name__ == "__main__":
    main() 