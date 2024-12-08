import os
import toml


def modify_theme(base, primaryColor, backgroundColor, secondaryBackgroundColor, textColor, font):
    """
    Streamlit Theme Customization Function

    This function dynamically modifies the Streamlit configuration file (.streamlit/config.toml)
    to customize the application's visual theme, providing a flexible and programmatic 
    approach to UI personalization.

    Parameters:
    -----------
    base : str
        The base theme to use as a starting point (e.g., 'light' or 'dark')
    primaryColor : str
        The primary accent color for interactive elements (buttons, highlights)
        Accepts hex color codes or standard color names
    backgroundColor : str
        The main background color of the application
        Accepts hex color codes or standard color names
    secondaryBackgroundColor : str
        The background color for secondary elements like sidebars or card backgrounds
        Accepts hex color codes or standard color names
    textColor : str
        The primary text color used throughout the application
        Accepts hex color codes or standard color names
    font : str
        The font family to be used for text rendering
        Accepts standard font family names or web fonts

    Theme Configuration Workflow:
    ----------------------------
    1. Dynamically locate the Streamlit configuration file
    2. Prepare a configuration dictionary with theme parameters
    3. Write the configuration to the .toml file
    4. Enable runtime theme customization

    Key Features:
    ------------
    - Supports dynamic, programmatic theme modification
    - Provides granular control over UI color scheme
    - Maintains Streamlit's configuration file structure
    - Allows easy theme switching and personalization

    File Management:
    ---------------
    - Constructs config path relative to the script's location
    - Creates .streamlit directory if it doesn't exist
    - Ensures configuration file is always up-to-date

    Error Handling:
    --------------
    - Implicitly handles potential file writing errors
    - Supports graceful theme configuration updates

    Example:
    --------
    modify_theme(
        base='light', 
        primaryColor='#FF5733', 
        backgroundColor='#FFFFFF', 
        secondaryBackgroundColor='#F0F0F0', 
        textColor='#000000', 
        font='Arial'
    )
    # Customizes Streamlit app theme with specified parameters
    """
    
    # Construct the path to config.toml dynamically
    config_path = os.path.join(os.path.dirname(__file__), '..', '.streamlit', 'config.toml')

    # Load existing configuration
    with open(config_path, 'r') as f:
        config = toml.load(f)

    # Modify theme settings
    config['theme'] = {
        'base': base,
        'primaryColor': primaryColor,
        'backgroundColor': backgroundColor,
        'secondaryBackgroundColor': secondaryBackgroundColor,
        'textColor': textColor,
        'font': font
    }

    # Write updated configuration back to file
    with open(config_path, 'w') as f:
        toml.dump(config, f)