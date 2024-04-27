def validate_file_extension(value):
    pass
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.zip', '.xlsx']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Extensão de arquivo não suportada. Escolha algum dos seguintes formatos: .pdf, .doc, .docx, .jpg, .png, .zip, .xlsx')