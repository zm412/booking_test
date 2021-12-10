# Generated by Django 3.2.5 on 2021-12-10 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_auto_20211208_1927'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation_day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=8)),
                ('list_of_periods', models.ManyToManyField(blank=True, related_name='hours_list', to='booking.List_periods')),
                ('parking_lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.parking')),
            ],
        ),
        migrations.RemoveField(
            model_name='userfollowing',
            name='follower_user',
        ),
        migrations.RemoveField(
            model_name='userfollowing',
            name='following_user',
        ),
        migrations.RemoveField(
            model_name='booking_session',
            name='list_of_periods',
        ),
        migrations.RemoveField(
            model_name='booking_session',
            name='parking_lot',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='UserFollowing',
        ),
        migrations.AddField(
            model_name='booking_session',
            name='reservation_day',
            field=models.ManyToManyField(blank=True, related_name='days_list', to='booking.Reservation_day'),
        ),
    ]
