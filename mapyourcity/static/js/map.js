function initMap() {
  var attr_osm = 'Map data &copy; <a href="http://openstreetmap.org/">OpenStreetMap</a> contributors';
  var osm = new L.TileLayer('http://{s}.tile.cloudmade.com/cd33cf0ed5eb47bea3410fa19efe3c6a/1714/256/{z}/{x}/{y}.png', {attribution: [attr_osm]});

  map = new L.Map('map', {
    center: new L.LatLng(47.07, 15.43),
      zoom: 17,
      layers: osm,
  });

  map.getControl = function () {
    var ctrl = new L.Control.Layers({
       'Minimal': osm
    });
    return function () {
      return ctrl;
    }
  }();
  map.addControl(map.getControl());

  L.LatLngBounds.prototype.toOverpassBBoxString = function (){
    var a = this._southWest,
        b = this._northEast;
    return [a.lat, a.lng, b.lat, b.lng].join(",");
  }

  var path_style = L.Path.prototype._updateStyle;
  L.Path.prototype._updateStyle = function () {
    path_style.apply(this);
    for (k in this.options.svg) {
      this._path.setAttribute(k, this.options.svg[k]);
    }
  }

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (position) {
      var center = new L.LatLng(position.coords.latitude, position.coords.longitude);
      map.setView(center, 16);
    });
  }
  return map;
}

function parseOverpassJSON(overpassJSON, callbackNode) {
  var nodes = {};
  for (var i = 0; i < overpassJSON.elements.length; i++) {
    var p = overpassJSON.elements[i];
    if (p.type == 'node') {
        p.coordinates = [p.lon, p.lat];
        p.geometry = {type: 'Point', coordinates: p.coordinates};
        p.tags.id=p.id;
        nodes[p.id] = p;
        if (typeof callbackNode === 'function') callbackNode(p);
    }
  }
}