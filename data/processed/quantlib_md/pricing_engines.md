# Pricing Engines

## Black & Bachelier Engines

The price engine module provides with a set of functions from the two cornerstones models in mathematical finance: the **Black** and **Bachelier** option pricing formulas, also exposing their implied volatility inverses, and related probabilities such as *in-the-money (ITM) probabilities*.

These functions are commonly used for pricing and risk analysis in derivatives models based on lognormal (Black) or normal (Bachelier) assumptions.

## Bond Pricing Engines

### DiscountingBondEngine

-
ql.DiscountingBondEngine(
*discountCurve*)

```
crv = ql.FlatForward(ql.Date().todaysDate(),0.04875825,ql.Actual365Fixed())
yts = ql.YieldTermStructureHandle(crv)
engine = ql.DiscountingBondEngine(yts)
```

### BlackCallableFixedRateBondEngine

-
ql.BlackCallableFixedRateBondEngine(
*fwdYieldVol*,*discountCurve*)

```
crv = ql.FlatForward(ql.Date().todaysDate(),0.04875825,ql.Actual365Fixed())
yts = ql.YieldTermStructureHandle(crv)
vol = ql.QuoteHandle(ql.SimpleQuote(0.55))
engine = ql.BlackCallableFixedRateBondEngine(vol, yts)
```

### TreeCallableFixedRateEngine

-
ql.TreeCallableFixedRateBondEngine(
*shortRateModel*,*size*,*discountCurve*)

```
crv = ql.FlatForward(ql.Date().todaysDate(),0.04875825,ql.Actual365Fixed())
yts = ql.YieldTermStructureHandle(crv)
model = ql.Vasicek()
engine = ql.TreeCallableFixedRateBondEngine(model, 10, yts)
```

-
ql.TreeCallableFixedRateBondEngine(
*shortRateModel*,*size*)

```
model = ql.Vasicek()
engine = ql.TreeCallableFixedRateBondEngine(model, 10)
```

-
ql.TreeCallableFixedRateBondEngine(
*shortRateModel*,*TimeGrid*,*discountCurve*)

```
crv = ql.FlatForward(ql.Date().todaysDate(),0.04875825,ql.Actual365Fixed())
yts = ql.YieldTermStructureHandle(crv)
model = ql.Vasicek()
grid = ql.TimeGrid(5,10)
engine = ql.TreeCallableFixedRateBondEngine(model, grid, yts)
```

-
ql.TreeCallableFixedRateBondEngine(
*shortRateModel*,*TimeGrid*)

```
crv = ql.FlatForward(ql.Date().todaysDate(),0.04875825,ql.Actual365Fixed())
yts = ql.YieldTermStructureHandle(crv)
model = ql.Vasicek()
grid = ql.TimeGrid(5,10)
engine = ql.TreeCallableFixedRateBondEngine(model, grid)
```

## Cap Pricing Engines

### BlackCapFloorEngine

-
ql.BlackCapFloorEngine(
*yieldTermStructure*,*quoteHandle*)

```
vols = ql.QuoteHandle(ql.SimpleQuote(0.547295))
engine = ql.BlackCapFloorEngine(yts, vols)
cap.setPricingEngine(engine)
```

-
ql.BlackCapFloorEngine(
*yieldTermStructure*,*OptionletVolatilityStructure*)

### BachelierCapFloorEngine

-
ql.BachelierCapFloorEngine(
*yieldTermStructure*,*quoteHandle*)

```
vols = ql.QuoteHandle(ql.SimpleQuote(0.00547295))
engine = ql.BachelierCapFloorEngine(yts, vols)
```

-
ql.BachelierCapFloorEngine(
*yieldTermStructure*,*OptionletVolatilityStructure*)

### AnalyticCapFloorEngine

-
ql.AnalyticCapFloorEngine(
*OneFactorAffineModel*,*YieldTermStructure*)

-
ql.AnalyticCapFloorEngine(
*OneFactorAffineModel*)

OneFactorAffineModel

HullWhite : (termStructure, a=0.1, sigma=0.01)

Vasicek : (r0=0.05, a=0.1, b=0.05, sigma=0.01, lambda=0.0)

CoxIngersollRoss [NOT IMPLEMENTED]

GeneralizedHullWhite [NOT IMPLEMENTED]


```
yts = ql.YieldTermStructureHandle(ql.FlatForward(ql.Date().todaysDate(), 0.0121, ql.Actual360()))
models = [
ql.HullWhite (yts),
ql.Vasicek(r0=0.008),
]
for model in models:
analyticEngine = ql.AnalyticCapFloorEngine(model, yts)
cap.setPricingEngine(analyticEngine)
print(f"Cap npv is: {cap.NPV():,.2f}")
```

