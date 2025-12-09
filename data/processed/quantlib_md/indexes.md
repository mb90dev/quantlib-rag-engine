# Indexes

QuantLib provides a set of classes that represent various types of Indexes.

The available classes under the **Interest Rate Indexes** are:

`IborIndex`

`OvernightIndex`

`SpreadIndex`

`SwapSpreadIndex`


The available classes under the **Inflation Indexes** are:

`InflationIndex`

`ZeroInflationIndex`

`YoYInflationIndex`


The class that defines that main interface for all the following classes is the purely abstract `Index`

class

## Index

-
*class*Index The Index class defines the following methods that every subclass inherits:

- name()
Returns the name of the index.

- Returns:
The name of the index.

- Return type:
str



- fixingCalendar()
Returns the calendar defining valid fixing dates for the index.

- Returns:
The fixing calendar.

- Return type:
ql.Calendar



-
isValidFixingDate(
*fixingDate: ql.Date*) Checks if the given date is a valid fixing date for the index.

- Parameters:
**fixingDate**(*ql.Date*) – The date to check.- Returns:
True if the date is a valid fixing date, False otherwise.

- Return type:
bool



-
hasHistoricalFixing(
*fixingDate: ql.Date*) Returns whether a historical fixing was stored for the given date.

- Parameters:
**fixingDate**(*ql.Date*) – The date to check.- Returns:
True if a historical fixing exists for the date, False otherwise.

- Return type:
bool



-
fixing(
*fixingDate: ql.Date*,*forecastTodaysFixing: bool = False*) Returns the fixing for the given date.

- Parameters:
**fixingDate**(*ql.Date*) – The date for which the fixing is requested.**forecastTodaysFixing**(*bool*) – If True, today’s fixing is forecasted instead of retrieved from history.

- Returns:
The fixing value.

- Return type:
float



-
pastFixing(
*fixingDate: ql.Date*) Returns a past fixing for the given date.

- Parameters:
**fixingDate**(*ql.Date*) – The date for which the past fixing is requested.- Returns:
The past fixing value.

- Return type:
float



- timeSeries()
Returns the time series of historical fixings for the index.

- Returns:
The time series of fixings.

- Return type:
ql.TimeSeries



- allowsNativeFixings()
Returns whether the index allows for native fixings.

- Returns:
True if native fixings are allowed, False otherwise.

- Return type:
bool



-
addFixing(
*fixingDate: ql.Date*,*fixing: float*,*forceOverwrite: bool = False*) Stores a historical fixing at the given date.

- Parameters:
**fixingDate**(*ql.Date*) – The date of the fixing.**fixing**(*float*) – The fixing value.**forceOverwrite**(*bool*) – If True, overwrites any existing fixing for the date.



-
addFixings(
*timeSeries: ql.TimeSeries*,*forceOverwrite: bool = False*) Stores historical fixings from a time series.

- Parameters:
**timeSeries**(*ql.TimeSeries*) – The time series of fixings to add.**forceOverwrite**(*bool*) – If True, overwrites any existing fixings for the dates.



- clearFixings()
Clears all stored historical fixings for the index.



## IndexManager

To avoid discrepancies between the indexes themselves QuantLib employes a unique global repository for the various registered indexes under the `IndexManager`

class.
`IndexManager`

basically stores for each index added a timeseries of the past fixings.

The public methods that `IndexManager`

exposes are:

The `IndexManager`

instance can be accessed thought:

```
ql.IndexManager.instance()
```

## Interest Rate

In the following block there are going to be listed all the classes that are subclasses of the `InterestRateIndex`

class.
`InterestRateIndex`

class itself if a child class of the `Index`

class and serves as the abstract base for all interest rate indexes in QuantLib, including IBOR and overnight indexes.

-
*class*InterestRateIndex Base class for interest rate indexes.

This class extends

`Index`

and provides the common interface for all interest rate indexes in QuantLib, such as Ibor and Overnight indexes. It is not meant to be instantiated directly, but provides additional methods for tenor, currency, day count, and date calculations.**Additional Methods**- familyName()
Returns the family name of the index.

- Returns:
The family name.

- Return type:
str



- tenor()
Returns the tenor (e.g., 3M, 6M) of the index.

- Returns:
The tenor.

- Return type:
ql.Period



