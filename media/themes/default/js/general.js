/*globals $ window document */
// the line above helps JSLint ignore certain globals; keep it and customize it if you're using JSLint's "good parts" to check your scripts

// The script below does essentially nothing other than define some nearly empty methods and a few settings for demonstration purposes
// You can delete this whole thing, or do whatever you want with it, it's just a basic starting point that I've been using lately

$(function () {
	// variable for caching settings
	var s = null,

	DDTCMS = {
		// define your oft-used settings below
		settings: {
			basicExample: $("#main"),
			nestedExample: {
				first: true,
				second: true,
				third: true,
				fourth: true,
				fifth: ['one', 'two', 'three', 'four', 'five', 'six']
			},

			foo: "bar"
		},

		// the method that initializes stuff
		init: function () {
			/*	the line below can be included in each method to reference the settings 
				without always having to type "this.settings" each time */
			s = this.settings;
			// using firebug you can view all settings with "console.log(s)";

			// after you do stuff here, you can call the next method
			// You can use "this" in the current context to reference "PrimaryNameSpace" directly
			this.nextMethod();

		},
		
		nextMethod: function () {
			s = this.settings;
			// do stuff here
		},
		
		anotherMethod: function () {
			s = this.settings;
			// do more stuff here
		},
		
		doSwitchLinksTab: function () {
			$(document).ready(function() {
				var A=$(".lisort").find("li"),B=$(".link_content").find(".lilink");
				A.each(function() {
					$(this).mouseover(function() {
						A.removeClass("cur");
						$(this).addClass("cur");
						B.hide();
						B.eq($(this).attr("rel")).show();
					})
				});
			})
		},

		setFullSearch: function () {
			s = this.settings;
			var curtopid='23';
			if(curtopid=="")curtopid="";
			curtopid=(curtopid?curtopid:0)
			$(".searchtype li").each(function(){
				var panel=$(this);
				if(panel.find("span").attr("rel")==curtopid){
					panel.addClass("cur");
					$(".fullSearch #typeid").val(curtopid);
				}else panel.removeClass("cur");
				panel.find("span").bind("click",function(){
					$(".fullSearch #typeid").val($(this).attr("rel"))
					$(".searchtype li").each(function(){$(this).removeClass("cur")});
					panel.addClass("cur")
				})
			})
		},
		
		doChangeColor: function () {
			s = this.settings;
			$(document.body).click(function () {
					$("nav ul li").each(function (i) {
				        if (this.style.color != "blue") {
				          this.style.color = "blue";
				        } else {
				          this.style.color = "";
				        }
		      		});
	    	});
		}
		

    
		// remember not to use a trailing comma after the last method is defined; you could leave a dummy method here to prevent that error
	};

	// This line initializes the whole thing; you could pass in some JSON data or some other object that needs to be worked with
	DDTCMS.init();
	DDTCMS.doSwitchLinksTab();
	DDTCMS.setFullSearch();
});