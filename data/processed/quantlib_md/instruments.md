# Instruments

## Fixed Income

### Forwards

#### Forward Rate Agreement

-
*class*ql.ForwardRateAgreement(*valueDate*,*maturityDate*,*position*,*strikeForward*,*notional*,*iborIndex*,*discountCurve=ql.YieldTermStructureHandle()*) fra = ql.ForwardRateAgreement( ql.Date(15,6,2020), ql.Date(15,12,2020), ql.Position.Long, 0.01, 1e6, ql.Euribor6M(yts), yts )

- .NPV()

- .businessDayConvention()

- .calendar()

- .dayCounter()

- .discountCurve()

- .fixingDate()

- .forwardRate()

- .forwardValue()

-
.impliedYield(
*underlyingSpotValue*,*forwardValue*,*settlementDate*,*compoundingConvention*,*dayCounter*)

- .incomeDiscountCurve()

- .isExpired()

- .settlementDate()

-
.spotIncome(
*yts*)

- .spotValue()


#### FixedRateBondForward

-
*class*ql.FixedRateBondForward(*valueDate*,*maturityDate*,*Position::Type*,*strike*,*settlementDays*,*dayCounter*,*calendar*,*businessDayConvention*,*FixedRateBond*,*yieldTermStructure=ql.YieldTermStructureHandle()*,*incomeDiscountCurve=ql.YieldTermStructureHandle()*) Position:

ql.Position.Long

ql.Position.Short


valueDate = ql.Date(24, 6, 2020) maturityDate = ql.Date(31, 5, 2032) position = ql.Position.Long strike = 100 settlementDays = 2 dayCounter = ql.Actual360() calendar = ql.TARGET() businessDayConvention = ql.Following bond = ql.FixedRateBond(2, ql.TARGET(), 100.0, ql.Date(31, 5, 2032), ql.Date(30, 5, 2035), ql.Period('1Y'), [0.05], ql.ActualActual()) bond.setPricingEngine(engine) fwd = ql.FixedRateBondForward( valueDate, maturityDate, position, strike, settlementDays, dayCounter , calendar, businessDayConvention, bond, yts, yts)


### Bonds

#### Bond

Redemptions and maturity are calculated from the coupon data, if available. Therefore, redemptions must not be included in the passed cash flows.

-
*class*ql.Bond(*settlementDays*,*calendar*,*issueDate*,*coupons*) start = ql.Date(15,12,2019) maturity = ql.Date(15,12,2020) schedule = ql.MakeSchedule(start, maturity, ql.Period('6M')) interest = ql.FixedRateLeg(schedule, ql.Actual360(), [100.], [0.05]) bond = ql.Bond(0, ql.TARGET(), start, interest)

-
.bondYield(
*dayCounter*,*compounding*,*frequency*,*accuracy=1.0e-8*,*maxEvaluations=100*)

-
.bondYield(
*cleanPrice*,*dayCounter*,*compounding*,*frequency*,*settlementDate=Date*,*accuracy=1.0e-8*,*maxEvaluations=100*) bond.bondYield(100, ql.Actual360(), ql.Compounded, ql.Annual)


- .dirtyPrice()
bond.dirtyPrice()


-
.dirtyPrice(
*yield*,*dayCount*,*compounding*,*frequency*) bond.dirtyPrice(0.05, ql.Actual360(), ql.Compounded, ql.Annual)


