# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CashOnDeliveryTransaction'
        db.create_table(u'cashondelivery_cashondeliverytransaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order_number', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=2, blank=True)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=8, null=True, blank=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(default='02c33566-7a34-4a02-a9e7-5951da975580', unique=True, max_length=100, blank=True)),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_confirmed', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('cashondelivery', ['CashOnDeliveryTransaction'])


    def backwards(self, orm):
        # Deleting model 'CashOnDeliveryTransaction'
        db.delete_table(u'cashondelivery_cashondeliverytransaction')


    models = {
        'cashondelivery.cashondeliverytransaction': {
            'Meta': {'ordering': "('-date_created',)", 'object_name': 'CashOnDeliveryTransaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'date_confirmed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_number': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'reference': ('django.db.models.fields.CharField', [], {'default': "'895fcaca-3129-47fd-9897-a829084f3256'", 'unique': 'True', 'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['cashondelivery']