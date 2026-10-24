from django.db import migrations

EXTRA_BOOKS = [
    dict(title="Чотири шаблі", author="Юрій Яновський", catalog_index="821.161.2 Я64-2",
         genre="Роман", year="1930", pages_total=210, rating=4, shelf_label="розстріляне відродження",
         summary=("Роман про чотирьох побратимів-повстанців часів громадянської війни, "
                   "їхню дружбу, кохання і боротьбу за нову Україну. Романтизований, "
                   "поетичний стиль оспівує революційну героїку 1920-х років.")),
    dict(title="Чайковський", author="Євген Гребінка", catalog_index="821.161.2 Г75",
         genre="Повість", year="1843", pages_total=100, rating=3, shelf_label="класика",
         summary=("Історична повість про козака Чайковського, який після зради коханої "
                   "стає ватажком розбійників, месником за особисту і соціальну "
                   "несправедливість на Поділлі XVIII століття.")),
    dict(title="Ворскло", author="Яків Щоголів", catalog_index="821.161.2 Щ33",
         genre="Збірка поезій", year="1883", pages_total=90, rating=3, shelf_label="поезія",
         summary=("Збірка ліричних поезій, названа на честь річки Ворскло, у якій автор "
                   "оспівує красу рідної природи та тишу степового пейзажу в мелодійних, "
                   "музичних віршах.")),
    dict(title="Товаришки", author="Олена Пчілка", catalog_index="821.161.2 П92",
         genre="Оповідання", year="кінець ХІХ ст.", pages_total=40, rating=3, shelf_label="проза",
         summary=("Оповідання про дружбу двох дівчат з різних соціальних станів, які "
                   "попри відмінності у вихованні й статках залишаються вірними одна одній "
                   "у складних життєвих випробуваннях.")),
    dict(title="Ліричні поезії", author="Микола Вороний", catalog_index="821.161.2 В75",
         genre="Збірка поезій", year="1911", pages_total=100, rating=3, shelf_label="поезія",
         summary=("Збірка віршів про красу природи, кохання й тривоги доби, у якій автор "
                   "поєднує імпресіоністичну образність із глибоким ліризмом.")),
    dict(title="З журбою радість обнялася", author="Олександр Олесь",
         catalog_index="821.161.2 О-52", genre="Збірка поезій", year="1907", pages_total=110,
         rating=4, shelf_label="поезія",
         summary=("Перша й найвідоміша збірка поезій, у якій легкий, музичний вірш "
                   "поєднує смуток і надію, ставши взірцем українського символізму "
                   "початку ХХ століття.")),
    dict(title="По ревізії", author="Марко Кропивницький", catalog_index="821.161.2 К83-3",
         genre="Комедія", year="1882", pages_total=60, rating=3, shelf_label="драматургія",
         summary=("Комедія про сільського старосту, який перед приїздом ревізора "
                   "намагається приховати свої зловживання, потрапляючи у кумедні й "
                   "викривальні ситуації.")),
    dict(title="Наймичка", author="Іван Карпенко-Карий", catalog_index="821.161.2 К26-4",
         genre="Драма", year="1885", pages_total=70, rating=4, shelf_label="драматургія",
         summary=("Драма про наймичку Харитину, яка потайки народжує дитину від пана і "
                   "мусить віддати її на виховання чужим людям, приховуючи материнську "
                   "таємницю все життя.")),
    dict(title="Талан", author="Михайло Старицький", catalog_index="821.161.2 С77-3",
         genre="Драма", year="1893", pages_total=80, rating=3, shelf_label="драматургія",
         summary=("Драма про долю талановитої актриси, яка заради сцени і мистецтва "
                   "жертвує особистим щастям, зрештою залишаючись самотньою й забутою.")),
    dict(title="Люба-згуба", author="Юрій Федькович", catalog_index="821.161.2 Ф42-2",
         genre="Повість", year="1870-ті", pages_total=70, rating=3, shelf_label="проза",
         summary=("Повість про трагічне кохання, зруйноване суспільними забобонами й "
                   "родинними чварами, витримана у ліричному, сповненому суму стилі "
                   "буковинського письменника.")),
]


def add_books(apps, schema_editor):
    Book = apps.get_model('library', 'Book')
    start_order = Book.objects.count()
    for i, data in enumerate(EXTRA_BOOKS):
        Book.objects.create(order=start_order + i, **data)


def remove_books(apps, schema_editor):
    Book = apps.get_model('library', 'Book')
    for data in EXTRA_BOOKS:
        Book.objects.filter(title=data["title"], author=data["author"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_seed_more_books'),
    ]

    operations = [
        migrations.RunPython(add_books, remove_books),
    ]
