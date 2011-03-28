<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:Immunization">
    <facts>
      <fact>
        <date_administered><xsl:value-of select='indivodoc:dateAdministered/text()' /></date_administered>
        <administered_by><xsl:value-of select='indivodoc:administeredBy/text()' /></administered_by>
        <xsl:apply-templates select='indivodoc:vaccine' />  
        <sequence><xsl:value-of select='indivodoc:sequence/text()' /></sequence>
        <anatomic_surface><xsl:value-of select='indivodoc:anatomicSurface/text()' /></anatomic_surface>
        <xsl:if test="indivodoc:anatomic_surface">
  	      <anatomic_surface_type><xsl:value-of select='indivodoc:anatomic_surface/@type' /></anatomic_surface_type>
  	      <anatomic_surface_value><xsl:value-of select='indivodoc:anatomic_surface/@value' /></anatomic_surface_value>
  	      <anatomic_surface_abbrev><xsl:value-of select='indivodoc:anatomic_surface/@abbrev' /></anatomic_surface_abbrev>
        </xsl:if>
        <adverse_event><xsl:value-of select='indivodoc:adverseEvent/text()' /></adverse_event>
      </fact>
    </facts>
  </xsl:template>
  <xsl:template match="indivodoc:vaccine">
    <vaccine_type><xsl:value-of select='indivodoc:type/text()' /></vaccine_type>
    <xsl:if test="indivodoc:type">
	    <vaccine_type_type><xsl:value-of select='indivodoc:type/@type' /></vaccine_type_type>
	    <vaccine_type_value><xsl:value-of select='indivodoc:type/@value' /></vaccine_type_value>
	    <vaccine_type_abbrev><xsl:value-of select='indivodoc:type/@abbrev' /></vaccine_type_abbrev>
    </xsl:if>
    <xsl:if test="indivodoc:manufacturer">
	    <vaccine_manufacturer><xsl:value-of select='indivodoc:manufacturer/text()' /></vaccine_manufacturer>
    </xsl:if>
    <xsl:if test="indivodoc:lot">
	    <vaccine_lot><xsl:value-of select='indivodoc:lot/text()' /></vaccine_lot>
    </xsl:if>
    <xsl:if test="indivodoc:expiration">
	    <vaccine_expiration><xsl:value-of select='indivodoc:expiration/text()' /></vaccine_expiration>
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>
