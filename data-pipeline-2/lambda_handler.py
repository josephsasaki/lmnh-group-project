import logging
from pipeline import run_archive_pipeline


def lambda_handler(event, context):
    '''This function is called by the AWS Lambda to run the Python scripts.'''
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    try:
        logger.info("Running...")
        run_archive_pipeline()
        logger.info("Successful")
        return {
            'status_code': 200,
            'body': 'Success'
        }
    except Exception as e:
        return {
            'status_code': 400,
            'body': str(e)
        }
