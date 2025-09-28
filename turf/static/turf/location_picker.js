(function(){
  // Namespace
  window.TurfLocationPicker = {
    init: function(selector){
      var el = document.querySelector(selector);
      if (!el) return;

      var latInput = document.getElementById('id_latitude');
      var lngInput = document.getElementById('id_longitude');
      if (!latInput || !lngInput) return;

      var lat = parseFloat(el.getAttribute('data-lat')) || 0.0;
      var lng = parseFloat(el.getAttribute('data-lng')) || 0.0;
      var center = { lat: lat, lng: lng };

      var map = new google.maps.Map(el, {
        center: center,
        zoom: 15,
        mapTypeId: 'roadmap'
      });

      var marker = new google.maps.Marker({
        position: center,
        map: map,
        draggable: true
      });

      // Update inputs when marker moves
      marker.addListener('dragend', function(ev){
        var p = ev.latLng;
        latInput.value = p.lat().toFixed(6);
        lngInput.value = p.lng().toFixed(6);
      });

      // Click to move marker
      map.addListener('click', function(ev){
        marker.setPosition(ev.latLng);
        latInput.value = ev.latLng.lat().toFixed(6);
        lngInput.value = ev.latLng.lng().toFixed(6);
      });

      // If user types coordinates manually, move the marker
      function updateMarkerFromInputs(){
        var latVal = parseFloat(latInput.value);
        var lngVal = parseFloat(lngInput.value);
        if (!isNaN(latVal) && !isNaN(lngVal)){
          var pos = { lat: latVal, lng: lngVal };
          marker.setPosition(pos);
          map.setCenter(pos);
        }
      }

      latInput.addEventListener('change', updateMarkerFromInputs);
      lngInput.addEventListener('change', updateMarkerFromInputs);
    }
  };
})();