-
.bondYield(

#### ZeroCouponBond

-
ql.ZeroCouponBond(
*settlementDays*,*calendar*,*faceAmount*,*maturityDate*)

```
bond = ql.ZeroCouponBond(2, ql.TARGET(), 100, ql.Date(20,6,2020))
```

#### FixedRateBond

-
ql.FixedRateBond(
*settlementDays*,*calendar*,*faceAmount*,*startDate*,*maturityDate*,*tenor*,*coupon*,*paymentConvention*)

-
ql.FixedRateBond(
*settlementDays*,*faceAmount*,*schedule*,*coupon*,*paymentConvention*)

```
bond = ql.FixedRateBond(2, ql.TARGET(), 100.0, ql.Date(15,12,2019), ql.Date(15,12,2024), ql.Period('1Y'), [0.05], ql.ActualActual(ql.ActualActual.Bond))
```

#### AmortizingFixedRateBond

-
ql.AmortizingFixedRateBond(
*settlementDays*,*notionals*,*schedule*,*coupons*,*accrualDayCounter*,*paymentConvention=Following*,*issueDate=Date()*)

```
notionals = [100,100,100,50]
schedule = ql.MakeSchedule(ql.Date(25,1,2018), ql.Date(25,1,2022), ql.Period('1y'))
bond = ql.AmortizingFixedRateBond(0, notionals, schedule, [0.03], ql.Thirty360(ql.Thirty360.USA))
```

#### FloatingRateBond

-
ql.FloatingRateBond(
*settlementDays*,*faceAmount*,*schedule*,*index*,*dayCounter*,*paymentConvention*)

```
schedule = ql.MakeSchedule(ql.Date(15,6,2020), ql.Date(15,6,2022), ql.Period('6m'))
index = ql.Euribor6M()
bond = ql.FloatingRateBond(2,100, schedule, index, ql.Actual360(), spreads=[0.01])
```

#### AmortizingFloatingRateBond

-
ql.FloatingRateBond(
*settlementDays*,*notionals*,*schedule*,*index*,*dayCounter*)

```
notional = [100, 50]
schedule = ql.MakeSchedule(ql.Date(15,6,2020), ql.Date(15,6,2022), ql.Period('1Y'))
index = ql.Euribor6M()
bond = ql.AmortizingFloatingRateBond(2, notional, schedule, index, ql.ActualActual(ql.ActualActual.Bond))
```

#### CMS Rate Bond

-
ql.CmsRateBond(
*settlementDays*,*faceAmount*,*schedule*,*index*,*dayCounter*,*paymentConvention*,*fixingDays*,*gearings*,*spreads*,*caps*,*floors*)

```
schedule = ql.MakeSchedule(ql.Date(15,6,2020), ql.Date(15,6,2022), ql.Period('1Y'))
index = ql.EuriborSwapIsdaFixA(ql.Period('10y'))
bond = ql.CmsRateBond(2, 100, schedule, index, ql.Actual360(), ql.ModifiedFollowing, fixingDays=2, gearings=[1], spreads=[0], caps=[], floors=[])
```

#### Callable Bond

-
ql.CallableFixedRateBond(
*settlementDays*,*faceAmount*,*schedule*,*coupons*,*accrualDayCounter*,*paymentConvention*,*redemption*,*issueDate*,*putCallSchedule*)

```
schedule = ql.MakeSchedule(ql.Date(15,6,2020), ql.Date(15,6,2022), ql.Period('1Y'))
putCallSchedule = ql.CallabilitySchedule()
my_price = ql.BondPrice(100, ql.BondPrice.Clean)
putCallSchedule.append(
ql.Callability(my_price, ql.Callability.Call, ql.Date(15,6,2021))
)
bond = ql.CallableFixedRateBond(2, 100, schedule, [0.01], ql.Actual360(), ql.ModifiedFollowing, 100, ql.Date(15,6,2020), putCallSchedule)
```

#### Convertible Bond

#### BondFunctions

```
bond = ql.FixedRateBond(
2, ql.TARGET(), 100.0,
ql.Date(15,12,2019), ql.Date(15,12,2024), ql.Period('1Y'),
[0.05], ql.ActualActual(ql.ActualActual.Bond))
```

**Date Inspectors**

```
ql.BondFunctions.startDate(bond)
ql.BondFunctions.maturityDate(bond)
ql.BondFunctions.isTradable(bond)
```

**Cashflow Inspectors**

```
ql.BondFunctions.previousCashFlowDate(bond)
ql.BondFunctions.previousCashFlowDate(bond, ql.Date(15,12,2020))
ql.BondFunctions.previousCashFlowAmount(bond)
ql.BondFunctions.previousCashFlowAmount(bond, ql.Date(15,12,2020))
ql.BondFunctions.nextCashFlowDate(bond)
ql.BondFunctions.nextCashFlowDate(bond, ql.Date(15,12,2020))
ql.BondFunctions.nextCashFlowAmount(bond)
ql.BondFunctions.nextCashFlowAmount(bond, ql.Date(15,12,2020))
```

**Coupon Inspectors**

```
ql.BondFunctions.previousCouponRate(bond)
ql.BondFunctions.nextCouponRate(bond)
ql.BondFunctions.accrualStartDate(bond)
ql.BondFunctions.accrualEndDate(bond)
ql.BondFunctions.accrualPeriod(bond)
ql.BondFunctions.accrualDays(bond)
ql.BondFunctions.accruedPeriod(bond)
ql.BondFunctions.accruedDays(bond)
ql.BondFunctions.accruedAmount(bond)
```

**YieldTermStructure**

```
crv = ql.FlatForward(2, ql.TARGET(), 0.04, ql.Actual360())
ql.BondFunctions.cleanPrice(bond, crv)
ql.BondFunctions.bps(bond, crv)
ql.BondFunctions.atmRate(bond, crv)
```

**Yield (a.k.a. Internal Rate of Return, i.e. IRR) functions**

```
rate = ql.InterestRate(0.05, ql.Actual360(), ql.Compounded, ql.Annual)
ql.BondFunctions.cleanPrice(bond, rate)
ql.BondFunctions.bps(bond, rate)
ql.BondFunctions.duration(bond, rate)
ql.BondFunctions.convexity(bond, rate)
ql.BondFunctions.basisPointValue(bond, rate)
ql.BondFunctions.yieldValueBasisPoint(bond, rate)
```

**Z-spread functions**

```
crv = ql.FlatForward(2, ql.TARGET(), 0.04, ql.Actual360())
ql.BondFunctions.zSpread(bond, 101, crv, ql.Actual360(), ql.Compounded, ql.Annual)
```

### Swaps

#### VanillaSwap

-
ql.VanillaSwap(
*type*,*nominal*,*fixedSchedule*,*fixedRate*,*fixedDayCount*,*floatSchedule*,*index*,*spread*,*floatingDayCount*)

Types:

ql.VanillaSwap.Payer

ql.VanillaSwap.Receiver


```
calendar = ql.TARGET()
start = ql.Date(17,6,2019)
maturity = calendar.advance(start, ql.Period('5y'))
fixedSchedule = ql.MakeSchedule(start, maturity, ql.Period('1Y'))
floatSchedule = ql.MakeSchedule(start, maturity, ql.Period('6M'))
swap = ql.VanillaSwap(
ql.VanillaSwap.Payer, 100,
fixedSchedule, 0.01, ql.Thirty360(),
floatSchedule, ql.Euribor6M(), 0, ql.Actual360()
)
```

#### Swap

-
ql.Swap(
*firstLeg*,*secondLeg*)

```
fixedSchedule = ql.MakeSchedule(start, maturity, ql.Period('1Y'))
fixedLeg = ql.FixedRateLeg(fixedSchedule, ql.Actual360(), [100], [0.01])
floatSchedule = ql.MakeSchedule(start, maturity, ql.Period('6M'))
floatLeg = ql.IborLeg([100], floatSchedule, ql.Euribor6M(), ql.Actual360())
swap = ql.Swap(fixedLeg, floatLeg)
```

#### MakeVanillaSwap

-
ql.MakeVanillaSwap(
*tenor*,*index*,*fixedRate*,*forwardStart*)

**Optional params:**

fixedLegDayCount

Nominal

receiveFixed,

swapType

settlementDays

effectiveDate

terminationDate

dateGenerationRule

fixedLegTenor

fixedLegCalendar

fixedLegConvention

fixedLegDayCount

floatingLegTenor

floatingLegCalendar

floatingLegConvention

floatingLegDayCount

floatingLegSpread

discountingTermStructure

pricingEngine

fixedLegTerminationDateConvention

fixedLegDateGenRule

fixedLegEndOfMonth

fixedLegFirstDate

fixedLegNextToLastDate,

floatingLegTerminationDateConvention

floatingLegDateGenRule

floatingLegEndOfMonth

floatingLegFirstDate

floatingLegNextToLastDate


```
tenor = ql.Period('5y')
index = ql.Euribor6M()
fixedRate = 0.05
forwardStart = ql.Period("2D")
swap = ql.MakeVanillaSwap(tenor, index, fixedRate, forwardStart, Nominal=100)
swap = ql.MakeVanillaSwap(tenor, index, fixedRate, forwardStart, swapType=ql.VanillaSwap.Payer)
```

#### Amortizing Swap

```
calendar = ql.TARGET()
start = ql.Date(17,6,2019)
maturity = calendar.advance(start, ql.Period('2y'))
fixedSchedule = ql.MakeSchedule(start, maturity, ql.Period('1Y'))
fixedLeg = ql.FixedRateLeg(fixedSchedule, ql.Actual360(), [100, 50], [0.01])
floatSchedule = ql.MakeSchedule(start, maturity, ql.Period('6M'))
floatLeg = ql.IborLeg([100, 100, 50, 50], floatSchedule, ql.Euribor6M(), ql.Actual360())
swap = ql.Swap(fixedLeg, floatLeg)
```

#### FloatFloatSwap

```
ql.FloatFloatSwap(ql.VanillaSwap.Payer,
[notional] * (len(float3m)-1),
[notional] * (len(float6m)-1),
float3m,
index3m,
ql.Actual360(),
float6m,
index6m,
ql.Actual360(), False, False,
[1] * (len(float3m)-1),
[spread] * (len(float3m)-1))
```

#### AssetSwap

-
ql.AssetSwap(
*payFixed*,*bond*,*cleanPrice*,*index*,*spread*)

-
ql.AssetSwap(
*payFixed*,*bond*,*cleanPrice*,*index*,*spread*,*schedule*,*dayCount*,*bool*)

```
payFixedRate = True
bond = ql.FixedRateBond(2, ql.TARGET(), 100.0, ql.Date(15,12,2019), ql.Date(15,12,2024),
ql.Period('1Y'), [0.05], ql.ActualActual()
)
bondCleanPrice = 100
index = ql.Euribor6M()
spread = 0.0
ql.AssetSwap(payFixedRate, bond, bondCleanPrice, index, spread, ql.Schedule(), ql.ActualActual(), True)
```

#### OvernightIndexedSwap

-
ql.OvernightIndexedSwap(
*swapType*,*nominal*,*schedule*,*fixedRate*,*fixedDC*,*overnightIndex*)

Or array of nominals

-
ql.OvernightIndexedSwap(
*swapType*,*nominals*,*schedule*,*fixedRate*,*fixedDC*,*overnightIndex*)

Optional params:

spread=0.0

paymentLag=0

paymentAdjustment=ql.Following()

paymentCalendar=ql.Calendar()

telescopicValueDates=false


Types:

ql.OvernightIndexedSwap.Receiver

ql.OvernightIndexedSwap.Receiver


```
swapType = ql.OvernightIndexedSwap.Receiver
nominal = 100
schedule = ql.MakeSchedule(ql.Date(15,6,2020), ql.Date(15,6,2021), ql.Period('1Y'), calendar=ql.TARGET())
fixedRate = 0.01
fixedDC = ql.Actual360()
overnightIndex = ql.Eonia()
ois_swap = ql.OvernightIndexedSwap(swapType, nominal, schedule, fixedRate, fixedDC, overnightIndex)
```

#### MakeOIS

-
ql.MakeOIS(
*swapTenor*,*overnightIndex*,*fixedRate*)

Optional params:

fwdStart=Period(0, Days)

receiveFixed=True,

swapType=OvernightIndexedSwap.Payer

nominal=1.0

settlementDays=2

effectiveDate=None

terminationDate=None

dateGenerationRule=DateGeneration.Backward

paymentFrequency=Annual

paymentAdjustmentConvention=Following

paymentLag=0

paymentCalendar=None

endOfMonth=True

fixedLegDayCount=None

overnightLegSpread=0.0

discountingTermStructure=None

telescopicValueDates=False

pricingEngine=None


```
swapTenor = ql.Period('1Y')
overnightIndex = ql.Eonia()
fixedRate = 0.01
ois_swap = ql.MakeOIS(swapTenor, overnightIndex, fixedRate)
```

#### NonstandardSwap

-
ql.NonstandardSwap(
*swapType*,*fixedNominal*,*floatingNominal*,*fixedSchedule*,*fixedRate*,*fixedDayCount*,*floatingSchedule*,*iborIndex*,*gearing*,*spread*,*floatDayCount*)

Optional params:

intermediateCapitalExchange = False

finalCapitalExchange = False,

paymentConvention = None


```
swapType = ql.VanillaSwap.Payer
fixedNominal = [100, 100]
floatingNominal = [100] * 4
fixedSchedule = ql.MakeSchedule(ql.Date(15,6,2020), ql.Date(15,6,2022), ql.Period('1Y'))
fixedRate = [0.02] * 2
fixedDayCount = ql.Thirty360()
floatingSchedule = ql.MakeSchedule(ql.Date(15,6,2020), ql.Date(15,6,2022), ql.Period('6M'))
iborIndex = ql.Euribor6M()
gearing = [1.] * 4
spread = [0.] * 4
floatDayCount = iborIndex.dayCounter()
nonstandardSwap = ql.NonstandardSwap(
swapType, fixedNominal, floatingNominal,
fixedSchedule, fixedRate, fixedDayCount,
floatingSchedule, iborIndex, gearing, spread, floatDayCount)
```

### Swaptions

**Exercises**

ql.EuropeanExercise(start)

ql.AmericanExercise(earliestDate, latestDate)

ql.BermudanExercise(dates)


**Settlement Type/Method**

- ql.Settlement.Cash
ql.Settlement.CollateralizedCashPrice

ql.Settlement.ParYieldCurve



- ql.Settlement.Physical
ql.Settlement.PhysicalCleared

ql.Settlement.PhysicalOTC




#### Swaption

-
ql.Swaption(
*swap*,*exercise*,*settlementType=ql.Settlement.Physical*,*settlementMethod=ql.Settlement.PhysicalOTC*)

```
calendar = ql.TARGET()
today = ql.Date().todaysDate()
exerciseDate = calendar.advance(today, ql.Period('5y'))
exercise = ql.EuropeanExercise(exerciseDate)
swap = ql.MakeVanillaSwap(ql.Period('5y'), ql.Euribor6M(), 0.05, ql.Period('5y'))
swaption = ql.Swaption(swap, exercise)
swaption = ql.Swaption(swap, exercise, ql.Settlement.Cash, ql.Settlement.ParYieldCurve)
swaption = ql.Swaption(swap, exercise, ql.Settlement.Physical, ql.Settlement.PhysicalCleared)
```

#### Nonstandard Swaption

#### FloatFloatSwaption

### Caps & Floors

#### Cap

-
ql.Cap(
*floatingLeg*,*exerciseRates*)

```
schedule = ql.MakeSchedule(ql.Date(15,6,2020), ql.Date(16,6,2022), ql.Period('6M'))
ibor_leg = ql.IborLeg([100], schedule, ql.Euribor6M())
strike = 0.01
cap = ql.Cap(ibor_leg, [strike])
```

#### Floor

-
ql.Floor(
*floatingLeg*,*exerciseRates*)

```
schedule = ql.MakeSchedule(ql.Date(15,6,2020), ql.Date(16,6,2022), ql.Period('6M'))
ibor_leg = ql.IborLeg([100], schedule, ql.Euribor6M())
strike = 0.00
floor = ql.Floor(ibor_leg, [strike])
```

#### Collar

-
ql.Collar(
*floatingLeg*,*capRates*,*floorRates*)

```
schedule = ql.MakeSchedule(ql.Date(15,6,2020), ql.Date(16,6,2022), ql.Period('6M'))
ibor_leg = ql.IborLeg([100], schedule, ql.Euribor6M())
capStrike = 0.02
floorStrike = 0.00
collar = ql.Collar(ibor_leg, [capStrike], [floorStrike])
```

## Inflation

### CPI Bond

-
ql.CPIBond(
*settlementDays*,*notional*,*growthOnly*,*baseCPI*,*contractObservationLag*,*inflationIndex*,*observationInterpolation*,*fixedSchedule*,*fixedRates*,*fixedDayCounter*,*fixedPaymentConvention*)

```
calendar = ql.UnitedKingdom()
today = ql.Date(5,3,2008)
evaluationDate = calendar.adjust(today)
issue_date = calendar.advance(evaluationDate,-1, ql.Years)
maturity_date = ql.Date(2,9,2052)
settlementDays = 3
notional = 1000000
growthOnly = False
baseCPI = 206.1
contractObservationLag = ql.Period(3, ql.Months)
inflationIndex = ql.UKRPI(False)
observationInterpolation = ql.CPI.Flat
fixedSchedule = ql.MakeSchedule(issue_date, maturity_date, ql.Period(ql.Semiannual))
fixedRates = [0.1]
fixedDayCounter = ql.Actual365Fixed()
fixedPaymentConvention = ql.ModifiedFollowing
bond = ql.CPIBond(settlementDays,
notional,
growthOnly,
baseCPI,
contractObservationLag,
inflationIndex,
observationInterpolation,
fixedSchedule,
fixedRates,
fixedDayCounter,
fixedPaymentConvention)
```

### CPISwap

-
ql.CPISwap(
*swapType*,*nominal*,*subtractInflationNominal*,*spread*,*floatDayCount*,*schedule*,*floatPaymentConvention*,*fixingDays*,*floatIndex*,*fixedRate*,*baseCPI*,*fixedDayCount*,*schedule*,*fixedPaymentConvention*,*contractObservationLag*,*fixedIndex*,*observationInterpolation*)

```
swapType = ql.CPISwap.Payer
nominal = 1e6
subtractInflationNominal = True
spread = 0.0
floatDayCount = ql.Actual365Fixed()
floatPaymentConvention = ql.ModifiedFollowing
fixingDays = 0;
floatIndex = ql.GBPLibor(ql.Period('6M'))
fixedRate = 0.1;
baseCPI = 206.1;
fixedDayCount = ql.Actual365Fixed()
fixedPaymentConvention = ql.ModifiedFollowing;
fixedIndex = ql.UKRPI(False);
contractObservationLag = ql.Period('3M')
observationInterpolation = ql.CPI.Linear
startDate = ql.Date(2,10,2007)
endDate = ql.Date(2,10,2052)
schedule = ql.MakeSchedule(startDate, endDate, ql.Period('6m'))
zisV = ql.CPISwap(
swapType, nominal, subtractInflationNominal, spread,
floatDayCount, schedule, floatPaymentConvention, fixingDays, floatIndex,
fixedRate, baseCPI, fixedDayCount, schedule, fixedPaymentConvention,
contractObservationLag, fixedIndex, observationInterpolation)
```

### ZeroCouponInflationSwap

-
ql.ZeroCouponInflationSwap(
*swapType*,*notional*,*start*,*maturity*,*calendar*,*BusinessDayConvention*,*DayCounter*,*fixedRate*,*ZeroInflationIndex*,*observationLag*)

```
swapType = ql.ZeroCouponInflationSwap.Payer
calendar = ql.TARGET()
nominal = 1e6
startDate = ql.Date(11,1,2022)
endDate = ql.Date(11,1,2023)
fixedRate = 0.1;
dc = ql.Actual365Fixed()
inflationIndex = ql.EUHICPXT(True)
contractObservationLag = ql.Period(3, ql.Months)
bdc = ql.ModifiedFollowing
swap = ql.ZeroCouponInflationSwap(swapType, nominal, startDate, endDate, calendar, bdc, dc, fixedRate, inflationIndex, contractObservationLag)
```

### YearOnYearInflationSwap

-
ql.YearOnYearInflationSwap(
*swapType*,*nominal*,*fixedSchedule*,*fixedRate*,*fixedDayCounter*,*yoySchedule*,*index*,*lag*,*spread*,*yoyDayCounter*,*paymentCalendar*)

```
swapType = ql.YearOnYearInflationSwap.Payer
nominal = 1e6
startDate = ql.Date(2,10,2007)
endDate = ql.Date(2,10,2052)
fixedSchedule = ql.MakeSchedule(startDate, endDate, ql.Period('6m'))
fixedRate = 0.1;
fixedDayCounter = ql.Actual365Fixed()
yoySchedule = ql.MakeSchedule(startDate, endDate, ql.Period('6m'))
index = ql.YYEUHICP(False)
lag = ql.Period('3m')
spread = 0.0
yoyDayCounter = ql.Actual365Fixed()
paymentCalendar = ql.TARGET()
swap = ql.YearOnYearInflationSwap(swapType, nominal, fixedSchedule, fixedRate, fixedDayCounter, yoySchedule, index, lag, spread, yoyDayCounter, paymentCalendar)
```

### YoYInflationCap

### YoYInflationFloor

### YoYInflationCollar

## Credit

### CreditDefaultSwap

-
ql.CreditDefaultSwap(
*side*,*nominal*,*spread*,*cdsSchedule*,*convention*,*dayCounter*)

```
side = ql.Protection.Seller
nominal = 10e6
spread = 34.6 / 10000
cdsSchedule = ql.MakeSchedule(ql.Date(20, 12, 2019), ql.Date(20, 12, 2024), ql.Period('3M'),
ql.Quarterly, ql.TARGET(), ql.Following, ql.Unadjusted, ql.DateGeneration.TwentiethIMM)
cds = ql.CreditDefaultSwap(side, nominal, spread, cdsSchedule, ql.Following, ql.Actual360())
```

### CdsOption

-
ql.CdsOption(
*CreditDefaultSwap*,*exercise*,*knocksOut=true*)

```
expiry = ql.Date(15,6,2020)
exercise = ql.EuropeanExercise(expiry)
ql.CdsOption(cds, exercise, True)
```

## Options

### Vanilla Options

-
ql.VanillaOption(
*payoff*,*europeanExercise*)

Exercise Types:

ql.EuropeanExercise(date)

ql.AmericanExercise(earliestDate, latestDate)

ql.BermudanExercise(dates)

ql.RebatedExercise


Payoffs:

ql.Option.Call

ql.Option.Put


```
strike = 100.0
maturity = ql.Date(15,6,2025)
option_type = ql.Option.Call
payoff = ql.PlainVanillaPayoff(option_type, strike)
binaryPayoff = ql.CashOrNothingPayoff(option_type, strike, 1)
europeanExercise = ql.EuropeanExercise(maturity)
europeanOption = ql.VanillaOption(payoff, europeanExercise)
americanExercise = ql.AmericanExercise(ql.Date().todaysDate(), maturity)
americanOption = ql.VanillaOption(payoff, americanExercise)
bermudanExercise = ql.BermudanExercise([ql.Date(15,6,2024), ql.Date(15,6,2025)])
bermudanOption = ql.VanillaOption(payoff, bermudanExercise)
binaryOption = ql.VanillaOption(binaryPayoff, european_exercise)
```

### Asian Options

-
ql.DiscreteAveragingAsianOption(
*averageType*,*runningAccumulator*,*pastFixings*,*fixingDates*,*payoff*,*exercise*)

Averaging Types:

ql.ContinuousAveragingAsianOption(arithmeticAverage, vanillaPayoff, europeanExercise)

ql.DiscreteAveragingAsianOption(arithmeticAverage, arithmeticRunningAccumulator, pastFixings, asianFutureFixingDates, vanillaPayoff, europeanExercise)


Average Definitions:

ql.Average().Arithmetic

ql.Average().Geometric


```
today = ql.Date().todaysDate()
periods = [ql.Period("6M"), ql.Period("12M"), ql.Period("18M"), ql.Period("24M")]
pastFixings = 0 # Empty because this is a new contract
asianFutureFixingDates = [today + period for period in periods]
asianExpiryDate = today + periods[-1]
strike = 100
vanillaPayoff = ql.PlainVanillaPayoff(ql.Option.Call, strike)
europeanExercise = ql.EuropeanExercise(asianExpiryDate)
arithmeticAverage = ql.Average().Arithmetic
arithmeticRunningAccumulator = 0.0
discreteArithmeticAsianOption = ql.DiscreteAveragingAsianOption(arithmeticAverage, arithmeticRunningAccumulator, pastFixings, asianFutureFixingDates, vanillaPayoff, europeanExercise)
geometricAverage = ql.Average().Geometric
geometricRunningAccumulator = 1.0
discreteGeometricAsianOption = ql.DiscreteAveragingAsianOption(geometricAverage, geometricRunningAccumulator, pastFixings, asianFutureFixingDates, vanillaPayoff, europeanExercise)
continuousGeometricAsianOption = ql.ContinuousAveragingAsianOption(geometricAverage, vanillaPayoff, europeanExercise)
```

### Barrier Options

-
ql.BarrierOption(
*barrierType*,*barrier*,*rebate*,*payoff*,*exercise*)

Barrier Types:

ql.Barrier.UpIn

ql.Barrier.UpOut

ql.Barrier.DownIn

ql.Barrier.DownOut


```
T = 1
K = 100.
barrier = 110.
rebate = 0.
barrierType = ql.Barrier.UpOut
today = ql.Date().todaysDate()
maturity = today + ql.Period(int(T*365), ql.Days)
payoff = ql.PlainVanillaPayoff(ql.Option.Call, K)
amExercise = ql.AmericanExercise(today, maturity, True)
euExercise = ql.EuropeanExercise(maturity)
barrierOption = ql.BarrierOption(barrierType, barrier, rebate, payoff, euExercise)
```

-
ql.DoubleBarrierOption(
*barrierType*,*barrier_lo*,*barrier_hi*,*rebate*,*payoff*,*exercise*)

Double Barrier Types:

ql.DoubleBarrier.KnockIn

ql.DoubleBarrier.KnockOut

ql.DoubleBarrier.KIKO

ql.DoubleBarrier.KOKI


```
T = 1
K = 100.
barrier_lo, barrier_hi = 90., 110.
rebate = 0.
barrierType = ql.DoubleBarrier.KnockOut
today = ql.Date().todaysDate()
maturity = today + ql.Period(int(T*365), ql.Days)
payoff = ql.PlainVanillaPayoff(ql.Option.Call, K)
euExercise = ql.EuropeanExercise(maturity)
doubleBarrierOption = ql.DoubleBarrierOption(barrierType, barrier_lo, barrier_hi, rebate, payoff, euExercise)
```

-
ql.PartialTimeBarrierOption(
*barrierType*,*barrieRange*,*barrier*,*rebate*,*coverEventDate*,*payoff*,*exercise*)

Partial Barrier Ranges Types:

ql.PartialBarrier.Start: Monitor the barrier from the start of the option lifetime until the so-called cover event.

ql.PartialBarrier.EndB1: Monitor the barrier from the cover event to the exercise date; trigger a knock-out only if the barrier is hit or crossed from either side, regardless of the underlying value when monitoring starts.

ql.PartialBarrier.EndB2: Monitor the barrier from the cover event to the exercise date; immediately trigger a knock-out if the underlying value is on the wrong side of the barrier when monitoring starts.


```
today = ql.Date().todaysDate()
maturity = calendar.advance(today, ql.Period(360, ql.Days))
K = 110.
barrier = 125.
rebate = 0.
barrier_type = ql.Barrier.UpOut
cover_event_date = calendar.advance(today, ql.Period(180, ql.Days))
payoff = ql.PlainVanillaPayoff(ql.Option.Call, K)
exercise = ql.EuropeanExercise(maturity)
partial_time_barrier_opt = ql.PartialTimeBarrierOption(
barrier_type,
ql.PartialBarrier.EndB1, # time range for partial-time barrier option
barrier, rebate,
cover_event_date,
payoff, exercise
)
```

### Basket Options

-
ql.BasketOption(
*payoff*,*exercise*)

Payoff Types:

ql.MinBasketPayoff(payoff)

ql.AverageBasketPayoff(payoff, numInstruments)

ql.MaxBasketPayoff(payoff)


```
today = ql.Date().todaysDate()
exp_date = today + ql.Period(1, ql.Years)
strike = 100
number_of_underlyings = 5
exercise = ql.EuropeanExercise(exp_date)
vanillaPayoff = ql.PlainVanillaPayoff(ql.Option.Call, strike)
payoffMin = ql.MinBasketPayoff(vanillaPayoff)
basketOptionMin = ql.BasketOption(payoffMin, exercise)
payoffAverage = ql.AverageBasketPayoff(vanillaPayoff, number_of_underlyings)
basketOptionAverage = ql.BasketOption(payoffAverage, exercise)
payoffMax = ql.MaxBasketPayoff(vanillaPayoff)
basketOptionMax = ql.BasketOption(payoffMax, exercise)
```

### Cliquet Options

### Forward Options

-
ql.ForwardVanillaOption(
*moneyness*,*resetDate*,*payoff*,*exercise*)

```
today = ql.Date().todaysDate()
resetDate = today + ql.Period(1, ql.Years)
expiryDate = today + ql.Period(2, ql.Years)
moneyness, strike = 1., 100 # nb. strike is required for the payoff, but ignored in pricing
exercise = ql.EuropeanExercise(expiryDate)
vanillaPayoff = ql.PlainVanillaPayoff(ql.Option.Call, strike)
forwardStartOption = ql.ForwardVanillaOption(moneyness, resetDate, vanillaPayoff, exercise)
```