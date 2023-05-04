import os, sys
import pandas as pd
import numpy as np
from ml.constant import *
from ml.logger import logging
from ml.exception import CustomException
from ml.pipeline.pipeline import Pipeline
import os, sys


def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()
    except Exception as e:
        logging.error(f"{e}")


if __name__ == "__main__":
    main()
