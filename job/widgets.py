'''
from django import forms
from django.db import models


class LocationPickerWidget(forms.TextInput):
    class Media:
        css = {
            'all': (
                'http://localhost/tulong/static/css/location_picker.css',
            )
        }
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js',
            'http://www.google.com/jsapi?key=' + settings.MAPS_API_KEY+'&sensor=false',
            #'https://maps.googleapis.com/maps/api/js?key='+settings.MAPS_API_KEY+'&sensor=false',
            'http://localhost/tulong/static/js/jquery.location_picker.js',
        )


    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        super(LocationPickerWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        if None == attrs:
            attrs = {}
        attrs['class'] = 'location_picker'
        return super(LocationPickerWidget, self).render(name, value, attrs)

class LocationField(models.CharField):

    def formfield(self, **kwargs):
        kwargs['widget'] = LocationPickerWidget
        return super(LocationField, self).formfield(**kwargs)

'''

from django import forms
from django.db import models
from django.utils.safestring import mark_safe
from django.conf import settings
DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 300

DEFAULT_LAT = 14.625361
DEFAULT_LNG = 121.124482

class LocationWidget(forms.TextInput):
    def __init__(self, *args, **kw):

        self.map_width = kw.get("map_width", DEFAULT_WIDTH)
        self.map_height = kw.get("map_height", DEFAULT_HEIGHT)

        super(LocationWidget, self).__init__(*args, **kw)
        self.inner_widget = forms.widgets.HiddenInput()

    def render(self, name, value, *args, **kwargs):
        if value is None:
            lat, lng = DEFAULT_LAT, DEFAULT_LNG
        else:
            if isinstance(value, unicode):
                a, b = value.split(',')
            else:
                a, b = value
            lat, lng = float(a), float(b)

        js = '''
<script type="text/javascript">
    var map_%(name)s;

    function savePosition_%(name)s(point)
    {
        var input = document.getElementById("id_%(name)s");
        input.value = point.lat().toFixed(6) + "," + point.lng().toFixed(6);
        map_%(name)s.panTo(point);
    }
    

    function load_%(name)s() {
        var point = new google.maps.LatLng(%(lat)f, %(lng)f);
        var mapElem = document.getElementById("map_%(name)s")


        var mapOptions = {
              center: point,
              zoom: 14,
              mapTypeId: google.maps.MapTypeId.ROADMAP
            };
       
        map_%(name)s = new google.maps.Map(mapElem, mapOptions);
        
        var marker = new google.maps.Marker({
                map: map_%(name)s,
                position: new google.maps.LatLng(%(lat)f, %(lng)f),
                draggable: true
        
        });
        google.maps.event.addListener(marker, 'dragend', function(mouseEvent) {
            savePosition_%(name)s(mouseEvent.latLng);
        });

        google.maps.event.addListener(map_%(name)s, 'click', function(mouseEvent){
            marker.setPosition(mouseEvent.latLng);
            savePosition_%(name)s(mouseEvent.latLng);
        });
    }
    
    $(document).ready(function(){
        load_%(name)s();
    });

</script>
        ''' % dict(name=name, lat=lat, lng=lng)
        html = self.inner_widget.render("%s" % name, "%f,%f" % (lat, lng), dict(id='id_%s' % name))
        html += '<div id="map_%s" style="width: %dpx; height: %dpx"></div>' % (name, self.map_width, self.map_height)

        return mark_safe(js + html)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js',
            #'http://maps.google.com/maps/api/js?sensor=false',
            'https://maps.googleapis.com/maps/api/js?&sensor=false',
        )

class LocationFormField(forms.CharField):
    def clean(self, value):
        if isinstance(value, unicode):
            a, b = value.split(',')
        else:
            a, b = value

        lat, lng = float(a), float(b)
        return "%f,%f" % (lat, lng)

class LocationField(models.CharField):
    def formfield(self, **kwargs):
        defaults = {'form_class': LocationFormField}
        defaults.update(kwargs)
        defaults['widget'] = LocationWidget
        return super(LocationField, self).formfield(**defaults)