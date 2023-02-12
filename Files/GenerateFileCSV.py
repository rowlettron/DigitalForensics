import os
import os.path
import time

import pandas as pd
import argparse
import hashlib

def get_args():
    parser = argparse.ArgumentParser(description="Scan all magic files")
    parser.add_argument("path", help="Path to folder")

    return parser.parse_args()

def create_dataframe():
    COLUMN_NAMES=['Folder','FileName','CreateDate','LastAccessDateTime','ModifiedTime','Size','FileHash']
    df = pd.DataFrame(columns=COLUMN_NAMES)

    return df

def file_sha1_hash(path):
    hasher = hashlib.sha1()
    fh = open(path, "rb")
    chunk = fh.read(HASH_FILE_CHUNK_SIZE)
    while chunk:
        hasher.update(chunk)
        chunk = fh.read(HASH_FILE_CHUNK_SIZE)

    fh.close()
    return hasher.hexdigest()

def insert_row(df, my_row):
    df.loc[len(df)] = my_row

def parse_folders(path,df):
    for (root,dirs,files) in os.walk(path, topdown=True):
        for file in files:
            completefilename = os.path.abspath(root) + '/' + file
            folder = os.path.abspath(root)
            filename = file
            createdate = time.ctime(os.path.getctime(completefilename))
            lastaccessdatetime = time.ctime(os.path.getatime(completefilename))
            modifieddate = time.ctime(os.path.getmtime(completefilename))
            size = os.path.getsize(completefilename)

            filehash = file_sha1_hash(completefilename)

            # print('{0},{1},{2},{3},{4},{5},{6}'.format(folder, filename, createdate, lastaccessdatetime, modifieddate, size, filehash))
            insert_row(df, [folder, filename, createdate, lastaccessdatetime, modifieddate, size, filehash])

def export_df_to_csv(df):
    df.to_csv('Files.csv', index=False)

def main():
    args = get_args()
    # print(args.path)
    dfFile = create_dataframe()

    parse_folders(args.path,dfFile)

    export_df_to_csv(dfFile)
    
    print(dfFile)
    

################# Main Processing Section ##############################

if __name__ == '__main__':
    start_date = '2022-07-10'
    end_date = '2022-07-20'
    HASH_FILE_CHUNK_SIZE = 8192
    HASH_ZERO_FILE = "0" * 40
    main()
