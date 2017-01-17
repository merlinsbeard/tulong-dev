# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PaymentType'
        db.create_table('payment_paymenttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('payment_type', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('info', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=200)),
        ))
        db.send_create_signal('payment', ['PaymentType'])


    def backwards(self, orm):
        # Deleting model 'PaymentType'
        db.delete_table('payment_paymenttype')


    models = {
        'payment.paymenttype': {
            'Meta': {'object_name': 'PaymentType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['payment']