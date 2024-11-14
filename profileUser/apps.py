from django.apps import AppConfig


    

class ProfileuserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "profileUser"
    def ready(self):
        import profileUser.signals  # Đăng ký tín hiệu