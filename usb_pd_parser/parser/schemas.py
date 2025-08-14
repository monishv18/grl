from jsonschema import validate

TOC_SCHEMA = {
    "type": "object",
    "properties": {
        "doc_title": {"type": "string"},
        "section_id": {"type": "string"},
        "title": {"type": "string"},
        "page": {"type": "integer"},
        "level": {"type": "integer"},
        "parent_id": {"type": ["string", "null"]},
        "full_path": {"type": "string"},
        "tags": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["doc_title", "section_id", "title", "page", "level", "parent_id", "full_path"]
}

SECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "doc_title": {"type": "string"},
        "section_id": {"type": "string"},
        "title": {"type": "string"},
        "page": {"type": "integer"},
        "level": {"type": "integer"},
        "parent_id": {"type": ["string", "null"]},
        "full_path": {"type": "string"},
        "content": {"type": "string"},
        "tags": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["doc_title", "section_id", "title", "page", "level", "parent_id", "full_path", "content"]
}

def validate_toc_entry(entry):
    validate(instance=entry, schema=TOC_SCHEMA)

def validate_section_entry(entry):
    validate(instance=entry, schema=SECTION_SCHEMA)
