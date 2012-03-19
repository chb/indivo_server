<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:Medication">
    <Models>
      <Model name="Medication">
        <Field name="date_started"><xsl:value-of select='indivodoc:dateStarted/text()' /></Field>
        <Field name="date_stopped"><xsl:value-of select='indivodoc:dateStopped/text()' /></Field>
        <xsl:if test="indivodoc:name">
	  <Field name="name"><xsl:value-of select='indivodoc:name/text()' /></Field>
	  <Field name="name_type"><xsl:value-of select='indivodoc:name/@type' /></Field>
	  <Field name="name_value"><xsl:value-of select='indivodoc:name/@value' /></Field>
	  <Field name="name_abbrev"><xsl:value-of select='indivodoc:name/@abbrev' /></Field>
        </xsl:if>
        <xsl:if test="indivodoc:brandName">
	  <Field name="brand_name"><xsl:value-of select='indivodoc:brandName/text()' /></Field>
	  <Field name="brand_name_type"><xsl:value-of select='indivodoc:brandName/@type' /></Field>
	  <Field name="brand_name_value"><xsl:value-of select='indivodoc:brandName/@value' /></Field>
	  <Field name="brand_name_abbrev"><xsl:value-of select='indivodoc:brandName/@abbrev' /></Field>
        </xsl:if>
        <xsl:apply-templates select='indivodoc:dose' /> 
        <xsl:if test="indivodoc:route">
          <Field name="route"><xsl:value-of select='indivodoc:route/text()' /></Field>
          <Field name="route_type"><xsl:value-of select='indivodoc:route/@type' /></Field>
          <Field name="route_value"><xsl:value-of select='indivodoc:route/@value' /></Field>
          <Field name="route_abbrev"><xsl:value-of select='indivodoc:route/@abbrev' /></Field>
        </xsl:if>
        <xsl:apply-templates select='indivodoc:strength' />
        <xsl:if test="indivodoc:frequency">
          <Field name="frequency"><xsl:value-of select='indivodoc:frequency/text()' /></Field>
          <Field name="frequency_type"><xsl:value-of select='indivodoc:frequency/@type' /></Field>
          <Field name="frequency_value"><xsl:value-of select='indivodoc:frequency/@value' /></Field>
          <Field name="frequency_abbrev"><xsl:value-of select='indivodoc:frequency/@abbrev' /></Field>
        </xsl:if>

        <xsl:apply-templates select='indivodoc:prescription' />  
      </Model>
    </Models>
  </xsl:template>
  <xsl:template match="indivodoc:dose">
    <xsl:if test="indivodoc:textValue">
      <Field name="dose_textvalue"><xsl:value-of select='indivodoc:textValue/text()' /></Field>
    </xsl:if>
    <xsl:if test="indivodoc:value">
      <Field name="dose_value"><xsl:value-of select='indivodoc:value/text()' /></Field>
    </xsl:if>
    <xsl:if test="indivodoc:unit">
      <Field name="dose_unit">
        <xsl:value-of select='indivodoc:unit/text()' />
      </Field>
      <Field name="dose_unit_type"><xsl:value-of select='indivodoc:unit/@type' /></Field>
      <Field name="dose_unit_value"><xsl:value-of select='indivodoc:unit/@value' /></Field>
      <Field name="dose_unit_abbrev"><xsl:value-of select='indivodoc:unit/@abbrev' /></Field>
    </xsl:if>
  </xsl:template>

  <xsl:template match="indivodoc:strength">
    <xsl:if test="indivodoc:textValue">
      <Field name="strength_textvalue"><xsl:value-of select='indivodoc:textValue/text()' /></Field>
    </xsl:if>
    <xsl:if test="indivodoc:value">
      <Field name="strength_value">
        <xsl:value-of select='indivodoc:value/text()' />
      </Field>
    </xsl:if>
    <xsl:if test="indivodoc:unit">
      <Field name="strength_unit">
        <xsl:value-of select='indivodoc:unit/text()' />
      </Field>
      <Field name="strength_unit_type">
        <xsl:value-of select='indivodoc:unit/@type' />
      </Field>
      <Field name="strength_unit_value">
        <xsl:value-of select='indivodoc:unit/@value' />
      </Field>
      <Field name="strength_unit_abbrev">
        <xsl:value-of select='indivodoc:unit/@abbrev' />
      </Field>
    </xsl:if>
  </xsl:template>

  <xsl:template match="indivodoc:prescription">
    <xsl:if test="indivodoc:by">
      <Field name="prescribed_by_name">
        <xsl:value-of select='indivodoc:by/name/text()' />
      </Field>
      <Field name="prescribed_by_institution">
        <xsl:value-of select='indivodoc:by/institution/text()' />
      </Field>
    </xsl:if>
    <Field name="prescribed_on">
      <xsl:value-of select='indivodoc:on/text()' />
    </Field>
    <Field name="prescribed_stop_on">
      <xsl:value-of select='indivodoc:stopOn/text()' />
    </Field>
    <Field name="dispense_as_written">
      <xsl:value-of select='indivodoc:dispenseAsWritten/text()' />
    </Field>
    <Field name="prescription_duration">
      <xsl:value-of select='indivodoc:duration/text()' />
    </Field>
    <Field name="prescription_refill_info">
      <xsl:value-of select='indivodoc:refillInfo/text()' />
    </Field>
    <Field name="prescription_instructions">
      <xsl:value-of select='indivodoc:instructions/text()' />
    </Field>
  </xsl:template>
</xsl:stylesheet>
