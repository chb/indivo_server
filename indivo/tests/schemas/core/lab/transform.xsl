<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"
		xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:Lab">
    <Models>
      <Model name="Lab">
        <Field name="date_measured"><xsl:value-of select='indivodoc:dateMeasured/text()' /></Field>
        <Field name="lab_type"><xsl:value-of select='indivodoc:labType/text()' /></Field>
        <Field name="lab_name"><xsl:value-of select='indivodoc:laboratory/indivodoc:name/text()' /></Field>
        <Field name="lab_address"><xsl:value-of select='indivodoc:laboratory/indivodoc:address/text()' /></Field>
        <Field name="lab_comments"><xsl:value-of select='indivodoc:comments/text()' /></Field>

	<xsl:if test="indivodoc:labPanel">
	  <Field name="first_panel_name"><xsl:value-of select='indivodoc:labPanel/indivodoc:name/text()' /></Field>
	</xsl:if>

	<xsl:choose>
	  <xsl:when test="indivodoc:labTest">
	    <Field name="first_lab_test_name"><xsl:value-of select='indivodoc:labTest/indivodoc:name/text()' /></Field>
	    <xsl:apply-templates select='indivodoc:labTest[1]/indivodoc:result' />
	  </xsl:when>
	  <xsl:otherwise>
<!--	    <xsl:if test="count(indivodoc:labPanel/indivodoc:labTest) = 1">
	      <first_lab_test_name><xsl:value-of select='indivodoc:labPanel/indivodoc:labTest/indivodoc:name/text()' /></first_lab_test_name>
	      <xsl:apply-templates select='indivodoc:labPanel/indivodoc:labTest[1]/indivodoc:result' />
	    </xsl:if>-->
	  </xsl:otherwise>
	</xsl:choose>
      </Model>
    </Models>
  </xsl:template>

  <xsl:template match="indivodoc:result">
    <Field name="first_lab_test_value">
    <xsl:if test="indivodoc:valueAndUnit">
      <xsl:choose>
	<xsl:when test="indivodoc:valueAndUnit/indivodoc:value">
	  <xsl:value-of select="indivodoc:valueAndUnit/indivodoc:value/text()" />  <xsl:value-of select="indivodoc:valueAndUnit/indivodoc:unit/text()" />
	</xsl:when>
	<xsl:otherwise>
	  <xsl:value-of select="indivodoc:valueAndUnit/indivodoc:textValue/text()" />
	</xsl:otherwise>
      </xsl:choose>
    </xsl:if>
    <xsl:if test="indivodoc:value">
      <xsl:value-of select="indivodoc:value" />
    </xsl:if>
    </Field>
    
    <xsl:if test="indivodoc:valueAndUnit or indivodoc:value">
      <xsl:if test="indivodoc:normalRange/indivodoc:minimum">
	<Field name="normal_range_minimum"><xsl:value-of select="indivodoc:normalRange/indivodoc:minimum/text()"/>
	  <xsl:if test="indivodoc:normalRange/indivodoc:unit">
	    <xsl:value-of select="indivodoc:normalRange/indivodoc:unit/@indivodoc:abbrev"/>
	  </xsl:if>
	</Field>
      </xsl:if>
      
      <xsl:if test="indivodoc:normalRange/indivodoc:maximum">
	<Field name="normal_range_maximum"><xsl:value-of select="indivodoc:normalRange/indivodoc:maximum/text()"/>
	  <xsl:if test="indivodoc:normalRange/indivodoc:unit">
	    <xsl:value-of select="indivodoc:normalRange/indivodoc:unit/@indivodoc:abbrev"/>
	  </xsl:if>
	</Field>
      </xsl:if>
      
      <xsl:if test="indivodoc:nonCriticalRange/indivodoc:minimum">
	<Field name="non_critical_range_minimum"><xsl:value-of select="indivodoc:nonCriticalRange/indivodoc:minimum/text()"/>
	  <xsl:if test="indivodoc:nonCriticalRange/indivodoc:unit">
	    <xsl:value-of select="indivodoc:nonCriticalRange/indivodoc:unit/@indivodoc:abbrev"/>
	  </xsl:if>
	</Field>
      </xsl:if>
      
      <xsl:if test="indivodoc:nonCriticalRange/indivodoc:maximum">
	<Field name="non_critical_range_maximum"><xsl:value-of select="indivodoc:nonCriticalRange/indivodoc:maximum/text()"/>
	  <xsl:if test="indivodoc:nonCriticalRange/indivodoc:unit">
	    <xsl:value-of select="indivodoc:nonCriticalRange/indivodoc:unit/@indivodoc:abbrev"/>
	  </xsl:if>
	</Field>
      </xsl:if>
      
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>
