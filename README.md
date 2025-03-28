# QARecorder Project (QARecorder 專案)
## Overview (概述)
This project is designed to provide a simple command-line based question-answering system that leverages the OpenAI API to generate answers. Users have two input methods: manually entering questions or reading questions from a text file. The system processes the questions, retrieves answers via the API, and then saves the results into an Excel file along with generating an HTML report.

這個專案旨在提供一個簡單的命令列問題回答系統，利用 OpenAI API 產生答案。使用者可以透過兩種方式輸入問題：手動輸入或從文本文件讀取。系統處理問題後，將透過 API 取得答案，並保存到 Excel 文件，同時生成 HTML 報告。

## Features (功能)
Manual Question Input (手動輸入問題):
Users can directly enter a question via the command line.
使用者可直接在命令列輸入問題。

File-based Input (文件輸入):
Questions can be read from a text file with error handling if the file is missing.
系統能夠從文本文件讀取問題，並針對文件不存在的狀況進行錯誤處理。

API Integration (API 整合):
The system calls the OpenAI API to process and answer the questions.
系統透過呼叫 OpenAI API 來處理與回答問題。

Report Generation (報告生成):
Answers are saved in an Excel file and an HTML report is generated for easy review.
回答結果將保存於 Excel 文件中，並生成 HTML 報告以便檢視。

Main Menu Navigation (主選單介面):
A user-friendly main menu allows selection between input methods and program termination.
友善的主選單介面讓使用者可以在輸入方式與程式結束之間切換。

## Flow Diagram (流程圖)
Below is the Mermaid diagram that illustrates the system workflow:
![image](https://github.com/cba542/api_agent/blob/main/Test_flow.png)

### mermaid
```
graph TD
    A[開始  Start ] --> B[初始化QARecorder  Initialize QARecorder ]
    B --> C{顯示主選單<br/> Display Main Menu }
    C --> |選擇1<br/> Option 1 | D[手動輸入問題<br/> Manually Enter Question ]
    C --> |選擇2<br/> Option 2 | E[讀取文本文件<br/> Read Text File ]
    C --> |選擇3<br/> Option 3 | F[結束程序<br/> End Program ]
    
    D --> G[調用process_input方法<br/> Call process_input method ]
    G --> H[調用ask_question方法<br/> Call ask_question method ]
    H --> I[調用OpenAI API<br/> Call OpenAI API ]
    I --> J[返回回答<br/> Return Answer ]
    J --> K[調用save_to_excel方法<br/> Call save_to_excel method ]
    K --> L[保存到Excel文件<br/> Save to Excel File ]
    K --> M[生成HTML報告<br/> Generate HTML Report ]
    L --> C
    M --> C
    
    E --> N[檢查文件是否存在?<br/> Check if file exists? ]
    N --> |存在<br/> Exists | O[逐行讀取問題<br/> Read questions line by line ]
    N --> |不存在<br/> Doesn't exist | P[顯示錯誤訊息<br/> Display error message ]
    P --> C
    O --> G
    
    F --> Q[結束<br/> Terminate ]
    
    style A fill:#9f9,stroke:#333
    style Q fill:#f99,stroke:#333
    style N fill:#f96,stroke:#333
    style P fill:#fcc,stroke:#333
```
## Installation (安裝)
### Prerequisites (環境需求)
- Python 3.x
- pip (Python 套件管理器)

## Setup (設置):
1. 複製專案到本地：
```bash
git clone https://github.com/yourusername/qa_recorder.git
cd qa_recorder
```

2. 複製 config.py 為 config_local.py
```bash
cp config.py config_local.py
```

3. 在 config_local.py 中填入你的實際配置：
```python
API_KEY = "your-api-key-here"  # 例如: "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
API_BASE = "your-api-base-here"  # 例如: "https://api.siliconflow.cn/v1"
MODEL_NAME = "your-model-name-here"  # 例如: "deepseek-ai/DeepSeek-V3"
```

4. 安裝必要的 Python 套件：
```bash
pip install openai pandas openpyxl
```

## Usage (使用方式):
執行主程式：
```bash
python qa_recorder.py
```

選擇操作模式：
1. 手動輸入問題：直接輸入單一問題
2. 讀取文本文件：從 input_questions.txt 批量讀取問題
3. 結束程序

### 批量處理模式
系統使用文本文件格式 (input_questions.txt) 來批量處理問題：

- 使用 "---" 作為問題分隔符
- 每個問題可以包含多行內容
- 支持標題和詳細描述

範例格式：
```text
# 問題一：Python 文件處理
請詳細說明如何使用 Python 處理文件，包含以下幾點：
1. 文件的讀寫操作
2. 常見的文件處理方法
3. 錯誤處理機制
---
# 問題二：機器學習概述
什麼是機器學習？
這個技術有什麼應用？
為什麼現在這麼流行？
---
# 問題三：API 介紹
請解釋 API 是什麼：
1. API 的定義
2. 常見用途
3. 優缺點
```

注意：
- 每個問題之間使用 "---" 分隔
- 可以使用 # 開頭的行作為問題標題（可選）
- 問題內容可以包含多行文字
- 支持項目符號和編號列表

## Project Structure (專案結構):
```
qa_recorder/
├── qa_recorder.py     # 主程式
├── config.py          # 配置模板
├── config_local.py    # 本地配置（需自行建立）
├── .gitignore         # Git 忽略檔案設定
├── README.md          # 專案說明文件
├── input_questions.txt # 批量問題輸入檔案
└── output/           # 輸出目錄
    ├── qa_records.xlsx # Excel 格式記錄
    └── qa_records.html # HTML 格式報告
```

## Notes (注意事項)
- 請確保 config_local.py 已加入 .gitignore 以保護 API 金鑰
- 所有文字檔案請使用 UTF-8 編碼
- HTML 報告會在每次新增問答時自動更新

## License (授權)
MIT License
