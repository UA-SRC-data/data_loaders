# Water Quality

To retrieve data:

- Go to https://www.waterqualitydata.us/
- Under Location, select 'US' and 'US:AZ' and 'UA:AZ:025' (Yavapai County, but I included Apache, Cochise, and Greenlea, too)
- Under Sampling Parameters, Sampling Media, select 'Water' and 'water'
- Under Sampling Parameters, Characteristic Group, select 'Inorganics, Major Metals' and 'Inorganics, Minor Metals'
- Under Select data to download, select 'Sample results (narrow)'
- Under File Format, select 'Comma-separated’

https://www.waterqualitydata.us/portal/#countrycode=US&statecode=US%3A04&countycode=US%3A04%3A001&countycode=US%3A04%3A003&countycode=US%3A04%3A011&countycode=US%3A04%3A025&sampleMedia=water&sampleMedia=Water&characteristicType=Inorganics%2C%20Major%2C%20Metals&characteristicType=Inorganics%2C%20Minor%2C%20Metals&mimeType=csv

## Data

Data looks like this:

```
// ****** Record 1 ****** //
OrganizationIdentifier                         : USGS-AZ
OrganizationFormalName                         : USGS Arizona Water Science Center
ActivityIdentifier                             : nwisaz.01.98500948
ActivityStartDate                              : 1985-04-25
ActivityStartTime/Time                         : 
ActivityStartTime/TimeZoneCode                 : 
MonitoringLocationIdentifier                   : USGS-09396100
ResultIdentifier                               : NWIS-48614982
DataLoggerLine                                 : 
ResultDetectionConditionText                   : 
MethodSpecificationName                        : 
CharacteristicName                             : Calcium
ResultSampleFractionText                       : Total
ResultMeasureValue                             : 310
ResultMeasure/MeasureUnitCode                  : mg/l CaCO3
MeasureQualifierCode                           : 
ResultStatusIdentifier                         : Historical
StatisticalBaseCode                            : 
ResultValueTypeName                            : Actual
ResultWeightBasisText                          : 
ResultTimeBasisText                            : 
ResultTemperatureBasisText                     : 
ResultParticleSizeBasisText                    : 
PrecisionValue                                 : 
DataQuality/BiasValue                          : 
ConfidenceIntervalValue                        : 
UpperConfidenceLimitValue                      : 
LowerConfidenceLimitValue                      : 
ResultCommentText                              : 
USGSPCode                                      : 00910
ResultDepthHeightMeasure/MeasureValue          : 
ResultDepthHeightMeasure/MeasureUnitCode       : 
ResultDepthAltitudeReferencePointText          : 
ResultSamplingPointName                        : 
BiologicalIntentName                           : 
BiologicalIndividualIdentifier                 : 
SubjectTaxonomicName                           : 
UnidentifiedSpeciesIdentifier                  : 
SampleTissueAnatomyName                        : 
GroupSummaryCountWeight/MeasureValue           : 
GroupSummaryCountWeight/MeasureUnitCode        : 
CellFormName                                   : 
CellShapeName                                  : 
HabitName                                      : 
VoltismName                                    : 
TaxonomicPollutionTolerance                    : 
TaxonomicPollutionToleranceScaleText           : 
TrophicLevelName                               : 
FunctionalFeedingGroupName                     : 
TaxonomicDetailsCitation/ResourceTitleName     : 
TaxonomicDetailsCitation/ResourceCreatorName   : 
TaxonomicDetailsCitation/ResourceSubjectText   : 
TaxonomicDetailsCitation/ResourcePublisherName : 
TaxonomicDetailsCitation/ResourceDate          : 
TaxonomicDetailsCitation/ResourceIdentifier    : 
FrequencyClassInformationUrl                   : 
ResultAnalyticalMethod/MethodIdentifier        : 
ResultAnalyticalMethod/MethodIdentifierContext : 
ResultAnalyticalMethod/MethodName              : 
ResultAnalyticalMethod/MethodUrl               : 
ResultAnalyticalMethod/MethodQualifierTypeName : 
MethodDescriptionText                          : 
LaboratoryName                                 : 
AnalysisStartDate                              : 
AnalysisStartTime/Time                         : 
AnalysisStartTime/TimeZoneCode                 : 
AnalysisEndDate                                : 
AnalysisEndTime/Time                           : 
AnalysisEndTime/TimeZoneCode                   : 
ResultLaboratoryCommentCode                    : 
ResultLaboratoryCommentText                    : 
ResultDetectionQuantitationLimitUrl            : 
LaboratoryAccreditationIndicator               : 
LaboratoryAccreditationAuthorityName           : 
TaxonomistAccreditationIndicator               : 
TaxonomistAccreditationAuthorityName           : 
LabSamplePreparationUrl                        : 
ProviderName                                   : NWIS
```

## Measurements

Run get_measurements.py to extract the 179 measurments:

* Field 12: CharacteristicName
* Field 15: ResultMeasure/MeasureUnitCode

