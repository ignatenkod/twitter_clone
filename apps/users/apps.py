from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Конфигурация приложения пользователей"""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    verbose_name = 'Пользователи'

    def ready(self):
        """Инициализация приложения"""
        # Импортируем сигналы, чтобы они зарегистрировались
        import apps.users.signals
