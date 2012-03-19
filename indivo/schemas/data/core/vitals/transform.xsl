<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:VitalSign">
    <Models>
      <Model name="Vitals">
        <Field name="date_measured"><xsl:value-of select='indivodoc:dateMeasured/text()' /></Field>
        <xsl:if test="indivodoc:name">
	  <Field name="name"><xsl:value-of select='indivodoc:name/text()' /></Field>
	  <Field name="name_type"><xsl:value-of select='indivodoc:name/@type' /></Field>
	  <Field name="name_value"><xsl:value-of select='indivodoc:name/@value' /></Field>
	  <Field name="name_abbrev"><xsl:value-of select='indivodoc:name/@abbrev' /></Field>
        </xsl:if>
        <Field name="value"><xsl:value-of select='indivodoc:value/text()' /></Field>
        <xsl:if test="indivodoc:unit">
	  <Field name="unit"><xsl:value-of select='indivodoc:unit/text()' /></Field>
	  <Field name="unit_type"><xsl:value-of select='indivodoc:unit/@type' /></Field>
	  <Field name="unit_value"><xsl:value-of select='indivodoc:unit/@value' /></Field>
	  <Field name="unit_abbrev"><xsl:value-of select='indivodoc:unit/@abbrev' /></Field>
        </xsl:if>
        <Field name="site"><xsl:value-of select='indivodoc:site/text()' /></Field>
        <Field name="position"><xsl:value-of select='indivodoc:position/text()' /></Field>
        <Field name="comments"><xsl:value-of select='indivodoc:comments/text()' /></Field>
      </Model>
    </Models>
  </xsl:template>
</xsl:stylesheet>