- fixingDays()
Returns the number of fixing days for the index.

- Returns:
The number of fixing days.

- Return type:
int



- currency()
Returns the currency of the index.

- Returns:
The currency.

- Return type:
ql.Currency



- dayCounter()
Returns the day count convention used by the index.

- Returns:
The day counter.

- Return type:
ql.DayCounter



-
fixingDate(
*valueDate: ql.Date*) Returns the fixing date corresponding to a given value date.

- Parameters:
**valueDate**(*ql.Date*) – The value date.- Returns:
The fixing date.

- Return type:
ql.Date



-
valueDate(
*fixingDate: ql.Date*) Returns the value date corresponding to a given fixing date.

- Parameters:
**fixingDate**(*ql.Date*) – The fixing date.- Returns:
The value date.

- Return type:
ql.Date



-
maturityDate(
*valueDate: ql.Date*) Returns the maturity date corresponding to a given value date.

- Parameters:
**valueDate**(*ql.Date*) – The value date.- Returns:
The maturity date.

- Return type:
ql.Date



-
forecastFixing(
*fixingDate: ql.Date*) Returns the forecasted fixing for the given fixing date.

- Parameters:
**fixingDate**(*ql.Date*) – The fixing date.- Returns:
The forecasted fixing value.

- Return type:
float




### IborIndex

-
*class*IborIndex(*familyName: str*,*tenor: ql.Period*,*settlementDays: int*,*currency: ql.Currency*,*fixingCalendar: ql.Calendar*,*convention: ql.Convention*,*endOfMonth: bool*,*dayCounter: ql.DayCounter*,*h: ql.YieldTermStructureHandle = ql.YieldTermStructureHandle()*) Base class for Interbank Offered Rate (IBOR) indexes.

- Parameters:
**familyName**(*str*) – The name of the index family (e.g., “Euribor”, “Libor”).**tenor**(*ql.Period*) – The tenor of the index (e.g., 3M, 6M).**settlementDays**(*int*) – Number of settlement days.**currency**(*ql.Currency*) – The currency of the index.**fixingCalendar**(*ql.Calendar*) – The calendar used for fixing dates.**convention**(*ql.Convention*) – The business day convention for the index.**endOfMonth**(*bool*) – Whether end-of-month adjustment is used.**dayCounter**(*ql.DayCounter*) – The day count convention for interest calculation.**h**(*Optional**[**ql.YieldTermStructureHandle**]*) – (Optional) The yield term structure handle used for forecasting fixings.

- Returns:
An instance of IborIndex.

- Return type:
ql.IborIndex


**Example:**

```
ql.IborIndex('MyIndex', ql.Period('6m'), 2, ql.EURCurrency(), ql.TARGET(), ql.ModifiedFollowing, True, ql.Actual360())
ql.Libor('MyIndex', ql.Period('6M'), 2, ql.USDCurrency(), ql.TARGET(), ql.Actual360())
ql.Euribor(ql.Period('6M'))
ql.USDLibor(ql.Period('6M'))
ql.Euribor6M()
```

The most notable derived classes are:

`ql.Euribor()`

`ql.Euribor1M()`

`ql.Euribor3M()`

`ql.Euribor6M()`

`ql.GBPLibor()`

`ql.USDLibor()`

`ql.CHFLibor()`


The `IborIndex`

other subclasses can be found under ql/indexes/ibor (in QuantLib C++ Library).

Constructors for derived classes:

-
*class*Euribor(*tenor: ql.Period*)

-
*class*Euribor(*tenor: ql.Period*,*yts: ql.YieldTermStructureHandle*)

While for Fixed Tenor classes (like `ql.Euribor3M`

) the constructor is the following

-
*class*Euribor6M(*yts: ql.YieldTermStructureHandle*)

From QuantLib 1.39 the class `CustomIborIndex`

will be available, which lets you define a LIBOR-like index that allows specifying custom calendars for value and maturity date calculations.

-
*class*CustomIborIndex(*familyName: str*,*tenor: ql.Period*,*settlementDays: int*,*currency: ql.Currency*,*fixingCalendar: ql.Calendar*,*valueCalendar: ql.Calendar*,*maturityCalendar: ql.Calendar*,*convention: ql.BusinessDayConvention*,*endOfMonth: bool*,*dayCounter: ql.DayCounter*,*h: ql.YieldTermStructureHandle | None = None*) - Typical LIBOR indexes use:
fixingCalendar = valueCalendar = UK, maturityCalendar = JoinHolidays(UK, CurrencyCalendar) for non-EUR currencies.

