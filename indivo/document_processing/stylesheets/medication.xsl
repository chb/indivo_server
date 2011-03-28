<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:Medication">
    <facts>
      <fact>
        <date_started><xsl:value-of select='indivodoc:dateStarted/text()' /></date_started>
        <date_stopped><xsl:value-of select='indivodoc:dateStopped/text()' /></date_stopped>
        <xsl:if test="indivodoc:name">
	        <name><xsl:value-of select='indivodoc:name/text()' /></name>
	        <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
	        <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
	        <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
        </xsl:if>
        <xsl:if test="indivodoc:brandName">
	        <brand_name><xsl:value-of select='indivodoc:brandName/text()' /></brand_name>
	        <brand_name_type><xsl:value-of select='indivodoc:brandName/@type' /></brand_name_type>
	        <brand_name_value><xsl:value-of select='indivodoc:brandName/@value' /></brand_name_value>
	        <brand_name_abbrev><xsl:value-of select='indivodoc:brandName/@abbrev' /></brand_name_abbrev>
        </xsl:if>
        <xsl:apply-templates select='indivodoc:dose' /> 
        <xsl:if test="indivodoc:route">
          <route><xsl:value-of select='indivodoc:route/text()' /></route>
          <route_type><xsl:value-of select='indivodoc:route/@type' /></route_type>
          <route_value><xsl:value-of select='indivodoc:route/@value' /></route_value>
          <route_abbrev><xsl:value-of select='indivodoc:route/@abbrev' /></route_abbrev>
        </xsl:if>
        <xsl:apply-templates select='indivodoc:strength' />
        <xsl:if test="indivodoc:frequency">
          <frequency><xsl:value-of select='indivodoc:frequency/text()' /></frequency>
          <frequency_type><xsl:value-of select='indivodoc:frequency/@type' /></frequency_type>
          <frequency_value><xsl:value-of select='indivodoc:frequency/@value' /></frequency_value>
          <frequency_abbrev><xsl:value-of select='indivodoc:frequency/@abbrev' /></frequency_abbrev>
        </xsl:if>

        <xsl:apply-templates select='indivodoc:prescription' />  
      </fact>
    </facts>
  </xsl:template>
  <xsl:template match="indivodoc:dose">
    <xsl:if test="indivodoc:textValue">
      <dose_textvalue><xsl:value-of select='indivodoc:textValue/text()' /></dose_textvalue>
    </xsl:if>
    <xsl:if test="indivodoc:value">
      <dose_value><xsl:value-of select='indivodoc:value/text()' /></dose_value>
    </xsl:if>
    <xsl:if test="indivodoc:unit">
      <dose_unit>
        <xsl:value-of select='indivodoc:unit/text()' />
      </dose_unit>
      <dose_unit_type><xsl:value-of select='indivodoc:unit/@type' /></dose_unit_type>
      <dose_unit_value><xsl:value-of select='indivodoc:unit/@value' /></dose_unit_value>
      <dose_unit_abbrev><xsl:value-of select='indivodoc:unit/@abbrev' /></dose_unit_abbrev>
    </xsl:if>
  </xsl:template>

  <xsl:template match="indivodoc:strength">
    <xsl:if test="indivodoc:textValue">
      <strength_textvalue><xsl:value-of select='indivodoc:textValue/text()' /></strength_textvalue>
    </xsl:if>
    <xsl:if test="indivodoc:value">
      <strength_value>
        <xsl:value-of select='indivodoc:value/text()' />
      </strength_value>
    </xsl:if>
    <xsl:if test="indivodoc:unit">
      <strength_unit>
        <xsl:value-of select='indivodoc:unit/text()' />
      </strength_unit>
      <strength_unit_type>
        <xsl:value-of select='indivodoc:unit/@type' />
      </strength_unit_type>
      <strength_unit_value>
        <xsl:value-of select='indivodoc:unit/@value' />
      </strength_unit_value>
      <strength_unit_abbrev>
        <xsl:value-of select='indivodoc:unit/@abbrev' />
      </strength_unit_abbrev>
    </xsl:if>
  </xsl:template>

  <xsl:template match="indivodoc:prescription">
    <xsl:if test="indivodoc:by">
      <prescribed_by_name>
        <xsl:value-of select='indivodoc:by/name/text()' />
      </prescribed_by_name>
      <prescribed_by_institution>
        <xsl:value-of select='indivodoc:by/institution/text()' />
      </prescribed_by_institution>
    </xsl:if>
    <prescribed_on>
      <xsl:value-of select='indivodoc:on/text()' />
    </prescribed_on>
    <prescribed_stop_on>
      <xsl:value-of select='indivodoc:stopOn/text()' />
    </prescribed_stop_on>
    <dispense_as_written>
      <xsl:value-of select='indivodoc:dispenseAsWritten/text()' />
    </dispense_as_written>
    <prescription_duration>
      <xsl:value-of select='indivodoc:duration/text()' />
    </prescription_duration>
    <prescription_refill_info>
      <xsl:value-of select='indivodoc:refillInfo/text()' />
    </prescription_refill_info>
    <prescription_instructions>
      <xsl:value-of select='indivodoc:instructions/text()' />
    </prescription_instructions>
  </xsl:template>
</xsl:stylesheet>
