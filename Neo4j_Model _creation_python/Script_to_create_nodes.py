# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 17:52:30 2019

@author: Mohammad.Tappa
"""

from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config

config.DATABASE_URL = 'bolt://neo4j:1234@localhost:7687'

import pandas as pd

sales_data = pd.read_csv("D:\Assignment\sample_brand_dataset.csv")
address_dict = {}
brand_group_dict = {}

class Address(StructuredNode):
    name = StringProperty(unique_index=True)
    address_code = StringProperty(unique_index=True)
    brands = RelationshipFrom('Brand', 'Brand Location')

class Brand(StructuredNode):
    unique_key = StringProperty(unique_index=True)
    name = StringProperty(unique_index=True)
    brand_parent = RelationshipTo('BrandParent', 'Brand Parent Group')
    address = RelationshipTo('Address', 'Brand Location')
    
class BrandParent(StructuredNode):
    name = StringProperty(unique_index=True)
    brands = RelationshipFrom('Brand', 'Brand Parent Group')

for index, row in sales_data.iterrows():
    b_group = None
    address_name = None
    brand_node = Brand(unique_key=row['Unique Key'], name = row['Brand Name']).save()
    grp_name = row['Brand Parent Group']
    adr_name = row['Address']
    if grp_name not in brand_group_dict.keys():        
        b_group =  BrandParent(name=grp_name).save()
        brand_group_dict[grp_name] = b_group
    else:
        b_group = brand_group_dict[grp_name]
        
    if adr_name not in address_dict.keys():        
        adr_code = row['Address Code']
        address_name = Address(name = adr_name,address_code=adr_code).save()
        address_dict[adr_name] = address_name
    else:
        address_name = address_dict[adr_name]
    brand_node.brand_parent.connect(b_group)
    brand_node.address.connect(address_name)