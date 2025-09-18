# Data Quality Rule Generator

An AI-powered Streamlit application that automatically generates comprehensive data quality rules for CSV datasets. The tool analyzes your data and creates rules covering accuracy, completeness, uniqueness, consistency, timeliness, and validity dimensions.

## Features

- 🤖 **AI-Powered Analysis**: Uses OpenAI's API to generate intelligent data quality rules
- 📊 **Interactive Dashboard**: Modern UI with comprehensive KPI visualizations
- 🔍 **Multi-Dimensional Analysis**: Covers all major data quality dimensions
- 📈 **Real-time Metrics**: Live analysis of rule coverage and complexity
- 💾 **Export Options**: Download rules as JSON or SQL code
- 🎨 **Modern UI**: Clean, responsive design with custom typography

## Data Quality Dimensions Covered

- **Accuracy**: Data reflects reality correctly
- **Completeness**: No missing values where expected
- **Uniqueness**: No duplicate records
- **Consistency**: Data follows expected patterns
- **Timeliness**: Data is current and up-to-date
- **Validity**: Data conforms to defined schemas

## Installation

1. Clone the repository:
```bash
git clone https://github.com/juansegiraldo/DQRuleGenerator.git
cd DQRuleGenerator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
streamlit run main.py
```

## Usage

1. **Upload Data**: Upload your CSV file through the web interface
2. **Provide Context**: Optionally add context about your data domain and requirements
3. **Generate Rules**: Click "Generate Data Quality Rules" to analyze your data
4. **Review Results**: Explore the generated rules organized by category
5. **Export**: Download rules as JSON or SQL code for implementation

## Project Structure

```
DQRuleGenerator/
├── main.py                 # Main Streamlit application
├── utils/
│   ├── data_analyzer.py    # Data analysis utilities
│   ├── openai_helper.py    # OpenAI API integration
│   ├── rule_generator.py   # Rule generation logic
│   └── kpi_analyzer.py     # KPI analysis and metrics
├── test_data.csv          # Sample dataset for testing
├── pyproject.toml         # Project dependencies
└── README.md              # This file
```

## Dependencies

- `streamlit>=1.42.0` - Web application framework
- `pandas>=2.2.3` - Data manipulation
- `openai>=1.61.1` - AI API integration
- `plotly>=5.17.0` - Interactive visualizations
- `python-dotenv>=1.0.0` - Environment variable management

## Example Output

The application generates rules like:

```sql
-- ACCURACY: Email addresses should be valid
SELECT * FROM table_name 
WHERE email_column NOT REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$';

-- COMPLETENESS: Required fields should not be null
SELECT * FROM table_name 
WHERE customer_id IS NULL OR customer_name IS NULL;
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**Juan Sebastián Giraldo**
- GitHub: [@juansegiraldo](https://github.com/juansegiraldo)

## Acknowledgments

- OpenAI for providing the AI capabilities
- Streamlit team for the excellent web framework
- The data quality community for best practices and standards
