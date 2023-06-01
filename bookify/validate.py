from django.core.exceptions import ValidationError


def validate_file_size(file):
    max_kb_size = 300

    if file.size > max_kb_size * 100:
        raise ValidationError(f"Files cannot be larger than {max_kb_size}KB!")