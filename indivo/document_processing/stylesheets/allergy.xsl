<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:Allergy">
    <facts>
      <fact>
        <date_diagnosed><xsl:value-of select='indivodoc:dateDiagnosed/text()' /></date_diagnosed>
        <diagnosed_by><xsl:value-of select='indivodoc:diagnosedBy/text()' /></diagnosed_by>

        <allergen_type><xsl:value-of select='indivodoc:allergen/indivodoc:type/text()' /></allergen_type>
        <allergen_type_type><xsl:value-of select='indivodoc:allergen/indivodoc:type/@type' /></allergen_type_type>
        <allergen_type_value><xsl:value-of select='indivodoc:allergen/indivodoc:type/@value' /></allergen_type_value>
        <allergen_type_abbrev><xsl:value-of select='indivodoc:allergen/indivodoc:type/@abbrev' /></allergen_type_abbrev>

        <allergen_name><xsl:value-of select='indivodoc:allergen/indivodoc:name/text()' /></allergen_name>
        <allergen_name_type><xsl:value-of select='indivodoc:allergen/indivodoc:name/@type' /></allergen_name_type>
        <allergen_name_value><xsl:value-of select='indivodoc:allergen/indivodoc:name/@value' /></allergen_name_value>
        <allergen_name_abbrev><xsl:value-of select='indivodoc:allergen/indivodoc:name/@abbrev' /></allergen_name_abbrev>

        <specifics><xsl:value-of select='indivodoc:specifics/text()' /></specifics>
        <reaction><xsl:value-of select='indivodoc:reaction/text()' /></reaction>
      </fact>
    </facts>
  </xsl:template>
</xsl:stylesheet>
