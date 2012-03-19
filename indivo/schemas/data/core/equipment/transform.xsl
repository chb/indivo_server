<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:Equipment">
    <Models>
      <Model name="Equipment">
        <Field name="date_started"><xsl:value-of select='indivodoc:dateStarted/text()' /></Field>
        <Field name="date_stopped"><xsl:value-of select='indivodoc:dateStopped/text()' /></Field>
        <Field name="name"><xsl:value-of select='indivodoc:name/text()' /></Field>
        <Field name="vendor"><xsl:value-of select='indivodoc:vendor/text()' /></Field>
        <Field name="description"><xsl:value-of select='indivodoc:description' /></Field>
      </Model>
    </Models>
  </xsl:template>
</xsl:stylesheet>
