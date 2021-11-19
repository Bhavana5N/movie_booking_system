from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(selfself, customuser, timestamp):
        return (six.text_type(customuser.email)+six.text_type(timestamp)+six.text_type(customuser.is_active))

generate_token=TokenGenerator( )