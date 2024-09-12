from users.models import UserPaymentMethod
from ..serializers.payment import UserPaymentMethodSerializer
import secrets

class PaymentService:

    @staticmethod
    def generate_token():
        """
        Generates a cryptographically secure token.
        """
        return secrets.token_hex(8)  # Generates a 16-character hexadecimal token

    @staticmethod
    def add_payment_method(user_id, method_id, last_four_digits, expiration_date):
        """
        Adds a payment method for a user.
        """
        try:
            # Generate token
            token = PaymentService.generate_token()

            # Create and save the payment method
            payment_method = UserPaymentMethod.objects.create(
                user_id=user_id,
                method_id=method_id,
                token=token,
                last_four_digits=last_four_digits,
                expiration_date=expiration_date
            )
            serializer = UserPaymentMethodSerializer(payment_method)
            return serializer.data
        except Exception as e:
            raise e
