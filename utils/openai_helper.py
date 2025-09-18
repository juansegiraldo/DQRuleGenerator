import os
from openai import OpenAI
import json

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
class OpenAIHelper:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"

    def analyze_data_sample(self, data_sample, column_info, user_context=""):
        context_prompt = f"\nAdditional context about the data: {user_context}" if user_context else ""

        prompt = f"""You are a data quality expert. Your task is to analyze the provided data and generate data quality rules with SQL code.

        STEP 1: Analyze this data sample and column information:
        {data_sample}
        {column_info}{context_prompt}

        STEP 2: For each rule you generate, you MUST include these 4 fields:
        - "rule": A clear description of the validation rule
        - "columns": Array of column names this rule applies to
        - "type": The validation type (range, pattern, null_check, etc.)
        - "pseudo_sql": A complete SQL query that can be used to find violations

        STEP 3: Generate rules for these categories:
        - accuracy: Value ranges, formats, business logic
        - completeness: Null checks, required fields
        - uniqueness: Unique constraints, composite keys
        - consistency: Cross-field validation, format standards
        - timeliness: Date formats, temporal constraints
        - validity: Data types, allowed values

        STEP 4: For the pseudo_sql field, write complete SELECT statements that identify data quality violations.
        Use "table_name" as the table name placeholder.
        Examples of good SQL:
        - Range validation: "SELECT * FROM table_name WHERE age < 0 OR age > 120"
        - Pattern validation: "SELECT * FROM table_name WHERE email NOT REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{{2,}}$'"
        - Null check: "SELECT * FROM table_name WHERE name IS NULL"
        - Uniqueness: "SELECT email, COUNT(*) FROM table_name GROUP BY email HAVING COUNT(*) > 1"

        CRITICAL REQUIREMENT: Every single rule object MUST have a "pseudo_sql" field with a complete SQL query.
        If you omit the pseudo_sql field, the response will be considered invalid.

        Respond with valid JSON only, following this exact structure:
        {{
            "rules": {{
                "accuracy": [
                    {{
                        "rule": "Age must be between 0 and 65 based on the valid range from the data.",
                        "columns": ["age"],
                        "type": "range",
                        "pseudo_sql": "SELECT * FROM table_name WHERE age < 0 OR age > 65"
                    }}
                ],
                "completeness": [
                    {{
                        "rule": "Name field must not be null.",
                        "columns": ["name"],
                        "type": "null_check",
                        "pseudo_sql": "SELECT * FROM table_name WHERE name IS NULL"
                    }}
                ],
                "uniqueness": [
                    {{
                        "rule": "Email must be unique across all records.",
                        "columns": ["email"],
                        "type": "unique",
                        "pseudo_sql": "SELECT email, COUNT(*) as count FROM table_name GROUP BY email HAVING COUNT(*) > 1"
                    }}
                ],
                "consistency": [],
                "timeliness": [],
                "validity": []
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

        prompt = f"""You are a data quality expert. Generate cross-column validation rules with SQL code.

        STEP 1: Analyze these columns and their relationships:
        Columns: {column_names}
        Correlations: {sample_correlations}{context_prompt}

        STEP 2: For each cross-column rule, you MUST include these 4 fields:
        - "rule": A clear description of the cross-column validation
        - "columns_involved": Array of column names involved in the validation
        - "validation_type": The type of validation (logical, business, temporal, etc.)
        - "pseudo_sql": A complete SQL query that finds violations

        STEP 3: Focus on these relationship types:
        - Logical dependencies (if A then B)
        - Mathematical relationships (A > B, A + B = C)
        - Business rules (age requirements, salary constraints)
        - Temporal relationships (dates, time sequences)
        - Categorical hierarchies (department relationships)

        STEP 4: For the pseudo_sql field, write complete SELECT statements that identify cross-column violations.
        Use "table_name" as the table name placeholder.
        Examples of good cross-column SQL:
        - Logical: "SELECT * FROM table_name WHERE active = true AND (name IS NULL OR name = '')"
        - Business: "SELECT * FROM table_name WHERE active = true AND age < 18"
        - Mathematical: "SELECT * FROM table_name WHERE salary < 0"

        CRITICAL REQUIREMENT: Every single rule object MUST have a "pseudo_sql" field with a complete SQL query.
        If you omit the pseudo_sql field, the response will be considered invalid.

        Respond with valid JSON only, following this exact structure:
        {{
            "cross_column_rules": [
                {{
                    "rule": "The 'name' field must not be empty if the 'active' field is set to true.",
                    "columns_involved": ["name", "active"],
                    "validation_type": "logical",
                    "pseudo_sql": "SELECT * FROM table_name WHERE active = true AND (name IS NULL OR name = '')"
                }},
                {{
                    "rule": "The 'age' of the employee must be at least 18 years to be considered active.",
                    "columns_involved": ["age", "active"],
                    "validation_type": "business",
                    "pseudo_sql": "SELECT * FROM table_name WHERE active = true AND age < 18"
                }}
            ]
        }}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)