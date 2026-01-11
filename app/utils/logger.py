import logging
import os

def get_logger(name:str) -> logging.Logger:
   """
   Creates and returns a logger with the specified name.
    Args:
         name (str): The name of the logger.
    Returns:
         logging.Logger: Configured logger instance.

   """ 
   logger=logging.getLogger(name)
   logger.setLevel(logging.DEBUG)
   formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
   # Create console handler
   ch=logging.StreamHandler()
   ch.setFormatter(formatter)
   logger.addHandler(ch)

   #Create file 
   os.makedirs('logs', exist_ok=True)
   fh=logging.FileHandler('logs/app.log')
   fh.setFormatter(formatter)
   logger.addHandler(fh)

   return logger