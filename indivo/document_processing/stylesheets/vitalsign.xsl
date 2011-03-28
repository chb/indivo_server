<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:VitalSign">
    <facts>
      <fact>
        <date_measured><xsl:value-of select='indivodoc:dateMeasured/text()' /></date_measured>
        <xsl:if test="indivodoc:name">
	        <name><xsl:value-of select='indivodoc:name/text()' /></name>
	        <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
	        <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
	        <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
        </xsl:if>
        <value><xsl:value-of select='indivodoc:value/text()' /></value>
        <xsl:if test="indivodoc:unit">
	        <unit><xsl:value-of select='indivodoc:unit/text()' /></unit>
	        <unit_type><xsl:value-of select='indivodoc:unit/@type' /></unit_type>
	        <unit_value><xsl:value-of select='indivodoc:unit/@value' /></unit_value>
	        <unit_abbrev><xsl:value-of select='indivodoc:unit/@abbrev' /></unit_abbrev>
        </xsl:if>
        <site><xsl:value-of select='indivodoc:site/text()' /></site>
        <position><xsl:value-of select='indivodoc:position/text()' /></position>
        <comments><xsl:value-of select='indivodoc:comments/text()' /></comments>
      </fact>
    </facts>
  </xsl:template>
</xsl:stylesheet>
