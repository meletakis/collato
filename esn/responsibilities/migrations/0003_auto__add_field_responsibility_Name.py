# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Responsibility.Name'
        db.add_column(u'responsibilities_responsibility', 'Name',
                      self.gf('django.db.models.fields.CharField')(default='test', unique=True, max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Responsibility.Name'
        db.delete_column(u'responsibilities_responsibility', 'Name')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'responsibilities.assignment': {
            'Meta': {'object_name': 'Assignment'},
            'Responsibility': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['responsibilities.Responsibility']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'responsibilities.responsibility': {
            'Meta': {'object_name': 'Responsibility'},
            'Name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['responsibilities']