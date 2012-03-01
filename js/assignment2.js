// To do:
// - Get the XML retrieval part working
// - Convert XML to RDF (write XSLT)
// - Store RDF in triple store
// - Query triple store
// - Show results on webpage


function getEventData(query){
	
	// Look up all literals (= words surrounded either by ' or by ")
	var literals = query.match(/['"](.*?)['"]/g);
	
	// Remove the ' or " from the literals
	for (i=0;i<literals.length;i++)
	{
		literals[i] = literals[i].replace(/['"]/g,'');
	}
		
	
	// Retrieve the XML for every literal - not working yet
	for (j=0;j<literals.length;j++)
	{
	
		var apiKey = "fZbWS6qHrqnNvPW7";
	
		var xmlUrl = "http://api.eventful.com/rest/events/search?app_key=" + apiKey + "&keywords=" + literals[j];
	
		// alert(xmlUrl);
	
		// Not working, because of "... is not allowed by Access-Control-Allow-Origin."
		
		$.ajax({
		dataType: "xml", 
		url: xmlUrl,
		crossDomain: false, 
		type: "GET", 
		success: function(xml){
			
			$xml = $(xml); 
			alert('Retrieved an XML!');
			
			// Load an XSLT stylesheet:
			// xsl = loadXMLDoc("xml2rdf.xsl");
			
			// Convert to RDF:
			// xsltProcessor = new XSLTProcessor();
			// xsltProcessor.importStylesheet(xsl);
			// rdf = xsltProcessor.transformToFragment(xml,document);
			
		},

		error: function(jqXHR, textStatus, erroThrown){
			alert('jqXHR: '+jqXHR+', textStatus: '+textStatus+', errorThrown: '+erroThrown); 
		}
		});
		
	
	}
	
}


function loadXMLDoc(dname) {

	if (window.XMLHttpRequest) {
		xhttp=new XMLHttpRequest();
	}

	else {
		xhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	
	http.open("GET",dname,false);
	xhttp.send("");
	return xhttp.responseXML;
	
} 