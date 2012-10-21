window.onerror = function(){ return true; }


var showImageIndex = -1;
var imageTimer;
function showImage(imageIndex)
{
	var flash_img_div = document.getElementById("flash_img");
	var flash_title = document.getElementById("flash_title");	
	
	if(imageIndex>fImgs.length-1){
		imageIndex = 0;
	}
	
	if(!fImgs[imageIndex] || imageIndex==showImageIndex)
		return false;	/*
	if(imageIndex==0){
		document.getElementById("img_prev_btn").style.visibility = "hidden";
	}else if(imageIndex==fImgs.length-1){
		document.getElementById("img_next_btn").style.visibility = "hidden";
	}else{
		document.getElementById("img_prev_btn").style.visibility = "inherit";
		document.getElementById("img_next_btn").style.visibility = "inherit";
	}
	*/
	var imgId = "__fImg"+imageIndex;
	flash_img_div.filters && flash_img_div.filters[0].Apply();
	for(i=0; i<flash_img_div.childNodes.length; i++){
		flash_img_div.childNodes[i].style.display = "none";
	}
	if( document.getElementById(imgId) ){
		var imga = document.getElementById(imgId);
		imga.style.display = "block";
		if(imga.tagName=="OBJECT"){
			imga.rewind();
			imga.Play();
		}
	}else{

			var img = new Image();
			img.border = "0";
			img.src = fImgs[imageIndex].img;
			img.width = "320";
			img.height = "240";
			var a = document.createElement("a");
			a.href = fImgs[imageIndex].href;
			a.target = "_blank";
			a.id = imgId;
			a.appendChild(img);
			//flash_img_div.innerHTML = "";
			flash_img_div.appendChild(a);
		
	}
	flash_img_div.filters && flash_img_div.filters[0].Play();
	var flash_show_ctl_msg = document.getElementById("flash_show_ctl_msg");
	flash_show_ctl_msg.filters && flash_show_ctl_msg.filters[0].Apply();
	flash_title.href = fImgs[imageIndex].href;
	flash_title.innerHTML = fImgs[imageIndex].title;
	flash_show_ctl_msg.filters && flash_show_ctl_msg.filters[0].Play();
	showImageIndex = imageIndex;
	return true;
}
function imagePlay()
{
	if(imageTimer) return;
	if(showImageIndex>=fImgs.length-1){
		showImageIndex = -1;
	}
	showImage(showImageIndex+1);
	imageTimer = setInterval(function(){
					var stat = showImage(showImageIndex+1);
					if(!stat){
						stop();
					}	
				},8000);
}
function stop(){
	clearInterval(imageTimer);
	imageTimer = null;
}
function showNextImage(){
	showImage(showImageIndex+1);
}
function showPrevImage(){
	showImage(showImageIndex-1);
}




function ShowHidden(eleID)
{
    ele=document.getElementById(eleID);
	if (ele.style.display=="")
	{
		ele.style.display = "none";
	}
	else
	{
		ele.style.display = "";
	}
}