from marshmallow import Schema, fields, pprint, validate, validates_schema, pre_load

#預設的錯誤訊息
# ma.Field.default_error_messages["required"] = "boom!"
fields.Field.default_error_messages['validator_failed'] = '錯誤'


class AppError(Exception):
    pass

class ShortUrlSchema(Schema):
    url = fields.Url(required=True, error_messages={
        'required':'請輸入URL',
        'invalid':'您輸入錯誤的URL'
    })
    # error_messages = {
    #     "unknown": "Custom unknown field error message.",
    #     "type": "Custom invalid type error message.",
    #     "url": "Custom invalid type error message."
    # }
    # def validate_url(self, url):
    #     self.error = 'error'


    # url = fields.Str(required=True, validate=validate_url, error_messages={
    #     'required':'請填入URL'
    # })

    # @pre_load
    # def unwrap_envelope(self, data, **kwargs):
    #     if "data" not in data:
    #         raise ValidationError(
    #             'Input data must have a "data" key.', "_preprocessing"
    #         )
    #     return data

    # def handle_error(self, exc, data, **kwargs):
    #     """Log and raise our custom exception when (de)serialization fails."""
    #     return exc

