import logging
from pipeline import run_archive_pipeline


def lambda_handler(event: None, context: None):
    '''This function is called by the AWS Lambda to run the Python scripts.'''
    logger = logging.getLogger()
    logger.setLevel("INFO")
    try:
        logger.info("Running...")
        run_archive_pipeline()
        logger.info("Successful")
        return {
            'status_code': 200
        }
    except Exception as e:
        logger.error("Error: %s", e)
        raise
