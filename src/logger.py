import logging
import os


# Ensure the "logs" directory exists
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

def get_logger(name):
    """Get a logger instance with the specified name and configuration."""
    logger = logging.getLogger(name)
    logger.setLevel('DEBUG')
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel('DEBUG')
    
    log_file_path = os.path.join(log_dir, f'{name}.log')
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel('DEBUG')
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger