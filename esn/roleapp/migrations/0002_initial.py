# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Role'
        db.create_table(u'roleapp_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=50L, null=True)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=100L, null=True)),
        ))
        db.send_create_signal(u'roleapp', ['Role'])


    def backwards(self, orm):
        # Deleting model 'Role'
        db.delete_table(u'roleapp_role')


    models = {
        u'roleapp.role': {
            'Meta': {'object_name': 'Role'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50L', 'null': 'True'})
        }
    }

    complete_apps = ['roleapp']