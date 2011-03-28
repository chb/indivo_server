<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:Problem">
    <facts>
      <fact>
        <date_onset><xsl:value-of select='indivodoc:dateOnset/text()' /></date_onset>
        <date_resolution><xsl:value-of select='indivodoc:dateResolution/text()' /></date_resolution>
        <xsl:if test="indivodoc:name">
	        <name><xsl:value-of select='indivodoc:name/text()' /></name>
	        <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
	        <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
	        <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
        </xsl:if>
        <comments><xsl:value-of select='indivodoc:comments/text()' /></comments>
        <diagnosed_by><xsl:value-of select='indivodoc:diagnosedBy/text()' /></diagnosed_by>
      </fact>
    </facts>
  </xsl:template>
</xsl:stylesheet>
