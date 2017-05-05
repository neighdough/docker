import numpy as np
import pandas as pd
import collections
import csv
import os
from fuzzywuzzy import fuzz
import string
import re
from pyspark.sql import DataFrameReader
from pyspark.sql.functions import udf, concat_ws, lit
from pyspark.sql.types import (StringType, DoubleType, LongType, DateType,
                                StructField, StructType)
from pyspark import SparkConf
import sys
from caeser import utils

os.chdir(r'/home/ubuntu/data')
sys.path.append('.')
conf = SparkConf()
exp = '[{}]?'.format(string.punctuation)
idx_props = 0
idx_alias = 0

def no_tax_list():
    lst_tax = []
    with open('missing_city_taxes.csv','rb') as f:
        r = csv.reader(f)
        r.next()
        for row in r:     
            lst_tax.append(row[2].strip())
    return lst_tax

#taxes = set(lst_tax)    
 
def assessor_table(table):
    """
    builds nested dictionary containing records from assessor's table
    whose parcelid is contained in missing tax table
    nested key values are derived from table header
    """
    assessor_dict = collections.defaultdict(list)
    with open(table, 'rb') as f:
        reader = csv.reader(f)
        header = [i.lower() for i in reader.next() if i != 'PARID']
        for row in reader:
            if row[0] in lst_tax:
                assessor_dict[row[0]] = {header[i]: row[ i + 1] for i in range(len(header))}
    return assessor_dict    

def luc_codes():
    luc_desc = collections.defaultdict(str)
    with open('AEDIT.txt', 'rb') as f:
        reader = csv.reader(f)
        reader.next()
        for row in reader:
            if row[0] == 'ASMT' and row[1] == 'LUC':
                print row[2], row[3].split('-')[1].strip()
                luc_desc[row[2]] = row[3].split('-')[1].strip()
    return luc_desc
        
def match_owners(record):
    '''
    >>>match_owners('dockery charles', 'docker charlie')
    False
    >>>match_owners('dawning investments llc series a', 'dawning investments llc series f')
    True
    >>>match_owners('davis lillian', 'davis lillian c')
    True
    >>>match_owners('d and d enterprise', 'd and d enterprise llc')
    True
    >>>match_owners('burress leland & shirley','burress leland jr & shirley j)
    True
    >>>match_owners('smith jasper and kenney r smith and', 'smith jasper and kenny r smith and')
    True
    >>>match_owners('smith mary e', 'smith mary g')
    False    
    '''
    if owner1 == owner2:
        update(owner1)
    else:
        return fuzz.partial_ratio(owner1, s2)
    
def clean_string(text):
    '''
    takes raw string from assessor's database and returns a standardized version
    in lower case without any punctuation
    '''
    text = re.sub(exp, '', text)
    return re.sub('\s{2,}', ' ', text)
            
def remove_values(s1,ls):
    """ s1 --> string to match
        list1 --> list of closest matches returned from difflib.get_close_matches
        return --> a list containing the closest matching string, and a sequence 
                    of match ratios generated from fuzzywuzzy module
    
    difflib.get_close_matches returns matches in decreasing order of match
    with the first result always being an exact match because it's included
    in the full list, therefore, picking the second in the list means that 
    it's the next closest match besides its match"""
    drop_vals = filter(lambda x:match_score(s1,x) > 75 and match_score(s1,x) <100, ls)
    return drop_vals

def match_score(s1, s2):
    ratio = fuzz.ratio(s1,s2)
    token_ratio = fuzz.token_set_ratio(s1, s2)
    partial_ratio = fuzz.token_sort_ratio(s1,s2)
    avg = np.mean((ratio,token_ratio,partial_ratio))
    return avg
    
def next_largest(list1):
    m = max(list1)
    return max(n for n in list1 if n != m)

def accuracy(min_distance):
    est_own = df_dup[df_dup.own_distance >= min_distance]
    est_addr = df_dup[(df_dup.adr_distance >= min_distance) & (df_dup.adr_distance < 100)]
    own_count = float(len(est_own.groupby('OWN1_x').count()))
    addr_count = float(len(est_addr.groupby('OWN1_x').count()))
    return (own_count, addr_count)

def update(owner):
    owner = owner.union(row)

def update_alias(row):
    pass

def update_props(row):
    pass

def owner():
    """creates empty RDD dataframe for owner info
    """
    fields = [StructField("id", LongType()), StructField("name", StringType()),
              StructField("addr", StringType())]
    return sqlContext.createDataFrame(sc.emptyRDD(), StructType(fields))

def props():
    """creates empty RDD dataframe for owner properties info
    """
    fields = [StructField("id", LongType()), StructField("ownid", LongType()),
              StructField("parid", StringType()), StructField("addr", StringType()),
              StructField("date", DateType())]
    return sqlContext.createDataFrame(sc.emptyRDD(), StructType(fields))

def alias():
    """creates empty RDD dataframe for owner alias info
    """
    fields = [StructField("id", LongType()), StructField("name", StringType()),
              StructField("ownid", LongType())]
    return sqlContext.createDataFrame(sc.emptyRDD(), StructType(fields))

if __name__=='__main__':
    """
        host: db host name
        master: master connection string (eg. spark://master_ip:7077)
    """
    host, master = sys.argv[1:]
    conf.setMaster(master)
    host = sys.argv[1]
    params = utils.connection_properties(host, db='owner')
    url = 'postgresql://{host}:{port}/{db}'.format(**params)
    df = DataFrameReader(sqlContext).jdbc(url='jdbc:{}'.format(url),
                                            table='assessor.owndat', 
                                            properties=params,
                                            numPartitions=8)
    
    df = df.withColumn('adrconcat', concat_ws(' ',df.adrno, df.adrdir, 
        df.adrstr, df.adrsuf, df.cityname, df.statecode,df.zip1))

    func_clean_string = udf(clean_string, StringType())
    df = df.withColumn('own1', func_clean_string('own1'))
    df = df.withColumn('adrconcat', func_clean_string('adrconcat'))
    uniq_own = df.select(df.own1.alias('uniq_own')).distinct()
    
    df = df.withColumn('key', lit(0))
    uniq_own = uniq_own.withColumn('key', lit(0))

    a = df.select(df.own1, df.adrconcat, df.parid, df.key).sample(False, .0001, 42)
    b = uniq_own.select(uniq_own.uniq_own,uniq_own.key).sample(False, .0001, 42)
    c = a.join(b, a.key==b.key, 'outer')
    own_score = udf(match_score, DoubleType())
    c = c.withColumn('own_score', own_score('own1', 'uniq_own'))


