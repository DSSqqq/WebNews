from django.apps import AppConfig
#from .tasks import start_scheduler больше не нужен, убираем его

class NewsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsapp'

    def ready(self):
        import newsapp.signals
        from .tasks import setup_periodic_tasks
        setup_periodic_tasks()
        # start_scheduler() больше не нужен, убираем его