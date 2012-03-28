<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:Immunization">
    <Models>
      <Model name="Immunization">
        <Field name="date_administered"><xsl:value-of select='indivodoc:dateAdministered/text()' /></Field>
        <Field name="administered_by"><xsl:value-of select='indivodoc:administeredBy/text()' /></Field>
        <xsl:apply-templates select='indivodoc:vaccine' />  
        <Field name="sequence"><xsl:value-of select='indivodoc:sequence/text()' /></Field>
        <Field name="anatomic_surface"><xsl:value-of select='indivodoc:anatomicSurface/text()' /></Field>
        <xsl:if test="indivodoc:anatomic_surface">
  	  <Field name="anatomic_surface_type"><xsl:value-of select='indivodoc:anatomic_surface/@type' /></Field>
  	  <Field name="anatomic_surface_value"><xsl:value-of select='indivodoc:anatomic_surface/@value' /></Field>
  	  <Field name="anatomic_surface_abbrev"><xsl:value-of select='indivodoc:anatomic_surface/@abbrev' /></Field>
        </xsl:if>
        <Field name="adverse_event"><xsl:value-of select='indivodoc:adverseEvent/text()' /></Field>
      </Model>
    </Models>
  </xsl:template>
  <xsl:template match="indivodoc:vaccine">
    <Field name="vaccine_type"><xsl:value-of select='indivodoc:type/text()' /></Field>
    <xsl:if test="indivodoc:type">
      <Field name="vaccine_type_type"><xsl:value-of select='indivodoc:type/@type' /></Field>
      <Field name="vaccine_type_value"><xsl:value-of select='indivodoc:type/@value' /></Field>
      <Field name="vaccine_type_abbrev"><xsl:value-of select='indivodoc:type/@abbrev' /></Field>
    </xsl:if>
    <xsl:if test="indivodoc:manufacturer">
      <Field name="vaccine_manufacturer"><xsl:value-of select='indivodoc:manufacturer/text()' /></Field>
    </xsl:if>
    <xsl:if test="indivodoc:lot">
      <Field name="vaccine_lot"><xsl:value-of select='indivodoc:lot/text()' /></Field>
    </xsl:if>
    <xsl:if test="indivodoc:expiration">
      <Field name="vaccine_expiration"><xsl:value-of select='indivodoc:expiration/text()' /></Field>
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>
