import logging
import time

from error.RetryException import RetryException

logger = logging.getLogger(__name__)


def retry_function(function, retries=2, delay=10, **kwargs):
    for attempt in range(retries):

        logger.info(f"Delaying retry for {delay} sec")
        time.sleep(delay)

        try:
            logger.info(f"Retry attempt {attempt+1} of {retries} for function: {function.__name__} ")
            return function(**kwargs)
        except Exception as e:
            logger.error(f"Retry attempt number {attempt+1} for {function.__name__} failed with message {e}")

    raise RetryException(f"Function: {function.__name__} with arguments {kwargs} failed all {retries} attempts")
