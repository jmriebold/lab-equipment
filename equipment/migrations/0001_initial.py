# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table(u'equipment_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('netid', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('privilege_level', self.gf('django.db.models.fields.CharField')(default=1, max_length=1)),
        ))
        db.send_create_signal(u'equipment', ['Person'])

        # Adding model 'Equipment'
        db.create_table(u'equipment_equipment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('lab', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('lab_or_field', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('manufacturer', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('equip_model', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('reservable', self.gf('django.db.models.fields.BooleanField')()),
            ('max_reservation_length', self.gf('django.db.models.fields.IntegerField')()),
            ('privilege_level', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'equipment', ['Equipment'])

        # Adding model 'Book'
        db.create_table(u'equipment_book', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lab', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('reservable', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'equipment', ['Book'])

        # Adding model 'Reservation'
        db.create_table(u'equipment_reservation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reserved_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['equipment.Person'])),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('course', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('reservation_start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('reservation_end_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'equipment', ['Reservation'])

        # Adding M2M table for field equipment on 'Reservation'
        m2m_table_name = db.shorten_name(u'equipment_reservation_equipment')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reservation', models.ForeignKey(orm[u'equipment.reservation'], null=False)),
            ('equipment', models.ForeignKey(orm[u'equipment.equipment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['reservation_id', 'equipment_id'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table(u'equipment_person')

        # Deleting model 'Equipment'
        db.delete_table(u'equipment_equipment')

        # Deleting model 'Book'
        db.delete_table(u'equipment_book')

        # Deleting model 'Reservation'
        db.delete_table(u'equipment_reservation')

        # Removing M2M table for field equipment on 'Reservation'
        db.delete_table(db.shorten_name(u'equipment_reservation_equipment'))


    models = {
        u'equipment.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'reservable': ('django.db.models.fields.BooleanField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'equipment.equipment': {
            'Meta': {'object_name': 'Equipment'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'equip_model': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'lab_or_field': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'max_reservation_length': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'privilege_level': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'reservable': ('django.db.models.fields.BooleanField', [], {})
        },
        u'equipment.person': {
            'Meta': {'object_name': 'Person'},
            'department': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'netid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'privilege_level': ('django.db.models.fields.CharField', [], {'default': '1', 'max_length': '1'})
        },
        u'equipment.reservation': {
            'Meta': {'object_name': 'Reservation'},
            'course': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'equipment': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['equipment.Equipment']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'reservation_end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'reservation_start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'reserved_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['equipment.Person']"})
        }
    }

    complete_apps = ['equipment']