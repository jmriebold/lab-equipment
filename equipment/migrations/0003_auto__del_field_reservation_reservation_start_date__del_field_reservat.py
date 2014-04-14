# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Reservation.reservation_start_date'
        db.delete_column(u'equipment_reservation', 'reservation_start_date')

        # Deleting field 'Reservation.reservation_end_date'
        db.delete_column(u'equipment_reservation', 'reservation_end_date')

        # Adding field 'Reservation.start_date'
        db.add_column(u'equipment_reservation', 'start_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 8, 0, 0)),
                      keep_default=False)

        # Adding field 'Reservation.end_date'
        db.add_column(u'equipment_reservation', 'end_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 8, 0, 0)),
                      keep_default=False)

        # Adding field 'Equipment.image'
        db.add_column(u'equipment_equipment', 'image',
                      self.gf('django.db.models.fields.files.ImageField')(default='equipment_images/null.jpg', max_length=100),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Reservation.reservation_start_date'
        raise RuntimeError("Cannot reverse this migration. 'Reservation.reservation_start_date' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Reservation.reservation_start_date'
        db.add_column(u'equipment_reservation', 'reservation_start_date',
                      self.gf('django.db.models.fields.DateTimeField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Reservation.reservation_end_date'
        raise RuntimeError("Cannot reverse this migration. 'Reservation.reservation_end_date' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Reservation.reservation_end_date'
        db.add_column(u'equipment_reservation', 'reservation_end_date',
                      self.gf('django.db.models.fields.DateTimeField')(),
                      keep_default=False)

        # Deleting field 'Reservation.start_date'
        db.delete_column(u'equipment_reservation', 'start_date')

        # Deleting field 'Reservation.end_date'
        db.delete_column(u'equipment_reservation', 'end_date')

        # Deleting field 'Equipment.image'
        db.delete_column(u'equipment_equipment', 'image')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "'equipment_images/null.jpg'", 'max_length': '100'}),
            'lab': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'lab_or_field': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'max_reservation_length': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'privilege_level': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'reservable': ('django.db.models.fields.BooleanField', [], {})
        },
        u'equipment.reservation': {
            'Meta': {'object_name': 'Reservation'},
            'course': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'equipment': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['equipment.Equipment']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'reserved_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['equipment']