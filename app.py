"""
Module for processing email content and extracting insights using OpenAI's GPT-3.5.
"""

import os
import json
import logging
import sys
from dotenv import load_dotenv
from llama_index.program.openai import OpenAIPydanticProgram
from llama_index.core.prompts.base import ChatPromptTemplate
from llama_index.core.prompts.base import ChatMessage
from llama_index.llms.openai import OpenAI
from content_loader import load_email_data, load_outlook_message
from email_data import EmailData

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

email_msg_content = load_email_data("email.eml")
outlook_msg_content = load_outlook_message("email.msg")

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def process_content(content):
    """
    Process the given email content and extract insights using OpenAI's GPT-3.5.

    Args:
        content (str): The email content to be processed.

    Returns:
        EmailData: The extracted insights in the form of an EmailData object.
    """
    prompt = ChatPromptTemplate(
    message_templates=[
            ChatMessage(
                role="system",
                content=(
                    "You are an expert assitant for extracting insights from email in JSON format. \n"
                    "You extract data and returns it in JSON format, according to provided JSON schema, from given email message. \n"
                    "REMEMBER to return extracted data only from provided email message."
                ),
            ),
            ChatMessage(
                role="user",
                content=(
                    "Email Message: \n" "------\n" "{content}\n" "------"
                ),
            ),
        ]
    )

    llm = OpenAI(model="gpt-3.5-turbo-1106")

    program = OpenAIPydanticProgram.from_defaults(
        output_cls=EmailData,
        llm=llm,
        prompt=prompt,
        verbose=True,
    )

    output = program(content=content)
    # print("Output JSON From .eml File: ")
    # print(json.dumps(output.dict(), indent=2))
    return output

expected_output = {
    "etfs": [
        {
            "etf_ticker": "ARKK",
            "trade_date": "2022-01-01",
            "stocks": [
                {
                    "direction": "Buy",
                    "ticker": "AAPL",
                    "company_name": "Apple Inc",
                    "shares_traded": 100.0,
                    "percent_of_etf": 10.0,
                },
                {
                    "direction": "Sell",
                    "ticker": "TSLA",
                    "company_name": "Tesla Inc",
                    "shares_traded": 50.0,
                    "percent_of_etf": 5.0,
                },
            ],
        },
        {
            "etf_ticker": "FSPTX",
            "trade_date": "2022-01-01",
            "stocks": [
                {
                    "direction": "Buy",
                    "ticker": "MSFT",
                    "company_name": "Microsoft Corporation",
                    "shares_traded": 200.0,
                    "percent_of_etf": 20.0,
                },
                {
                    "direction": "Sell",
                    "ticker": "VZ",
                    "company_name": "Verizon Communications Inc",
                    "shares_traded": 150.0,
                    "percent_of_etf": 15.0,
                },
            ],
        },
    ],
    "trade_notification_date": "2022-01-01",
    "sender_email_id": "ark@ark-funds.com",
    "email_date_time": "1/12/2024"
}

def compare_content(actual, expected):
    """
    Compare the actual and expected content.

    Args:
        actual (dict): The actual content.
        expected (dict): The expected content.

    Returns:
        bool: True if the actual content matches the expected content, False otherwise.
    """
    json_actual_str = json.dumps(actual.dict(),indent=2)
    json_expect_str = json.dumps(expected_output, indent=2)

    actual_length = len(json_actual_str)
    expect_length = len(json_expect_str)
    print(f"Actual Length: {actual_length}")
    print(f"Expect Length: {expect_length}")

    return actual == expected


def test_eml_file():
    """
    Test the processing of an Email message file.
    Returns:
        bool: True if the actual content matches the expected content, False otherwise
    """
    actual = process_content(email_msg_content)
    return compare_content(actual, expected_output)


def test_msg_file():
    """
    Test the processing of an Outlook message file.
    Returns:
        bool: True if the actual content matches the expected content, False otherwise
    """
    actual = process_content(outlook_msg_content)
    return compare_content(actual, expected_output)


if __name__ == "__main__":
    print(f"test_eml_file: {test_eml_file()}")
    print(f"test_msg_file: {test_msg_file()}")
    print("All tests finished!")