fixingCalendar = JoinHolidays(UK, TARGET), valueCalendar = maturityCalendar = TARGET for EUR.



- Parameters:
**familyName**(*str*) – The name of the index family (e.g., “USD-LIBOR”, “EURIBOR”).**tenor**(*ql.Period*) – The tenor of the index (e.g., 3M, 6M).**settlementDays**(*int*) – The number of settlement days for the index.**currency**(*ql.Currency*) – The currency of the index.**fixingCalendar**(*ql.Calendar*) – The calendar used for fixing dates.**valueCalendar**(*ql.Calendar*) – The calendar used for value date calculations.**maturityCalendar**(*ql.Calendar*) – The calendar used for maturity date calculations.**convention**(*ql.BusinessDayConvention*) – The business day convention for date adjustments.**endOfMonth**(*bool*) – Whether end-of-month adjustment is used.**dayCounter**(*ql.DayCounter*) – The day count convention used for interest calculation.**h**(*Optional**[**ql.YieldTermStructureHandle**]*) – (Optional) The yield term structure used to forecast fixings. If not provided, it can be linked later.


The

`CustomIborIndex`

expose the following methods:-
valueDate(
*fixingDate: ql.Date*) Advances the given

`fixingDate`

on the valueCalendar and adjusts on the maturityCalendar.- Returns:
The new adjusted date.

- Return type:
ql.Date



-
maturityDate(
*valueDate: ql.Date*) Advances the given

`valueDate`

on the maturityCalendar.- Returns:
The new adjusted date.

- Return type:
ql.Date



-
fixingDate(
*valueDate: float*) Draw back the given

`fixingDate`

minus the`settlementDays`

on the valueCalendar.- Returns:
The new adjusted date.

- Return type:
ql.Date




### OvernightIndex

-
*class*OvernightIndex(*familyName: str*,*settlementDays: int*,*currency: ql*,*Currency*,*fixingCalendar: ql.Calendar*,*dayCounter: ql.DayCounter*,*h: ql.YieldTermStructureHandle | None*) Base class for overnight interbank offered rate indexes (e.g., ESTR, SOFR, SONIA).

- Parameters:
**familyName**(*str*) – The name of the index family (e.g., “EONIA”, “FedFunds”, “SONIA”).**settlementDays**(*int*) – The number of settlement days for the index.**currency**(*ql.Currency*) – The currency of the index.**fixingCalendar**(*ql.Calendar*) – The calendar used for fixing dates.**dayCounter**(*ql.DayCounter*) – The day count convention used for interest calculation.**yieldTermStructure**(*Optional**[**ql.YieldTermStructureHandle**]*) – (Optional) The yield term structure used to forecast fixings. If not provided, it can be linked later.


**Example**

```
name = 'CNYRepo7D'
fixingDays = 1
currency = ql.CNYCurrency()
calendar = ql.China()
dayCounter = ql.Actual365Fixed()
overnight_index = ql.OvernightIndex(name, fixingDays, currency, calendar, dayCounter)
```

The most notable derived classes are:

`ql.Estr()`

`ql.Sofr()`

`ql.Sonia()`

`ql.Saron()`

`ql.Aonia()`

`ql.Corra()`

`ql.Kofr()`


The `OvernightIndex`

other subclasses can be found under ql/indexes/ibor (in QuantLib C++ Library).

### SwapIndex

-
*class*SwapIndex(*familyName: str*,*tenor: ql.Period*,*settlementDays: int*,*currency: ql.Currency*,*fixingCalendar: ql.Calendar*,*fixedLegTenor: ql.Period*,*fixedLegConvention: ql.BusinessDayConvention*,*fixedLegDayCounter: ql.DayCounter*,*index: ql.IborIndex*) Main constructor for SwapIndex.

