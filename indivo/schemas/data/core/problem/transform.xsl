<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:Problem">
    <Models>
      <Model name="Problem">
        <Field name="startDate"><xsl:value-of select='indivodoc:dateOnset/text()' /></Field>
        <Field name="endDate"><xsl:value-of select='indivodoc:dateResolution/text()' /></Field>
        <xsl:if test="indivodoc:name">
	      <Field name="name_title"><xsl:value-of select='indivodoc:name/text()' /></Field>
	      <Field name="name_system"><xsl:value-of select='indivodoc:name/@type' /></Field>
	      <Field name="name_identifier"><xsl:value-of select='indivodoc:name/@value' /></Field>
        </xsl:if>
      </Model>
    </Models>
  </xsl:template>
</xsl:stylesheet>
