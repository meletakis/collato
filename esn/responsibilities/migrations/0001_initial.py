# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Responsibility'
        db.create_table(u'responsibilities_responsibility', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal(u'responsibilities', ['Responsibility'])

        # Adding model 'Responsibility_assign'
        db.create_table(u'responsibilities_responsibility_assign', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Responsibility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['responsibilities.Responsibility'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'responsibilities', ['Responsibility_assign'])


    def backwards(self, orm):
        # Deleting model 'Responsibility'
        db.delete_table(u'responsibilities_responsibility')

        # Deleting model 'Responsibility_assign'
        db.delete_table(u'responsibilities_responsibility_assign')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'responsibilities.responsibility': {
            'Meta': {'object_name': 'Responsibility'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'responsibilities.responsibility_assign': {
            'Meta': {'object_name': 'Responsibility_assign'},
            'Responsibility': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['responsibilities.Responsibility']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['responsibilities']