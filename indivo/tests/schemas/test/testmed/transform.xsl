<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#">
    <xsl:output method = "xml" indent = "yes" />
    <xsl:template match="indivodoc:TestMed">
        <Models>
            <Model name="TestMed">
                <Field name="date_started">
                    <xsl:value-of select='indivodoc:dateStarted/text()' />
                </Field>
                <xsl:if test="indivodoc:name">
                    <Field name="name">
                        <xsl:value-of select='indivodoc:name/text()' />
                    </Field>
                </xsl:if>
                <xsl:if test="indivodoc:brandName">
                    <Field name="brand_name">
                        <xsl:value-of select='indivodoc:brandName/text()' />
                    </Field>
                </xsl:if>
                <xsl:if test="indivodoc:frequency">
                    <Field name="frequency">
                        <xsl:value-of select='indivodoc:frequency/text()' />
                    </Field>
                </xsl:if>
                <Field name="prescription">
                    <xsl:apply-templates select="indivodoc:Prescription" />
                </Field>
                <Field name="fills">
                    <Models>
                        <xsl:apply-templates select="indivodoc:TestFills/indivodoc:TestFill" />
                    </Models>
                </Field>
            </Model>
        </Models>
    </xsl:template>
    <xsl:template match="indivodoc:Prescription">
        <Model name="TestPrescription">
            <xsl:if test="indivodoc:prescribedByName">
                <Field name="prescribed_by_name">
                    <xsl:value-of select='indivodoc:prescribedByName/text()' />
                </Field>
            </xsl:if>
            <xsl:if test="indivodoc:prescribedByInstitution">
                <Field name="prescribed_by_institution">
                    <xsl:value-of select='indivodoc:prescribedByInstitution/text()' />
                </Field>
            </xsl:if>
            <xsl:if test="indivodoc:prescribedOn">
                <Field name="prescribed_on">
                    <xsl:value-of select='indivodoc:prescribedOn/text()' />
                </Field>
            </xsl:if>
        </Model>
    </xsl:template>
    <xsl:template match="indivodoc:TestFill">
        <Model name="TestFill">
            <xsl:if test="indivodoc:dateFilled">
                <Field name="date_filled">
                    <xsl:value-of select='indivodoc:dateFilled/text()' />
                </Field>
            </xsl:if>
            <xsl:if test="indivodoc:supplyDays">
                <Field name="supply_days">
                    <xsl:value-of select='indivodoc:supplyDays/text()' />
                </Field>
            </xsl:if>
        </Model>
    </xsl:template>
</xsl:stylesheet>
