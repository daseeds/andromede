

/*// Twitter code
!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+'://platform.twitter.com/widgets.js';fjs.parentNode.insertBefore(js,fjs);}}(document, 'script', 'twitter-wjs');


// Google+ code
window.___gcfg = {lang: 'fr'};

(function() {
	var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
	po.src = 'https://apis.google.com/js/platform.js';
	var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
})();

// FB code
(function(d, s, id) {
	var js, fjs = d.getElementsByTagName(s)[0];
	if (d.getElementById(id)) return;
	js = d.createElement(s); js.id = id;
	js.src = "//connect.facebook.net/en_US/all.js#xfbml=1";
	fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));*/

$(document).ready(function () {
    supportTouch = !! ('ontouchstart' in window) || !! ('msmaxtouchpoints' in window.navigator);

})



//Google Map API v3

var manoirLatLng = {
    latLng: new google.maps.LatLng(49.5062536,-1.4668496),
    label: "Little and Co."
}

var map;
function initialize() {
	var map_canvas = document.getElementById("map-canvas");
	var map_options = {
	        center: manoirLatLng.latLng,
	        zoom: 17,
	        mapTypeId: google.maps.MapTypeId.ROADMAP,
	        mapTypeControl: false,
	        maxZoom: 20,
	        minZoom: 5,
	        scrollwheel: false,
	        draggable: !supportTouch //turn off draggable when device support touch(such as phone/tablet)
	    };
	map = new google.maps.Map(map_canvas, map_options);

	var iconBase = 'http://google.com/mapfiles/ms/micons/';
	var marker = new google.maps.Marker({
		position: new google.maps.LatLng(49.5062536,-1.4668496),
		map: map,
		title: "cabinet",
		icon: iconBase + 'blue.png',
		content: "<p>920 Second Avenue S.<br /> Suite 1400 (International Centre II) <br />Minneapolis, MN 55402 <br />612-375-0077<p>Elevator Lobby located to the right of Caf&eacute; Patteen, we are on the 14th floor.</p>"
	});
}
google.maps.event.addDomListener(window, 'load', initialize);

