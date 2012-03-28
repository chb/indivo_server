<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:Allergy">
    <Models>
      <Model name="Allergy">
        <Field name="date_diagnosed"><xsl:value-of select='indivodoc:dateDiagnosed/text()' /></Field>
        <Field name="diagnosed_by"><xsl:value-of select='indivodoc:diagnosedBy/text()' /></Field>

        <Field name="allergen_type"><xsl:value-of select='indivodoc:allergen/indivodoc:type/text()' /></Field>
        <Field name="allergen_type_type"><xsl:value-of select='indivodoc:allergen/indivodoc:type/@type' /></Field>
        <Field name="allergen_type_value"><xsl:value-of select='indivodoc:allergen/indivodoc:type/@value' /></Field>
        <Field name="allergen_type_abbrev"><xsl:value-of select='indivodoc:allergen/indivodoc:type/@abbrev' /></Field>

        <Field name="allergen_name"><xsl:value-of select='indivodoc:allergen/indivodoc:name/text()' /></Field>
        <Field name="allergen_name_type"><xsl:value-of select='indivodoc:allergen/indivodoc:name/@type' /></Field>
        <Field name="allergen_name_value"><xsl:value-of select='indivodoc:allergen/indivodoc:name/@value' /></Field>
        <Field name="allergen_name_abbrev"><xsl:value-of select='indivodoc:allergen/indivodoc:name/@abbrev' /></Field>

        <Field name="specifics"><xsl:value-of select='indivodoc:specifics/text()' /></Field>
        <Field name="reaction"><xsl:value-of select='indivodoc:reaction/text()' /></Field>
      </Model>
    </Models>
  </xsl:template>
</xsl:stylesheet>
