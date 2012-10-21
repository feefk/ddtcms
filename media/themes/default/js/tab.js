<!--
function tab(mod,cursor,n){
	for(i=1;i<=n;i++){
		var nav=document.getElementById(mod+i);
		var cont=document.getElementById(mod+"_"+"cont"+i);
		nav.className=i==cursor?"current":"";
		cont.style.display=i==cursor?"block":"none";
	}
}
//-->