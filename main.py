import streamlit as st
import pandas as pd
from utils.data_analyzer import DataAnalyzer
from utils.openai_helper import OpenAIHelper
from utils.rule_generator import RuleGenerator
from utils.kpi_analyzer import KPIAnalyzer
import json
from datetime import datetime
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Data Quality Rule Generator",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for white backgrounds and typography
st.markdown("""
<style>
/* Import modern sans-serif fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap');

/* Global typography - apply to all elements */
* {
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
}

/* Main content typography */
.main .block-container {
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
}

/* Headers */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
    font-weight: 600 !important;
}

/* File uploader styling - comprehensive coverage */
.stFileUploader {
    background-color: white !important;
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
}

.stFileUploader > div {
    background-color: white !important;
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
}

.stFileUploader > div > div {
    background-color: white !important;
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
}

.stFileUploader > div > div > div {
    background-color: white !important;
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
}

.stFileUploader > div > div > div > div {
    background-color: white !important;
    border: 2px dashed #ccc !important;
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
}

.stFileUploader > div > div > div > div > div {
    background-color: white !important;
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
}

.stFileUploader > div > div > div > div > div > div {
    background-color: white !important;
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
}

/* Browse files button */
.stFileUploader > div > div > div > div > button {
    background-color: white !important;
    color: black !important;
    border: 1px solid #ccc !important;
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
    font-weight: 500 !important;
}

/* Uploaded file display */
.stFileUploader > div > div > div > div > div > div {
    background-color: white !important;
    border: 1px solid #ccc !important;
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
}

/* File uploader help text */
.stFileUploader > div > div > div > div > small {
    background-color: white !important;
    color: #666 !important;
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
}

/* Text area styling */
.stTextArea > div > div > textarea {
    background-color: white !important;
    border: 1px solid #ccc !important;
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
    font-size: 14px !important;
    line-height: 1.5 !important;
}

/* Additional file uploader elements */
.stFileUploader label {
    background-color: white !important;
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
    font-weight: 500 !important;
}

.stFileUploader .uploadedFile {
    background-color: white !important;
    border: 1px solid #ccc !important;
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
}

/* Ensure all nested elements have white background and proper typography */
.stFileUploader * {
    background-color: white !important;
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
}

/* Override any dark themes */
.stFileUploader .uploadedFileContent {
    background-color: white !important;
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
}

/* Streamlit specific elements */
.stApp {
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
}

.stMarkdown {
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
}

.stButton > button {
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
    font-weight: 500 !important;
}

.stSelectbox > div > div {
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
}

.stDataFrame {
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

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
            kpi_analyzer = KPIAnalyzer()

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
                    
                    # Analyze KPIs
                    kpi_data = kpi_analyzer.analyze_rules(rules, data_analyzer)

                # Display KPI Dashboard
                st.header("Rules Generated")
                
                # Summary metrics
                summary_metrics = kpi_analyzer.get_summary_metrics()
                quality_score = kpi_analyzer.get_quality_score()
                
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("Total Rules", summary_metrics["total_rules"])
                with col2:
                    st.metric("SQL Coverage", summary_metrics["sql_coverage"])
                with col3:
                    st.metric("Quality Score", f"{quality_score}/100")
                with col4:
                    st.metric("Top Category", summary_metrics["top_category"])
                with col5:
                    st.metric("Complexity Ratio", summary_metrics["complexity_ratio"])
                
                # KPI Charts
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Rules by Category")
                    category_breakdown = kpi_analyzer.get_category_breakdown()
                    if category_breakdown["categories"]:
                        fig = px.pie(
                            values=category_breakdown["counts"],
                            names=category_breakdown["categories"],
                            title="Distribution of Rules by Category"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No category data available")
                
                with col2:
                    st.subheader("Column Coverage")
                    column_coverage = kpi_analyzer.get_column_coverage_analysis()
                    if column_coverage["columns"]:
                        # Show top 10 most covered columns
                        top_columns = column_coverage["columns"][:10]
                        top_coverage = column_coverage["coverage"][:10]
                        
                        fig = px.bar(
                            x=top_coverage,
                            y=top_columns,
                            orientation='h',
                            title="Top 10 Most Covered Columns",
                            labels={'x': 'Number of Rules', 'y': 'Columns'}
                        )
                        fig.update_layout(yaxis={'categoryorder':'total ascending'})
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No column coverage data available")
                
                # Detailed KPI Analysis
                with st.expander("📈 Detailed KPI Analysis", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Rule Complexity Distribution")
                        complexity = kpi_data["rule_complexity"]
                        complexity_data = {
                            "Type": ["Simple Rules", "Complex Rules", "Cross-Column Rules"],
                            "Count": [complexity["simple_rules"], complexity["complex_rules"], complexity["cross_column_rules"]]
                        }
                        complexity_df = pd.DataFrame(complexity_data)
                        st.dataframe(complexity_df, use_container_width=True)
                        
                        # Validation types
                        st.subheader("Validation Types")
                        validation_breakdown = kpi_analyzer.get_validation_type_breakdown()
                        if validation_breakdown["types"]:
                            validation_df = pd.DataFrame({
                                "Validation Type": validation_breakdown["types"],
                                "Count": validation_breakdown["counts"]
                            })
                            st.dataframe(validation_df, use_container_width=True)
                    
                    with col2:
                        st.subheader("Data Quality Dimensions")
                        dimensions = kpi_data["data_quality_dimensions"]
                        dimensions_data = {
                            "Dimension": list(dimensions.keys()),
                            "Rule Count": list(dimensions.values())
                        }
                        dimensions_df = pd.DataFrame(dimensions_data)
                        st.dataframe(dimensions_df, use_container_width=True)
                        
                        # Data context
                        if "data_context" in kpi_data:
                            st.subheader("Data Context")
                            context = kpi_data["data_context"]
                            context_data = {
                                "Metric": ["Total Rows", "Total Columns", "Rules per Column", "Rules per Row"],
                                "Value": [context["total_rows"], context["total_columns"], 
                                        context["rules_per_column"], context["rules_per_row"]]
                            }
                            context_df = pd.DataFrame(context_data)
                            st.dataframe(context_df, use_container_width=True)
                
                st.divider()
                
                # Display rules by category
                st.header("Generated Data Quality Rules")
                

                for category, rule_list in formatted_rules.items():
                    with st.expander(category, expanded=True):
                        for rule in rule_list:
                            if isinstance(rule, dict):
                                # Handle detailed rule objects with error checking
                                try:
                                    rule_text = rule.get('rule', 'No rule description available')
                                    # Check for both 'columns' (new format) and 'columns_involved' (cross-column format)
                                    columns = rule.get('columns', rule.get('columns_involved', ['Unknown columns']))
                                    # Check for both 'type' (new format) and 'validation_type' (cross-column format)
                                    validation_type = rule.get('type', rule.get('validation_type', 'Unknown type'))
                                    # Get pseudo SQL code
                                    pseudo_sql = rule.get('pseudo_sql', 'No SQL code available')
                                    
                                    # Use native Streamlit components for clean layout
                                    st.subheader("Rule Description", divider=True)
                                    st.write(rule_text)

                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.caption("**Affected Columns**")
                                        st.write(', '.join(columns) if isinstance(columns, list) else str(columns))

                                    with col2:
                                        st.caption("**Validation Type**")
                                        st.write(validation_type)

                                    # Display pseudo SQL code in a code block
                                    if pseudo_sql and pseudo_sql != 'No SQL code available':
                                        st.caption("**Implementation**")
                                        st.code(pseudo_sql, language='sql')

                                    st.divider()
                                    
                                except Exception as e:
                                    # Fallback for malformed rule objects
                                    st.markdown(f"• {str(rule)}")
                            else:
                                # Handle simple rules
                                st.markdown(f"• {rule}")

                # Export rules and KPIs
                st.header("📥 Export Options")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    rules_json = rule_generator.export_rules_to_json(rules)
                    st.download_button(
                        label="📋 Download Rules as JSON",
                        data=rules_json,
                        file_name="data_quality_rules.json",
                        mime="application/json"
                    )
                
                with col2:
                    # Extract and export SQL code only - simplified approach
                    sql_content = "-- Data Quality Rules - Pseudo SQL Code\n"
                    sql_content += f"-- Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    
                    sql_found = False
                    for category, rule_list in rules.items():
                        if isinstance(rule_list, list):
                            for rule in rule_list:
                                if isinstance(rule, dict) and 'pseudo_sql' in rule:
                                    sql_found = True
                                    sql_content += f"-- {category.upper()}: {rule.get('rule', '')}\n"
                                    columns = rule.get('columns', rule.get('columns_involved', []))
                                    sql_content += f"-- Columns: {', '.join(columns) if isinstance(columns, list) else columns}\n"
                                    sql_content += f"{rule.get('pseudo_sql', '')}\n\n"
                    
                    if sql_found:
                        st.download_button(
                            label="💾 Download SQL Code Only",
                            data=sql_content,
                            file_name="data_quality_rules.sql",
                            mime="text/plain"
                        )
                
                with col3:
                    # Export KPI report
                    kpi_report = kpi_analyzer.export_kpi_report()
                    st.download_button(
                        label="📊 Download KPI Report",
                        data=kpi_report,
                        file_name="data_quality_kpi_report.json",
                        mime="application/json"
                    )

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    main()