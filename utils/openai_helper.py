import os
from openai import OpenAI
import json

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
class OpenAIHelper:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-4o"

    def analyze_data_sample(self, data_sample, column_info, user_context=""):
        context_prompt = f"\nAdditional context about the data: {user_context}" if user_context else ""

        prompt = f"""Analyze this data sample and generate specific, actionable data quality rules.
        Focus on these key aspects, providing detailed rules for each category:

        1. Accuracy: 
         - Define acceptable value ranges based on field type and domain
         - Identify format patterns for text fields
         - Specify business logic constraints

        2. Completeness:
         - List critical fields that must not be null
         - Define conditional completeness rules
         - Specify minimum data requirements

        3. Uniqueness:
         - Identify fields that must be unique
         - Define composite uniqueness rules
         - Specify business-level uniqueness requirements

        4. Consistency:
         - Define cross-field validation rules
         - Specify format standardization rules
         - List business logic consistency checks

        5. Timeliness:
         - Define date/time format requirements
         - Specify acceptable time ranges
         - List temporal validation rules

        6. Validity:
         - Define format patterns for each field type
         - Specify allowed values and ranges
         - List domain-specific validation rules

        Data sample and column info:
        {data_sample}
        {column_info}{context_prompt}

        For each rule category, provide clear, specific, and implementable rules.
        Respond with JSON in this format:
        {{
            "rules": {{
                "accuracy": [list of specific rules],
                "completeness": [list of specific rules],
                "uniqueness": [list of specific rules],
                "consistency": [list of specific rules],
                "timeliness": [list of specific rules],
                "validity": [list of specific rules]
            }}
        }}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def suggest_cross_column_rules(self, column_names, sample_correlations, user_context=""):
        context_prompt = f"\nAdditional context about the data: {user_context}" if user_context else ""

        prompt = f"""Generate specific cross-column validation rules based on these columns and their correlations.
        Consider business logic, statistical relationships, and domain constraints.

        Columns: {column_names}
        Correlations: {sample_correlations}{context_prompt}

        Focus on:
        1. Logical dependencies between columns
        2. Mathematical relationships
        3. Business rules and constraints
        4. Temporal relationships
        5. Categorical hierarchies

        Respond with JSON in this format:
        {{
            "cross_column_rules": [
                {{
                    "rule": "detailed rule description",
                    "columns_involved": ["col1", "col2"],
                    "validation_type": "logical|mathematical|business|temporal|categorical"
                }}
            ]
        }}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)