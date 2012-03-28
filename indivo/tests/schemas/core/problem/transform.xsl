<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:Problem">
    <Models>
      <Model name="Problem">
        <Field name="date_onset"><xsl:value-of select='indivodoc:dateOnset/text()' /></Field>
        <Field name="date_resolution"><xsl:value-of select='indivodoc:dateResolution/text()' /></Field>
        <xsl:if test="indivodoc:name">
	  <Field name="name"><xsl:value-of select='indivodoc:name/text()' /></Field>
	  <Field name="name_type"><xsl:value-of select='indivodoc:name/@type' /></Field>
	  <Field name="name_value"><xsl:value-of select='indivodoc:name/@value' /></Field>
	  <Field name="name_abbrev"><xsl:value-of select='indivodoc:name/@abbrev' /></Field>
        </xsl:if>
        <Field name="comments"><xsl:value-of select='indivodoc:comments/text()' /></Field>
        <Field name="diagnosed_by"><xsl:value-of select='indivodoc:diagnosedBy/text()' /></Field>
      </Model>
    </Models>
  </xsl:template>
</xsl:stylesheet>
