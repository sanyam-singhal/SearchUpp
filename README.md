# SearchUpp

SearchUpp is an intelligent web research assistant that helps you gather, analyze, and summarize information from multiple web sources. It combines powerful web scraping capabilities with AI-driven summarization to streamline your research process.

## Interactive Demo 

Find the demo [here](https://app.arcade.software/share/Z49Xibxk5GCP9En9oAMo)

![SearchUpp Demo](https://github.com/yourusername/searchupp/blob/main/assets/searchupp.png?raw=true)

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
  - Flexible choice between local and cloud-based LLMs
  - Local summarization using Ollama with open-source models
  - Cloud-based summarization using Google Gemini AI
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
- Required API keys and services:
  - Brave Search API key
  - Google Gemini API key (optional, needed if using cloud-based summarization)
  - Ollama installed and running (optional, needed if using local summarization)

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
MODE='Cloud'  # 'Cloud' for Gemini or 'Local' for Ollama
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
│   ├── ai_modules.py       # AI-powered summarization (Ollama & Gemini)
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
- Flexible choice between local and cloud-based summarization:
  - **Local Mode**: Uses Ollama to run open-source models locally
  - **Cloud Mode**: Utilizes Google's Gemini AI
- Customizable system instructions for content summarization
- Maintains context and relationships between ideas
- Generates comprehensive summaries (1000-4000 words)

## 📝 Usage

1. **Start a New Search**:
   - Enter your research query
   - Choose between simple and advanced search modes
   - Select local or cloud-based summarization
   - Wait for the search results and web scraping to complete
   - Review the generated summary

2. **View History**:
   - Access past searches from the History page
   - Click on any past search to view details
   - Navigate through your research history

3. **Customize Settings**:
   - Configure API keys and search parameters
   - Choose between local and cloud-based summarization
   - Customize the theme to your preference
   - Modify LLM system instructions for content summarization
   - Adjust the number of search results

## 🎛️ Configuration

SearchUpp offers two modes of operation:

### Simple Search
- Uses simpler models (Gemini Flash or Ollama's basic models)
- Fetches 5 search results
- Optimized for quick research tasks

### Advanced Search
- Uses more advanced models
- Fetches 10 search results
- Better for in-depth research requiring more comprehensive results

### Summarization Modes

#### Local Mode (Ollama)
- Runs open-source models locally
- No API costs or usage limits
- Requires more computational resources
- Default model: llama3.2:1b

#### Cloud Mode (Gemini)
- Uses Google's Gemini AI
- Faster processing
- Requires API key and has associated costs
- Default model: gemini-1.5-flash-002

All settings can be configured through the Settings page (⚙️) in the application, including:
- API Keys (Brave Search and Google Gemini)
- Search results count for both modes
- AI model selection for both modes
- LLM system instructions for content summarization
- Summarization mode (Local/Cloud)

## 🗂️ Application Pages

- **Search** (🔍): Main search interface with toggle for Advanced Search
- **History** (📜): View all past searches
- **Recap** (🤔): Detailed view of past search results
- **Settings** (⚙️): Configure application settings and customize theme

## ⚙️ Configuration

The application can be configured through environment variables:
- `BRAVE_KEY`: Your Brave Search API key
- `GEMINI_KEY`: Your Google Gemini API key (required for cloud mode)
- `SIMPLE_SEARCH_NUMBER`: Number of results for simple search
- `COMPLEX_SEARCH_NUMBER`: Number of results for complex search
- `SIMPLE_LLM_MODEL`: Model used for simple search summarization
- `COMPLEX_LLM_MODEL`: Model used for complex search summarization
- `SEARCH_SUMMARY_INSTRUCTIONS`: Custom instructions for LLM content summarization
- `MODE`: Summarization mode ('Local' for Ollama or 'Cloud' for Gemini)

## 📚 Documentation

For detailed documentation of all functions and modules, please refer to the `modules/MODULE_DOCUMENTATION.md` file.

## 👥 Contributing

We welcome contributions to SearchUpp! Whether you're fixing bugs, adding new features, improving documentation, or suggesting enhancements, your help is appreciated.

### How to Contribute

1. **Fork the Repository**
   - Fork the project repository to your GitHub account

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/your-username/searchupp.git
   cd searchupp
   ```

3. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**
   - Write your code
   - Follow the existing code style
   - Add or update documentation as needed
   - Add appropriate tests if applicable

5. **Test Your Changes**
   - Ensure all tests pass
   - Test the functionality thoroughly

6. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add a descriptive commit message"
   ```

7. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Submit a Pull Request**
   - Open a pull request from your fork to our main repository
   - Provide a clear description of your changes
   - Reference any related issues

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Write clear, descriptive commit messages
- Document new features or changes in the README
- Update requirements.txt if adding new dependencies

### Need Help?

If you have questions or need help with the contribution process, feel free to:
- Open an issue for discussion
- Ask questions in pull requests
- Reach out to the maintainers

Thank you for contributing to SearchUpp! 🎉

## 🔄 Recent Updates (12-12-2024)

### Environment and Configuration
- Simplified `.env` file to only require user-specific API keys (GEMINI_KEY and BRAVE_KEY)
- All other configuration values are now set with sensible defaults in the application
- Added dynamic project directory path resolution
- Updated requirements.txt to include all necessary dependencies

### User Interface Improvements
- Added query display in search results for better context
- Enhanced link security by adding `rel="noopener noreferrer"` to external links
- Improved history page error handling
- Updated "Recap" page title and styling

### Code Organization
- Removed redundant environment variables from startup scripts
- Added automatic search directory creation
- Improved code documentation and error handling
- Updated package dependencies and versions

---

**Generated on:** 2024-12-12
**Version:** 2.1
