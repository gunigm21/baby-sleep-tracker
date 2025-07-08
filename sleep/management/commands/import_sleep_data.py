import json
from datetime import datetime
from django.core.management.base import BaseCommand
from sleep.models import SleepSession

class Command(BaseCommand):
    help = 'Импорт данных сна из файла baby.json'

    def handle(self, *args, **kwargs):
        try:
            with open("baby.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("Файл baby.json не найден."))
            return

        records = data.get("records", [])
        sleep_records = [r for r in records if r.get("type") == "SLEEPING"]

        count = 0
        for record in sleep_records:
            try:
                start = datetime.strptime(record["fromDate"], "%Y-%m-%d %H:%M:%S")
                end = datetime.strptime(record["toDate"], "%Y-%m-%d %H:%M:%S")
                note = record.get("details", "")

                SleepSession.objects.create(start_time=start, end_time=end, note=note)
                count += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Ошибка в записи: {record} — {e}"))

        self.stdout.write(self.style.SUCCESS(f"Импортировано {count} записей сна."))
