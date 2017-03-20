from .jj_aoc import jj_aoc
from .jj_brand_db_interface import jj_brand, jj_brand_extract, \
    jj_brand_media_spend
from .jj_oral_care_db_interface import jj_oral_care_sku, \
    jj_oral_care_media_spend, jj_oral_care_rgm_sales
from .jj_extract import jj_extract
from .jj_oc_data_proc import jj_oc_data_proc
from .common import week_to_month
from .common import date_monthly_excel_number
from .common import date_jj_1week

from .jj_lean import (
    jj_lean_init,
    jj_lean_media_spend,
    jj_lean_nielsen,
    jj_lean_aggr_weeks
)
from .jj_oral_care import (
    jj_oral_care_init,
    loader,
    jj_oral_care_sales,
    jj_oral_care_trends
)


def process(config, dfs):

    state = dfs[2].rename(columns={'Postal Code': 'zip_code'})
    result = dfs[0].merge(state, how='left', on=['zip_code'])
    return result