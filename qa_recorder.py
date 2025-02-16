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
        new_record = pd.DataFrame({
            'Date': [current_date],
            'Question': [question],
            'Result': [answer]
        })

        if os.path.exists(self.excel_path):
            # 如果文件存在，讀取並附加新記錄
            existing_df = pd.read_excel(self.excel_path)
            updated_df = pd.concat([existing_df, new_record], ignore_index=True)
        else:
            # 如果文件不存在，創建新的 DataFrame
            updated_df = new_record

        # 保存到 Excel
        updated_df.to_excel(self.excel_path, index=False)
        
        # 生成 HTML 文件
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
            {updated_df.to_html(index=False, classes='qa-table', escape=False)}
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

def process_text_file(file_path, recorder):
    """
    處理文本文件中的問題
    :param file_path: 文本文件路徑
    :param recorder: QARecorder 實例
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        questions = file.readlines()
    
    for question in questions:
        question = question.strip()
        if question:  # 確保不是空行
            recorder.process_input(question)

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
                    file_path = os.path.join(os.path.dirname(__file__), "input_question.txt")
                    try:
                        if not os.path.exists(file_path):
                            print(f"錯誤：找不到文件 {file_path}")
                            print("請確保在程式同目錄下存在 input_question.txt 文件")
                            continue
                            
                        process_text_file(file_path, debug_recorder)
                        print("文件處理完成！")
                    except Exception as e:
                        print(f"處理文件時發生錯誤: {str(e)}")

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
            file_path = os.path.join(os.path.dirname(__file__), "input_question.txt")
            try:
                if not os.path.exists(file_path):
                    print(f"錯誤：找不到文件 {file_path}")
                    print("請確保在程式同目錄下存在 input_question.txt 文件")
                    continue
                    
                process_text_file(file_path, recorder)
                print("文件處理完成！")
            except Exception as e:
                print(f"處理文件時發生錯誤: {str(e)}")

        elif choice == "3":
            print("程序結束")
            break

        else:
            print("無效的選擇，請重試")

if __name__ == "__main__":
    main() 