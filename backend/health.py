import os

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = [
        'ANTHROPIC_API_KEY',
        'PORT',
        'PYTHONPATH',
        'DOCS_PATH',
        'DB_PATH'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")
    
    return True 