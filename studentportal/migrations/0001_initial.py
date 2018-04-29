# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-27 19:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='advisor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('batch', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='course',
            fields=[
                ('course_id', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('credit_struct', models.CharField(max_length=25)),
                ('title', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='dean',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateto', models.DateField()),
                ('datefrom', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='dean_staff_office',
            fields=[
                ('staff_id', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('staff_name', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=12)),
                ('email_id', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='department',
            fields=[
                ('dept_id', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('dept_name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='faculty',
            fields=[
                ('faculty_id', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=12)),
                ('email_id', models.EmailField(max_length=254)),
                ('dept_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentportal.department')),
            ],
        ),
        migrations.CreateModel(
            name='hod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateto', models.DateField()),
                ('datefrom', models.DateField()),
                ('faculty_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentportal.faculty')),
            ],
        ),
        migrations.CreateModel(
            name='related',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateto', models.DateField()),
                ('datefrom', models.DateField()),
                ('faculty_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentportal.faculty')),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentportal.dean_staff_office')),
            ],
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('student_id', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('cgpa', models.DecimalField(decimal_places=2, max_digits=3)),
                ('curr_registered_credits', models.IntegerField()),
                ('max_credit', models.IntegerField()),
                ('total_credits', models.IntegerField()),
                ('current_year', models.IntegerField()),
                ('current_sem', models.IntegerField()),
                ('password', models.CharField(max_length=12)),
                ('dept_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentportal.department')),
            ],
        ),
        migrations.CreateModel(
            name='successfull_register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentportal.student')),
            ],
        ),
        migrations.CreateModel(
            name='takes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentportal.student')),
            ],
        ),
        migrations.CreateModel(
            name='teaches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_id', models.CharField(max_length=25)),
                ('semester', models.IntegerField()),
                ('year', models.IntegerField()),
                ('slot', models.CharField(max_length=2)),
                ('constraint', models.DecimalField(decimal_places=2, max_digits=3)),
                ('stream_batch', models.TextField()),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentportal.course')),
                ('faculty_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentportal.faculty')),
            ],
        ),
        migrations.CreateModel(
            name='token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField()),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentportal.student')),
                ('teaches', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentportal.teaches')),
            ],
        ),
        migrations.AddField(
            model_name='takes',
            name='teaches',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentportal.teaches'),
        ),
        migrations.AddField(
            model_name='successfull_register',
            name='teaches',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentportal.teaches'),
        ),
        migrations.AddField(
            model_name='dean',
            name='faculty_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentportal.faculty'),
        ),
        migrations.AddField(
            model_name='course',
            name='dept_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentportal.department'),
        ),
        migrations.AddField(
            model_name='advisor',
            name='faculty_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentportal.faculty'),
        ),
        migrations.AlterUniqueTogether(
            name='token',
            unique_together=set([('student_id', 'teaches')]),
        ),
        migrations.AlterUniqueTogether(
            name='teaches',
            unique_together=set([('faculty_id', 'section_id', 'course_id', 'semester', 'year', 'slot')]),
        ),
        migrations.AlterUniqueTogether(
            name='takes',
            unique_together=set([('student_id', 'teaches')]),
        ),
        migrations.AlterUniqueTogether(
            name='successfull_register',
            unique_together=set([('student_id', 'teaches')]),
        ),
        migrations.AlterUniqueTogether(
            name='related',
            unique_together=set([('staff_id', 'dateto', 'datefrom')]),
        ),
        migrations.AlterUniqueTogether(
            name='hod',
            unique_together=set([('dateto', 'datefrom', 'faculty_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='dean',
            unique_together=set([('dateto', 'datefrom', 'faculty_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='advisor',
            unique_together=set([('faculty_id', 'year')]),
        ),
    ]
