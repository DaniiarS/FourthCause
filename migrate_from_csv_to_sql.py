import csv
from myapp.models import Card
from myapp import app, db
import os


app.app_context().push()
db.create_all()

cwd = os.getcwd() + "/myapp/database"
files = os.listdir(cwd)
print(files)

for file in files:
    file_name, extension = os.path.splitext(file)
    with open(f"myapp/database/{file}", "r") as file:
        csv_db = csv.reader(file)

        for row in csv_db:
            category = row[-1]
            if category == "pdf":
                category = "book"

            title = row[0]
            image_file = row[1]
            description = row[2]
            language = row[3]
            source = row[4]
            link = row[5]

            card = Card(category=category, field=file_name, title=title, image_file=image_file, description=description,language=language, source=source, link=link)

            db.session.add(card)
            db.session.commit()