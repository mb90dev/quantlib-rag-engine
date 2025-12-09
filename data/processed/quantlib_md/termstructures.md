# Term Structures

QuantLib provides a module for the representation of different term structures used in Quantitative Finance. A term structure describe the evolution of any variable defined across maturities. Mathematically a term structure describe the stochastic evolution of a variable , indexed by current time and maturity , such that the processes satisfies no-arbitrage conditions and is consistent with observed market prices.

In QuantLib, term structures (represented as objects) are defined for several financial variables, the main categories are:

## Yield Term Structures

-
*class*YieldTermStructure Abstract base class for interest-rate term structures.

This class defines the interface for all concrete interest rate term structures in QuantLib. It is not meant to be instantiated directly, but provides the common API for all yield curve objects such as FlatForward, ZeroCurve, ForwardCurve, etc.

Child classes inherit the following important methods:

**Discount Factors**-
discount(
*date: ql.Date*,*extrapolate=False*)

-
discount(
*time: float*,*extrapolate=False*) Returns the discount factor from the given date or time to the reference date.

- Parameters:
**date**(*ql.Date*) – The date for which the discount factor is requested.**time**(*float*) – The time (in years) from the reference date.**extrapolate**(*bool*) – Whether to allow extrapolation beyond the curve’s range.

- Returns:
The discount factor.

- Return type:
float



**Zero-Yield Rates**-
zeroRate(
*date: ql.Date*,*dayCounter: ql.DayCounter*,*compounding: ql.Compounding*,*frequency=Annual*,*extrapolate=False*)

-
zeroRate(
*time: float*,*compounding: ql.Compounding*,*frequency=Annual*,*extrapolate=False*) Returns the implied zero-coupon yield for the given date or time.

- Parameters:
**date**(*ql.Date*) – The date for which the zero rate is requested.**time**(*float*) – The time (in years) from the reference date.**dayCounter**(*ql.DayCounter*) – The day count convention for the result.**compounding**(*ql.Compounding*) – The compounding convention (e.g., Continuous, Compounded).**frequency**(*ql.Frequency*) – The compounding frequency (default: Annual).**extrapolate**(*bool*) – Whether to allow extrapolation beyond the curve’s range.

- Returns:
The zero rate as a ql.InterestRate object.

- Return type:
ql.InterestRate



**Forward Rates**-
forwardRate(
*date1: ql.Date*,*date2: ql.Date*,*dayCounter: ql.DayCounter*,*compounding: ql.Compounding*,*frequency=Annual*,*extrapolate=False*)

-
forwardRate(
*date: ql.Date*,*period: ql.Period*,*dayCounter: ql.DayCounter*,*compounding: ql.Compounding*,*frequency=Annual*,*extrapolate=False*)

-
forwardRate(
*time1: float*,*time2: float*,*compounding: ql.Compounding*,*frequency=Annual*,*extrapolate=False*) Returns the forward rate between two dates or times.

- Parameters:
**date1**(*ql.Date*) – The start date.**date2**(*ql.Date*) – The end date.**period**(*ql.Period*) – The period from the start date.**time1**(*float*) – The start time (in years).**time2**(*float*) – The end time (in years).**dayCounter**(*ql.DayCounter*) – The day count convention for the result.**compounding**(*ql.Compounding*) – The compounding convention.**frequency**(*ql.Frequency*) – The compounding frequency (default: Annual).**extrapolate**(*bool*) – Whether to allow extrapolation beyond the curve’s range.

- Returns:
The forward rate as a ql.InterestRate object.

- Return type:
ql.InterestRate



**Jump Inspectors**- jumpDates()
Returns the list of dates at which jumps (discontinuities) in the curve occur.

- Returns:
List of jump dates.

- Return type:
list of ql.Date



- jumpTimes()
Returns the list of times (in years) at which jumps in the curve occur.

- Returns:
List of jump times.

- Return type:
list of float



**Notes**All concrete term structure classes (such as FlatForward, ZeroCurve, etc.) inherit these methods.

The discount, zeroRate, and forwardRate methods are the primary interface for querying the curve.

The extrapolate argument controls whether the curve can be queried outside its original range.


