<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE rdf:RDF [
	<!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#">
	<!ENTITY ns "http://www.iro.umontreal.ca/lapalme/ns#">             
]>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0" xmlns:rdf="&rdf;">   
	
	<xsl:strip-space elements="*"/>                                  
	<xsl:output indent="yes"/>
	
	<xsl:template match="/">                                         
		<rdf:RDF xmlns:rdf='&rdf;' xmlns:ns="&ns;">
			<xsl:call-template name="element"/>
        </rdf:RDF>
    </xsl:template>
	
</xsl:stylesheet>