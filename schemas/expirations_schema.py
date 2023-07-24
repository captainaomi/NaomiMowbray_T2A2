from init import ma
from marshmallow import fields


class ExpirationsSchema(ma.Schema):
    pilot = fields.Nested('PilotSchema', only=['name'])
    medical = fields.Date(format='%Y-%m-%-d', required=True)
    biannual_review = fields.Date(format='%Y-%m-%-d', required=True)
    company_review = fields.Date(format='%Y-%m-%-d', required=True)
    dangerous_goods = fields.Date(format='%Y-%m-%-d', required=True)
    asic = fields.Date(format='%Y-%m-%-d')

    class Meta:
        fields = (
            'pilot',
            'id',
            'medical',
            'biannual_review',
            'company_review',
            'dangerous_goods',
            'asic'
            )
        ordered = True

expirations_schema = ExpirationsSchema()
expirationsz_schema = ExpirationsSchema(many=True)