### TreeCapFloorEngine

-
ql.TreeCapFloorEngine(
*ShortRateModel*,*Size*,*YieldTermStructure*)

-
ql.TreeCapFloorEngine(
*ShortRateModel*,*Size*)

-
ql.TreeCapFloorEngine(
*ShortRateModel*,*Size*,*TimeGrid*,*YieldTermStructure*)

-
ql.TreeCapFloorEngine(
*ShortRateModel*,*Size*,*TimeGrid*)

Models

HullWhite : (YieldTermStructure, a=0.1, sigma=0.01)

BlackKarasinski : (YieldTermStructure, a=0.1, sigma=0.1)

Vasicek : (r0=0.05, a=0.1, b=0.05, sigma=0.01, lambda=0.0)

G2 : (termStructure, a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)

GeneralizedHullWhite [NOT IMPLEMENTED]

CoxIngersollRoss [NOT IMPLEMENTED]

ExtendedCoxIngersollRoss [NOT IMPLEMENTED]


```
models = [
ql.HullWhite (yts),
ql.BlackKarasinski(yts),
ql.Vasicek(0.0065560),
ql.G2(yts)
]
for model in models:
treeEngine = ql.TreeCapFloorEngine(model, 60, yts)
cap.setPricingEngine(treeEngine)
print(f"Cap npv is: {cap.NPV():,.2f}")
```

## Swap Pricing Engines

### DiscountingSwapEngine

-
ql.DiscountingSwapEngine(
*YieldTermStructure*)

```
yts = ql.YieldTermStructureHandle(ql.FlatForward(2, ql.TARGET(), 0.5, ql.Actual360()))
engine = ql.DiscountingSwapEngine(yts)
```

## Swaption Pricing Engines

### BlackSwaptionEngine

-
ql.BlackSwaptionEngine(
*yts*,*quote*)

-
ql.BlackSwaptionEngine(
*yts*,*swaptionVolatilityStructure*)

-
ql.BlackSwaptionEngine(
*yts*,*quote*,*dayCounter*)

-
ql.BlackSwaptionEngine(
*yts*,*quote*,*dayCounter*,*displacement*)

```
blackEngine = ql.BlackSwaptionEngine(yts, ql.QuoteHandle(ql.SimpleQuote(0.55)))
blackEngine = ql.BlackSwaptionEngine(yts, ql.QuoteHandle(ql.SimpleQuote(0.55)), ql.ActualActual())
blackEngine = ql.BlackSwaptionEngine(yts, ql.QuoteHandle(ql.SimpleQuote(0.55)), ql.ActualActual(), 0.01)
```

### BachelierSwaptionEngine

-
ql.BachelierSwaptionEngine(
*yts*,*quote*)

-
ql.BachelierSwaptionEngine(
*yts*,*swaptionVolatilityStructure*)

-
ql.BachelierSwaptionEngine(
*yts*,*quote*,*dayCounter*)

```
bachelierEngine = ql.BachelierSwaptionEngine(yts, ql.QuoteHandle(ql.SimpleQuote(0.0055)))
swaption.setPricingEngine(bachelierEngine)
swaption.NPV()
```

### FdHullWhiteSwaptionEngine

-
ql.FdHullWhiteSwaptionEngine(
*model*,*range*,*interval*)

```
model = ql.HullWhite(yts)
engine = ql.FdHullWhiteSwaptionEngine(model)
swaption.setPricingEngine(engine)
swaption.NPV()
```

### FdG2SwaptionEngine

-
ql.FdG2SwaptionEngine(
*model*)

```
model = ql.G2(yts)
engine = ql.FdG2SwaptionEngine(model)
swaption.setPricingEngine(engine)
swaption.NPV()
```

### G2SwaptionEngine

-
ql.G2SwaptionEngine(
*model*,*range*,*interval*)

```
model = ql.G2(yts)
g2Engine = ql.G2SwaptionEngine(model, 4, 4)
swaption.setPricingEngine(g2Engine)
swaption.NPV()
```

### JamshidianSwaptionEngine

-
ql.JamshidianSwaptionEngine(
*OneFactorAffineModel*)

-
ql.JamshidianSwaptionEngine(
*OneFactorAffineModel*,*YieldTermStructure*)

```
model = ql.HullWhite(yts)
engine = ql.JamshidianSwaptionEngine(model, yts)
swaption.setPricingEngine(g2Engine)
swaption.NPV()
```

### TreeSwaptionEngine

