from django.core.management.base import BaseCommand
from main.management.commands.feed_train_data import feed_data
import threading

class Command(BaseCommand):
    help = 'Starts feeding data to the server'

    def handle(self, *args, **kwargs):
        script_thread = threading.Thread(target=feed_data)
        script_thread.start()
        self.stdout.write(self.style.SUCCESS('Started the feeding data script'))