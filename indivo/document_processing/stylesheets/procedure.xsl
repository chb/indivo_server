<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:Procedure">
    <facts>
      <fact>
        <date_performed><xsl:value-of select='indivodoc:datePerformed/text()' /></date_performed>
        <xsl:if test="indivodoc:name">
	        <name><xsl:value-of select='indivodoc:name/text()' /></name>
	        <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
	        <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
	        <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
        </xsl:if>
        <xsl:apply-templates select='indivodoc:provider' />
        <location><xsl:value-of select='indivodoc:location/text()' /></location>
        <comments><xsl:value-of select='indivodoc:comments/text()' /></comments>
      </fact>
    </facts>
  </xsl:template>
  <xsl:template match="indivodoc:provider">
    <xsl:if test="indivodoc:name">
      <provider_name><xsl:value-of select='indivodoc:name/text()' /></provider_name>
    </xsl:if>
    <xsl:if test="indivodoc:institution">
      <provider_institution><xsl:value-of select='indivodoc:institution/text()' /></provider_institution>
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>
