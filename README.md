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
### mermaid
```
graph TD
    A[開始 (Start)] --> B[初始化QARecorder (Initialize QARecorder)]
    B --> C{顯示主選單<br/>(Display Main Menu)}
    C --> |選擇1<br/>(Option 1)| D[手動輸入問題<br/>(Manually Enter Question)]
    C --> |選擇2<br/>(Option 2)| E[讀取文本文件<br/>(Read Text File)]
    C --> |選擇3<br/>(Option 3)| F[結束程序<br/>(End Program)]
    
    D --> G[調用process_input方法<br/>(Call process_input method)]
    G --> H[調用ask_question方法<br/>(Call ask_question method)]
    H --> I[調用OpenAI API<br/>(Call OpenAI API)]
    I --> J[返回回答<br/>(Return Answer)]
    J --> K[調用save_to_excel方法<br/>(Call save_to_excel method)]
    K --> L[保存到Excel文件<br/>(Save to Excel File)]
    K --> M[生成HTML報告<br/>(Generate HTML Report)]
    L --> C
    M --> C
    
    E --> N[檢查文件是否存在?<br/>(Check if file exists?)]
    N --> |存在<br/>(Exists)| O[逐行讀取問題<br/>(Read questions line by line)]
    N --> |不存在<br/>(Doesn't exist)| P[顯示錯誤訊息<br/>(Display error message)]
    P --> C
    O --> G
    
    F --> Q[結束<br/>(Terminate)]
    
    style A fill:#9f9,stroke:#333
    style Q fill:#f99,stroke:#333
    style N fill:#f96,stroke:#333
    style P fill:#fcc,stroke:#333
```
## Installation (安裝)

## Setup (設置):

## Usage (使用方式):
Run the main script to start the application:
```
python main.py
```

Upon running, the main menu will be displayed:

* Option 1 (手動輸入問題): Manually enter a question.
* Option 2 (讀取文本文件): Load questions from a text file.
* Option 3 (結束程序): Exit the application.

## Project Structure (專案結構):
* main.py: Main script to launch the application.
* qa_recorder.py: Contains the QARecorder class and associated methods.
* utils.py: Utility functions for file handling, error checking, etc.
* reports/: Directory for saving generated Excel and HTML reports.
* requirements.txt: List of Python packages required for the project.
