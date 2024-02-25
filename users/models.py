from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.utils.translation import gettext_lazy as _
import re
from users import utils
from django.contrib.auth.hashers import make_password



class User(AbstractUser):
    email = models.EmailField(
        _('Correo Electrónico'),
        validators=[validators.validate_email],
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text=_('Date time on which the object was created')

    )
    type = models.CharField(max_length=15, choices=utils.Type, default=utils.STUDENT)
    modified = models.DateTimeField(
        _('created at'),
        auto_now=True,
        help_text=_('Date time on which the object was last modified')
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    @classmethod
    def generate_unique_username(cls, email: str) -> str:
        local_part = email.split('@')[0]
        username_base = re.sub(r'\W+', '', local_part).lower()
        username = username_base
        count = 1
        while User.objects.filter(username=username).exists():
            username = f"{username_base}_{count}"
            count += 1
        return username

    def create_reset_token(self):  # noqa
        payload = {
            'user_id': self.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=settings.PASSWORD_RESET_EXPIRE_DAYS),
            'iat': datetime.datetime.utcnow(),
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    def send_password_reset_email(self):
        if self.is_active:

            domain = Site.objects.get_current().domain
            reset_token = self.create_reset_token()

            activation_link = f"{domain}/account/password-reset-confirm/?reset_token={reset_token}"
            subject = _("Restablecer Contraseña")
            html_message = render_to_string('emails/reset_password.html', {
                'first_name': self.first_name,
                'activation_link': activation_link
            })
            send_mail(
                subject, '',
                settings.DEFAULT_FROM_EMAIL,
                [self.email],
                fail_silently=False,
                html_message=html_message)
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.type = 'ADMINISTRATOR'
        if self.type == 'ADMINISTRATOR':
            self.is_superuser = True
        self.is_active = True
        self.username = self.generate_unique_username(self.email)
        self.password = make_password(self.password)
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")
        get_latest_by = 'created'
        ordering = ['-created', '-modified']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class CodeRecoverPassword(models.Model):
    code = models.IntegerField(verbose_name=_(
        'Codigo de seguridad'), null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_created=True)
    expiration = models.DateTimeField(verbose_name=_(
        'tiempo de valido  del codigo'), null=False)

    class Meta:
        verbose_name = _('Codigo de seguridad restablecimiento de contraseña')
        verbose_name_plural = _(
            'Codigos de seguridad restablecimiento de contraseñas')
