<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:SimpleClinicalNote">
    <Models>
      <Model name="SimpleClinicalNote">
        <Field name="date_of_visit"><xsl:value-of select='indivodoc:dateOfVisit/text()' /></Field>
        <xsl:if test="indivodoc:finalizedAt">
          <Field name="finalized_at"><xsl:value-of select='indivodoc:finalizedAt/text()' /></Field>
	</xsl:if>
        <xsl:if test="indivodoc:visitType">
	  <Field name="visit_type"><xsl:value-of select='indivodoc:visitType/text()' /></Field>
	  <Field name="visit_type_type"><xsl:value-of select='indivodoc:visitType/@type' /></Field>
	  <Field name="visit_type_value"><xsl:value-of select='indivodoc:visitType/@value' /></Field>
	  <Field name="visit_type_abbrev"><xsl:value-of select='indivodoc:visitType/@abbrev' /></Field>
        </xsl:if>
        <Field name="visit_location"><xsl:value-of select='indivodoc:visitLocation/text()' /></Field>
        <xsl:if test="indivodoc:specialty">
	  <Field name="specialty"><xsl:value-of select='indivodoc:specialty/text()' /></Field>
	  <Field name="specialty_type"><xsl:value-of select='indivodoc:specialty/@type' /></Field>
	  <Field name="specialty_value"><xsl:value-of select='indivodoc:specialty/@value' /></Field>
	  <Field name="specialty_abbrev"><xsl:value-of select='indivodoc:specialty/@abbrev' /></Field>
        </xsl:if>
	<xsl:if test="indivodoc:signature">
	  <Field name="signed_at"><xsl:value-of select="indivodoc:signature/indivodoc:at/text()" /></Field>
	  <Field name="provider_name"><xsl:value-of select="indivodoc:signature/indivodoc:provider/indivodoc:name/text()" /></Field>
	  <Field name="provider_institution"><xsl:value-of select="indivodoc:signature/indivodoc:provider/indivodoc:institution/text()" /></Field>
	</xsl:if>
        <Field name="chief_complaint"><xsl:value-of select='indivodoc:chiefComplaint/text()' /></Field>
        <Field name="content"><xsl:value-of select='indivodoc:content/text()' /></Field>
      </Model>
    </Models>
  </xsl:template>
</xsl:stylesheet>
