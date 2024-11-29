from django.db import models
from django.core.validators import FileExtensionValidator
import uuid
from asgiref.sync import sync_to_async


class Bot_user(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.BigIntegerField(null=True)
    name = models.CharField(null=True, blank=True,
                            max_length=256, default='', verbose_name='Имя')
    username = models.CharField(
        null=True, blank=True, max_length=256, verbose_name='username')
    firstname = models.CharField(
        null=True, blank=True, max_length=256, verbose_name='Никнейм')
    phone = models.CharField(null=True, blank=True,
                             max_length=16, default='', verbose_name='Телефон')
    lang = models.CharField(null=True, blank=True,
                            max_length=4, default='uz', verbose_name='')
    date = models.DateTimeField(
        db_index=True, null=True, auto_now_add=True, blank=True, verbose_name='Дата регистрации')

    @property
    async def get_referral(self):
        obj = await Referral.objects.filter(bot_user__id=self.id).afirst()
        return obj

    def __str__(self) -> str:
        try:
            return self.name + ' ' + str(self.phone)
        except:
            return super().__str__()

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"


class Referral(models.Model):
    bot_user = models.OneToOneField(
        Bot_user, on_delete=models.PROTECT, verbose_name="Пользователь бота"
    )
    referrer = models.ForeignKey(
        Bot_user, related_name="referrall_referrer", on_delete=models.PROTECT, verbose_name="Реферер"
    )

    @property
    @sync_to_async
    def get_referrer(self):
        return self.referrer

    class Meta:
        verbose_name = "Рефераль"
        verbose_name_plural = "Рефералы"


class Message(models.Model):
    bot_users = models.ManyToManyField(
        'bot.Bot_user', blank=True, related_name='bot_users_list', verbose_name='Пользователи бота')
    text = models.TextField(null=True, blank=False,
                            max_length=1024, verbose_name='Текст')
    photo = models.FileField(null=True, blank=True, upload_to="message/photo/", verbose_name='Фото',
                             validators=[FileExtensionValidator(
                                 allowed_extensions=['jpg', 'jpeg', 'png', 'bmp', 'gif'])]
                             )
    video = models.FileField(
        null=True, blank=True, upload_to="message/video/", verbose_name='Видео',
        validators=[FileExtensionValidator(
            allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])]
    )
    file = models.FileField(null=True, blank=True,
                            upload_to="message/file/", verbose_name='Файл')
    is_sent = models.BooleanField(default=False)
    date = models.DateTimeField(
        db_index=True, null=True, auto_now_add=True, blank=True, verbose_name='Дата')

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Text(models.Model):
    hello = models.TextField(null=True, blank=True, verbose_name="Текст приветствия")
    start = models.TextField(null=True, blank=True, verbose_name="Старт")
    main_menu = models.TextField(
        null=True, blank=True, verbose_name="Главное меню")
    after_join_request = models.TextField(
        null=True, blank=True, verbose_name="После запроса на присоединение")
    joined_to_channel = models.TextField(
        null=True, blank=True, verbose_name="Успешное присоединение к каналу")
    given_bonus = models.TextField(
        null=True, blank=True, verbose_name="Вы получали бонус за привлечение рефералов")
    error_in_payment = models.TextField(
        null=True, blank=True, verbose_name="Ошибка при оплате")
    subscription_renewed = models.TextField(
        null=True, blank=True, verbose_name="Подписка продлена")
    banned = models.TextField(null=True, blank=True,
                              verbose_name="Вы заблокированы на канале")
    cannot_charge = models.TextField(
        null=True, blank=True, verbose_name="Не удается продлить подписку")

    class Meta:
        verbose_name = "Текст"
        verbose_name_plural = "Тексты"
