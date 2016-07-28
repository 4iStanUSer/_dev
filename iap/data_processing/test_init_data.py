import os
from IAP.data_processing.data_proc_manager import DataUploadManager
from IAP.data_processing.processors import jj_aoc, jj_extract 
from IAP.data_processing.processors.jj_aggr_map import DataAggregate

def test_processing_data():
    func_list = {'MyReport (Benadryl SI Other Accaunts)': 
                        {'func': jj_aoc,
                         'meta_cols': ['Category', 'Segment', 'SubSegment',
                                       'Brand', 'SubBrand'],
                         'data_cols': 'N/A',
                         'dates_cols': {'N/A': 'N/A'}},
                 'JNJ_SALES_EXTRACT_FOR_4I_201603':  
                        {'func': jj_extract, 
                         'meta_cols': {3: 'LVL1', 5: 'LVL2', 6: ''},
                         'data_cols': {8: 'A', 10: 'B', 11: 'C', 12: 'D'},
                         'dates_cols': {0: 'campaign'}}
                 }
    # Rules for rows sum
    sum_rules_file1 = [{'Name':'%ACV', 'TimeScale': 'average', 'FactScale': 'sum'},
                       {'Name':'TDP', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'$', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'Base $', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'Units', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'Base Units', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'Price Decr $', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'Price Decr Base $', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'Disp w/o Feat $', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'Disp w/o Feat Base $', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'Feat w/o Disp $', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Feat w/o Disp Base $', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Feat & Disp $', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Feat & Disp Base $', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Disp w/o Feat Units', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Disp w/o Feat Base Units', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Feat w/o Disp Units', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Feat w/o Disp Base Units', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Feat & Disp Units', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Feat & Disp Base Units', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Price Decr Units', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Price Decr Base Units', 'TimeScale': 'average', 'FactScale': 'average'}]
    sum_rules_file2 = [{'Name':'A', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'B', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'C', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'D', 'TimeScale': 'sum', 'FactScale': 'sum'}]
    sum_rules=[]
    sum_rules.append(sum_rules_file1)
    sum_rules.append(sum_rules_file2)

    map_rules = []
    map_rules1 = []
    map_sub_rule_1_1 = {'in': {'SubBrand': 'BENADRYL SI'},
                    'out': {'Category': 'TestCategory1'}}
    map_rules1.append(map_sub_rule_1_1)
    map_sub_rule_1_2 = {'in': {'Brand': 'BENADRYL',
                               'SubBrand': 'BENADRYL SI'},
                    'out': {'Brand': 'TestBrand1',
                            'Segment': 'TestSegment1'}}
    map_rules1.append(map_sub_rule_1_2)
    map_rules2 = []
    map_sub_rule_2_1 = {'in': {'LVL1': 'DRUG CHANNEL',
                               'LVL2': 'RITE AID'},
                        'out': {'LVL1': 'Ecomm'}}
    map_rules2.append(map_sub_rule_2_1)
    map_rules.append(map_rules1)
    map_rules.append(map_rules2)

    data_proc_path = os.path.dirname(os.path.abspath(__file__))
    paths = []
    paths.append(os.path.join(data_proc_path, 'test_inputs', 
                              'MyReport (Benadryl SI Other Accaunts).xlsx'))
    paths.append(os.path.join(data_proc_path, 'test_inputs', 
                              'JNJ_SALES_EXTRACT_FOR_4I_201603.xlsx'))
    upload_manager = DataUploadManager()
    for idx, val in enumerate(paths):
        output = upload_manager.process_files(val, func_list)
        data_aggr = DataAggregate(output, sum_rules[idx], map_rules[idx], 
                                  dates_source='weekly', dates_target='monthly')
        new_output = data_aggr.meta_map_by_rules()
        new_output = data_aggr.sum_by_meta()
        print (output[0])