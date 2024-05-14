import openai

def call_openai_api(api_key, ticker, data, item_type):
    client = openai.OpenAI(api_key=api_key)

    if item_type == "item_7A":
        system_message = "You are an assistant specialized in analyzing the Quantitative and Qualitative Disclosures about Market Risk from Edgar 10-K reports. Your role is to extract and organize information, including tabular data."
        task_description = """
        Task: Analyze the Item 7A data provided in the Edgar 10-K report. Focus on:
        - Extracting and organizing quantitative data about market risks such as interest rate, foreign exchange, and commodity price risks.
        - Summarizing qualitative disclosures about how these risks are managed by the company.
        - Presenting this information in structured tables to highlight key data points and trends.
        - Discussing any significant changes in risk exposure compared to the previous period.
        
        Ensure the analysis is detailed and clear, using bullet points for qualitative insights and structured tables for quantitative data. This helps in understanding the impact of market risks on the company's financial health.
        """
    elif item_type == "item_8":
        system_message = "You are an assistant specialized in financial reporting and analysis. Your primary task is to organize financial data into table formats and provide insights based on the financial statements and supplementary data from Edgar 10-K reports."
        task_description = """
        Task: Analyze the financial data provided in Edgar 10-K Item 8. Organize the key financial metrics such as total assets, total liabilities, equity, revenue, and cash flows into a table format. Include columns for the current period, the previous period, and the percentage change to highlight significant trends and changes.
        Your output should focus on:
        - Creating structured tables for the financial metrics.
        - Summarizing the financial health and performance.
        - Highlighting any significant financial trends or changes from the previous reporting period.
        Provide your analysis in a detailed and accessible manner using bullet points and structured formats where applicable.
        """
    else:
        system_message = "You are a financial analysis assistant."
        task_description = "Provide a detailed summary and analysis based on the provided financial data."
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Here is the data for ticker {ticker} 10-k report {item_type}: {data}. {task_description}"}
        ],
        temperature=0
    )
    return completion.choices[0].message.content