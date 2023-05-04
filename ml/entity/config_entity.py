from collections import namedtuple


DataIngestionConfig=namedtuple("DataIngestionConfig",
["dataset_download_url","raw_data_dir","ingested_train_dir","ingested_test_dir"])