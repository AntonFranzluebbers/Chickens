function versionNum() {
	var ver=1.3;
	var v=document.getElementById("version");
	v.innerHTML="Version " + ver;
}

function current() {
	var d = document.getElementsByClassName("d");
	var t = document.getElementById("toggles");

	for (i=0; i<d.length;i++) {
		if (d[i].style.opacity == "1") {
			d[i].style.opacity = ".1";
		}
		else {
			d[i].style.opacity = "1";
		}
	}
	
	t.classList.toggle("toggledown");
}
