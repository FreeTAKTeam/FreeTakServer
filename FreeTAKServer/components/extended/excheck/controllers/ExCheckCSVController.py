"""
Filename: checklist.py
Author: Corvo
Date: 26 May 2023
python implementation of this S***T
- https://github.com/TAK-Product-Center/Server/blob/cbbaa66f88b9478262de60041eea586c199746c3/src/takserver-core/takserver-war/src/main/java/com/bbn/marti/excheck/ExCheckService.java#L37
- https://github.com/TAK-Product-Center/Server/blob/cbbaa66f88b9478262de60041eea586c199746c3/src/takserver-core/takserver-war/src/main/java/com/bbn/marti/excheck/checklist/excheck.xsd

Description: This script contains functions to manipulate 
a checklist data structure. It includes the following functions:
- parse_header_row(): Extracts columns from a CSV header row.
- parse_format_row(): Formats a row based on a specified format.
- copy_notes(): Copies any pre-seeded notes in the checklist into 
                the notes field of each task in the checklist, and 
                removes the original notes column if it exists.
These functions are designed to handle tasks related to checklist 
management, such as formatting rows, parsing headers, and copying 
task notes.

The script assumes that Checklist, ChecklistDetails, ChecklistColumns, 
ChecklistTasks, and ChecklistTask are domain classes.
"""

from FreeTAKServer.components.extended.echeck.domain.Checklist import Checklist
from FreeTAKServer.components.extended.echeck.domain.ChecklistDetails import ChecklistDetails
from FreeTAKServer.components.extended.echeck.domain.ChecklistColumns import ChecklistColumns
from FreeTAKServer.components.extended.echeck.domain.ChecklistTasks import ChecklistTasks
from FreeTAKServer.components.extended.echeck.domain.ChecklistTask import ChecklistTask
import uuid
import re

# A regular expression pattern to ignore commas within double quotes
CSV_IGNORE_COMMAS_IN_DOUBLEQUOTES = re.compile(r',(?=(?:(?:[^\"]*\"){2})*[^\"]*$)')

def parse_template(template_csv):
    checklist = Checklist()

    # assign a uid for the template
    checklist.checklist_details = ChecklistDetails()
    checklist.checklist_details.uid = uuid.uuid4()

    template_csv = template_csv.replace("\r", "")
    rows = template_csv.split("\n")
    if len(rows) < 3:
        return None

    # parse the labels from the header row
    header = parse_header_row(rows[0])

    # parse the format instructions, add them to the header row
    header = parse_format_row(rows[1], header)

    # create the ChecklistColumns and add them to the header
    checklist_columns = ChecklistColumns()
    checklist_columns.checklist_column.extend(header)
    checklist.checklist_columns = checklist_columns

    # parse the remainder of the rows
    checklist_tasks = ChecklistTasks()
    for i in range(2, len(rows)):
        if len(rows[i]) == 0:
            continue
        checklist_task = parse_checklist_task(rows[i], len(header))
        checklist_tasks.checklist_task.append(checklist_task)
    checklist.checklist_tasks = checklist_tasks

    checklist = copy_notes(checklist)

    return checklist
    
def parse_header_row(header):
    checklist_columns = []

    columns = header.split(CSV_IGNORE_COMMAS_IN_DOUBLEQUOTES)
    for ndx, column_name in enumerate(columns):
        if ndx == 0:
            continue

        col = ChecklistColumn()
        column_name = column_name.replace("\",\"", ",")
        col.column_name = column_name.strip()
        checklist_columns.append(col)

    return checklist_columns
    
def parse_format_row(format_row, header):
    
    format_cols = format_row.split(CSV_IGNORE_COMMAS_IN_DOUBLEQUOTES)
    format_cols.pop(0)

    if len(format_cols) != len(header):
        return None

    for ndx, next_format_col in enumerate(format_cols):
        next_col = header[ndx]
        for next_format_key_val in next_format_col.split("|"):
            format_key_val = next_format_key_val.split("=")
            if format_key_val[0].lower() == "type":
                next_col.column_type = ChecklistColumnType.from_value(format_key_val[1])
            elif format_key_val[0].lower() == "width":
                next_col.column_width = int(format_key_val[1])
            elif format_key_val[0].lower() == "bgcolor":
                next_col.column_bg_color = format_key_val[1]
            elif format_key_val[0].lower() == "textcolor":
                next_col.column_text_color = format_key_val[1]
            elif format_key_val[0].lower() == "editable":
                next_col.column_editable = bool(format_key_val[1])

    return header

def copy_notes(checklist):
    # did the user include a Notes column?
    notes_ndx = -1
    for i in range(len(checklist.checklist_columns.checklist_column)):
        if checklist.checklist_columns.checklist_column[i].column_name.lower() == "notes":
            notes_ndx = i
            break

    # bail if no notes to copy over
    if notes_ndx == -1:
        return checklist

    # remove notes column added by the user
    checklist.checklist_columns.checklist_column.pop(notes_ndx)

    # iterate over the tasks, copying any preseeded notes into the notes field
    for task in checklist.checklist_tasks.checklist_task:
        notes = task.value[notes_ndx]
        if notes and len(notes) > 0:
            task.notes = notes

        # remove the notes column added by the user
        task.value.pop(notes_ndx)

    return checklist