-
ql.TreeSwaptionEngine(
*ShortRateModel*,*Size*,*YieldTermStructure*)

-
ql.TreeSwaptionEngine(
*ShortRateModel*,*Size*)

-
ql.TreeSwaptionEngine(
*ShortRateModel*,*TimeGrid*,*YieldTermStructure*)

-
ql.TreeSwaptionEngine(
*ShortRateModel*,*TimeGrid*)

```
model = ql.HullWhite(yts)
engine = ql.TreeSwaptionEngine(model, 10)
swaption.setPricingEngine(g2Engine)
swaption.NPV()
```

## Credit Pricing Engines

### IsdaCdsEngine

-
ql.IsdaCdsEngine(
*defaultProbability*,*recoveryRate*,*yieldTermStructure*,*includeSettlementDateFlows=None*,*numericalFix=ql.IsdaCdsEngine.Taylor*,*AccrualBias accrualBias=ql.IsdaCdsEngine.HalfDayBias*,*forwardsInCouponPeriod=ql.IsdaCdsEngine.Piecewise*)

```
today = ql.Date().todaysDate()
defaultProbability = ql.DefaultProbabilityTermStructureHandle(
ql.FlatHazardRate(today, ql.QuoteHandle(ql.SimpleQuote(0.01)), ql.Actual360())
)
yieldTermStructure = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual360()))
recoveryRate = 0.4
engine = ql.IsdaCdsEngine(defaultProbability, recoveryRate, yieldTermStructure)
```

### MidPointCdsEngine

-
ql.MidPointCdsEngine(
*defaultProbability*,*recoveryRate*,*yieldTermStructure*)

```
today = ql.Date().todaysDate()
defaultProbability = ql.DefaultProbabilityTermStructureHandle(
ql.FlatHazardRate(today, ql.QuoteHandle(ql.SimpleQuote(0.01)), ql.Actual360())
)
yieldTermStructure = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual360()))
recoveryRate = 0.4
engine = ql.MidPointCdsEngine(defaultProbability, recoveryRate, yieldTermStructure)
```

### IntegralCdsEngine

-
ql.IntegralCdsEngine(
*integrationStep*,*probability*,*recoveryRate*,*discountCurve*,*includeSettlementDateFlows=False*)

```
today = ql.Date().todaysDate()
defaultProbability = ql.DefaultProbabilityTermStructureHandle(
ql.FlatHazardRate(today, ql.QuoteHandle(ql.SimpleQuote(0.01)), ql.Actual360())
)
yieldTermStructure = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual360()))
integralStep = ql.Period('1d')
engine = ql.IntegralCdsEngine(integralStep, defaultProbability, 0.4, yieldTermStructure, includeSettlementDateFlows=False)
```

### BlackCdsOptionEngine

-
ql.BlackCdsOptionEngine(
*defaultProbability*,*recoveryRate*,*yieldTermStructure*,*vol*)

```
today = ql.Date().todaysDate()
defaultProbability = ql.DefaultProbabilityTermStructureHandle(
ql.FlatHazardRate(today, ql.QuoteHandle(ql.SimpleQuote(0.01)), ql.Actual360())
)
yieldTermStructure = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual360()))
vol = ql.QuoteHandle(ql.SimpleQuote(0.2))
engine = ql.BlackCdsOptionEngine(defaultProbability, 0.4, yieldTermStructure, vol)
```

## Option Pricing Engines

### Vanilla Options

#### AnalyticEuropeanEngine

-
ql.AnalyticEuropeanEngine(
*GeneralizedBlackScholesProcess*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
volatility = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), 0.1, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
process = ql.BlackScholesMertonProcess(initialValue, dividendTS, riskFreeTS, volatility)
engine = ql.AnalyticEuropeanEngine(process)
```

#### MCEuropeanEngine

-
ql.MCEuropeanEngine(
*GeneralizedBlackScholesProcess*,*traits*,*timeSteps=None*,*timeStepsPerYear=None*,*brownianBridge=False*,*antitheticVariate=False*,*requiredSamples=None*,*requiredTolerance=None*,*maxSamples=None*,*seed=0*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
volatility = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), 0.1, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
process = ql.BlackScholesMertonProcess(initialValue, dividendTS, riskFreeTS, volatility)
steps = 2
rng = "pseudorandom" # could use "lowdiscrepancy"
numPaths = 100000
engine = ql.MCEuropeanEngine(process, rng, steps, requiredSamples=numPaths)
```

#### FdBlackScholesVanillaEngine

Note that this engine is capable of pricing both European and American payoffs!

