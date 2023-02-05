from marshmallow import Schema, fields, validates, ValidationError, validate
from marshmallow.validate import Length
from backend.user.user_model import User

class CreateUserSchema(Schema):

    firstname = fields.Str(required=True, validate=Length(max=100, min=3))
    lastname = fields.Str(required=True, validate=Length(max=100, min=3))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=Length(max=100))
    privilege = fields.Str(required=True, validate=validate.OneOf(["User", "Admin"]))

    @validates("email")
    def validate_email(self, email):
        """________________________validate email___________________________"""
        user = User.query.filter(User.email==email).all()
        if user:
            raise ValidationError("This email is already used !")

class UpdateUserSchema(Schema):
    firstname = fields.Str(required=True, validate=Length(max=100, min=3))
    lastname = fields.Str(required=True, validate=Length(max=100, min=3))
    privilege = fields.Str(required=True, validate=validate.OneOf(["User", "Admin"]))

class UpdateUserPasswordSchema(Schema):
    current_password = fields.Str(required=True, validate=Length(max=100))
    new_password = fields.Str(required=True, validate=Length(max=100))

create_user_validator = CreateUserSchema()
update_user_validator = UpdateUserSchema()
update_user_password_validator = UpdateUserPasswordSchema()