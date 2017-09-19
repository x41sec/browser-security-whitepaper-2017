var count = 0;
var notify_url = "http://10.0.60.13:3000";
var parallel_tabs = 10;
var to_process = [];

var slices = 9;        // CHANGE THIS to 1 if you want only 1 slice, as in running only from 1 browser
var process_slice = 7; // CHANGE THIS TO 0,1,2,3 according to which slice you want to process
var instance = 'w7';   // as the process_slice, a unique name to identify your instance, like w0, w1, w2, etc.

var close_tab_each = 8000;
var spawn_tab_each = 9000;

var skip_first = 0;

function getData(){
	var x = new XMLHttpRequest();
	x.open('GET', 'http://10.0.60.13:3000' + '/phishtank_missed?slices=' + slices + '&slice=' + process_slice, false);
		x.onreadystatechange = function(){
		   	if (x.readyState == 4) {
	   			var op_urls = x.responseText.split('\n');

				if(skip_first != 0){
					to_process = op_urls.splice(skip_first, op_urls.length);
					console.log("To Process: " + op_urls.length + "\Skipped: " + skip_first + "\nConcurrent tabs: " + parallel_tabs);
				}else{
					to_process = op_urls;
					console.log("To Process: " + op_urls.length + "\nConcurrent tabs: " + parallel_tabs);
				}
		   	} 
	   };
	x.send();
}

function notify(url){
	var x = new XMLHttpRequest();
	x.open('GET', notify_url + '/allowed?inst=' + instance + '&url=' + encodeURIComponent(url) + "&count=" + count );
	x.send();
};

var to_ignore = ['disabled', 'suspended', 
    	'permanently removed', 'something went wrong', '404', 'Not Found', 'Internal server error',
    	'removed', 'not available', '404 - File or directory not found'];

function screenshot(url){
	// first retrieves the URL via XHR to check the response for stuff to ignore
    var x = new XMLHttpRequest();
	x.open('GET', url, true);
		x.onreadystatechange = function(){
		   	if (x.readyState == 4) {
		   			var response = x.responseText;
                    for(var i=0; i < to_ignore.length ; i++){
                    	if(response.indexOf(to_ignore[i]) !== -1){
                    		// ignore!
							//console.log("URL ignored: " + url);
 							break;
                    	}
                    }
                    // if the page is not to be ignored, take a screenshot
	                chrome.tabs.captureVisibleTab(null, {"format": "png"}, function (duri) {
				        var x = new XMLHttpRequest();
						x.open('POST', notify_url + '/screenshot?inst=' + instance + '&url=' + encodeURIComponent(url) + "&count=" + count );
						x.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
						x.send("datauri=" + encodeURIComponent(duri));
						//console.log("Taken screenshot for url: " + url);
					});		    
		   	} 
	   };
	x.send();
};

var allowed_urls = [];

chrome.tabs.onUpdated.addListener( function (tabId, changeInfo, tab) {
  if (changeInfo.status == 'complete'){
        var url = tab.url;

        if(!allowed_urls.includes(url)){
        	allowed_urls.push(url);
			screenshot(url);
        }
  }
});

getData();

setTimeout(function(){
	var loop = setInterval(function(){
		if(count == to_process.length - 1){ clearInterval(loop); }

	    for(var c=0; c<parallel_tabs ; c++){
			chrome.tabs.create({url:to_process[count]}, function(tab){
				setTimeout(function(){
					if(tab.status == 'loading'){
						chrome.tabs.remove(tab.id);
					}
				}, close_tab_each);
			});
			count++;
	    }
	},spawn_tab_each);
},2000);