-
ql.FdBlackScholesVanillaEngine(
*GeneralizedBlackScholesProcess*,*tGrid*,*xGrid*,*dampingSteps=0*,*schemeDesc=ql.FdmSchemeDesc.Douglas()*,*localVol=False*,*illegalLocalVolOverwrite=None*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
volatility = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), 0.1, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
process = ql.BlackScholesMertonProcess(initialValue, dividendTS, riskFreeTS, volatility)
tGrid, xGrid = 2000, 200
engine = ql.FdBlackScholesVanillaEngine(process, tGrid, xGrid)
```

#### MCAmericanEngine

-
ql.MCAmericanEngine(
*GeneralizedBlackScholesProcess*,*traits*,*timeSteps=None*,*timeStepsPerYear=None*,*antitheticVariate=False*,*controlVariate=False*,*requiredSamples=None*,*requiredTolerance=None*,*maxSamples=None*,*seed=0*,*polynomOrder=2*,*polynomType=0*,*nCalibrationSamples=2048*,*antitheticVariateCalibration=None*,*seedCalibration=None*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
volatility = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), 0.1, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
process = ql.BlackScholesMertonProcess(initialValue, dividendTS, riskFreeTS, volatility)
steps = 200
rng = "pseudorandom" # could use "lowdiscrepancy"
numPaths = 100000
engine = ql.MCAmericanEngine(process, rng, steps, requiredSamples=numPaths)
```

#### MCDigitalEngine

This engine prices american (ie. knock-in) cash-or-nothing payoffs only

-
ql.MCDigitalEngine(
*GeneralizedBlackScholesProcess*,*traits*,*timeSteps=None*,*timeStepsPerYear=None*,*brownianBridge=False*,*antitheticVariate=False*,*requiredSamples=None*,*requiredTolerance=None*,*maxSamples=None*,*seed=0*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
volatility = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), 0.1, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
process = ql.BlackScholesMertonProcess(initialValue, dividendTS, riskFreeTS, volatility)
steps = 200
rng = "pseudorandom" # could use "lowdiscrepancy"
numPaths = 100000
engine = ql.MCDigitalEngine(process, rng, steps, requiredSamples=numPaths)
```

#### AnalyticHestonEngine

-
ql.AnalyticHestonEngine(
*HestonModel*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
v0 = 0.005
kappa = 0.8
theta = 0.008
rho = 0.2
sigma = 0.1
hestonProcess = ql.HestonProcess(riskFreeTS, dividendTS, initialValue, v0, kappa, theta, sigma, rho)
hestonModel = ql.HestonModel(hestonProcess)
engine = ql.AnalyticHestonEngine(hestonModel)
```

#### MCEuropeanHestonEngine

