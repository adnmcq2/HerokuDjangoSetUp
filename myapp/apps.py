from django.apps import AppConfig
from django.db.models.signals import pre_save


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'
    label = 'myapp'

    def ready(self):
        # importing model classes
        # from .models import MyModel  # or...
        # MyModel = self.get_model('MyModel')

        # MyTransaction = self.get_model('MyTransaction')

        # registering signals with the model's string label
        # pre_save.connect(receiver, sender='app_label.MyModel')

        import myapp.signals # noqa
