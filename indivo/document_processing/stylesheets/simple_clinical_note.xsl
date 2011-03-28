<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:SimpleClinicalNote">
    <facts>
      <fact>
        <date_of_visit><xsl:value-of select='indivodoc:dateOfVisit/text()' /></date_of_visit>
        <xsl:if test="indivodoc:finalizedAt">
          <finalized_at><xsl:value-of select='indivodoc:finalizedAt/text()' /></finalized_at>
	</xsl:if>
        <xsl:if test="indivodoc:visitType">
	        <visit_type><xsl:value-of select='indivodoc:visitType/text()' /></visit_type>
	        <visit_type_type><xsl:value-of select='indivodoc:visitType/@type' /></visit_type_type>
	        <visit_type_value><xsl:value-of select='indivodoc:visitType/@value' /></visit_type_value>
	        <visit_type_abbrev><xsl:value-of select='indivodoc:visitType/@abbrev' /></visit_type_abbrev>
        </xsl:if>
        <visit_location><xsl:value-of select='indivodoc:visitLocation/text()' /></visit_location>
        <xsl:if test="indivodoc:specialty">
	        <specialty><xsl:value-of select='indivodoc:specialty/text()' /></specialty>
	        <specialty_type><xsl:value-of select='indivodoc:specialty/@type' /></specialty_type>
	        <specialty_value><xsl:value-of select='indivodoc:specialty/@value' /></specialty_value>
	        <specialty_abbrev><xsl:value-of select='indivodoc:specialty/@abbrev' /></specialty_abbrev>
        </xsl:if>
	<xsl:if test="indivodoc:signature">
	  <signed_at><xsl:value-of select="indivodoc:signature/indivodoc:at/text()" /></signed_at>
	  <provider_name><xsl:value-of select="indivodoc:signature/indivodoc:provider/indivodoc:name/text()" /></provider_name>
	  <provider_institution><xsl:value-of select="indivodoc:signature/indivodoc:provider/indivodoc:institution/text()" /></provider_institution>
	</xsl:if>
        <chief_complaint><xsl:value-of select='indivodoc:chiefComplaint/text()' /></chief_complaint>
        <content><xsl:value-of select='indivodoc:content/text()' /></content>
      </fact>
    </facts>
  </xsl:template>
</xsl:stylesheet>
