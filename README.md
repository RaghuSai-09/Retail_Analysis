# Retail Analysis

A comprehensive retail analytics web application built with Flask that provides insights into household shopping patterns, customer behavior, and product trends. The application features interactive dashboards, market basket analysis, customer churn prediction, and advanced search capabilities.

## 🌟 Features

- **Interactive Dashboard**: Visualize retail data with multiple charts and graphs
  - Total spend by household size
  - Spending patterns by presence of children
  - Store region performance analysis
  - Yearly spending trends
  - Department-wise analysis over time
  - Top-selling products
  - Brand type distribution
  - Units sold by product category

- **Customer Churn Analysis**: Identify and analyze customer disengagement patterns
  - Correlation analysis between disengagement and demographics
  - Spending trends by disengagement status
  - Purchase frequency analysis

- **Market Basket Analysis**: Discover product associations and buying patterns
  - Frequent itemset mining using Apriori algorithm
  - Association rules with support, confidence, and lift metrics
  - Product recommendation insights

- **Advanced Search**: Query and filter transaction data
  - Search by household number
  - Sort by multiple fields (basket number, product number, department, etc.)
  - Detailed transaction history

- **Data Upload**: Upload and manage datasets
  - Support for CSV and JSON file formats
  - Upload households, products, and transactions data
  - Real-time data refresh

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: MongoDB (with PyMongo integration)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Seaborn, Matplotlib
- **Machine Learning**: MLxtend (for association rule mining)
- **Deployment**: Google Cloud Platform (App Engine)
- **Server**: Gunicorn

## 📋 Prerequisites

- Python 3.10 or higher
- MongoDB instance (local or cloud)
- pip (Python package manager)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/RaghuSai-09/Retail_Analysis.git
   cd Retail_Analysis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```
   MONGO_URL=mongodb://localhost:27017/retail_analysis
   ```
   
   Replace with your MongoDB connection string if using a cloud database.

4. **Prepare data files**
   
   Create a `data` directory and add your CSV files:
   - `households.csv` - Household demographic information
   - `transactions.csv` - Transaction records
   - `products.csv` - Product catalog information

## 💾 Data Upload

Before running the application, upload the data to MongoDB:

```bash
python upload_data.py
```

This script will:
- Check if data already exists in the database
- Upload households, transactions, and products data
- Use bulk write operations for efficient transaction uploads
- Display progress with a progress bar

## 🏃 Running the Application

### Development Mode

```bash
python main.py
```

The application will start on `http://localhost:5000` with debug mode enabled.

### Production Mode

```bash
gunicorn -b :8080 main:app
```

## 🌐 Application Routes

- `/` - Login page (default credentials: admin/admin123)
- `/menu` - Main menu
- `/dashboard` - Interactive analytics dashboard
- `/churn` - Customer churn analysis
- `/basket` - Market basket analysis
- `/search` - Advanced search functionality
- `/upload` - Data upload interface

## 📁 Project Structure

```
Retail_Analysis/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── routes.py             # Main routes (login, dashboard, search, upload)
│   ├── chunk.py              # Customer churn analysis blueprint routes
│   ├── basket_analysis.py    # Market basket analysis routes
│   ├── data_preparation.py   # Data loading and preprocessing
│   ├── static/               # CSS, images, and static assets
│   └── templates/            # HTML templates
├── data/                     # Data directory (CSV files)
├── main.py                   # Application entry point
├── upload_data.py            # MongoDB data upload script
├── requirements.txt          # Python dependencies
├── app.yaml                  # Google Cloud App Engine configuration
├── .gcloudignore            # GCloud ignore file
└── .gitignore               # Git ignore file
```

## 📊 Data Schema

### Households
- `HSHD_NUM` - Household number
- `AGE_RANGE` - Age range of household head
- `INCOME_RANGE` - Income range
- `HH_SIZE` - Household size
- `CHILDREN` - Presence of children (Y/N)
- `STORE_R` - Store region

### Transactions
- `BASKET_NUM` - Unique basket/transaction identifier
- `HSHD_NUM` - Household number
- `PURCHASE_` - Purchase date
- `PRODUCT_NUM` - Product number
- `SPEND` - Amount spent
- `UNITS` - Number of units purchased

### Products
- `PRODUCT_NUM` - Product number
- `DEPARTMENT` - Product department
- `COMMODITY` - Product commodity
- `BRAND_TY` - Brand type

## 🔧 Configuration

### MongoDB Configuration

The application uses MongoDB for data storage. Configure the connection string in your `.env` file or set the `MONGO_URL` environment variable.

### Google Cloud Deployment

The project includes `app.yaml` for deployment to Google Cloud Platform App Engine:

```bash
gcloud app deploy
```

## 🔒 Authentication

The application includes basic authentication with a default user:
- **Username**: admin
- **Password**: admin123

⚠️ **Note**: For production use, implement proper authentication and change default credentials.

## 📈 Analytics Features

### Dashboard Visualizations
- Bar charts for household size and children impact on spending
- Store region performance comparison
- Time series analysis of yearly spending trends
- Department-wise spending over time
- Top 7 products by spend
- Brand type distribution pie chart
- Units sold trends by category

### Churn Analysis
- Identifies customers with declining spend or purchase frequency
- Correlation heatmap for demographic factors
- Visualizations of spending and frequency trends

### Market Basket Analysis
- Apriori algorithm for frequent itemset mining
- Association rules with configurable thresholds
- Support, confidence, and lift metrics

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

RaghuSai-09

## 🐛 Issues

If you encounter any problems, please file an issue on the GitHub repository.

## 🙏 Acknowledgments

- Built with Flask and Python
- Visualization powered by Plotly and Seaborn
- Market basket analysis using MLxtend
