import json
from datetime import datetime

class RuleGenerator:
    def __init__(self, data_analyzer, openai_helper):
        self.data_analyzer = data_analyzer
        self.openai_helper = openai_helper

    def generate_rules(self, user_context=""):
        # Get data insights
        column_types = self.data_analyzer.infer_column_types()
        column_profiles = self.data_analyzer.generate_column_profiles()
        correlations = self.data_analyzer.get_column_correlations()

        # Get AI-generated rules
        sample_data = self.data_analyzer.get_data_sample()
        column_info = {
            "types": column_types,
            "profiles": column_profiles
        }

        rules = self.openai_helper.analyze_data_sample(
            sample_data, 
            column_info,
            user_context
        )

        # Get cross-column rules
        cross_column_rules = self.openai_helper.suggest_cross_column_rules(
            list(column_types.keys()),
            correlations,
            user_context
        )

        # Combine all rules with error handling and SQL validation
        try:
            all_rules = rules.get("rules", {})
            cross_column_rules_list = cross_column_rules.get("cross_column_rules", [])
            all_rules["cross_column"] = cross_column_rules_list
            
            # Validate that SQL code is present in rules and add fallback if missing
            self._validate_and_fix_sql_presence(all_rules)
            
        except Exception as e:
            # Fallback if there's an issue with rule structure
            all_rules = {
                "accuracy": ["Error generating rules - please try again"],
                "completeness": [],
                "uniqueness": [],
                "consistency": [],
                "timeliness": [],
                "validity": [],
                "cross_column": []
            }

        return all_rules

    def _validate_and_fix_sql_presence(self, rules):
        """Validate that SQL code is present in the generated rules and add fallback SQL if missing."""
        missing_sql_count = 0
        total_rules = 0
        fixed_count = 0
        
        for category, rule_list in rules.items():
            if isinstance(rule_list, list):
                for rule in rule_list:
                    if isinstance(rule, dict):
                        total_rules += 1
                        if 'pseudo_sql' not in rule or not rule.get('pseudo_sql'):
                            missing_sql_count += 1
                            
                            # Generate fallback SQL code
                            fallback_sql = self._generate_fallback_sql(rule, category)
                            if fallback_sql:
                                rule['pseudo_sql'] = fallback_sql
                                fixed_count += 1
        
        # SQL validation completed silently

    def _generate_fallback_sql(self, rule, category):
        """Generate fallback SQL code for a rule that's missing it."""
        rule_text = rule.get('rule', '').lower()
        columns = rule.get('columns', rule.get('columns_involved', []))
        rule_type = rule.get('type', rule.get('validation_type', ''))
        
        if not columns:
            return None
            
        # Convert single column to list if needed
        if isinstance(columns, str):
            columns = [columns]
        
        # Generate SQL based on rule type and content
        if 'null' in rule_text or rule_type == 'null_check':
            if len(columns) == 1:
                return f"SELECT * FROM table_name WHERE {columns[0]} IS NULL"
            else:
                conditions = " OR ".join([f"{col} IS NULL" for col in columns])
                return f"SELECT * FROM table_name WHERE {conditions}"
        
        elif 'unique' in rule_text or rule_type in ['unique', 'composite_unique']:
            if len(columns) == 1:
                return f"SELECT {columns[0]}, COUNT(*) as count FROM table_name GROUP BY {columns[0]} HAVING COUNT(*) > 1"
            else:
                group_cols = ", ".join(columns)
                return f"SELECT {group_cols}, COUNT(*) as count FROM table_name GROUP BY {group_cols} HAVING COUNT(*) > 1"
        
        elif 'range' in rule_type or 'between' in rule_text:
            if len(columns) == 1:
                col = columns[0]
                if 'age' in col.lower():
                    return f"SELECT * FROM table_name WHERE {col} < 0 OR {col} > 120"
                elif 'salary' in col.lower():
                    return f"SELECT * FROM table_name WHERE {col} < 0"
                else:
                    return f"SELECT * FROM table_name WHERE {col} IS NULL"
            else:
                return f"SELECT * FROM table_name WHERE {' OR '.join([f'{col} IS NULL' for col in columns])}"
        
        elif 'pattern' in rule_type or 'format' in rule_type:
            if len(columns) == 1:
                col = columns[0]
                if 'email' in col.lower():
                    return f"SELECT * FROM table_name WHERE {col} NOT REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{{2,}}$'"
                elif 'date' in col.lower():
                    return f"SELECT * FROM table_name WHERE {col} NOT REGEXP '^[0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}$'"
                else:
                    return f"SELECT * FROM table_name WHERE {col} IS NULL"
            else:
                return f"SELECT * FROM table_name WHERE {' OR '.join([f'{col} IS NULL' for col in columns])}"
        
        elif 'active' in rule_text and 'name' in rule_text:
            return "SELECT * FROM table_name WHERE active = true AND (name IS NULL OR name = '')"
        
        elif 'active' in rule_text and 'age' in rule_text:
            return "SELECT * FROM table_name WHERE active = true AND age < 18"
        
        elif 'department' in rule_text:
            return "SELECT * FROM table_name WHERE department NOT IN ('Engineering', 'Marketing', 'Sales', 'Management')"
        
        else:
            # Generic fallback
            if len(columns) == 1:
                return f"SELECT * FROM table_name WHERE {columns[0]} IS NULL"
            else:
                conditions = " OR ".join([f"{col} IS NULL" for col in columns])
                return f"SELECT * FROM table_name WHERE {conditions}"

    def format_rules_for_display(self, rules):
        formatted_rules = {}
        categories = {
            "accuracy": "Accuracy Rules",
            "completeness": "Completeness Rules",
            "uniqueness": "Uniqueness Rules",
            "consistency": "Consistency Rules",
            "timeliness": "Timeliness Rules",
            "validity": "Validity Rules",
            "cross_column": "Cross-Column Rules"
        }

        for category, rules_list in rules.items():
            if category in categories:
                # Ensure rules_list is a list and handle None/empty cases
                if rules_list is None:
                    rules_list = []
                elif not isinstance(rules_list, list):
                    rules_list = [rules_list] if rules_list else []
                
                formatted_rules[categories[category]] = rules_list

        return formatted_rules

    def export_rules_to_json(self, rules):
        export_data = {
            "generated_at": datetime.now().isoformat(),
            "rules": rules
        }
        return json.dumps(export_data, indent=2)