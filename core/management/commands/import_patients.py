import csv
from django.core.management.base import BaseCommand
from datetime import datetime
from core.models import Patient

class Command(BaseCommand):
    help = 'Import patients from CSV file'

    def handle(self, *args, **kwargs):
        csv_path = 'core/dataset/patients_dataset.csv'  # Update path if needed

        def to_int(value, default=0):
            try:
                return int(value)
            except (ValueError, TypeError):
                return default

        def to_float(value, default=0.0):
            try:
                return float(value)
            except (ValueError, TypeError):
                return default

        def parse_date(value):
            try:
                # your CSV format: "29-04-2025 14:37"
                return datetime.strptime(value, "%d-%m-%Y %H:%M")
            except (ValueError, TypeError):
                return None

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            headers = [h.strip() for h in reader.fieldnames]
            print("CSV headers detected:", headers)

            for row in reader:
                row = {k.strip(): v.strip() for k, v in row.items()}

                if not row.get('Name'):
                    continue

                try:
                    Patient.objects.create(
                        name=row.get('Name', ''),
                        age=to_int(row.get('Age')),
                        gender=row.get('Gender', ''),
                        contact=row.get('Contact', ''),
                        registered_at=parse_date(row.get('Registered_At')),
                        blood_pressure=row.get('BP', ''),
                        heart_rate=to_int(row.get('Heart_Rate')),
                        sugar_level=to_int(row.get('Sugar')),
                        temperature=to_float(row.get('Temp')),
                        risk_level=row.get('Risk', '')
                    )
                    self.stdout.write(self.style.SUCCESS(f"Imported {row.get('Name')}"))
                except Exception as e:
                    self.stderr.write(f"Error importing row {row}: {e}")
