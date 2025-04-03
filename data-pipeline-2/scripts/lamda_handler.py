import logging
from pipeline import run_archive_pipeline


def lambda_handler(event: None, context: None):
    '''This function is called by the AWS Lambda to run the Python scripts.'''
    logger = logging.getLogger()
    logger.setLevel("INFO")
    try:
        logger.info(f"Running...")
        run_archive_pipeline()
        logger.info(f"Successful")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise
