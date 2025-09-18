import json
from datetime import datetime
from collections import defaultdict
import pandas as pd

class KPIAnalyzer:
    def __init__(self):
        self.kpi_data = {
            "generation_timestamp": None,
            "total_rules": 0,
            "rules_by_category": {},
            "rules_with_sql": 0,
            "rules_without_sql": 0,
            "sql_coverage_percentage": 0,
            "category_distribution": {},
            "rule_complexity": {
                "simple_rules": 0,
                "complex_rules": 0,
                "cross_column_rules": 0
            },
            "column_coverage": {},
            "validation_types": {},
            "data_quality_dimensions": {
                "accuracy": 0,
                "completeness": 0,
                "uniqueness": 0,
                "consistency": 0,
                "timeliness": 0,
                "validity": 0
            }
        }

    def analyze_rules(self, rules, data_analyzer=None):
        """Analyze generated rules and calculate KPIs"""
        self.kpi_data["generation_timestamp"] = datetime.now().isoformat()
        
        # Reset counters
        self.kpi_data["total_rules"] = 0
        self.kpi_data["rules_with_sql"] = 0
        self.kpi_data["rules_without_sql"] = 0
        self.kpi_data["rules_by_category"] = {}
        self.kpi_data["category_distribution"] = {}
        self.kpi_data["rule_complexity"] = {
            "simple_rules": 0,
            "complex_rules": 0,
            "cross_column_rules": 0
        }
        self.kpi_data["column_coverage"] = {}
        self.kpi_data["validation_types"] = {}
        
        # Analyze each category
        for category, rule_list in rules.items():
            if not isinstance(rule_list, list):
                continue
                
            category_count = len(rule_list)
            self.kpi_data["rules_by_category"][category] = category_count
            self.kpi_data["total_rules"] += category_count
            
            # Update data quality dimensions
            if category in self.kpi_data["data_quality_dimensions"]:
                self.kpi_data["data_quality_dimensions"][category] = category_count
            
            # Analyze individual rules
            for rule in rule_list:
                if isinstance(rule, dict):
                    self._analyze_rule_details(rule, category)
                else:
                    # Simple string rule
                    self.kpi_data["rule_complexity"]["simple_rules"] += 1
        
        # Calculate percentages and distributions
        self._calculate_percentages()
        
        # Add data context if available
        if data_analyzer:
            self._add_data_context(data_analyzer)
        
        return self.kpi_data

    def _analyze_rule_details(self, rule, category):
        """Analyze individual rule details"""
        # Check SQL presence
        if rule.get('pseudo_sql') and rule.get('pseudo_sql') != 'No SQL code available':
            self.kpi_data["rules_with_sql"] += 1
        else:
            self.kpi_data["rules_without_sql"] += 1
        
        # Analyze rule complexity
        columns = rule.get('columns', rule.get('columns_involved', []))
        if isinstance(columns, str):
            columns = [columns]
        
        if category == 'cross_column':
            self.kpi_data["rule_complexity"]["cross_column_rules"] += 1
        elif len(columns) > 1:
            self.kpi_data["rule_complexity"]["complex_rules"] += 1
        else:
            self.kpi_data["rule_complexity"]["simple_rules"] += 1
        
        # Track column coverage
        for column in columns:
            if column not in self.kpi_data["column_coverage"]:
                self.kpi_data["column_coverage"][column] = 0
            self.kpi_data["column_coverage"][column] += 1
        
        # Track validation types
        validation_type = rule.get('type', rule.get('validation_type', 'unknown'))
        if validation_type not in self.kpi_data["validation_types"]:
            self.kpi_data["validation_types"][validation_type] = 0
        self.kpi_data["validation_types"][validation_type] += 1

    def _calculate_percentages(self):
        """Calculate percentage distributions"""
        total = self.kpi_data["total_rules"]
        if total == 0:
            return
        
        # SQL coverage percentage
        self.kpi_data["sql_coverage_percentage"] = round(
            (self.kpi_data["rules_with_sql"] / total) * 100, 2
        )
        
        # Category distribution percentages
        for category, count in self.kpi_data["rules_by_category"].items():
            self.kpi_data["category_distribution"][category] = round(
                (count / total) * 100, 2
            )

    def _add_data_context(self, data_analyzer):
        """Add data context information to KPIs"""
        stats = data_analyzer.get_basic_stats()
        self.kpi_data["data_context"] = {
            "total_rows": stats["row_count"],
            "total_columns": stats["column_count"],
            "columns_with_missing_values": sum(1 for v in stats["missing_values"].values() if v > 0),
            "rules_per_column": round(self.kpi_data["total_rules"] / stats["column_count"], 2) if stats["column_count"] > 0 else 0,
            "rules_per_row": round(self.kpi_data["total_rules"] / stats["row_count"], 4) if stats["row_count"] > 0 else 0
        }

    def get_summary_metrics(self):
        """Get key summary metrics for dashboard display"""
        return {
            "total_rules": self.kpi_data["total_rules"],
            "sql_coverage": f"{self.kpi_data['sql_coverage_percentage']}%",
            "top_category": max(self.kpi_data["rules_by_category"].items(), key=lambda x: x[1])[0] if self.kpi_data["rules_by_category"] else "N/A",
            "most_covered_column": max(self.kpi_data["column_coverage"].items(), key=lambda x: x[1])[0] if self.kpi_data["column_coverage"] else "N/A",
            "complexity_ratio": f"{self.kpi_data['rule_complexity']['complex_rules']}/{self.kpi_data['rule_complexity']['simple_rules']}"
        }

    def get_category_breakdown(self):
        """Get detailed category breakdown for charts"""
        categories = []
        counts = []
        percentages = []
        
        for category, count in self.kpi_data["rules_by_category"].items():
            categories.append(category.replace('_', ' ').title())
            counts.append(count)
            percentages.append(self.kpi_data["category_distribution"].get(category, 0))
        
        return {
            "categories": categories,
            "counts": counts,
            "percentages": percentages
        }

    def get_validation_type_breakdown(self):
        """Get validation type breakdown"""
        return {
            "types": list(self.kpi_data["validation_types"].keys()),
            "counts": list(self.kpi_data["validation_types"].values())
        }

    def get_column_coverage_analysis(self):
        """Get column coverage analysis"""
        if not self.kpi_data["column_coverage"]:
            return {"columns": [], "coverage": []}
        
        # Sort by coverage count
        sorted_coverage = sorted(
            self.kpi_data["column_coverage"].items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return {
            "columns": [item[0] for item in sorted_coverage],
            "coverage": [item[1] for item in sorted_coverage]
        }

    def export_kpi_report(self):
        """Export comprehensive KPI report as JSON"""
        report = {
            "report_metadata": {
                "generated_at": self.kpi_data["generation_timestamp"],
                "report_type": "Data Quality Rules KPI Analysis"
            },
            "executive_summary": self.get_summary_metrics(),
            "detailed_analysis": self.kpi_data,
            "category_breakdown": self.get_category_breakdown(),
            "validation_analysis": self.get_validation_type_breakdown(),
            "column_coverage": self.get_column_coverage_analysis()
        }
        
        return json.dumps(report, indent=2)

    def get_quality_score(self):
        """Calculate an overall quality score based on various factors"""
        if self.kpi_data["total_rules"] == 0:
            return 0
        
        # Factors that contribute to quality score
        sql_coverage_score = self.kpi_data["sql_coverage_percentage"] / 100
        category_diversity_score = min(len(self.kpi_data["rules_by_category"]) / 6, 1)  # Max 6 categories
        complexity_balance_score = 0.5  # Default neutral score
        
        # Calculate complexity balance (prefer mix of simple and complex)
        total_complexity = (self.kpi_data["rule_complexity"]["simple_rules"] + 
                          self.kpi_data["rule_complexity"]["complex_rules"])
        if total_complexity > 0:
            simple_ratio = self.kpi_data["rule_complexity"]["simple_rules"] / total_complexity
            complexity_balance_score = 1 - abs(0.5 - simple_ratio) * 2  # Closer to 0.5 is better
        
        # Weighted quality score
        quality_score = (
            sql_coverage_score * 0.4 +
            category_diversity_score * 0.3 +
            complexity_balance_score * 0.3
        )
        
        return round(quality_score * 100, 1)
