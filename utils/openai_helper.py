import os
from openai import OpenAI
import json

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
class OpenAIHelper:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-4o"

    def analyze_data_sample(self, data_sample, column_info):
        prompt = f"""Analyze this data sample and generate data quality rules. Focus on:
        1. Accuracy: Identify plausible value ranges and patterns
        2. Completeness: Required vs optional fields
        3. Uniqueness: Fields that should be unique
        4. Consistency: Cross-field validations
        5. Timeliness: Date-related validations
        6. Validity: Format and type validations

        Data sample and column info:
        {data_sample}
        {column_info}

        Respond with JSON in this format:
        {{
            "rules": {{
                "accuracy": [list of rules],
                "completeness": [list of rules],
                "uniqueness": [list of rules],
                "consistency": [list of rules],
                "timeliness": [list of rules],
                "validity": [list of rules]
            }}
        }}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)

    def suggest_cross_column_rules(self, column_names, sample_correlations):
        prompt = f"""Generate cross-column validation rules based on these columns and their correlations:
        Columns: {column_names}
        Correlations: {sample_correlations}
        
        Respond with JSON in this format:
        {{
            "cross_column_rules": [
                {{
                    "rule": "rule description",
                    "columns_involved": ["col1", "col2"],
                    "validation_type": "type"
                }}
            ]
        }}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
