# SearchUpp

SearchUpp is an intelligent web research assistant that helps you gather, analyze, and summarize information from multiple web sources. It combines powerful web scraping capabilities with AI-driven summarization to streamline your research process.

## 🌟 Features

- **Smart Web Search**: 
  - Utilizes Brave Search API for accurate and privacy-focused web results
  - Semantic reranking of search results using vector embeddings
  - Enhanced scraping setup for improved content extraction
  - Optimized search result processing
- **Intelligent Web Scraping**: 
  - Human-like browsing behavior with random scrolling and mouse movements
  - Robust content extraction from various webpage structures
  - Handles dynamic content loading
- **Content Processing**:
  - Extracts structured content (headings, paragraphs, lists)
  - Maintains content hierarchy and relationships
  - Cleans and normalizes text for better readability
- **AI-Powered Summarization**:
  - Generates comprehensive summaries using Gemini AI
  - Maintains context and key relationships between ideas
  - Customizable summary length (1000-4000 words)
  - Configurable LLM system instructions for content summarization
- **Research History**:
  - Saves all research sessions
  - Easy access to past searches and summaries
  - Organized storage of scraped content
- **Advanced Search**: Toggle between simple and advanced search modes to customize search depth and model complexity.
- **Customizable Theme**:
  - Dynamic theme customization through Settings page
  - Control primary colors, background colors, and text colors
  - Font selection options
  - Changes persist across sessions
- **Comprehensive Documentation**:
  - Detailed function-level documentation
  - Clear explanation of each module's functionality
  - Examples and usage instructions for all components

## Performance Note

> **Current Bottleneck:** The primary performance bottleneck in the application is the web scraping process. The use of Selenium for scraping can be time-consuming, especially when dealing with a large number of URLs or complex webpages. Optimizing the scraping logic and exploring parallel scraping techniques could improve performance.

## 🚀 Getting Started

### Prerequisites

- Python 3.12 (not tested on other versions)
- Chrome browser installed (used by the Selenium package for scraping)
- Required API keys:
  - Brave Search API key
  - Google Gemini API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/searchupp.git
cd searchupp
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

> **Note:** The `requirements.txt` file specifies exact package versions (using `==`) instead of minimum versions (using `>=`). This ensures consistent behavior across different installations and environments.

3. Create a `.env` file in the project root with your API keys and settings:
```
BRAVE_KEY='your_brave_api_key'
GEMINI_KEY='your_gemini_api_key'
SIMPLE_SEARCH_NUMBER='5'
COMPLEX_SEARCH_NUMBER='10'
SIMPLE_LLM_MODEL='gemini-1.5-flash-002'
COMPLEX_LLM_MODEL='gemini-exp-1206'
PROJECT_DIR='your_project_directory_path'
SEARCH_SUMMARY_INSTRUCTIONS='your_custom_llm_instructions'
```

These settings can be configured through the Settings page in the application.

### Running the Application

You can run the application using the provided scripts:

**Windows**:
- Double-click the `run_searchupp.bat` file
- Or run from command prompt:
```bash
.\run_searchupp.bat
```

**macOS/Linux**:
- Make the script executable and run:
```bash
chmod +x run_searchupp.sh
./run_searchupp.sh
```

Alternatively, start the Streamlit app directly:
```bash
streamlit run app.py
```

## 🛠️ Project Structure

```
searchupp/
├── app.py                  # Main Streamlit application
├── modules/
│   ├── search_modules.py   # Core search and scraping functionality
│   └── modify_theme.py     # Theme customization functionality
├── paths/
│   ├── search.py          # Search page implementation
│   ├── history.py         # History page implementation
│   ├── past.py            # Past searches page implementation
│   └── settings.py        # Settings and theme management
├── .streamlit/
│   └── config.toml        # Streamlit configuration and theme settings
├── run_searchupp.bat      # Windows startup script
├── run_searchupp.sh       # macOS/Linux startup script
└── search/                # Directory for storing search results
```

## 🔧 Core Components

### Web Search
- Utilizes Brave Search API for comprehensive web results
- Implements semantic reranking using vector embeddings
- Extracts and processes URLs from search results
- Handles pagination and result filtering

### Web Scraping
- Uses Selenium for robust web scraping
- Implements human-like browsing behavior
- Extracts structured content while maintaining hierarchy
- Handles various webpage structures and dynamic content

### Content Processing
- Cleans and normalizes extracted text
- Maintains proper content structure
- Handles different content types (paragraphs, lists, headings)

### Summary Generation
- Utilizes Google's Gemini AI for intelligent summarization
- Customizable system instructions for content summarization
- Maintains context and relationships between ideas
- Generates comprehensive summaries (1000-4000 words)

## 📝 Usage

1. **Start a New Search**:
   - Enter your research query
   - Choose between simple and advanced search modes
   - Wait for the search results and web scraping to complete
   - Review the generated summary

2. **View History**:
   - Access past searches from the History page
   - Click on any past search to view details
   - Navigate through your research history

3. **Customize Settings**:
   - Configure API keys and search parameters
   - Customize the theme to your preference
   - Modify LLM system instructions for content summarization
   - Adjust the number of search results

## 🎛️ Configuration

SearchUpp offers two modes of operation:

### Simple Search
- Uses `gemini-1.5-flash-002` model by default
- Fetches 5 search results
- Optimized for quick research tasks

### Advanced Search
- Uses `gemini-1.5-flash-002` model by default
- Fetches 10 search results
- Better for in-depth research requiring more comprehensive results

All settings can be configured through the Settings page (⚙️) in the application, including:
- API Keys (Brave Search and Google Gemini)
- Search results count for both modes
- AI model selection for both modes
- LLM system instructions for content summarization

## 🗂️ Application Pages

- **Search** (🔍): Main search interface with toggle for Advanced Search
- **History** (📜): View all past searches
- **Recap** (🤔): Detailed view of past search results
- **Settings** (⚙️): Configure application settings and customize theme

## ⚙️ Configuration

The application can be configured through environment variables:
- `BRAVE_KEY`: Your Brave Search API key
- `GEMINI_KEY`: Your Google Gemini API key
- `SIMPLE_SEARCH_NUMBER`: Number of results for simple search
- `COMPLEX_SEARCH_NUMBER`: Number of results for complex search
- `SIMPLE_LLM_MODEL`: Model used for simple search summarization
- `COMPLEX_LLM_MODEL`: Model used for complex search summarization
- `SEARCH_SUMMARY_INSTRUCTIONS`: Custom instructions for LLM content summarization

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Brave Search](https://brave.com/search/) for providing the search API
- [Google Gemini](https://deepmind.google/technologies/gemini/) for AI-powered summarization
- [Selenium](https://www.selenium.dev/) for web automation
- [Streamlit](https://streamlit.io/) for the web interface
