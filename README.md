# SearchUpp

SearchUpp is an intelligent web research assistant that helps you gather, analyze, and summarize information from multiple web sources. It combines powerful web scraping capabilities with AI-driven summarization to streamline your research process.

## 🌟 Features

- **Smart Web Search**: Utilizes Brave Search API for accurate and privacy-focused web results
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
- **Research History**:
  - Saves all research sessions
  - Easy access to past searches and summaries
  - Organized storage of scraped content

## Performance Note

> **Current Bottleneck:** The primary performance bottleneck in the application is the web scraping process. The use of Selenium for scraping can be time-consuming, especially when dealing with a large number of URLs or complex webpages. Optimizing the scraping logic and exploring parallel scraping techniques could improve performance.

## 🚀 Getting Started

### Prerequisites

- Python 3.12 or higher
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

3. Create a `.env` file in the project root with your API keys:
```
BRAVE_KEY=your_brave_api_key
GEMINI_KEY=your_gemini_api_key
```

### Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

## 🛠️ Project Structure

```
searchupp/
├── app.py                 # Main Streamlit application
├── modules/
│   └── parallel_search.py # Core search and scraping functionality
├── paths/
│   ├── search.py         # Search page implementation
│   ├── history.py        # History page implementation
│   └── past.py           # Past searches page implementation
└── search/               # Directory for storing search results
```

## 🔧 Core Components

### Web Search
- Utilizes Brave Search API for comprehensive web results
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
- Maintains context and relationships between ideas
- Generates comprehensive summaries (1000-4000 words)

## 📝 Usage

1. **Start a New Search**:
   - Enter your research query
   - Wait for the search results and web scraping to complete
   - Review the generated summary

2. **View History**:
   - Access past searches from the History page
   - Click on any past search to view details
   - Navigate through your research history

## ⚙️ Configuration

The application can be configured through environment variables:
- `BRAVE_KEY`: Your Brave Search API key
- `GEMINI_KEY`: Your Google Gemini API key

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Brave Search](https://brave.com/search/) for providing the search API
- [Google Gemini](https://deepmind.google/technologies/gemini/) for AI-powered summarization
- [Selenium](https://www.selenium.dev/) for web automation
- [Streamlit](https://streamlit.io/) for the web interface
