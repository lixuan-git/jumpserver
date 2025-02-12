# -*- coding: utf-8 -*-
#

from smtplib import SMTPSenderRefused
from rest_framework.views import Response, APIView
from django.core.mail import send_mail, get_connection
from django.utils.translation import ugettext_lazy as _

from common.permissions import IsSuperUser
from common.utils import get_logger
from .. import serializers

logger = get_logger(__file__)

__all__ = ['MailTestingAPI']


class MailTestingAPI(APIView):
    permission_classes = (IsSuperUser,)
    serializer_class = serializers.MailTestSerializer
    success_message = _("Test mail sent to {}, please check")

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email_host = serializer.validated_data['EMAIL_HOST']
        email_port = serializer.validated_data['EMAIL_PORT']
        email_host_user = serializer.validated_data["EMAIL_HOST_USER"]
        email_host_password = serializer.validated_data['EMAIL_HOST_PASSWORD']
        email_from = serializer.validated_data["EMAIL_FROM"]
        email_recipient = serializer.validated_data["EMAIL_RECIPIENT"]
        email_use_ssl = serializer.validated_data['EMAIL_USE_SSL']
        email_use_tls = serializer.validated_data['EMAIL_USE_TLS']

        # 设置 settings 的值，会导致动态配置在当前进程失效
        # for k, v in serializer.validated_data.items():
        #     if k.startswith('EMAIL'):
        #         setattr(settings, k, v)
        try:
            subject = "Test"
            message = "Test smtp setting"
            email_from = email_from or email_host_user
            email_recipient = email_recipient or email_from
            connection = get_connection(
                host=email_host, port=email_port,
                username=email_host_user, password=email_host_password,
                use_tls=email_use_tls, use_ssl=email_use_ssl,
            )
            send_mail(
                subject, message, email_from, [email_recipient],
                connection=connection
            )
        except SMTPSenderRefused as e:
            error = e.smtp_error
            if isinstance(error, bytes):
                for coding in ('gbk', 'utf8'):
                    try:
                        error = error.decode(coding)
                    except UnicodeDecodeError:
                        continue
                    else:
                        break
            return Response({"error": str(error)}, status=400)
        except Exception as e:
            logger.error(e)
            return Response({"error": str(e)}, status=400)
        return Response({"msg": self.success_message.format(email_recipient)})