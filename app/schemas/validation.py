from pydantic import BaseModel, field_validator


class FileValidationModel(BaseModel):
    filename: str
    size: int
    available_memory: int
    needed_memory: int

    @field_validator('filename')
    def check_format(cls, v):
        if not v.endswith('.csv'):
            raise ValueError('Invalid file format. Please upload a CSV file.')
        return v

    @field_validator('size')
    def check_size(cls, v):
        if v > 20 * 1024 * 1024:  # 20MB limit
            raise ValueError('File size exceeds the limit of 20MB.')
        return v

    @field_validator('available_memory', 'needed_memory')
    def check_memory(cls, v, info):
        data = info.data
        if data.get('available_memory') is not None and data.get('needed_memory') is not None:
            if data['available_memory'] < data['needed_memory']:
                raise ValueError('Insufficient memory to process the file.')
        return v
