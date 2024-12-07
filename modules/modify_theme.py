import os
import toml


def modify_theme(base, primaryColor, backgroundColor, secondaryBackgroundColor, textColor, font):
    """
    Modifies the .streamlit/config.toml file with the specified theme settings.
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