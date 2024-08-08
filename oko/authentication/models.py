from django.contrib.auth.models import (
    AbstractUser, BaseUserManager
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext as _


USERNAME_MAX_LENGTN = 60
CHARFIELD_MAX_LENGTH = 150


class UserManager(BaseUserManager):
    """Расширение дефолтного менеджера пользователя."""
    def create_superuser(
        self, username, first_name, last_name, patronymic=None,
        email=None, password=None, **extra_fields
    ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not first_name:
            raise ValueError('Superuser должен иметь имя.')
        if not last_name:
            raise ValueError('Superuser должен иметь фамилию.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser должен иметь is_superuser=True.')

        return self._create_user(
            username, email, password,
            first_name, last_name, patronymic, **extra_fields
        )


class User(AbstractUser):
    """Расщирение дефолтной модели пользователя."""
    username = models.CharField(
        _('Логин'),
        max_length=USERNAME_MAX_LENGTN,
        unique=True,
        help_text=_(
            'Обязательное поле. '
            f'{USERNAME_MAX_LENGTN} символов или меньше. '
            'Только буквы, цифры и @/./+/-/_.'
        ),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _("Пользователь с данным логином уже существует."),
        },
    )
    first_name = models.CharField(_('Имя'), max_length=150)
    last_name = models.CharField(_('Фамилия'), max_length=150)
    patronymic = models.CharField(
        _('Отчество'),
        max_length=CHARFIELD_MAX_LENGTH,
        blank=True,
        help_text='Обязательно, если имеется.'
    )
    email = models.EmailField(_('Электронная почта'))
    is_staff = models.BooleanField(
        _('Доступность админки'),
        default=False,
        help_text=_(
            'Определяет, может ли пользователь войти в '
            'административную часть сайта.'
        ),
    )
    is_active = models.BooleanField(
        _('Признак активности.'),
        default=True,
        help_text=_(
            'Указывает на то, является ли пользователь активным. '
            'Отключите вместо удаления.'
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [  # Обязательно для createsuperuser
        'first_name', 'last_name', 'patronymic', 'email'
    ]

    class Meta:
        verbose_name = _('пользователя')
        verbose_name_plural = _('Пользователи')

    def get_full_name(self):
        """Возвращает ФИО пользователя."""
        if self.patronymic:
            return ('%s %s %s' % (
                self.first_name, self.last_name, self.patronymic
            )).strip()
        return super().get_full_name()

    def get_short_name(self):
        """Возвращает ИО пользователя."""
        if self.patronymic:
            return ('%s %s' % (self.first_name, self.last_name)).strip()
        return self.first_name

    def get_date_joined_display(self):
        return _('Дата создания учетной записи.')