- Parameters:
**familyName**(*str*) – The name of the swap index family (e.g., “EuriborSwapIsdaFixA”).**tenor**(*ql.Period*) – The tenor of the swap (e.g., 5Y, 10Y).**settlementDays**(*int*) – Number of settlement days for the swap.**currency**(*ql.Currency*) – The currency of the swap.**fixingCalendar**(*ql.Calendar*) – The calendar used for fixing dates.**fixedLegTenor**(*ql.Period*) – The tenor of the fixed leg payments (e.g., 1Y).**fixedLegConvention**– The business day convention for the fixed leg.**fixedLegDayCounter**– The day count convention for the fixed leg.**index**(*ql.IborIndex*) – The floating leg Ibor index.



-
*class*SwapIndex(*familyName: str*,*tenor: ql.Period*,*settlementDays: int*,*currency: ql.Currency*,*fixingCalendar: ql.Calendar*,*fixedLegTenor: ql.Period*,*fixedLegConvention: ql.BusinessDayConvention*,*fixedLegDayCounter: ql.DayCounter*,*index: ql.IborIndex*,*discountingTermStructure: ql.YieldTermStructureHandle*) Alternate constructor with explicit discounting term structure.

- Parameters:
**familyName**(*str*) – The name of the swap index family (e.g., “EuriborSwapIsdaFixA”).**tenor**(*ql.Period*) – The tenor of the swap (e.g., 5Y, 10Y).**settlementDays**(*int*) – Number of settlement days for the swap.**currency**(*ql.Currency*) – The currency of the swap.**fixingCalendar**(*ql.Calendar*) – The calendar used for fixing dates.**fixedLegTenor**(*ql.Period*) – The tenor of the fixed leg payments (e.g., 1Y).**fixedLegConvention**– The business day convention for the fixed leg.**fixedLegDayCounter**– The day count convention for the fixed leg.**index**(*ql.IborIndex*) – The floating leg Ibor index.**discountingTermStructure**(*ql.YieldTermStructureHandle*) – The yield term structure used for discounting.


-
underlyingSwap(
*fixingDate: ql.Date*) returns a

`ql.Swap`

(either a`VanillaSwap`

or an`OvernightIndexedSwap`

) that represents the underlying swap for the given fixing date.- Parameters:
**fixingDate**– The given fixingDate- Returns:
The new adjusted date.

- Return type:
ql.Date




Derived Classes:

`ql.ChfLiborSwapIsdaFix`

`ql.EuriborSwapIsdaFixA`

`ql.EuriborSwapIsdaFixB`

`ql.EuriborSwapIfrFix`

`ql.EurLiborSwapIfrFix`

`ql.EurLiborSwapIsdaFixA`

`ql.EurLiborSwapIsdaFixB`

`ql.GbpLiborSwapIsdaFix`

`ql.JpyLiborSwapIsdaFixAm`

`ql.JpyLiborSwapIsdaFixPm`

`ql.OvernightIndexedSwapIndex`

`ql.UsdLiborSwapIsdaFixAm`

`ql.UsdLiborSwapIsdaFixPm`


Constructors for derived classes:

-
*class*ql.EuriborSwapIsdaFixA(*period: ql.Period*)

-
*class*ql.EuriborSwapIsdaFixA(*period: ql.Period*,*yts: ql.YieldTermStructureHandle*)

-
*class*ql.EuriborSwapIsdaFixA(*period: ql.Period*,*forward_yts: ql.YieldTermStructureHandle*,*discounting_yts: ql.YieldTermStructureHandle*)

### SwapSpreadIndex

-
*class*SwapSpreadIndex(*familyName: str*,*swapIndex1: ql.SwapIndex*,*swapIndex2: ql.SwapIndex*,*gearing1: float = 1.0*,*gearing2: float = -1.0*) Constructor for swap-rate spread indexes objects

- Parameters:
**familyName**(*str*) – The name of the swap spread index family (e.g., “EuriborSwapSpread”).**swapIndex1**(*ql.SwapIndex*) – The first swap index in the spread.**swapIndex2**(*ql.SwapIndex*) – The second swap index in the spread.**gearing1**(*float*) – The multiplier applied to the first swap index (default is 1.0).**gearing2**(*float*) – The multiplier applied to the second swap index (default is -1.0).


**Example**:

