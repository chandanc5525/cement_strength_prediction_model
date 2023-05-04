import os, sys
import pandas as pd
import numpy as np
from ml.constant import *
from ml.logger import logging
from ml.entity.config_entity import DataIngestionConfig
from ml.entity.artifact_entity import DataIngestionArtifact
from ml.exception import CustomException
from datetime import date
from sklearn.model_selection import train_test_split
from six.moves import urllib
# download data ( Cloud, Databse, Github) -> Raw Data
# Split Data into train and test -> Ingested data

class DataIngestion:
    def __init__(self,data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e, sys) from e

    def download_data(self)->str:
        try:
            download_url = self.data_ingestion_config.dataset_download_url # able to download dataset

            raw_data_dir = self.data_ingestion_config.raw_data_dir

            os.makedirs(raw_data_dir, exist_ok=True)

            us_visa_file_name = os.path.basename(download_url)

            raw_file_path = os.path.join(raw_data_dir,us_visa_file_name)
            logging.info(f"Downloading file from: [{download_url}] into :[{raw_data_dir}]")

            urllib.request.urlretrieve(download_url, raw_file_path)

            logging.info(f"File: [{raw_file_path}] has been downloaded successfully")

            return raw_file_path

        except Exception as e:
            raise CustomException(e, sys) from e

    def split_data_as_train_test(self)->DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            file_name = os.listdir(raw_data_dir)[0]

            us_visa_file_name = os.path.join(raw_data_dir,file_name)

            today_date = date.today()
            current_year = today_date.year

            us_visa_dataframe = pd.read_csv(us_visa_file_name)

            us_visa_dataframe[COLUMN_COMPANY_AGE] = current_year - us_visa_dataframe[COLUMN_YEAR_ESTB]

            us_visa_dataframe.drop([COLUMN_ID, COLUMN_YEAR_ESTB], axis = 1, inplace= True)

            us_visa_dataframe[COLUMN_CASE_STATUS] = np.where(us_visa_dataframe[COLUMN_CASE_STATUS] == 'Denied',1,0 )

            train_set = None
            test_set = None

            train_set, test_set = train_test_split(us_visa_dataframe, test_size=0.2, random_state=42)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                           file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                          file_name)

            if train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir, exist_ok=True)
                logging.info(f"Exporting training dataset to file: [{train_file_path}]")
                train_set.to_csv(train_file_path, index= False)

            if test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok=True)
                logging.info(f"Exporting training dataset to file: [{test_file_path}]")
                test_set.to_csv(test_file_path, index= False)


            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                                            test_file_path=test_file_path,
                                                            is_ingested=True,
                                                            message = f"Data Ingestion Completed Successfully")
            logging.info(f"Data Ingestion Artifact: [{data_ingestion_artifact}]")

            return data_ingestion_artifact

        except Exception as e:
            raise CustomException(e, sys)(e)

    def initate_data_ingestion(self):
        try:
            raw_data_file = self.download_data()
            return self.split_data_as_train_test()
        except Exception as e:
            raise CustomException(e, sys)(e)

