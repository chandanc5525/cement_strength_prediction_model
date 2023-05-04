import os, sys
import pandas as pd
import numpy as np
from ml.constant import *
from ml.logger import logging
from ml.entity.config_entity import DataIngestionConfig
from ml.entity.artifact_entity import DataIngestionArtifact
from ml.exception import CustomException
from datetime import date
from collections import namedtuple
from ml.config.configuration import Configuartion
from ml.components.data_ingestion import DataIngestion


class Pipeline():
    def __init__(self, config: Configuartion = Configuartion()) -> None:
        try:
            self.config = config
        except Exception as e:
            raise CustomException(e , sys) from e

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initate_data_ingestion()
        except Exception as e:
            raise CustomException(e, sys) from e

    def run_pipeline(self):
        try:
            # Data Ingestion
            data_ingestion_artifact = self.start_data_ingestion()
        except Exception as e:
            raise CustomException(e, sys) from e
