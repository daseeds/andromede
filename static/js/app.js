$('body').backstretch("static/img/fond-ecran-nature-paysages-deserts-018.jpg");

// Twitter code
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
}(document, 'script', 'facebook-jssdk'));


//Google Map API v3
var map;
function initialize() {
	map = new google.maps.Map(document.getElementById("map-canvas"), {
		center: new google.maps.LatLng(49.5062536,-1.4668496),
		zoom: 16,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	});
	var iconBase = 'http://google.com/mapfiles/ms/micons/';
	var marker = new google.maps.Marker({
		position: new google.maps.LatLng(49.5062536,-1.4668496),
		map: map,
		icon: iconBase + 'blue.png'
	});
}
google.maps.event.addDomListener(window, 'load', initialize);