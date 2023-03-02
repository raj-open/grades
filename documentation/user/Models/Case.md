# Case
## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pathMinusinput** | [**String**](string.md) | Path to csv input file (including filename and extension). | [default to null]
**pathMinusoutput** | [**String**](string.md) | Path to output file (including filename and extension). | [default to null]
**tableMinusconfig** | [**TableConfig**](TableConfig.md) |  | [optional] [default to null]
**gradeMinusschema** | [**List**](Grade.md) | Key to grades as list.  **NOTE:** Sort this from _highest_ to _lowest_ grade! | [optional] [default to null]
**failMinusgrades** | [**List**](anyOf&lt;number,string,integer&gt;.md) | Value(s) of fail grade. | [optional] [default to []]
**removeMinusfail** | [**Boolean**](boolean.md) | Whether to filter out failing grades. | [optional] [default to false]
**title** | [**String**](string.md) | Title of plot. | [default to null]
**labelMinusfrequency** | [**String**](string.md) | Label for axis for frequency. | [optional] [default to Frequency]
**labelMinusfrequencyMinusrelative** | [**String**](string.md) | Label for axis for frequency. | [optional] [default to Frequency (%)]
**labelMinusgrades** | [**String**](string.md) | Label for axis for grades. | [optional] [default to Grades]
**labelMinuspoints** | [**String**](string.md) | Label for axis for points. | [optional] [default to Points]
**plotMinusorientation** | [**PLOTORIENTATION**](PLOTORIENTATION.md) |  | [optional] [default to null]
**asMinusgrades** | [**Boolean**](boolean.md) | Whether to present data by grades.  - if &#x60;True&#x60; data presented by grades-. - if &#x60;False&#x60; data presented by points but grouped by grades. | [optional] [default to false]
**relative** | [**Boolean**](boolean.md) | Whether to present histogram counts as absolute or relative frequencies. | [optional] [default to true]
**frequencyMinusrange** | [**List**](number.md) | Limits of frequency axis. | [optional] [default to null]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