-
ql.MCEuropeanHestonEngine(
*HestonProcess*,*traits*,*timeSteps=None*,*timeStepsPerYear=None*,*antitheticVariate=False*,*requiredSamples=None*,*requiredTolerance=None*,*maxSamples=None*,*seed=0*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
v0 = 0.005
kappa = 0.8
theta = 0.008
rho = 0.2
sigma = 0.1
hestonProcess = ql.HestonProcess(riskFreeTS, dividendTS, initialValue, v0, kappa, theta, sigma, rho)
steps = 2
rng = "pseudorandom" # could use "lowdiscrepancy"
numPaths = 100000
engine = ql.MCEuropeanHestonEngine(hestonProcess, rng, steps, requiredSamples=numPaths)
```

#### FdHestonVanillaEngine

If a leverage function (and optional mixing factor) is passed in to this function, it prices using the Heston Stochastic Local Vol model

-
ql.FdHestonVanillaEngine(
*HestonModel*,*tGrid=100*,*xGrid=100*,*vGrid=50*,*dampingSteps=0*,*FdmSchemeDesc=ql.FdmSchemeDesc.Hundsdorfer()*,*leverageFct=LocalVolTermStructure()*,*mixingFactor=1.0*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
v0 = 0.005
kappa = 0.8
theta = 0.008
rho = 0.2
sigma = 0.1
hestonProcess = ql.HestonProcess(riskFreeTS, dividendTS, initialValue, v0, kappa, theta, sigma, rho)
hestonModel = ql.HestonModel(hestonProcess)
tGrid, xGrid, vGrid = 100, 100, 50
dampingSteps = 0
fdScheme = ql.FdmSchemeDesc.ModifiedCraigSneyd()
engine = ql.FdHestonVanillaEngine(hestonModel, tGrid, xGrid, vGrid, dampingSteps, fdScheme)
```

#### AnalyticPTDHestonEngine

-
ql.AnalyticPTDHestonEngine(
*PiecewiseTimeDependentHestonModel*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
times = [1.0, 2.0, 3.0]
grid = ql.TimeGrid(times)
v0 = 0.005
theta = [0.010, 0.015, 0.02]
kappa = [0.600, 0.500, 0.400]
sigma = [0.400, 0.350, 0.300]
rho = [-0.15, -0.10, -0.00]
kappaTS = ql.PiecewiseConstantParameter(times[:-1], ql.PositiveConstraint())
thetaTS = ql.PiecewiseConstantParameter(times[:-1], ql.PositiveConstraint())
rhoTS = ql.PiecewiseConstantParameter(times[:-1], ql.BoundaryConstraint(-1.0, 1.0))
sigmaTS = ql.PiecewiseConstantParameter(times[:-1], ql.PositiveConstraint())
for i, time in enumerate(times):
kappaTS.setParam(i, kappa[i])
thetaTS.setParam(i, theta[i])
rhoTS.setParam(i, rho[i])
sigmaTS.setParam(i, sigma[i])
hestonModelPTD = ql.PiecewiseTimeDependentHestonModel(riskFreeTS, dividendTS, initialValue, v0, thetaTS, kappaTS, sigmaTS, rhoTS, grid)
engine = ql.AnalyticPTDHestonEngine(hestonModelPTD)
```

### Asian Options

#### AnalyticDiscreteGeometricAveragePriceAsianEngine

-
ql.AnalyticDiscreteGeometricAveragePriceAsianEngine(
*GeneralizedBlackScholesProcess*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
volatility = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), 0.1, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
process = ql.BlackScholesMertonProcess(initialValue, dividendTS, riskFreeTS, volatility)
engine = ql.AnalyticDiscreteGeometricAveragePriceAsianEngine(process)
```

#### AnalyticContinuousGeometricAveragePriceAsianEngine

-
ql.AnalyticContinuousGeometricAveragePriceAsianEngine(
*GeneralizedBlackScholesProcess*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
volatility = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), 0.1, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
process = ql.BlackScholesMertonProcess(initialValue, dividendTS, riskFreeTS, volatility)
engine = ql.AnalyticContinuousGeometricAveragePriceAsianEngine(process)
```

#### MCDiscreteGeometricAPEngine

-
ql.MCDiscreteGeometricAPEngine(
*GeneralizedBlackScholesProcess*,*traits*,*brownianBridge=False*,*antitheticVariate=False*,*requiredSamples=None*,*requiredTolerance=None*,*maxSamples=None*,*seed=0*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
volatility = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), 0.1, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
process = ql.BlackScholesMertonProcess(initialValue, dividendTS, riskFreeTS, volatility)
rng = "pseudorandom" # could use "lowdiscrepancy"
numPaths = 100000
engine = ql.MCDiscreteGeometricAPEngine(process, rng, requiredSamples=numPaths)
```

#### MCDiscreteArithmeticAPEngine

-
ql.MCDiscreteArithmeticAPEngine(
*GeneralizedBlackScholesProcess*,*traits*,*brownianBridge=False*,*antitheticVariate=False*,*controlVariate=False*,*requiredSamples=None*,*requiredTolerance=None*,*maxSamples=None*,*seed=0*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
volatility = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), 0.1, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
process = ql.BlackScholesMertonProcess(initialValue, dividendTS, riskFreeTS, volatility)
rng = "pseudorandom" # could use "lowdiscrepancy"
numPaths = 100000
engine = ql.MCDiscreteArithmeticAPEngine(process, rng, requiredSamples=numPaths)
```

#### FdBlackScholesAsianEngine

Note that this engine will throw an error if asked to price Geometric averaging options. It only prices Discrete Arithmetic Asians.

-
ql.FdBlackScholesAsianEngine(
*GeneralizedBlackScholesProcess*,*tGrid=100*,*xGrid=100*,*aGrid=50*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
volatility = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), 0.1, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
process = ql.BlackScholesMertonProcess(initialValue, dividendTS, riskFreeTS, volatility)
tGrid, xGrid, aGrid = 100, 100, 50
engine = ql.FdBlackScholesAsianEngine(process, tGrid=tGrid, xGrid=xGrid, aGrid=aGrid)
```

#### AnalyticDiscreteGeometricAveragePriceAsianHestonEngine

-
ql.AnalyticDiscreteGeometricAveragePriceAsianHestonEngine(
*HestonProcess*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
v0, kappa, theta, rho, sigma = 0.005, 0.8, 0.008, 0.2, 0.1
hestonProcess = ql.HestonProcess(riskFreeTS, dividendTS, initialValue, v0, kappa, theta, sigma, rho)
engine = ql.AnalyticDiscreteGeometricAveragePriceAsianHestonEngine(hestonProcess)
```

#### AnalyticContinuousGeometricAveragePriceAsianHestonEngine

-
ql.AnalyticContinuousGeometricAveragePriceAsianHestonEngine(
*HestonProcess*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
v0, kappa, theta, rho, sigma = 0.005, 0.8, 0.008, 0.2, 0.1
hestonProcess = ql.HestonProcess(riskFreeTS, dividendTS, initialValue, v0, kappa, theta, sigma, rho)
engine = ql.AnalyticContinuousGeometricAveragePriceAsianHestonEngine(hestonProcess)
```

#### MCDiscreteGeometricAPHestonEngine

-
ql.MCDiscreteGeometricAPHestonEngine(
*HestonProcess*,*traits*,*antitheticVariate=False*,*requiredSamples=None*,*requiredTolerance=None*,*maxSamples=None*,*seed=0*,*timeSteps=None*,*timeStepsPerYear=None*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
v0, kappa, theta, rho, sigma = 0.005, 0.8, 0.008, 0.2, 0.1
hestonProcess = ql.HestonProcess(riskFreeTS, dividendTS, initialValue, v0, kappa, theta, sigma, rho)
rng = "pseudorandom" # could use "lowdiscrepancy"
numPaths = 100000
engine = ql.MCDiscreteGeometricAPHestonEngine(hestonProcess, rng, requiredSamples=numPaths)
```

#### MCDiscreteArithmeticAPHestonEngine

-
ql.MCDiscreteArithmeticAPHestonEngine(
*HestonProcess*,*traits*,*antitheticVariate=False*,*requiredSamples=None*,*requiredTolerance=None*,*maxSamples=None*,*seed=0*,*timeSteps=None*,*timeStepsPerYear=None*,*controlVariate=False*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
v0, kappa, theta, rho, sigma = 0.005, 0.8, 0.008, 0.2, 0.1
hestonProcess = ql.HestonProcess(riskFreeTS, dividendTS, initialValue, v0, kappa, theta, sigma, rho)
rng = "pseudorandom" # could use "lowdiscrepancy"
numPaths = 100000
engine = ql.MCDiscreteArithmeticAPHestonEngine(hestonProcess, rng, requiredSamples=numPaths)
```

#### TurnbullWakemanAsianEngine

-
ql.TurnbullWakemanAsianEngine(
*GeneralizedBlackScholesProcess*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
volatility = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), 0.1, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
process = ql.BlackScholesMertonProcess(initialValue, dividendTS, riskFreeTS, volatility)
engine = ql.TurnbullWakemanAsianEngine(process)
```

### Barrier Options

#### BinomialBarrierEngine

-
ql.BinomialBarrierEngine(
*process*,*type*,*steps*)

```
today = ql.Date().todaysDate()
spotHandle = ql.QuoteHandle(ql.SimpleQuote(100))
flatRateTs = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
flatVolTs = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.UnitedStates(), 0.2, ql.Actual365Fixed()))
bsm = ql.BlackScholesProcess(spotHandle, flatRateTs, flatVolTs)
binomialBarrierEngine = ql.BinomialBarrierEngine(bsm, 'crr', 200)
```

#### AnalyticBarrierEngine

-
ql.AnalyticBarrierEngine(
*process*)

```
today = ql.Date().todaysDate()
spotHandle = ql.QuoteHandle(ql.SimpleQuote(100))
flatRateTs = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
flatVolTs = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.UnitedStates(), 0.2, ql.Actual365Fixed()))
bsm = ql.BlackScholesProcess(spotHandle, flatRateTs, flatVolTs)
analyticBarrierEngine = ql.AnalyticBarrierEngine(bsm)
```

#### FdBlackScholesBarrierEngine

-
ql.FdBlackScholesBarrierEngine(
*process*,*tGrid=100*,*xGrid=100*,*dampingSteps=0*,*FdmSchemeDesc=ql.FdmSchemeDesc.Douglas()*,*localVol=False*,*illegalLocalVolOverwrite=None*)

```
today = ql.Date().todaysDate()
spotHandle = ql.QuoteHandle(ql.SimpleQuote(100))
flatRateTs = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
flatVolTs = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.UnitedStates(), 0.2, ql.Actual365Fixed()))
bsm = ql.BlackScholesProcess(spotHandle, flatRateTs, flatVolTs)
fdBarrierEngine = ql.FdBlackScholesBarrierEngine(bsm)
```

#### FdBlackScholesRebateEngine

-
ql.FdBlackScholesRebateEngine(
*process*,*tGrid=100*,*xGrid=100*,*dampingSteps=0*,*FdmSchemeDesc=ql.FdmSchemeDesc.Douglas()*,*localVol=False*,*illegalLocalVolOverwrite=None*)

```
today = ql.Date().todaysDate()
spotHandle = ql.QuoteHandle(ql.SimpleQuote(100))
flatRateTs = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
flatVolTs = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.UnitedStates(), 0.2, ql.Actual365Fixed()))
bsm = ql.BlackScholesProcess(spotHandle, flatRateTs, flatVolTs)
fdRebateEngine = ql.FdBlackScholesRebateEngine(bsm)
```

#### AnalyticBinaryBarrierEngine

-
ql.AnalyticBinaryBarrierEngine(
*process*)

```
today = ql.Date().todaysDate()
spotHandle = ql.QuoteHandle(ql.SimpleQuote(100))
flatRateTs = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
flatVolTs = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.UnitedStates(), 0.2, ql.Actual365Fixed()))
bsm = ql.BlackScholesProcess(spotHandle, flatRateTs, flatVolTs)
analyticBinaryBarrierEngine = ql.AnalyticBinaryBarrierEngine(bsm)
```

#### FdHestonBarrierEngine

If a leverage function (and optional mixing factor) is passed in to this function, it prices using the Heston Stochastic Local Vol model

-
ql.FdHestonBarrierEngine(
*HestonModel*,*tGrid=100*,*xGrid=100*,*vGrid=50*,*dampingSteps=0*,*FdmSchemeDesc=ql.FdmSchemeDesc.Hundsdorfer()*,*leverageFct=LocalVolTermStructure()*,*mixingFactor=1.0*)

```
today = ql.Date().todaysDate()
spotHandle = ql.QuoteHandle(ql.SimpleQuote(100))
flatRateTs = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
flatDividendTs = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
v0, kappa, theta, sigma, rho = 0.01, 2.0, 0.01, 0.01, 0.0
hestonProcess = ql.HestonProcess(flatRateTs, flatDividendTs, spotHandle, v0, kappa, theta, sigma, rho)
hestonModel = ql.HestonModel(hestonProcess)
hestonBarrierEngine = ql.FdHestonBarrierEngine(hestonModel)
```

#### AnalyticDoubleBarrierEngine

-
ql.AnalyticDoubleBarrierEngine(
*process*)

```
today = ql.Date().todaysDate()
spotHandle = ql.QuoteHandle(ql.SimpleQuote(100))
flatRateTs = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
flatVolTs = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.UnitedStates(), 0.2, ql.Actual365Fixed()))
bsm = ql.BlackScholesProcess(spotHandle, flatRateTs, flatVolTs)
analyticDoubleBarrierEngine = ql.AnalyticDoubleBarrierEngine(bsm)
```

#### AnalyticDoubleBarrierBinaryEngine

-
ql.AnalyticDoubleBarrierBinaryEngine(
*process*)

```
today = ql.Date().todaysDate()
spotHandle = ql.QuoteHandle(ql.SimpleQuote(100))
flatRateTs = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
flatVolTs = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.UnitedStates(), 0.2, ql.Actual365Fixed()))
bsm = ql.BlackScholesProcess(spotHandle, flatRateTs, flatVolTs)
analyticDoubleBinaryBarrierEngine = ql.AnalyticDoubleBarrierBinaryEngine(bsm)
```

#### FdHestonDoubleBarrierEngine

If a leverage function (and optional mixing factor) is passed in to this function, it prices using the Heston Stochastic Local Vol model

-
ql.FdHestonDoubleBarrierEngine(
*HestonModel*,*tGrid=100*,*xGrid=100*,*vGrid=50*,*dampingSteps=0*,*FdmSchemeDesc=ql.FdmSchemeDesc.Hundsdorfer()*,*leverageFct=LocalVolTermStructure()*,*mixingFactor=1.0*)

```
today = ql.Date().todaysDate()
spotHandle = ql.QuoteHandle(ql.SimpleQuote(100))
flatRateTs = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
flatDividendTs = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
v0, kappa, theta, sigma, rho = 0.01, 2.0, 0.01, 0.01, 0.0
hestonProcess = ql.HestonProcess(flatRateTs, flatDividendTs, spotHandle, v0, kappa, theta, sigma, rho)
hestonModel = ql.HestonModel(hestonProcess)
hestonDoubleBarrierEngine = ql.FdHestonDoubleBarrierEngine(hestonModel)
```

#### AnalyticPartialTimeBarrierOptionEngine

-
ql.AnalyticPartialTimeBarrierOptionEngine(
*process*)

```
today = ql.Date.todaysDate()
ql.Settings.instance().evaluationDate = today
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
volatility = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), 0.1, ql.Actual365Fixed()))
initialValue = ql.makeQuoteHandle(100)
process = ql.BlackScholesMertonProcess(initialValue, dividendTS, riskFreeTS, volatility)
engine = ql.AnalyticPartialTimeBarrierOptionEngine(process)
```

### Basket Options

#### MCEuropeanBasketEngine

-
ql.MCEuropeanBasketEngine(
*GeneralizedBlackScholesProcess*,*traits*,*timeSteps=None*,*timeStepsPerYear=None*,*brownianBridge=False*,*antitheticVariate=False*,*requiredSamples=None*,*requiredTolerance=None*,*maxSamples=None*,*seed=0*)

```
# Create a StochasticProcessArray for the various underlyings
underlying_spots = [100., 100., 100., 100., 100.]
underlying_vols = [0.1, 0.12, 0.13, 0.09, 0.11]
underlying_corr_mat = [[1, 0.1, -0.1, 0, 0], [0.1, 1, 0, 0, 0.2], [-0.1, 0, 1, 0, 0], [0, 0, 0, 1, 0.15], [0, 0.2, 0, 0.15, 1]]
today = ql.Date().todaysDate()
day_count = ql.Actual365Fixed()
calendar = ql.NullCalendar()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.0, day_count))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.0, day_count))
processes = [ql.BlackScholesMertonProcess(ql.QuoteHandle(ql.SimpleQuote(x)),
dividendTS,
riskFreeTS,
ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, calendar, y, day_count)))
for x, y in zip(underlying_spots, underlying_vols)]
multiProcess = ql.StochasticProcessArray(processes, underlying_corr_mat)
# Create the pricing engine
rng = "pseudorandom"
numSteps = 500000
stepsPerYear = 1
seed = 43
engine = ql.MCEuropeanBasketEngine(multiProcess, rng, timeStepsPerYear=stepsPerYear, requiredSamples=numSteps, seed=seed)
```

### Cliquet Options

### Forward Options

#### ForwardEuropeanEngine

This engine in python implements the C++ engine QuantLib::ForwardVanillaEngine (notice the subtle name change)

-
ql.ForwardEuropeanEngine(
*process*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
volatility = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), 0.1, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
process = ql.BlackScholesMertonProcess(initialValue, dividendTS, riskFreeTS, volatility)
engine = ql.ForwardEuropeanEngine(process)
```

