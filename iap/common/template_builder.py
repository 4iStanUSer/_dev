import os.path
import xlrd
import json
from types import *

def generate_templates(folder):
    infile = os.path.join(folder, 'templates.xlsx')
    with open(infile, 'rb') as file:
        wb = xlrd.open_workbook(file_contents=file.read())
        for sheet in wb.sheets():
            template = _generate_template(sheet)
            outfile = os.path.join(folder, sheet.name + '.json')
            with open(outfile, 'w') as outfile:
                json.dump(template, outfile, indent=4)
    return


def _generate_template(sheet):
    sections = _scan_sheet(sheet)

    template = dict()

    if 'storage' in sections:
        template['dev_storage'] = \
            _process_storage(sheet, sections['storage'])

    section_names = [
        'entities',
        'entities_variables',
        'project_properties',
        'timescale_properties',
        'entity_properties',
        'variable_properties',
        'decomposition_properties',
        'selector_properties',
        'view_properties',
        'factor_drivers',
        'wh_inputs',
        'timelines',
        'timelines_properties',
        'features',
        'user_data_access'
    ]

    for name in section_names:
        if name in sections:
            template[name] = \
                _process_section(sheet, sections[name])

    return template


def _scan_sheet(sheet):
    sections = dict()
    prev_section = ''
    for row_index in range(0, sheet.nrows):
        cell_val = sheet.cell(row_index, 0).value
        if cell_val != '':
            if prev_section != '':
                sections[prev_section]['end'] = row_index - 1
            header_len = 0
            j = 1
            while True:
                if j == sheet.ncols:
                    header_len = j
                    break
                if sheet.cell(row_index, j).value == '':
                    header_len = j
                    break
                j += 1
            sections[cell_val] = dict(
                start=row_index,
                end=0,
                header_len=header_len
            )
            prev_section = cell_val
    sections[prev_section]['end'] = sheet.nrows
    return sections


def _process_section(sheet, section):
    result = []
    if section['end'] - section['start'] > 1:
        header_row = sheet.row_slice(section['start'], 0,
                                     end_colx=section['header_len'])
        for i in range(section['start'] + 1, section['end']):
            result_row = dict()
            for j in range(1, len(header_row)):
                header_val = header_row[j].value
                cell_val = sheet.cell(i, j).value
                if type(header_val) == str and header_val[:4] == 'lang':

                    lang = header_val[5:7]
                    par_name = header_val[8:]
                    if 'languages' not in result_row:
                        result_row['languages'] = dict()
                    if lang not in result_row['languages']:
                        result_row['languages'][lang] = dict()
                    result_row['languages'][lang][par_name] = cell_val
                else:
                    key = header_val
                    if key in ["value"]:
                        cell_val = \
                            [x for x in cell_val.split('*-*') if x != '']
                    if key == 'address':
                        div_index = cell_val.find(':')
                        key = cell_val[:div_index]
                        cell_val = cell_val[div_index + 1:]
                    if type(cell_val) == unicode or type(cell_val)==str:
                        if '*-*' in cell_val:
                            cell_val = \
                                [x for x in cell_val.split('*-*')if x != '']
                    if type(cell_val)==float:
                        cell_val = str(int(cell_val))
                    result_row[key] = cell_val
            result.append(result_row)
    return result


def _process_storage(sheet, section):
    dev_storage = []
    if section['end'] - section['start'] > 1:
        header_row = sheet.row_slice(section['start'], 0,
                                     end_colx=section['header_len'])
        for i in range(section['start'] + 1, section['end']):
            result_row = dict()
            for j in range(1, 6):
                val = sheet.cell(i, j).value
                if type(val) == float:
                    val = str(int(val))
                if type(val) == str or type(val) == unicode:
                    if '*-*' in val:
                        val = [x for x in val.split('*-*') if x != '']
                result_row[header_row[j].value] = val
            result_row['values'] = []
            j = 7
            data_started = False
            while True:
                if j == sheet.ncols:
                    break
                if sheet.cell(i, j).value == '':
                    if data_started:
                        break
                else:
                    data_started = True
                    result_row['values'].append(sheet.cell(i, j).value)
                j += 1
            dev_storage.append(result_row)
    return dev_storage
