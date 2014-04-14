// JavaScript Document
// transforms this:	<span class="mailScr">Text to be email-linkified: local[AT domain DOT extension]</span>
// into this:		<span class="mailScr"><a href="mailto:local@domain.extension">Text to be email-linkified</a></span>
// if there is no text specified, 
// the result is: 	<span class="mailScr"><a href="mailto:local@domain.extension">local@domain.extension</a></span>
var emailScrambler2 = function() {
	var mailopen = '<a href="mailto:';
	var mailclose = '">';
	var anchorclose = '</a>';
	var linkText = '';
	var local = '';
	var domain = '';
	var extension = '';
	var address = '';
	var arr = new Array();
	arr = document.getElementsByName('mailScr');
	for(var i=0; i<arr.length; i++) {
		if(arr[i].innerHTML.indexOf(': ') < 0) {
			local = arr[i].innerHTML.split('[AT ');
			domain = local[1].split(' DOT ');
			extension = domain[1].split(']');
			address = local[0]+'@'+domain[0]+'.'+extension[0];
			arr[i].innerHTML = mailopen+address+mailclose+address+anchorclose;
		} else {
			linkText = arr[i].innerHTML.split(': ');
			local = linkText[1].split('[AT ');
			domain = local[1].split(' DOT ');
			extension = domain[1].split(']');
			address = local[0]+'@'+domain[0]+'.'+extension[0];
			arr[i].innerHTML = mailopen+address+mailclose+linkText[0]+anchorclose;
		}
	}
}
