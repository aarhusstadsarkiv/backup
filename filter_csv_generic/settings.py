import id_field_ops
import id_field_list_ops
import date_field_ops
import string_ops
import dict_field_ops
import string_list_ops

OPERATORS_ID_FIELD: dict = {
    "equalTo": id_field_ops.equal_to,
    "notEqualTo": id_field_ops.not_equal_to,
    "greaterThan": id_field_ops.greater_than,
    "lessThan": id_field_ops.less_than,
    "contains": id_field_ops.id_field_contains,
    "regex": id_field_ops.regex
}
OPERATORS_ID_FIELD_LIST: dict = {
    "equalTo": id_field_list_ops.equal_to,
    "greaterThan": id_field_list_ops.greater_than,
    "lessThan": id_field_list_ops.less_than,
    "contains": id_field_list_ops.id_field_list_contains,
    "regex": id_field_list_ops.regex
}
OPERATORS_DATE_FIELD: dict = {
    "equalTo": date_field_ops.equal_to,
    "greaterThan": date_field_ops.greater_than,
    "lessThan": date_field_ops.less_than,
    "regex": date_field_ops.regex
}
OPERATORS_STRING_FIELD: dict = {
    "equalTo": string_ops.equal_to,
    "contains": string_ops.contains,
    "regex": string_ops.regex
}
OPERATORS_DICT_FIELD: dict = {
    "hasKey": dict_field_ops.hasKey,
    "contains": dict_field_ops.contains,
    "regex": dict_field_ops.regex
}
OPERATORS_STRING_FIELD_LIST: dict = {
    "contains": string_list_ops.contains,
    "equalTo": string_list_ops.equal_to,
    "regex": string_list_ops.regex
}

FIELDS: dict = {
    "collection": OPERATORS_ID_FIELD,
    "curators": OPERATORS_ID_FIELD_LIST,
    "desc_notes": OPERATORS_STRING_FIELD,
    "date_from": OPERATORS_DATE_FIELD,
    "reg_id": OPERATORS_DATE_FIELD,
    "desc_data": OPERATORS_DICT_FIELD,
    "admin_data": OPERATORS_DICT_FIELD,
    "series": OPERATORS_STRING_FIELD,
    "locations": OPERATORS_ID_FIELD_LIST,
    "header": OPERATORS_STRING_FIELD,
    "related_content": OPERATORS_ID_FIELD,
    "availability": OPERATORS_ID_FIELD,
    "contractual_status": OPERATORS_ID_FIELD,
    "creative_creators": OPERATORS_ID_FIELD_LIST,
    "deployed_by": OPERATORS_STRING_FIELD,
    "created_by": OPERATORS_STRING_FIELD,
    "subjects:": OPERATORS_ID_FIELD_LIST,
    "storage_id": OPERATORS_STRING_FIELD_LIST,
    "schema": OPERATORS_STRING_FIELD,
    "copyright_status": OPERATORS_ID_FIELD,
    "other_restrictions": OPERATORS_ID_FIELD,
    "barcode": OPERATORS_STRING_FIELD_LIST,
    "content_type": OPERATORS_ID_FIELD_LIST,
    "date_to": OPERATORS_DATE_FIELD,
    "identifier": OPERATORS_DATE_FIELD,
    "creators": OPERATORS_ID_FIELD_LIST,
    "created_ts": OPERATORS_DATE_FIELD,
    "deployed_ts": OPERATORS_DATE_FIELD,
    "abstract": OPERATORS_STRING_FIELD,
    "physical_format": OPERATORS_DICT_FIELD,
    "original_id": OPERATORS_STRING_FIELD,
    "collection_tags": OPERATORS_STRING_FIELD_LIST,
    "organisations": OPERATORS_ID_FIELD_LIST,
    "people": OPERATORS_ID_FIELD_LIST,
    "admin_notes": OPERATORS_STRING_FIELD,
    "events": OPERATORS_STRING_FIELD_LIST,
    "rights_notes": OPERATORS_STRING_FIELD,
    "digital_size": OPERATORS_STRING_FIELD,
    "filename": OPERATORS_STRING_FIELD,
    "checksum_algorithm": OPERATORS_STRING_FIELD,
    "thumbnail": OPERATORS_STRING_FIELD,
    "last_checksum_date": OPERATORS_DATE_FIELD,
    "mimetype": OPERATORS_STRING_FIELD,
    "checksum": OPERATORS_STRING_FIELD,
    "representation_elements": OPERATORS_DICT_FIELD,
    "original_filename": OPERATORS_STRING_FIELD,
    "admin_tags": OPERATORS_STRING_FIELD_LIST,
    "private_data": OPERATORS_STRING_FIELD,
    "title": OPERATORS_STRING_FIELD,
    "format_type": OPERATORS_ID_FIELD,
}
