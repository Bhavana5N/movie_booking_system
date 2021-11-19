from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(selfself, user, timestamp):
        return (six.text_type(user.username)+six.text_type(timestamp)+six.text_type(user.is_active))

generate_token=TokenGenerator( )