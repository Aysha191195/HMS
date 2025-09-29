import csv
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from core.models import Patient

class Command(BaseCommand):
    help = 'Import patients from CSV file'

    def handle(self, *args, **kwargs):
        csv_path = 'core/dataset/patients_dataset.csv'  # Update path if needed

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            headers = [h.strip() for h in reader.fieldnames]  # strip spaces from headers
            print("CSV headers detected:", headers)

            for row in reader:
                # Strip spaces from row keys and values
                row = {k.strip(): v.strip() for k, v in row.items()}

                # Optional: skip empty rows
                if not row.get('Name'):
                    continue

                try:
                    Patient.objects.create(
                        name=row.get('Name', ''),
                        age=row.get('Age', 0),
                        gender=row.get('Gender', ''),
                        contact=row.get('Contact', ''),
                        registered_at=parse_datetime(row.get('Registered At', '')),
                        blood_pressure=row.get('BP', ''),
                        heart_rate=row.get('Heart Rate', ''),
                        sugar_level=row.get('Sugar', ''),
                        temperature=row.get('Temp', ''),
                        risk_level=row.get('Risk', '')
                    )
                    self.stdout.write(self.style.SUCCESS(f"Imported {row.get('Name')}"))
                except Exception as e:
                    self.stderr.write(f"Error importing row {row}: {e}")
