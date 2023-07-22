from init import ma
from marshmallow import fields


class ExpirationsSchema(ma.Schema):
    pilot = fields.Nested('PilotSchema', only=['id', 'arn', 'name'])

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