#### MCForwardEuropeanBSEngine

-
ql.MCForwardEuropeanBSEngine(
*process*,*traits*,*timeSteps=None*,*timeStepsPerYear=None*,*brownianBridge=False*,*antitheticVariate=False*,*requiredSamples=None*,*requiredTolerance=None*,*maxSamples=None*,*seed=0*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
volatility = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), 0.1, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
process = ql.BlackScholesMertonProcess(initialValue, dividendTS, riskFreeTS, volatility)
rng = "pseudorandom" # could use "lowdiscrepancy"
numPaths = 100000
engine = ql.MCForwardEuropeanBSEngine(process, rng, timeStepsPerYear=12, requiredSamples=numPaths)
```

#### AnalyticHestonForwardEuropeanEngine

-
ql.AnalyticHestonForwardEuropeanEngine(
*process*,*integrationOrder=144*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
v0, kappa, theta, rho, sigma = 0.005, 0.8, 0.008, 0.2, 0.2
hestonProcess = ql.HestonProcess(riskFreeTS, dividendTS, initialValue, v0, kappa, theta, sigma, rho)
engine = ql.AnalyticHestonForwardEuropeanEngine(hestonProcess)
```

#### MCForwardEuropeanHestonEngine

-
ql.MCForwardEuropeanHestonEngine(
*hestonProcess*,*traits*,*timeSteps=None*,*timeStepsPerYear=None*,*antitheticVariate=False*,*requiredSamples=None*,*requiredTolerance=None*,*maxSamples=None*,*seed=0*,*controlVariate=False*)

```
today = ql.Date().todaysDate()
riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
v0, kappa, theta, rho, sigma = 0.005, 0.8, 0.008, 0.2, 0.2
hestonProcess = ql.HestonProcess(riskFreeTS, dividendTS, initialValue, v0, kappa, theta, sigma, rho)
rng = "pseudorandom" # could use "lowdiscrepancy"
numPaths = 100000
engine = ql.MCForwardEuropeanHestonEngine(hestonProcess, rng, timeStepsPerYear=12, requiredSamples=numPaths)
```