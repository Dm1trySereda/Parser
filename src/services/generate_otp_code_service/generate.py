import base64
import hashlib
import io

import pyotp
import qrcode
from pydantic import EmailStr

from src.response_schemas.users import OneTimePassword
from src.services.generate_otp_code_service.abc import AbstractGenerateOTPCodeService


class GenerateOTPCodeService(AbstractGenerateOTPCodeService):

    async def generate_qrcode(self, recipient_email: EmailStr) -> OneTimePassword:
        hash_object = hashlib.sha256(recipient_email.encode())
        hex_dig = hash_object.hexdigest()
        user_secret = base64.b32encode(hex_dig.encode()).decode()
        totp = pyotp.TOTP(user_secret)
        code = totp.now()
        url = totp.provisioning_uri(name=recipient_email, issuer_name="OZBooks")
        qr_code = qrcode.make(url)
        buffered = io.BytesIO()
        qr_code.save(buffered)
        qr_code_str = base64.b64encode(buffered.getvalue()).decode()
        return OneTimePassword(
            user_email=recipient_email,
            user_secret=user_secret,
            qrcode=qr_code_str,
            otp_code=code,
        )
