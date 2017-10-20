from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def remove_users_and_students(apps, schema_editor):
    Student = apps.get_model('learn', 'Student')
    User = apps.get_model('auth', 'User')
    db_alias = schema_editor.connection.alias
    Student.objects.using(db_alias).all().delete()
    User.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0014_action'),
    ]

    operations = [
        migrations.RunPython(remove_users_and_students, remove_users_and_students),
        migrations.AddField(
            model_name='student',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
