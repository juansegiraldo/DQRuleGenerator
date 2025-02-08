import streamlit as st
import pandas as pd
from utils.data_analyzer import DataAnalyzer
from utils.openai_helper import OpenAIHelper
from utils.rule_generator import RuleGenerator
import json

# Page configuration
st.set_page_config(
    page_title="Data Quality Rule Generator",
    page_icon="📊",
    layout="wide"
)

# Load custom CSS
with open('.streamlit/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.title("Data Quality Rule Generator")
    st.markdown("""
    Upload your CSV file to generate comprehensive data quality rules using AI.
    The analysis will cover accuracy, completeness, uniqueness, consistency, timeliness, and validity.
    """)

    # File upload
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type="csv",
        help="Upload your CSV file to analyze"
    )

    if uploaded_file is not None:
        try:
            # Load and display data preview
            df = pd.read_csv(uploaded_file)

            with st.expander("Data Preview", expanded=True):
                st.dataframe(df.head(), use_container_width=True)

            # Data context input
            st.subheader("Data Context")
            user_context = st.text_area(
                "Provide additional context about your data (optional)",
                help="Describe the purpose, domain, and any specific requirements for your data. "
                "This will help generate more relevant and accurate rules.",
                placeholder="Example: This dataset contains customer transaction records for an e-commerce platform. "
                "Transaction dates should be within the last year, and all monetary values should be positive."
            )

            # Initialize analyzers
            data_analyzer = DataAnalyzer(df)
            openai_helper = OpenAIHelper()
            rule_generator = RuleGenerator(data_analyzer, openai_helper)

            # Display basic stats
            col1, col2, col3 = st.columns(3)
            stats = data_analyzer.get_basic_stats()

            with col1:
                st.metric("Total Rows", stats["row_count"])
            with col2:
                st.metric("Total Columns", stats["column_count"])
            with col3:
                st.metric("Columns with Missing Values", 
                         sum(1 for v in stats["missing_values"].values() if v > 0))

            # Generate rules button
            if st.button("Generate Data Quality Rules"):
                with st.spinner("Analyzing data and generating rules..."):
                    # Pass user context to rule generation
                    rules = rule_generator.generate_rules(user_context)
                    formatted_rules = rule_generator.format_rules_for_display(rules)

                # Display rules by category
                st.header("Generated Data Quality Rules")

                for category, rule_list in formatted_rules.items():
                    with st.expander(category, expanded=True):
                        for rule in rule_list:
                            if isinstance(rule, dict):
                                # Handle cross-column rules
                                st.markdown(f"""
                                **Rule:** {rule['rule']}  
                                **Columns:** {', '.join(rule['columns_involved'])}  
                                **Type:** {rule['validation_type']}
                                """)
                            else:
                                # Handle simple rules
                                st.markdown(f"• {rule}")

                # Export rules
                rules_json = rule_generator.export_rules_to_json(rules)
                st.download_button(
                    label="Download Rules as JSON",
                    data=rules_json,
                    file_name="data_quality_rules.json",
                    mime="application/json"
                )

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    main()