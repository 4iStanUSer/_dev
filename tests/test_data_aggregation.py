import os
from iap.data_processing.data_proc_manager import DataUploadManager
from iap.data_processing.data_loading import jj_aoc, jj_extract, jj_oc_data_proc
from iap.data_processing.data_loading.jj_aggr_map import DataAggregate


class TestDataAggregation:

    def setup_class(self):
        func_list = {'MyReport (Benadryl SI Other Accaunts)':
                         {'func': jj_aoc,
                          'meta_cols': ['Category', 'Segment', 'SubSegment',
                                        'Brand', 'SubBrand'],
                          'data_cols': 'N/A',
                          'dates_cols': {'N/A': 'N/A'}}
                     }
        # Rules for rows sum
        sum_rules = [
            {'Name': '%ACV', 'TimeScale': 'average', 'FactScale': 'sum'},
            {'Name': 'TDP', 'TimeScale': 'average', 'FactScale': 'average'},
            {'Name': '$', 'TimeScale': 'sum', 'FactScale': 'sum'},
            {'Name': 'Base $', 'TimeScale': 'sum', 'FactScale': 'sum'},
            {'Name': 'Units', 'TimeScale': 'sum', 'FactScale': 'sum'},
            {'Name': 'Base Units', 'TimeScale': 'sum', 'FactScale': 'sum'},
            {'Name': 'Price Decr $', 'TimeScale': 'sum', 'FactScale': 'sum'},
            {'Name': 'Price Decr Base $', 'TimeScale': 'sum',
             'FactScale': 'sum'},
            {'Name': 'Disp w/o Feat $', 'TimeScale': 'sum',
             'FactScale': 'sum'},
            {'Name': 'Disp w/o Feat Base $', 'TimeScale': 'sum',
             'FactScale': 'sum'},
            {'Name': 'Feat w/o Disp $', 'TimeScale': 'average',
             'FactScale': 'average'},
            {'Name': 'Feat w/o Disp Base $', 'TimeScale': 'average',
             'FactScale': 'average'},
            {'Name': 'Feat & Disp $', 'TimeScale': 'average',
             'FactScale': 'average'},
            {'Name': 'Feat & Disp Base $', 'TimeScale': 'average',
             'FactScale': 'average'},
            {'Name': 'Disp w/o Feat Units', 'TimeScale': 'average',
             'FactScale': 'average'},
            {'Name': 'Disp w/o Feat Base Units', 'TimeScale': 'average',
             'FactScale': 'average'},
            {'Name': 'Feat w/o Disp Units', 'TimeScale': 'average',
             'FactScale': 'average'},
            {'Name': 'Feat w/o Disp Base Units', 'TimeScale': 'average',
             'FactScale': 'average'},
            {'Name': 'Feat & Disp Units', 'TimeScale': 'average',
             'FactScale': 'average'},
            {'Name': 'Feat & Disp Base Units', 'TimeScale': 'average',
             'FactScale': 'average'},
            {'Name': 'Price Decr Units', 'TimeScale': 'average',
             'FactScale': 'average'},
            {'Name': 'Price Decr Base Units', 'TimeScale': 'average',
             'FactScale': 'average'}]

        map_rules = []
        map_sub_rule_1_1 = {'in': {'SubBrand': 'BENADRYL SI'},
                            'out': {'Category': 'TestCategory1'}}
        map_rules.append(map_sub_rule_1_1)
        map_sub_rule_1_2 = {'in': {'Brand': 'BENADRYL',
                                   'SubBrand': 'BENADRYL SI'},
                            'out': {'Brand': 'TestBrand1',
                                    'Segment': 'TestSegment1'}}
        map_rules.append(map_sub_rule_1_2)

        data_proc_path = os.path.dirname(os.path.abspath(__file__))
        path = (os.path.join(data_proc_path, 'test_inputs',
                             'MyReport (Benadryl SI Other Accaunts).xlsx'))
        upload_manager = DataUploadManager()
        output = upload_manager.process_files(path, func_list)
        self.data_aggr = DataAggregate(output, sum_rules, map_rules,
                                       dates_source='weekly',
                                       dates_target='monthly')
        # new_output = data_aggr.meta_map_by_rules()
        # new_output = data_aggr.sum_by_meta()

    def test_meta_map(self):
        self.data_aggr.meta_map_by_rules()

    def test_sum_by_meta(self):
        self.data_aggr.sum_by_meta()
