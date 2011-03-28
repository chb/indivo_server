<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:Equipment">
    <facts>
      <fact>
        <date_started><xsl:value-of select='indivodoc:dateStarted/text()' /></date_started>
        <date_stopped><xsl:value-of select='indivodoc:dateStopped/text()' /></date_stopped>
        <name><xsl:value-of select='indivodoc:name/text()' /></name>
        <vendor><xsl:value-of select='indivodoc:vendor/text()' /></vendor>
        <description><xsl:value-of select='indivodoc:description' /></description>
      </fact>
    </facts>
  </xsl:template>
</xsl:stylesheet>
