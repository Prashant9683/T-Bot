from django.core.management.base import BaseCommand
from main_app.telegram_bot import run_telegram_bot

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Telegram bot...'))
        try:
            run_telegram_bot()
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('Telegram bot stopped.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error running Telegram bot: {str(e)}'))