```
cms10y = ql.EuriborSwapIsdaFixA(ql.Period(10, ql.Years), for_yts, disc_yts)
cms2y = ql.EuriborSwapIsdaFixA(ql.Period(2, ql.Years), for_yts, disc_yts)
cms10y2y = ql.SwapSpreadIndex("cms10y2y", cms10y, cms2y)
cms10y.addFixing(refDate, 0.05)
```

## Inflation

-
*class*InflationIndex(*familyName: str*,*region: ql.Region*,*revised: bool*,*frequency: ql.Frequency*,*availabilityLag: ql.Period*,*currency: ql.Currency*) Base class for inflation-rate index

- Parameters:
**familyName**(*str*) – The name of the inflation index family (e.g., “CPI”, “HICP”).**region**(*ql.Region*) – The geographical region for which the index is published.**revised**(*bool*) – Whether the index can be revised after publication.**frequency**(*ql.Frequency*) – The frequency with which the index is published (e.g., Monthly, Quarterly).**availabilityLag**(*ql.Period*) – The lag between the reference period and the publication date.**currency**(*ql.Currency*) – The currency in which the index is quoted.



### Zero Inflation

-
*class*ZeroInflationIndex(*familyName: str*,*region: ql.Region*,*revised: bool*,*frequency: ql.Frequency*,*availabilityLag: ql.Period*,*currency: ql.Currency*,*h: ql.ZeroInflationTermStructureHandle | None*) Base class for zero inflation indices.

- Parameters:
**familyName**(*str*) – The name of the zero inflation index family (e.g., “CPI”, “HICP”).**region**(*ql.Region*) – The geographical region for which the index is published.**revised**(*bool*) – Whether the index can be revised after publication.**frequency**(*ql.Frequency*) – The frequency with which the index is published (e.g., Monthly, Quarterly).**availabilityLag**(*ql.Period*) – The lag between the reference period and the publication date.**currency**(*ql.Currency*) – The currency in which the index is quoted.**h**(*Optional**[**ql.ZeroInflationTermStructureHandle**]*) – (Optional) The zero inflation term structure handle used for forecasting.



Notable derived classes:

`ql.UKRPI`

`ql.USCPI`

`ql.EUHICP`

`ql.EUHICPXT`


The `ZeroInflationIndex`

other subclasses can be found under ql/indexes/inflation (in QuantLib C++ Library).

### YoY inflation

-
*class*YoYInflationIndex(*familyName: str*,*region: ql.Region*,*revised: bool*,*frequency: ql.Frequency*,*availabilityLag: ql.Period*,*currency: ql.Currency*,*h: ql.ZeroInflationTermStructureHandle | None*) Constructor for quoted year-on-year indices. An index built with this constructor needs its past fixings (i.e., the past year-on-year values) to be stored via the

`addFixing`

or`addFixings`

method.- Parameters:
**familyName**(*str*) – The name of the year-on-year inflation index family (e.g., “YYCPI”, “YYHICP”).**region**(*ql.Region*) – The geographical region for which the index is published.**revised**(*bool*) – Whether the index can be revised after publication.**frequency**(*ql.Frequency*) – The frequency with which the index is published (e.g., Monthly, Quarterly).**availabilityLag**(*ql.Period*) – The lag between the reference period and the publication date.**currency**(*ql.Currency*) – The currency in which the index is quoted.**h**(*Optional**[**ql.ZeroInflationTermStructureHandle**]*) – (Optional) The zero inflation term structure handle used for forecasting.



-
*class*YoYInflationIndex(*underlyingIndex: ql.ZeroInflationIndex*,*ts: ql.YoYInflationTermStructureHandle | None*) Constructor for year-on-year indices defined as a ratio. An index build with this constructor won’t store past fixings of its own; they will be calculated as a ratio from the past fixings stored in the underlying index.

- Parameters:
**underlyingIndex**(*ql.ZeroInflationIndex*) – The underlying zero inflation index used to compute year-on-year values.**ts**(*Optional**[**ql.YoYInflationTermStructureHandle**]*) – (Optional) The year-on-year inflation term structure handle used for forecasting.



The `YoYInflationIndex`

other subclasses can be found under ql/indexes/inflation (in QuantLib C++ Library).

`ql.YYEUHICP`

`ql.YYEUHICPXT`

`ql.YYFRHICP`

`ql.YYUKRPI`

`ql.YYUSCPI`

`ql.YYZACPI`