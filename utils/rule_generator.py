import json
from datetime import datetime

class RuleGenerator:
    def __init__(self, data_analyzer, openai_helper):
        self.data_analyzer = data_analyzer
        self.openai_helper = openai_helper

    def generate_rules(self):
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
        
        rules = self.openai_helper.analyze_data_sample(sample_data, column_info)
        
        # Get cross-column rules
        cross_column_rules = self.openai_helper.suggest_cross_column_rules(
            list(column_types.keys()),
            correlations
        )
        
        # Combine all rules
        all_rules = rules["rules"]
        all_rules["cross_column"] = cross_column_rules["cross_column_rules"]
        
        return all_rules

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
            formatted_rules[categories[category]] = rules_list
            
        return formatted_rules

    def export_rules_to_json(self, rules):
        export_data = {
            "generated_at": datetime.now().isoformat(),
            "rules": rules
        }
        return json.dumps(export_data, indent=2)
