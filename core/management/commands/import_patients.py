import csv
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from core.models import Patient

class Command(BaseCommand):
    help = 'Import patients from CSV file (clears old data first)'

    def handle(self, *args, **kwargs):
        csv_path = 'core/dataset/patients_dataset.csv'

        # Delete old data
        deleted_count, _ = Patient.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {deleted_count} old patient records.'))

        # Import new data
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            new_count = 0

            for row in reader:
                try:
                    # Clean whitespace
                    row = {k.strip(): v.strip() for k, v in row.items()}

                    # Parse registered_at properly (format: DD-MM-YYYY HH:MM)
                    registered_at = parse_datetime(
                        "-".join(row['Registered_At'].split(" ")[0].split("-")[::-1]) + 
                        " " + row['Registered_At'].split(" ")[1]
                    )

                    # Create patient
                    patient = Patient(
                        id=row['ID'],
                        name=row['Name'],
                        age=int(row['Age']),
                        gender=row['Gender'],
                        contact=row['Contact'] or None,
                        registered_at=registered_at,
                        blood_pressure=row['BP'] or None,
                        heart_rate=int(row['Heart_Rate']) if row['Heart_Rate'] else None,
                        sugar_level=float(row['Sugar']) if row['Sugar'] else None,
                        temperature=float(row['Temp']) if row['Temp'] else None,
                    )

                    patient.save()  # risk_level auto-calculated

                    new_count += 1

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error importing row {row}: {e}"))

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {new_count} new patients.'))
