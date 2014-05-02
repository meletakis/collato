# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Domain'
        db.create_table(u'applications_domain', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('Description', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal(u'applications', ['Domain'])

        # Adding model 'App'
        db.create_table(u'applications_app', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('responsibility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['responsibilities.Responsibility'])),
            ('source_code_host', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['applications.Domain'])),
        ))
        db.send_create_signal(u'applications', ['App'])

        # Adding model 'Data'
        db.create_table(u'applications_data', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('data_type', self.gf('django.db.models.fields.CharField')(default=None, max_length=50)),
            ('expiration_period', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['applications.Domain'])),
            ('semantics', self.gf('jsonfield.fields.JSONField')()),
        ))
        db.send_create_signal(u'applications', ['Data'])

        # Adding model 'IORegistry'
        db.create_table(u'applications_ioregistry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['applications.App'])),
            ('data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['applications.Data'])),
            ('data_type', self.gf('django.db.models.fields.CharField')(default=None, max_length=50)),
            ('idle', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'applications', ['IORegistry'])

        # Adding model 'Action'
        db.create_table(u'applications_action', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('actor_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='app_actor', to=orm['contenttypes.ContentType'])),
            ('actor_object_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('verb', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('target_content_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='app_target', null=True, to=orm['contenttypes.ContentType'])),
            ('target_object_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('action_object_content_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='app_action_object', null=True, to=orm['contenttypes.ContentType'])),
            ('action_object_object_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('data', self.gf('jsonfield.fields.JSONField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'applications', ['Action'])


    def backwards(self, orm):
        # Deleting model 'Domain'
        db.delete_table(u'applications_domain')

        # Deleting model 'App'
        db.delete_table(u'applications_app')

        # Deleting model 'Data'
        db.delete_table(u'applications_data')

        # Deleting model 'IORegistry'
        db.delete_table(u'applications_ioregistry')

        # Deleting model 'Action'
        db.delete_table(u'applications_action')


    models = {
        u'actstream.action': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'Action'},
            'action_object_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'action_object'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'action_object_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'actor_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actor'", 'to': u"orm['contenttypes.ContentType']"}),
            'actor_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'data': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'target_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'target'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'target_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'applications.action': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'Action'},
            'action_object_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'app_action_object'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'action_object_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'actor_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'app_actor'", 'to': u"orm['contenttypes.ContentType']"}),
            'actor_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'data': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'target_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'app_target'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'target_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'applications.app': {
            'Meta': {'object_name': 'App'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['applications.Domain']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'responsibility': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['responsibilities.Responsibility']"}),
            'source_code_host': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'applications.data': {
            'Meta': {'object_name': 'Data'},
            'data_type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['applications.Domain']"}),
            'expiration_period': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'semantics': ('jsonfield.fields.JSONField', [], {})
        },
        u'applications.domain': {
            'Description': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'Meta': {'object_name': 'Domain'},
            'Name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'applications.ioregistry': {
            'Meta': {'object_name': 'IORegistry'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['applications.App']"}),
            'data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['applications.Data']"}),
            'data_type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idle': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'relationships': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_to'", 'symmetrical': 'False', 'through': u"orm['relationships.Relationship']", 'to': u"orm['auth.User']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'relationships.relationship': {
            'Meta': {'ordering': "('created',)", 'unique_together': "(('from_user', 'to_user', 'status', 'site'),)", 'object_name': 'Relationship'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_users'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'relationships'", 'to': u"orm['sites.Site']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['relationships.RelationshipStatus']"}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_users'", 'to': u"orm['auth.User']"}),
            'weight': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'null': 'True', 'blank': 'True'})
        },
        u'relationships.relationshipstatus': {
            'Meta': {'ordering': "('name',)", 'object_name': 'RelationshipStatus'},
            'from_role': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'from_role'", 'null': 'True', 'to': u"orm['roleapp.Role']"}),
            'from_slug': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'symmetrical_slug': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'to_role': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'to_role'", 'null': 'True', 'to': u"orm['roleapp.Role']"}),
            'to_slug': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'responsibilities.responsibility': {
            'Meta': {'object_name': 'Responsibility'},
            'Name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'roleapp.role': {
            'Meta': {'object_name': 'Role'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '100L', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50L', 'null': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['applications']