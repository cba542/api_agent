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
    def __init__(self, api_key, api_base, model_name="gpt-3.5-turbo", excel_path="qa_records.xlsx"):
        """
        初始化 QA 記錄器
        :param api_key: OpenAI API 金鑰
        :param api_base: API 基礎 URL
        :param model_name: AI 模型名稱
        :param excel_path: Excel 文件路徑
        """
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=api_base,
            timeout=60  # 增加超時時間
        )
        self.model_name = model_name
        self.excel_path = excel_path

    def ask_question(self, question):
        """
        向 AI 詢問問題
        :param question: 問題內容
        :return: AI 的回答
        """
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
            print(f"詳細錯誤信息: {str(e)}")  # 添加詳細錯誤信息輸出
            return f"錯誤：{str(e)}"

    def save_to_excel(self, question, answer):
        """
        將問答記錄保存到 Excel
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
        print("\n1. 輸入問題")
        print("2. 從文本文件讀取問題")
        print("3. 退出")
        choice = input("請選擇操作 (1-3): ")

        if choice == "1":
            question = input("請輸入您的問題: ")
            answer = recorder.process_input(question)
            print(f"\n回答: {answer}")

        elif choice == "2":
            # 使用當前腳本所在目錄的 input_question.txt
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