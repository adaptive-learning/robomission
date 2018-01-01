from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0020_levels_ordering'),
    ]

    database_operations = [
        migrations.AlterModelTable('Feedback', 'monitoring_feedback')
    ]

    state_operations = [
        migrations.DeleteModel('Feedback')
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
            state_operations=state_operations)
    ]