-
discount(

### FlatForward

Flat interest-rate curve.

-
ql.FlatForward(
*date*,*quote*,*dayCounter*,*compounding*,*frequency*)

-
ql.FlatForward(
*integer*,*Calendar*,*quote*,*dayCounter*,*compounding*,*frequency*)

-
ql.FlatForward(
*integer*,*rate*,*dayCounter*)

Examples:

```
ql.FlatForward(ql.Date(15,6,2020), ql.QuoteHandle(ql.SimpleQuote(0.05)), ql.Actual360(), ql.Compounded, ql.Annual)
ql.FlatForward(ql.Date(15,6,2020), ql.QuoteHandle(ql.SimpleQuote(0.05)), ql.Actual360(), ql.Compounded)
ql.FlatForward(ql.Date(15,6,2020), ql.QuoteHandle(ql.SimpleQuote(0.05)), ql.Actual360())
ql.FlatForward(2, ql.TARGET(), ql.QuoteHandle(ql.SimpleQuote(0.05)), ql.Actual360())
ql.FlatForward(2, ql.TARGET(), 0.05, ql.Actual360())
```

### DiscountCurve

Term structure based on log-linear interpolation of discount factors.

-
ql.DiscountCurve(
*dates*,*dfs*,*dayCounter*,*cal=ql.NullCalendar()*)

Example:

```
dates = [ql.Date(7,5,2019), ql.Date(7,5,2020), ql.Date(7,5,2021)]
dfs = [1, 0.99, 0.98]
dayCounter = ql.Actual360()
curve = ql.DiscountCurve(dates, dfs, dayCounter)
```

### ZeroCurve

ZeroCurve

LogLinearZeroCurve

CubicZeroCurve

NaturalCubicZeroCurve

LogCubicZeroCurve

MonotonicCubicZeroCurve


-
ql.ZeroCurve(
*dates*,*yields*,*dayCounter*,*cal*,*i*,*comp*,*freq*)

Dates |
The date sequence, the maturity date corresponding to the zero interest rate. Note: The first date must be the base date of the curve, such as a date with a yield of 0.0. |
yields |
a sequence of floating point numbers, zero coupon yield |
dayCounter |
DayCounter object, number of days calculation rule |
cal |
Calendar object, calendar |
i |
Linear object, linear interpolation method |
comp and freq |
are preset integers indicating the way and frequency of payment |

```
dates = [ql.Date(31,12,2019), ql.Date(31,12,2020), ql.Date(31,12,2021)]
zeros = [0.01, 0.02, 0.03]
ql.ZeroCurve(dates, zeros, ql.ActualActual(), ql.TARGET())
ql.LogLinearZeroCurve(dates, zeros, ql.ActualActual(), ql.TARGET())
ql.CubicZeroCurve(dates, zeros, ql.ActualActual(), ql.TARGET())
ql.NaturalCubicZeroCurve(dates, zeros, ql.ActualActual(), ql.TARGET())
ql.LogCubicZeroCurve(dates, zeros, ql.ActualActual(), ql.TARGET())
ql.MonotonicCubicZeroCurve(dates, zeros, ql.ActualActual(), ql.TARGET())
```

### ForwardCurve

Term structure based on flat interpolation of forward rates.

-
ql.ForwardCurve(
*dates*,*rates*,*dayCounter*)

-
ql.ForwardCurve(
*dates*,*rates*,*dayCounter*,*calendar*,*BackwardFlat*)

-
ql.ForwardCurve(
*dates*,*date*,*rates*,*rate*,*dayCounter*,*calendar*)

-
ql.ForwardCurve(
*dates*,*date*,*rates*,*rate*,*dayCounter*)

```
dates = [ql.Date(15,6,2020), ql.Date(15,6,2022), ql.Date(15,6,2023)]
rates = [0.02, 0.03, 0.04]
ql.ForwardCurve(dates, rates, ql.Actual360(), ql.TARGET())
ql.ForwardCurve(dates, rates, ql.Actual360())
```

### Piecewise

Piecewise yield term structure. This term structure is bootstrapped on a number of interest rate instruments which are passed as a vector of RateHelper instances. Their maturities mark the boundaries of the interpolated segments.

Each segment is determined sequentially starting from the earliest period to the latest and is chosen so that the instrument whose maturity marks the end of such segment is correctly repriced on the curve.

PiecewiseLogLinearDiscount

PiecewiseLogCubicDiscount

PiecewiseLinearZero

PiecewiseCubicZero

PiecewiseLinearForward

PiecewiseSplineCubicDiscount


-
ql.Piecewise(
*referenceDate*,*helpers*,*dayCounter*)

```
helpers = []
helpers.append( ql.DepositRateHelper(0.05, ql.Euribor6M()) )
helpers.append(
ql.SwapRateHelper(0.06, ql.EuriborSwapIsdaFixA(ql.Period('1y')))
)
curve = ql.PiecewiseLogLinearDiscount(ql.Date(15,6,2020), helpers, ql.Actual360())
```

-
ql.PiecewiseYieldCurve(
*referenceDate*,*instruments*,*dayCounter*,*jumps*,*jumpDate*,*i=Interpolator()*,*bootstrap=bootstrap_type()*)

```
referenceDate = ql.Date(15,6,2020)
ql.PiecewiseLogLinearDiscount(referenceDate, helpers, ql.ActualActual())
jumps = [ql.QuoteHandle(ql.SimpleQuote(0.01))]
ql.PiecewiseLogLinearDiscount(referenceDate, helpers, ql.ActualActual(), jumps)
jumpDates = [ql.Date(15,9,2020)]
ql.PiecewiseLogLinearDiscount(referenceDate, helpers, ql.ActualActual(), jumps, jumpDates)
```

```
import pandas as pd
pgbs = pd.DataFrame(
{'maturity': ['15-06-2020', '15-04-2021', '17-10-2022', '25-10-2023',
'15-02-2024', '15-10-2025', '21-07-2026', '14-04-2027',
'17-10-2028', '15-06-2029', '15-02-2030', '18-04-2034',
'15-04-2037', '15-02-2045'],
'coupon': [4.8, 3.85, 2.2, 4.95, 5.65, 2.875, 2.875, 4.125,
2.125, 1.95, 3.875, 2.25, 4.1, 4.1],
'px': [102.532, 105.839, 107.247, 119.824, 124.005, 116.215, 117.708,
128.027, 115.301, 114.261, 133.621, 119.879, 149.427, 159.177]})
calendar = ql.TARGET()
today = calendar.adjust(ql.Date(19, 12, 2019))
ql.Settings.instance().evaluationDate = today
bondSettlementDays = 2
bondSettlementDate = calendar.advance(
today,
ql.Period(bondSettlementDays, ql.Days))
frequency = ql.Annual
dc = ql.ActualActual(ql.ActualActual.ISMA)
accrualConvention = ql.ModifiedFollowing
convention = ql.ModifiedFollowing
redemption = 100.0
instruments = []
for idx, row in pgbs.iterrows():
maturity = ql.Date(row.maturity, '%d-%m-%Y')
schedule = ql.Schedule(
bondSettlementDate,
maturity,
ql.Period(frequency),
calendar,
accrualConvention,
accrualConvention,
ql.DateGeneration.Backward,
False)
helper = ql.FixedRateBondHelper(
ql.QuoteHandle(ql.SimpleQuote(row.px)),
bondSettlementDays,
100.0,
schedule,
[row.coupon / 100],
dc,
convention,
redemption)
instruments.append(helper)
params = [bondSettlementDate, instruments, dc]
piecewiseMethods = {
'logLinearDiscount': ql.PiecewiseLogLinearDiscount(*params),
'logCubicDiscount': ql.PiecewiseLogCubicDiscount(*params),
'linearZero': ql.PiecewiseLinearZero(*params),
'cubicZero': ql.PiecewiseCubicZero(*params),
'linearForward': ql.PiecewiseLinearForward(*params),
'splineCubicDiscount': ql.PiecewiseSplineCubicDiscount(*params),
}
```

### ImpliedTermStructure

Implied term structure at a given date in the future

-
ql.ImpliedTermStructure(
*YieldTermStructure*,*date*)

```
crv = ql.FlatForward(ql.Date(10,1,2020),0.04875825,ql.Actual365Fixed())
yts = ql.YieldTermStructureHandle(crv)
ql.ImpliedTermStructure(yts, ql.Date(20,9,2020))
```

### ForwardSpreadedTermStructure

Term structure with added spread on the instantaneous forward rate.

-
ql.ForwardSpreadedTermStructure(
*YieldTermStructure*,*spread*)

```
crv = ql.FlatForward(ql.Date(10,1,2020),0.04875825,ql.Actual365Fixed())
yts = ql.YieldTermStructureHandle(crv)
spread = ql.QuoteHandle(ql.SimpleQuote(0.005))
ql.ForwardSpreadedTermStructure(yts, spread)
```

### ZeroSpreadedTermStructure

Term structure with an added spread on the zero yield rate

-
ql.ZeroSpreadedTermStructure(
*YieldTermStructure*,*spread*)

```
crv = ql.FlatForward(ql.Date(10,1,2020),0.04875825,ql.Actual365Fixed())
yts = ql.YieldTermStructureHandle(crv)
spread = ql.QuoteHandle(ql.SimpleQuote(0.005))
ql.ZeroSpreadedTermStructure(yts, spread)
```

### PiecewiseZeroSpreadedTermStructure

Represents a yield term structure constructed by applying a piecewise-linear interpolation of zero-rate spreads to an existing base curve. The resulting zero rate at any date is the base curve’s zero rate plus the interpolated spread at that date.

This structure is useful when modeling a market-implied yield curve that deviates from a base curve by a known set of spreads at given dates.

Other interpolations:

**SpreadedLinearZeroInterpolatedTermStructure**(alias for PiecewiseZeroSpreadedTermStructure)**SpreadedCubicZeroInterpolatedTermStructure****SpreadedKrugerZeroInterpolatedTermStructure****SpreadedSplineCubicZeroInterpolatedTermStructure****SpreadedParabolicCubicZeroInterpolatedTermStructure****SpreadedMonotonicParabolicCubicZeroInterpolatedTermStructure**

-
ql.PiecewiseZeroSpreadedTermStructure(
*baseCurve: ql.YieldTermStructureHandle, spreads: List[ql.Handle], dates: List[ql.Date], compounding: ql.Compounding = ql.Continuous, freq: ql.Frequency = ql.NoFrequency, dc: ql.DayCounter*) - Parameters:
**baseCurve**(*ql.YieldTermStructureHandle*) – The base yield term structure to which zero-rate spreads are applied.**spreads**(*List**[**ql.Handle**]*) – A list of handles to quotes representing the zero-rate spreads.**dates**(*List**[**ql.Date**]*) – The dates corresponding to each spread value. Must be in strictly increasing order.**compounding**(*ql.Compounding**,**optional*) – The compounding method used for zero rates. Defaults to ql.Continuous.**freq**(*ql.Frequency**,**optional*) – The frequency of compounding. Only relevant if compounding is not continuous. Defaults to ql.NoFrequency.**dc**(*ql.DayCounter**,**optional*) – The day count convention used for year fractions.



```
calendar = ql.TARGET()
today = ql.Date(9, 6, 2009)
ql.Settings.instance().evaluationDate = today
day_count = ql.Actual360()
compounding = ql.Continuous
# Build base term structure
settlement_days = 2
settlement_date = calendar.advance(today, ql.Period(settlement_days, ql.Days))
ts_days = [13, 41, 75, 165, 256, 345, 524, 703]
rates = [0.035, 0.033, 0.034, 0.034, 0.036, 0.037, 0.039, 0.040]
dates = [settlement_date] + [calendar.advance(today, n, ql.Days) for n in ts_days]
curve_rates = [0.035] + rates
term_structure = ql.ZeroCurve(dates, curve_rates, day_count)
# Spreads and spread dates
spread_1 = ql.makeQuoteHandle(0.02)
spread_2 = ql.makeQuoteHandle(0.03)
spreads = [spread_1, spread_2]
spread_dates = [
calendar.advance(today, 8, ql.Months),
calendar.advance(today, 15, ql.Months)
]
# PiecewiseZeroSpreadedTermStructure
spreaded_term_structure = ql.PiecewiseZeroSpreadedTermStructure(
ql.YieldTermStructureHandle(term_structure),
spreads, spread_dates
)
interpolation_date = calendar.advance(today, 6, ql.Months)
t = day_count.yearFraction(today, interpolation_date)
interpolated_zero_rate = spreaded_term_structure.zeroRate(t, compounding).rate()
```

### PiecewiseLinearForwardSpreadedTermStructure

Represents a yield term structure constructed by applying a piecewise-linear interpolation of **forward-rate** spreads to an existing base curve.
The resulting forward rate at any date is the base curve’s forward rate plus the interpolated spread at that date.

This structure is useful when modeling market-implied forward curves that deviate from a base term structure by a known set of spreads at given dates.

Other interpolations:

**PiecewiseForwardSpreadedTermStructure**(Backward-flat interpolated)

-
ql.PiecewiseLinearForwardSpreadedTermStructure(
*baseCurve: ql.YieldTermStructureHandle*,*spreads: List[ql.Handle]*,*dates: List[ql.Date]*,*dc: ql.DayCounter*) - Parameters:
**baseCurve**(*ql.YieldTermStructureHandle*) – The base yield term structure to which forward-rate spreads are applied.**spreads**(*List**[**ql.Handle**]*) – A list of handles to quotes representing the forward-rate spreads.**dates**(*List**[**ql.Date**]*) – The dates corresponding to each spread value. Must be in strictly increasing order.**dc**(*ql.DayCounter**,**optional*) – The day count convention used for computing year fractions.



Unlike the zero-spreaded structure, this one applies spreads to **instantaneous forward rates**, not zero yields. Therefore, the impact on discount factors and derived instruments may differ.

```
today = ql.Date(10, ql.January, 2024)
ql.Settings.instance().evaluationDate = today
# Define forward curve dates and rates (annualized, continuous compounding)
dates = [
today,
today + ql.Period(3, ql.Months),
today + ql.Period(6, ql.Months),
today + ql.Period(1, ql.Years),
today + ql.Period(2, ql.Years),
today + ql.Period(3, ql.Years),
today + ql.Period(5, ql.Years),
today + ql.Period(10, ql.Years)
]
forwards = [0.02, 0.021, 0.022, 0.023, 0.025, 0.025, 0.023, 0.022]
# Build the forward curve
calendar = ql.TARGET()
day_count = ql.Actual365Fixed()
forward_curve = ql.ForwardCurve(dates, forwards, day_count, calendar)
fwd_crv_handle = ql.YieldTermStructureHandle(forward_curve)
spreads = [ql.makeQuoteHandle(0.00), ql.makeQuoteHandle(0.005), ql.makeQuoteHandle(0.0025), ql.makeQuoteHandle(0.0)]
spread_dates = [ today,
calendar.advance(today, ql.Period(3, ql.Years)),
calendar.advance(today, ql.Period(5, ql.Years)),
calendar.advance(today, ql.Period(10, ql.Years))]
spreaded_fwd_crv = ql.PiecewiseLinearForwardSpreadedTermStructure(fwd_crv_handle, spreads, spread_dates, day_count)
```

### FittedBondCurve

-
ql.FittedBondDiscountCurve(
*bondSettlementDate*,*helpers*,*dc*,*method*,*accuracy=1.0e-10*,*maxEvaluations=10000*,*guess=Array()*,*simplexLambda=1.0*)

Methods:

CubicBSplinesFitting

ExponentialSplinesFitting

NelsonSiegelFitting

SimplePolynomialFitting

SvenssonFitting


```
pgbs = pd.DataFrame(
{'maturity': ['15-06-2020', '15-04-2021', '17-10-2022', '25-10-2023',
'15-02-2024', '15-10-2025', '21-07-2026', '14-04-2027',
'17-10-2028', '15-06-2029', '15-02-2030', '18-04-2034',
'15-04-2037', '15-02-2045'],
'coupon': [4.8, 3.85, 2.2, 4.95, 5.65, 2.875, 2.875, 4.125,
2.125, 1.95, 3.875, 2.25, 4.1, 4.1],
'px': [102.532, 105.839, 107.247, 119.824, 124.005, 116.215, 117.708,
128.027, 115.301, 114.261, 133.621, 119.879, 149.427, 159.177]})
calendar = ql.TARGET()
today = calendar.adjust(ql.Date(19, 12, 2019))
ql.Settings.instance().evaluationDate = today
bondSettlementDays = 2
bondSettlementDate = calendar.advance(
today,
ql.Period(bondSettlementDays, ql.Days))
frequency = ql.Annual
dc = ql.ActualActual(ql.ActualActual.ISMA)
accrualConvention = ql.ModifiedFollowing
convention = ql.ModifiedFollowing
redemption = 100.0
instruments = []
for idx, row in pgbs.iterrows():
maturity = ql.Date(row.maturity, '%d-%m-%Y')
schedule = ql.Schedule(
bondSettlementDate,
maturity,
ql.Period(frequency),
calendar,
accrualConvention,
accrualConvention,
ql.DateGeneration.Backward,
False)
helper = ql.FixedRateBondHelper(
ql.QuoteHandle(ql.SimpleQuote(row.px)),
bondSettlementDays,
100.0,
schedule,
[row.coupon / 100],
dc,
convention,
redemption)
instruments.append(helper)
params = [bondSettlementDate, instruments, dc]
cubicNots = [-30.0, -20.0, 0.0, 5.0, 10.0, 15.0,20.0, 25.0, 30.0, 40.0, 50.0]
fittingMethods = {
'NelsonSiegelFitting': ql.NelsonSiegelFitting(),
'SvenssonFitting': ql.SvenssonFitting(),
'SimplePolynomialFitting': ql.SimplePolynomialFitting(2),
'ExponentialSplinesFitting': ql.ExponentialSplinesFitting(),
'CubicBSplinesFitting': ql.CubicBSplinesFitting(cubicNots),
}
fittedBondCurveMethods = {
label: ql.FittedBondDiscountCurve(*params, method)
for label, method in fittingMethods.items()
}
curve = fittedBondCurveMethods.get('NelsonSiegelFitting')
```

### FXImpliedCurve

## Volatility

### SmileSections

A SmileSection in QuantLib is, as the word is saying, a class representing the portion of a volatility surface for a specific tenor. As we know, the volatility in real life is not flat across different tenors and different strikes, thus a vol surface can be described by a bidimensional function that maps a strike and a tenor to a specific volatility. A smile section, indeed is a function that maps a specific strike to a volatility value , think a partial application of the vol-surface function where the tenor is fixed.

The base class the represent a smile section in QuantLib is the `SmileSection`

class

-
*class*SmileSection Abstract base class representing a volatility smile at a fixed exercise date.

A

`SmileSection`

provides access to the volatility (or variance) surface as a function of**strike**, holding**expiry**constant. It is commonly used in local-volatility calibration, volatility interpolation, and model validation.Note

This is an abstract interface. Concrete implementations define the specific functional form of the smile (e.g.,

`ql.InterpolatedSmileSection`

,`ql.SabrSmileSection`

, etc.).- minStrike()
- Returns:
Returns the minimum strike value supported by the smile section.

- Return type:
float



- maxStrike()
- Returns:
Returns the maximum strike value supported by the smile section.

- Return type:
float



- atmLevel()
Returns the at-the-money (ATM) level used within this smile section, typically corresponding to the forward or spot level at expiry.

- Returns:
The ATM level used in this smile section.

- Return type:
float



-
variance(
*strike: float*) Returns the

**total variance**associated with the given strike.- Parameters:
**strike**– Strike rate at which to evaluate the variance.- Returns:
Total variance at the given strike.

- Return type:
float



-
volatility(
*strike: float*) Returns the

**volatility**corresponding to the given strike.- Parameters:
**strike**– Strike rate.- Returns:
Volatility at the given strike.

- Return type:
float



-
volatility(
*strike: float*,*type: ql.VolatilityType*,*shift: float = 0.0*) Returns the volatility corresponding to the given strike, expressed in a specific volatility type (e.g., normal, lognormal, shifted-lognormal).

- Parameters:
**strike**– Strike rate.**type**– The volatility type (see`ql.VolatilityType`

).**shift**– Optional shift parameter (for shifted models).

- Returns:
Volatility value.

- Return type:
float



- exerciseDate()
Returns the exercise (expiry) date associated with this smile section.

- Returns:
The exercise date.

- Return type:
ql.Date



- referenceDate()
Returns the reference (valuation) date used for this smile section.

- Returns:
The reference date.

- Return type:
ql.Date



- exerciseTime()
Returns the exercise time (in year fractions) corresponding to the expiry.

- Returns:
Exercise time in year fractions.

- Return type:
float



- dayCounter()
Returns the day-count convention used to compute the exercise time.

- Returns:
Day-count convention.

- Return type:
ql.DayCounter



- volatilityType()
Returns the volatility type (e.g., lognormal or normal) represented by this smile section.

- Returns:
Volatility type.

- Return type:
ql.VolatilityType



- shift()
Returns the shift value used when the volatility type is shifted-lognormal.

- Returns:
Shift value.

- Return type:
float



-
optionPrice(
*strike: float*,*type: ql.Option.Type = ql.Option.Call*,*discount: float = 1.0*) Computes the undiscounted option price implied by the smile section.

- Parameters:
**strike**– Strike rate.**type**– Option type (`ql.Option.Call`

or`ql.Option.Put`

).**discount**– Discount factor applied to the option payoff.

- Returns:
Option price implied by the smile.

- Return type:
float



-
digitalOptionPrice(
*strike: float*,*type: ql.Option.Type = ql.Option.Call*,*discount: float = 1.0*,*gap: float = 1.0e-5*) Computes the

**digital option**price implied by the smile section using a finite-difference approximation.- Parameters:
**strike**– Strike rate.**type**– Option type.**discount**– Discount factor applied to the payoff.**gap**– Finite-difference gap size for numerical differentiation.

- Returns:
Digital option price.

- Return type:
float



-
vega(
*strike: float*,*discount: float = 1.0*) Returns the

**vega**(sensitivity of the option price to volatility) at the given strike.- Parameters:
**strike**– Strike rate.**discount**– Discount factor.

- Returns:
Vega value.

- Return type:
float



-
density(
*strike: float*,*discount: float = 1.0*,*gap: float = 1.0e-4*) Returns the

**probability density**implied by the smile section at the given strike, derived via numerical differentiation.- Parameters:
**strike**– Strike rate.**discount**– Discount factor.**gap**– Finite-difference step size for derivative approximation.

- Returns:
Probability density value.

- Return type:
float




The concrete SmileSection classes exported in QuantLib Python are the following:

`LinearInterpolatedSmileSection`

`CubicInterpolatedSmileSection`

`MonotonicCubicInterpolatedSmileSection`

`SplineCubicInterpolatedSmileSection`


Those classes can be instantiated using one of the following constructors (example for the base class InterpolatedSmileSection, the constructor has the same signature also for the other classes):

-
*class*InterpolatedSmileSection(*expiryTime: float*,*strikes: list[float]*,*stdDevHandles: list[QuoteHandle]*,*atmLevel: QuoteHandle*,*interpolator: Interpolator = Interpolator()*,*dc: ql.DayCounter = ql.Actual365Fixed()*,*type: ql.VolatilityType = ql.ShiftedLognormal*,*shift: float = 0.0*)

-
*class*InterpolatedSmileSection(*expiryTime: float*,*strikes: list[float]*,*stdDevHandles: list[float]*,*atmLevel: float*,*interpolator: Interpolator = Interpolator()*,*dc: ql.DayCounter = ql.Actual365Fixed()*,*type: ql.VolatilityType = ql.ShiftedLognormal*,*shift: float = 0.0*)

-
*class*InterpolatedSmileSection(*date: ql.Date*,*strikes: list[float]*,*stdDevHandles: list[QuoteHandle]*,*atmLevel: QuoteHandle*,*dc: ql.DayCounter = ql.Actual365Fixed()*,*interpolator: Interpolator = Interpolator()*,*type: ql.VolatilityType = ql.ShiftedLognormal*,*shift: float = 0.0*)

-
*class*InterpolatedSmileSection(*date: ql:Date, strikes: list[float], stdDevHandles: list[float], atmLevel: float, dc : ql.DayCounter = ql.Actual365Fixed(), interpolator: Interpolator = Interpolator(), type: ql.VolatilityType = ql.ShiftedLognormal, shift: float = 0.0*)

### EquityFX

#### BlackConstantVol

-
ql.BlackConstantVol(
*date*,*calendar*,*volatility*,*dayCounter*)

-
ql.BlackConstantVol(
*date*,*calendar*,*volatilityHandle*,*dayCounter*)

-
ql.BlackConstantVol(
*days*,*calendar*,*volatility*,*dayCounter*)

-
ql.BlackConstantVol(
*days*,*calendar*,*volatilityHandle*,*dayCounter*)

```
date = ql.Date().todaysDate()
settlementDays = 2
calendar = ql.TARGET()
volatility = 0.2
volHandle = ql.QuoteHandle(ql.SimpleQuote(volatility))
dayCounter = ql.Actual360()
ql.BlackConstantVol(date, calendar, volatility, dayCounter)
ql.BlackConstantVol(date, calendar, volHandle, dayCounter)
ql.BlackConstantVol(settlementDays, calendar, volatility, dayCounter)
ql.BlackConstantVol(settlementDays, calendar, volHandle, dayCounter)
```

#### BlackVarianceCurve

-
ql.BlackVarianceCurve(
*referenceDate*,*expirations*,*volatilities*,*dayCounter*)

```
referenceDate = ql.Date(30, 9, 2013)
expirations = [ql.Date(20, 12, 2013), ql.Date(17, 1, 2014), ql.Date(21, 3, 2014)]
volatilities = [.145, .156, .165]
volatilityCurve = ql.BlackVarianceCurve(referenceDate, expirations, volatilities, ql.Actual360())
```

#### BlackVarianceSurface

-
ql.BlackVarianceSurface(
*referenceDate*,*calendar*,*expirations*,*strikes*,*volMatrix*,*dayCounter*)

```
referenceDate = ql.Date(30, 9, 2013)
ql.Settings.instance().evaluationDate = referenceDate;
calendar = ql.TARGET()
dayCounter = ql.ActualActual()
strikes = [1650.0, 1660.0, 1670.0]
expirations = [ql.Date(20, 12, 2013), ql.Date(17, 1, 2014), ql.Date(21, 3, 2014)]
volMatrix = ql.Matrix(len(strikes), len(expirations))
#1650 - Dec, Jan, Mar
volMatrix[0][0] = .15640; volMatrix[0][1] = .15433; volMatrix[0][2] = .16079;
#1660 - Dec, Jan, Mar
volMatrix[1][0] = .15343; volMatrix[1][1] = .15240; volMatrix[1][2] = .15804;
#1670 - Dec, Jan, Mar
volMatrix[2][0] = .15128; volMatrix[2][1] = .14888; volMatrix[2][2] = .15512;
volatilitySurface = ql.BlackVarianceSurface(
referenceDate,
calendar,
expirations,
strikes,
volMatrix,
dayCounter
)
volatilitySurface.enableExtrapolation()
```

#### HestonBlackVolSurface

-
ql.HestonBlackVolSurface(
*hestonModelHandle*)

```
flatTs = ql.YieldTermStructureHandle(
ql.FlatForward(ql.Date().todaysDate(), 0.05, ql.Actual365Fixed())
)
dividendTs = ql.YieldTermStructureHandle(
ql.FlatForward(ql.Date().todaysDate(), 0.02, ql.Actual365Fixed())
)
v0 = 0.01; kappa = 0.01; theta = 0.01; rho = 0.0; sigma = 0.01
spot = 100
process = ql.HestonProcess(flatTs, dividendTs,
ql.QuoteHandle(ql.SimpleQuote(spot)),
v0, kappa, theta, sigma, rho
)
hestonModel = ql.HestonModel(process)
hestonHandle = ql.HestonModelHandle(hestonModel)
hestonVolSurface = ql.HestonBlackVolSurface(hestonHandle)
```

#### AndreasenHugeVolatilityAdapter

An implementation of the arb-free Andreasen-Huge vol interpolation described in “Andreasen J., Huge B., 2010. Volatility Interpolation” (https://ssrn.com/abstract=1694972). An advantage of this method is that it can take a non-rectangular grid of option quotes.

-
ql.AndreasenHugeVolatilityAdapter(
*AndreasenHugeVolatilityInterpl*)

```
today = ql.Date().todaysDate()
calendar = ql.NullCalendar()
dayCounter = ql.Actual365Fixed()
spot = 100
r, q = 0.02, 0.05
spotQuote = ql.QuoteHandle(ql.SimpleQuote(spot))
ratesTs = ql.YieldTermStructureHandle(ql.FlatForward(today, r, dayCounter))
dividendTs = ql.YieldTermStructureHandle(ql.FlatForward(today, q, dayCounter))
# Market options price quotes
optionStrikes = [95, 97.5, 100, 102.5, 105, 90, 95, 100, 105, 110, 80, 90, 100, 110, 120]
optionMaturities = ["3M", "3M", "3M", "3M", "3M", "6M", "6M", "6M", "6M", "6M", "1Y", "1Y", "1Y", "1Y", "1Y"]
optionQuotedVols = [0.11, 0.105, 0.1, 0.095, 0.095, 0.12, 0.11, 0.105, 0.1, 0.105, 0.12, 0.115, 0.11, 0.11, 0.115]
calibrationSet = ql.CalibrationSet()
for strike, expiry, impliedVol in zip(optionStrikes, optionMaturities, optionQuotedVols):
payoff = ql.PlainVanillaPayoff(ql.Option.Call, strike)
exercise = ql.EuropeanExercise(calendar.advance(today, ql.Period(expiry)))
calibrationSet.push_back((ql.VanillaOption(payoff, exercise), ql.SimpleQuote(impliedVol)))
ahInterpolation = ql.AndreasenHugeVolatilityInterpl(calibrationSet, spotQuote, ratesTs, dividendTs)
ahSurface = ql.AndreasenHugeVolatilityAdapter(ahInterpolation)
```

#### BlackVolTermStructureHandle

-
ql.BlackVolTermStructureHandle(
*blackVolTermStructure*)

```
ql.BlackVolTermStructureHandle(constantVol)
ql.BlackVolTermStructureHandle(volatilityCurve)
ql.BlackVolTermStructureHandle(volatilitySurface)
```

#### RelinkableBlackVolTermStructureHandle

- ql.RelinkableBlackVolTermStructureHandle()

-
ql.RelinkableBlackVolTermStructureHandle(
*blackVolTermStructure*)

```
blackTSHandle = ql.RelinkableBlackVolTermStructureHandle(volatilitySurface)
blackTSHandle = ql.RelinkableBlackVolTermStructureHandle()
blackTSHandle.linkTo(volatilitySurface)
```

#### LocalConstantVol

-
ql.LocalConstantVol(
*date*,*volatility*,*dayCounter*)

```
date = ql.Date().todaysDate()
volatility = 0.2
dayCounter = ql.Actual360()
ql.LocalConstantVol(date, volatility, dayCounter)
```

#### LocalVolSurface

-
ql.LocalVolSurface(
*blackVolTs*,*ratesTs*,*dividendsTs*,*spot*)

```
today = ql.Date().todaysDate()
calendar = ql.NullCalendar()
dayCounter = ql.Actual365Fixed()
volatility = 0.2
r, q = 0.02, 0.05
blackVolTs = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, calendar, volatility, dayCounter))
ratesTs = ql.YieldTermStructureHandle(ql.FlatForward(today, r, dayCounter))
dividendTs = ql.YieldTermStructureHandle(ql.FlatForward(today, q, dayCounter))
spot = 100
ql.LocalVolSurface(blackVolTs, ratesTs, dividendTs, spot)
```

#### NoExceptLocalVolSurface

This powerful but dangerous surface will swallow any exceptions and return the specified override value when they occur. If your vol surface is well-calibrated, this protects you from crashes due to very far illiquid points on the local vol surface. But if your vol surface is not good, it could suppress genuine errors. Caution recommended.

-
ql.NoExceptLocalVolSurface(
*blackVolTs*,*ratesTs*,*dividendsTs*,*spot*,*illegalVolOverride*)

```
today = ql.Date().todaysDate()
calendar = ql.NullCalendar()
dayCounter = ql.Actual365Fixed()
r, q = 0.02, 0.05
volatility = 0.2
illegalVolOverride = 0.25
blackVolTs = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, calendar, volatility, dayCounter))
ratesTs = ql.YieldTermStructureHandle(ql.FlatForward(today, r, dayCounter))
dividendTs = ql.YieldTermStructureHandle(ql.FlatForward(today, q, dayCounter))
spot = 100
ql.NoExceptLocalVolSurface(blackVolTs, ratesTs, dividendTs, spot, illegalVolOverride)
```

#### AndreasenHugeLocalVolAdapter

-
ql.AndreasenHugeLocalVolAdapter(
*AndreasenHugeVolatilityInterpl*)

```
today = ql.Date().todaysDate()
calendar = ql.NullCalendar()
dayCounter = ql.Actual365Fixed()
spot = 100
r, q = 0.02, 0.05
spotQuote = ql.QuoteHandle(ql.SimpleQuote(spot))
ratesTs = ql.YieldTermStructureHandle(ql.FlatForward(today, r, dayCounter))
dividendTs = ql.YieldTermStructureHandle(ql.FlatForward(today, q, dayCounter))
# Market options price quotes
optionStrikes = [95, 97.5, 100, 102.5, 105, 90, 95, 100, 105, 110, 80, 90, 100, 110, 120]
optionMaturities = ["3M", "3M", "3M", "3M", "3M", "6M", "6M", "6M", "6M", "6M", "1Y", "1Y", "1Y", "1Y", "1Y"]
optionQuotedVols = [0.11, 0.105, 0.1, 0.095, 0.095, 0.12, 0.11, 0.105, 0.1, 0.105, 0.12, 0.115, 0.11, 0.11, 0.115]
calibrationSet = ql.CalibrationSet()
for strike, expiry, impliedVol in zip(optionStrikes, optionMaturities, optionQuotedVols):
payoff = ql.PlainVanillaPayoff(ql.Option.Call, strike)
exercise = ql.EuropeanExercise(calendar.advance(today, ql.Period(expiry)))
calibrationSet.push_back((ql.VanillaOption(payoff, exercise), ql.SimpleQuote(impliedVol)))
ahInterpolation = ql.AndreasenHugeVolatilityInterpl(calibrationSet, spotQuote, ratesTs, dividendTs)
ahLocalSurface = ql.AndreasenHugeLocalVolAdapter(ahInterpolation)
```

### Cap Volatility

#### ConstantOptionletVolatility

floating reference date, floating market data

-
ql.ConstantOptionletVolatility(
*settlementDays*,*cal*,*bdc*,*volatility (Quote)*,*dc*,*type=ShiftedLognormal*,*displacement=0.0*)

fixed reference date, floating market data

-
ql.ConstantOptionletVolatility(
*settlementDate*,*cal*,*bdc*,*volatility (Quote)*,*dc*,*type=ShiftedLognormal*,*displacement=0.0*)

floating reference date, fixed market data

-
ql.ConstantOptionletVolatility(
*settlementDays*,*cal*,*bdc*,*volatility (value)*,*dc*,*type=ShiftedLognormal*,*displacement=0.0*)

fixed reference date, fixed market data

-
ql.ConstantOptionletVolatility(
*settlementDate*,*cal*,*bdc*,*volatility (value)*,*dc*,*type=ShiftedLognormal*,*displacement=0.0*)

```
settlementDays = 2
settlementDate = ql.Date().todaysDate()
cal = ql.TARGET()
bdc = ql.ModifiedFollowing
volatility = 0.55
vol_quote = ql.QuoteHandle(ql.SimpleQuote(volatility))
dc = ql.Actual365Fixed()
#floating reference date, floating market data
c1 = ql.ConstantOptionletVolatility(settlementDays, cal, bdc, vol_quote, dc, ql.Normal)
#fixed reference date, floating market data
c2 = ql.ConstantOptionletVolatility(settlementDate, cal, bdc, vol_quote, dc)
#floating reference date, fixed market data
c3 = ql.ConstantOptionletVolatility(settlementDays, cal, bdc, volatility, dc)
#fixed reference date, fixed market data
c4 = ql.ConstantOptionletVolatility(settlementDate, cal, bdc, volatility, dc)
```

#### CapFloorTermVolCurve

Cap/floor at-the-money term-volatility vector.

**floating reference date, floating market data**

-
ql.CapFloorTermVolCurve(
*settlementDays*,*calendar*,*bdc*,*optionTenors*,*vols (Quotes)*,*dc=Actual365Fixed*)

**fixed reference date, floating market data**

-
ql.CapFloorTermVolCurve(
*settlementDate*,*calendar*,*bdc*,*optionTenors*,*vols (Quotes)*,*dc=Actual365Fixed*)

**fixed reference date, fixed market data**

-
ql.CapFloorTermVolCurve(
*settlementDate*,*calendar*,*bdc*,*optionTenors*,*vols (vector)*,*dc=Actual365Fixed*)

**floating reference date, fixed market data**

-
ql.CapFloorTermVolCurve(
*settlementDays*,*calendar*,*bdc*,*optionTenors*,*vols (vector)*,*dc=Actual365Fixed*)

```
settlementDate = ql.Date().todaysDate()
settlementDays = 2
calendar = ql.TARGET()
bdc = ql.ModifiedFollowing
optionTenors = [ql.Period('1y'), ql.Period('2y'), ql.Period('3y')]
vols = [0.55, 0.60, 0.65]
# fixed reference date, fixed market data
c3 = ql.CapFloorTermVolCurve(settlementDate, calendar, bdc, optionTenors, vols)
# floating reference date, fixed market data
c4 = ql.CapFloorTermVolCurve(settlementDays, calendar, bdc, optionTenors, vols)
```

#### CapFloorTermVolSurface

**floating reference date, floating market data**

-
ql.CapFloorTermVolSurface(
*settlementDays*,*calendar*,*bdc*,*expiries*,*strikes*,*vol_data (Handle)*,*daycount=ql.Actual365Fixed*)

**fixed reference date, floating market data**

-
ql.CapFloorTermVolSurface(
*settlementDate*,*calendar*,*bdc*,*expiries*,*strikes*,*vol_data (Handle)*,*daycount=ql.Actual365Fixed*)

**fixed reference date, fixed market data**

-
ql.CapFloorTermVolSurface(
*settlementDate*,*calendar*,*bdc*,*expiries*,*strikes*,*vol_data (Matrix)*,*daycount=ql.Actual365Fixed*)

**floating reference date, fixed market data**

-
ql.CapFloorTermVolSurface(
*settlementDays*,*calendar*,*bdc*,*expiries*,*strikes*,*vol_data (Matrix)*,*daycount=ql.Actual365Fixed*)

```
settlementDate = ql.Date().todaysDate()
settlementDays = 2
calendar = ql.TARGET()
bdc = ql.ModifiedFollowing
expiries = [ql.Period('9y'), ql.Period('10y'), ql.Period('12y')]
strikes = [0.015, 0.02, 0.025]
black_vols = [
[1. , 0.792 , 0.6873],
[0.9301, 0.7401, 0.6403],
[0.7926, 0.6424, 0.5602]]
# fixed reference date, fixed market data
s3 = ql.CapFloorTermVolSurface(settlementDate, calendar, bdc, expiries, strikes, black_vols)
# floating reference date, fixed market data
s4 = ql.CapFloorTermVolSurface(settlementDays, calendar, bdc, expiries, strikes, black_vols)
```

#### OptionletStripper1

-
ql.OptionletStripper1(
*CapFloorTermVolSurface*,*index*,*switchStrikes=Null*,*accuracy=1.0e-6*,*maxIter=100*,*discount=YieldTermStructure*,*type=ShiftedLognormal*,*displacement=0.0*,*dontThrow=false*)

```
index = ql.Euribor6M()
optionlet_surf = ql.OptionletStripper1(s3, index, type=ql.Normal)
```

#### StrippedOptionletAdapter

-
ql.StrippedOptionletAdapter(
*StrippedOptionletBase*)

#### OptionletVolatilityStructureHandle

-
ql.OptionletVolatilityStructureHandle(
*OptionletVolatilityStructure*)

```
ovs_handle = ql.OptionletVolatilityStructureHandle(
ql.StrippedOptionletAdapter(optionlet_surf)
)
```

#### RelinkableOptionletVolatilityStructureHandle

- ql.RelinkableOptionletVolatilityStructureHandle()

```
ovs_handle = ql.RelinkableOptionletVolatilityStructureHandle()
ovs_handle.linkTo(ql.StrippedOptionletAdapter(optionlet_surf))
```

### Swaption Volatility

#### ConstantSwaptionVolatility

Constant swaption volatility, no time-strike dependence.

**floating reference date, floating market data**

-
ql.ConstantSwaptionVolatility(
*settlementDays*,*cal*,*bdc*,*volatility*,*dc*,*type=ql.ShiftedLognormal*,*shift=0.0*)

**fixed reference date, floating market data**

-
ql.ConstantSwaptionVolatility(
*settlementDate*,*cal*,*bdc*,*volatility*,*dc*,*type=ql.ShiftedLognormal*,*shift=0.0*)

**floating reference date, fixed market data**

-
ql.ConstantSwaptionVolatility(
*settlementDays*,*cal*,*bdc*,*volatilityQuote*,*dc*,*type=ql.ShiftedLognormal*,*shift=0.0*)

**fixed reference date, fixed market data**

-
ql.ConstantSwaptionVolatility(
*settlementDate*,*cal*,*bdc*,*volatilityQuote*,*dc*,*type=ql.ShiftedLognormal*,*shift=0.0*)

```
constantSwaptionVol = ql.ConstantSwaptionVolatility(2, ql.TARGET(), ql.ModifiedFollowing, ql.QuoteHandle(ql.SimpleQuote(0.55)), ql.ActualActual())
```

#### SwaptionVolatilityMatrix

At-the-money swaption-volatility matrix.

**floating reference date, floating market data**

-
ql.SwaptionVolatilityMatrix(
*calendar*,*bdc*,*optionTenors*,*swapTenors*,*vols (Handles)*,*dayCounter*,*flatExtrapolation=false*,*type=ShiftedLognormal*,*shifts (vector)*)

fixed reference date, floating market data

-
ql.SwaptionVolatilityMatrix(
*referenceDate*,*calendar*,*bdc*,*optionTenors*,*swapTenors*,*vols (Handles)*,*dayCounter*,*flatExtrapolation=false*,*type=ShiftedLognormal*,*shifts (vector)*)

floating reference date, fixed market data

-
ql.SwaptionVolatilityMatrix(
*calendar*,*bdc*,*optionTenors*,*swapTenors*,*vols (matrix)*,*dayCounter*,*flatExtrapolation=false*,*type=ShiftedLognormal*,*shifts (matrix)*)

fixed reference date, fixed market data

-
ql.SwaptionVolatilityMatrix(
*referenceDate*,*calendar*,*bdc*,*optionTenors*,*swapTenors*,*vols (matrix)*,*dayCounter*,*flatExtrapolation=false*,*type=ShiftedLognormal*,*shifts (matrix)*)

fixed reference date and fixed market data, option dates

-
ql.SwaptionVolatilityMatrix(
*referenceDate*,*calendar*,*bdc*,*optionDates*,*swapTenors*,*vols (matrix)*,*dayCounter*,*flatExtrapolation=false*,*type=ShiftedLognormal*,*shifts (matrix)*)

```
# market Data 07.01.2020
swapTenors = [
'1Y', '2Y', '3Y', '4Y', '5Y',
'6Y', '7Y', '8Y', '9Y', '10Y',
'15Y', '20Y', '25Y', '30Y']
optionTenors = [
'1M', '2M', '3M', '6M', '9M', '1Y',
'18M', '2Y', '3Y', '4Y', '5Y', '7Y',
'10Y', '15Y', '20Y', '25Y', '30Y']
normal_vols = [
[8.6, 12.8, 19.5, 26.9, 32.7, 36.1, 38.7, 40.9, 42.7, 44.3, 48.8, 50.4, 50.8, 50.4],
[9.2, 13.4, 19.7, 26.4, 31.9, 35.2, 38.3, 40.2, 41.9, 43.1, 47.8, 49.9, 50.7, 50.3],
[11.2, 15.3, 21.0, 27.6, 32.7, 35.3, 38.4, 40.8, 42.6, 44.5, 48.6, 50.5, 50.9, 51.0],
[12.9, 17.1, 22.6, 28.8, 33.5, 36.0, 38.8, 41.0, 43.0, 44.6, 48.7, 50.6, 51.1, 51.0],
[14.6, 18.7, 24.6, 30.1, 34.2, 36.9, 39.3, 41.3, 43.2, 44.9, 48.9, 51.0, 51.3, 51.5],
[16.5, 20.9, 26.3, 31.3, 35.0, 37.6, 40.0, 42.0, 43.7, 45.3, 48.8, 50.9, 51.4, 51.7],
[20.9, 25.3, 30.0, 34.0, 37.0, 39.5, 41.9, 43.4, 45.0, 46.4, 49.3, 51.0, 51.3, 51.9],
[25.1, 28.9, 33.2, 36.2, 39.2, 41.2, 43.2, 44.7, 46.0, 47.3, 49.6, 51.0, 51.3, 51.6],
[34.0, 36.6, 39.2, 41.1, 43.2, 44.5, 46.1, 47.2, 48.0, 49.0, 50.3, 51.3, 51.3, 51.2],
[40.3, 41.8, 43.6, 44.9, 46.1, 47.1, 48.2, 49.2, 49.9, 50.5, 51.2, 51.3, 50.9, 50.7],
[44.0, 44.8, 46.0, 47.1, 48.4, 49.1, 49.9, 50.7, 51.4, 51.9, 51.6, 51.4, 50.6, 50.2],
[49.6, 49.7, 50.4, 51.2, 51.8, 52.2, 52.6, 52.9, 53.3, 53.8, 52.6, 51.7, 50.4, 49.6],
[53.9, 53.7, 54.0, 54.2, 54.4, 54.5, 54.5, 54.4, 54.4, 54.9, 53.1, 51.8, 50.1, 49.1],
[54.0, 53.7, 53.8, 53.7, 53.5, 53.6, 53.5, 53.3, 53.5, 53.7, 51.4, 49.8, 47.9, 46.6],
[52.8, 52.4, 52.6, 52.3, 52.2, 52.3, 52.0, 51.9, 51.8, 51.8, 49.5, 47.4, 45.4, 43.8],
[51.4, 51.2, 51.3, 51.0, 50.8, 50.7, 50.3, 49.9, 49.8, 49.7, 47.6, 45.3, 43.1, 41.4],
[49.6, 49.6, 49.7, 49.5, 49.5, 49.2, 48.6, 47.9, 47.4, 47.1, 45.1, 42.9, 40.8, 39.2]
]
swapTenors = [ql.Period(tenor) for tenor in swapTenors]
optionTenors = [ql.Period(tenor) for tenor in optionTenors]
normal_vols = [[vol / 10000 for vol in row] for row in normal_vols]
calendar = ql.TARGET()
bdc = ql.ModifiedFollowing
dayCounter = ql.ActualActual()
swaptionVolMatrix = ql.SwaptionVolatilityMatrix(
calendar, bdc,
optionTenors, swapTenors, ql.Matrix(normal_vols),
dayCounter, False, ql.Normal)
```

#### SwaptionVolCube1

#### SwaptionVolCube2

-
ql.SwaptionVolCube2(
*atmVolStructure*,*optionTenors*,*swapTenors*,*strikeSpreads*,*volSpreads*,*swapIndex*,*shortSwapIndex*,*vegaWeightedSmileFit*)

```
optionTenors = ['1y', '2y', '3y']
swapTenors = [ '5Y', '10Y']
strikeSpreads = [ -0.01, 0.0, 0.01]
volSpreads = [
[0.5, 0.55, 0.6],
[0.5, 0.55, 0.6],
[0.5, 0.55, 0.6],
[0.5, 0.55, 0.6],
[0.5, 0.55, 0.6],
[0.5, 0.55, 0.6],
]
optionTenors = [ql.Period(tenor) for tenor in optionTenors]
swapTenors = [ql.Period(tenor) for tenor in swapTenors]
volSpreads = [[ql.QuoteHandle(ql.SimpleQuote(v)) for v in row] for row in volSpreads]
swapIndexBase = ql.EuriborSwapIsdaFixA(ql.Period(1, ql.Years), e6m_yts, ois_yts)
shortSwapIndexBase = ql.EuriborSwapIsdaFixA(ql.Period(1, ql.Years), e6m_yts, ois_yts)
vegaWeightedSmileFit = False
volCube = ql.SwaptionVolatilityStructureHandle(
ql.SwaptionVolCube2(
ql.SwaptionVolatilityStructureHandle(swaptionVolMatrix),
optionTenors,
swapTenors,
strikeSpreads,
volSpreads,
swapIndexBase,
shortSwapIndexBase,
vegaWeightedSmileFit)
)
volCube.enableExtrapolation()
```

#### SwaptionVolatilityStructureHandle

-
ql.SwaptionVolatilityStructureHandle(
*swaptionVolStructure*)

```
swaptionVolHandle = ql.SwaptionVolatilityStructureHandle(swaptionVolMatrix)
```

#### RelinkableSwaptionVolatilityStructureHandle

- ql.RelinkableSwaptionVolatilityStructureHandle()

```
handle = ql.RelinkableSwaptionVolatilityStructureHandle()
handle.linkTo(swaptionVolMatrix)
```

### SABR

#### SabrSmileSection

-
ql.SabrSmileSection(
*date*,*fwd*, [*alpha*,*beta*,*nu*,*rho*, ]*dayCounter*,*Real*)

-
ql.SabrSmileSection(
*time*,*fwd*, [*alpha*,*beta*,*nu*,*rho*, ]*dayCounter*,*Real*)

```
alpha = 1.63
beta = 0.6
nu = 3.3
rho = 0.00002
ql.SabrSmileSection(17/365, 120, [alpha, beta, nu, rho])
```

#### sabrVolatility

-
ql.sabrVolatility(
*strike*,*forward*,*expiryTime*,*alpha*,*beta*,*nu*,*rho*)

```
alpha = 1.63
beta = 0.6
nu = 3.3
rho = 0.00002
ql.sabrVolatility(106, 120, 17/365, alpha, beta, nu, rho)
```

#### shiftedSabrVolatility

-
ql.shiftedSabrVolatility(
*strike*,*forward*,*expiryTime*,*alpha*,*beta*,*nu*,*rho*,*shift*)

```
alpha = 1.63
beta = 0.6
nu = 3.3
rho = 0.00002
shift = 50
ql.shiftedSabrVolatility(106, 120, 17/365, alpha, beta, nu, rho, shift)
```

#### sabrFlochKennedyVolatility

-
ql.sabrFlochKennedyVolatility(
*strike*,*forward*,*expiryTime*,*alpha*,*beta*,*nu*,*rho*)

```
alpha = 0.01
beta = 0.01
nu = 0.01
rho = 0.01
ql.sabrFlochKennedyVolatility(0.01,0.01, 5, alpha, beta, nu, rho)
```

## Credit Term Structures

### FlatHazardRate

Flat hazard-rate curve.

-
ql.FlatHazardRate(
*settlementDays*,*calendar*,*Quote*,*dayCounter*)

-
ql.FlatHazardRate(
*settelementDate*,*Quote*,*dayCounter*)

```
pd_curve = ql.FlatHazardRate(2, ql.TARGET(), ql.QuoteHandle(ql.SimpleQuote(0.05)), ql.Actual360())
pd_curve = ql.FlatHazardRate(ql.Date().todaysDate(), ql.QuoteHandle(ql.SimpleQuote(0.05)), ql.Actual360())
```

### PiecewiseFlatHazardRate

Piecewise default-probability term structure.

-
ql.PiecewiseFlatHazardRate(
*settlementDate*,*helpers*,*dayCounter*)

```
recoveryRate = 0.4
settlementDate = ql.Date().todaysDate()
yts = ql.FlatForward(2, ql.TARGET(), 0.05, ql.Actual360())
CDS_tenors = [ql.Period(6, ql.Months), ql.Period(1, ql.Years), ql.Period(2, ql.Years), ql.Period(3, ql.Years), \
ql.Period(4, ql.Years), ql.Period(5, ql.Years), ql.Period(7, ql.Years), ql.Period(10, ql.Years), ql.Period(50, ql.Years)]
CDS_ctpy = [26.65, 37.22, 53.17, 65.79, 77.39, 91.14, 116.84, 136.67, 136.67]
CDSHelpers_ctpy = [ql.SpreadCdsHelper((CDS_spread / 10000.0), CDS_tenor, 0, ql.TARGET(), ql.Quarterly, ql.Following, \
ql.DateGeneration.TwentiethIMM, ql.Actual360(), recoveryRate, ql.YieldTermStructureHandle(yts))
for CDS_spread, CDS_tenor in zip(CDS_ctpy, CDS_tenors)]
pd_curve = ql.PiecewiseFlatHazardRate(settlementDate, CDSHelpers_ctpy, ql.Thirty360())
```

### SurvivalProbabilityCurve

-
ql.SurvivalProbabilityCurve(
*dates*,*survivalProbabilities*,*dayCounter*,*calendar*)

```
today = ql.Date().todaysDate()
dates = [today + ql.Period(n , ql.Years) for n in range(11)]
sp = [1.0, 0.9941, 0.9826, 0.9674, 0.9488, 0.9246, 0.8945, 0.8645, 0.83484, 0.80614, 0.7784]
crv = ql.SurvivalProbabilityCurve(dates, sp, ql.Actual360(), ql.TARGET())
crv.enableExtrapolation()
```

## Inflation Term Structures

### ZeroInflationCurve

-
ql.PiecewiseZeroInflation(
*referenceDate*,*calendar*,*dayCounter*,*observationLag*,*frequency*,*bool indexIsInterpolated*,*baseZeroRate*,*nominalTS*,*helpers*,*accuracy=1.0e-12*,*interpolator=ql.Linear()*)