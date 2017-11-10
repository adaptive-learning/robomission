from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def remove_user_related_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Student = apps.get_model('learn', 'Student')
    TaskSession = apps.get_model('learn', 'TaskSession')
    ProgramSnapshot = apps.get_model('learn', 'ProgramSnapshot')
    Action = apps.get_model('learn', 'Action')
    db_alias = schema_editor.connection.alias
    Action.objects.using(db_alias).all().delete()
    ProgramSnapshot.objects.using(db_alias).all().delete()
    TaskSession.objects.using(db_alias).all().delete()
    Student.objects.using(db_alias).all().delete()
    User.objects.using(db_alias).all().delete()
    # TODO: Find how to retrieve historical version of Session model and remove
    #       sessions same way as the other models above. In the meantime,
    #       sessions can be deleted manually: ./backend/manage.py clearsessions


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0014_action'),
    ]

    operations = [
        migrations.RunPython(remove_user_related_data, remove_user_related_data),
        migrations.AddField(
            model_name='student',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
