document.addEventListener('DOMContentLoaded', function () {
    // Elements
    const billInput = document.getElementById('billInput');
    const billSlider = document.getElementById('billSlider');
    const pincodeInput = document.getElementById('pincode');
    const cityInput = document.getElementById('city');
    const pincodeError = document.getElementById('pincodeError');
    const emiSlider = document.getElementById('emiSlider');
    const emiTenureDisplay = document.getElementById('emiTenureDisplay');

    // Sync Input and Slider
    billInput.addEventListener('input', function () {
        let val = parseInt(this.value);
        if (val < 500) val = 500;
        billSlider.value = val;
        calculateSolar();
    });

    billSlider.addEventListener('input', function () {
        billInput.value = this.value;
        calculateSolar();
    });

    emiSlider.addEventListener('input', function () {
        emiTenureDisplay.innerText = this.value + (this.value == 1 ? " year" : " years");
        calculateSolar();
    });

    // Pincode Logic (Real API)
    pincodeInput.addEventListener('input', function () {
        const pin = this.value;
        if (pin.length === 6 && /^\d+$/.test(pin)) {
            fetchCityFromPincode(pin);
        } else {
            pincodeError.innerText = "";
        }
    });
    // Header Scroll Effect
    const header = document.querySelector('.header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    }

    // Result Elements
    const recSystemSize = document.getElementById('recSystemSize');
    const roofAreaEl = document.getElementById('roofArea');
    const monthlySavingsEl = document.getElementById('monthlySavings');
    const annualSavingsEl = document.getElementById('annualSavings');
    const systemCostEl = document.getElementById('systemCost');
    const centralSubsidyEl = document.getElementById('centralSubsidy');
    const stateSubsidyEl = document.getElementById('stateSubsidy');
    const netCostEl = document.getElementById('netCost');
    const lifetimeSavingsEl = document.getElementById('lifetimeSavings');
    const roiPercentEl = document.getElementById('roiPercent');

    // EMI Elements
    const downPaymentEl = document.getElementById('downPayment');
    const subsidyAdjustmentEl = document.getElementById('subsidyAdjustment');
    const monthlyEMIEl = document.getElementById('monthlyEMI');

    // Impact Elements
    const co2MitigatedEl = document.getElementById('co2Mitigated');
    const treesPlantedEl = document.getElementById('treesPlanted');
    const distanceDrivenEl = document.getElementById('distanceDriven');

    // Constants & Calibration based on User Data Analysis
    // Analysis of screenshots:
    // 1. Bill ₹3000 -> 3.78kW (Ratio: 0.00126)
    // 2. Bill ₹3700 -> 4.86kW (Ratio: 0.00131)
    // 3. Bill ₹5400 -> 7.02kW (Ratio: 0.0013)
    // using avg ratio 0.0013
    const BILL_TO_KW_RATIO = 0.0013;

    // Roof Area: 224/3.78 = 59.25, 288/4.86 = 59.25. Constant.
    const ROOF_AREA_PER_KW = 59.26;

    // Savings: 
    // Monthly: 3940/3.78 = 1042.32
    // Yearly: 47280/3.78 = 12507.9
    const MONTHLY_SAVINGS_PER_KW = 1042.33;
    const YEARLY_SAVINGS_PER_KW = 12508;

    // Cost Tiers (Keeping previous market estimates as screenshots cost isn't explicit per kW)
    // < 3kW: ~₹75,000/kW
    // 3kW - 10kW: ~₹60,000/kW
    // > 10kW: ~₹55,000/kW
    function getSystemCost(capacityKw) {
        if (capacityKw <= 3) return capacityKw * 75000;
        if (capacityKw <= 10) return capacityKw * 60000;
        return capacityKw * 55000;
    }

    // Subsidies (PM Surya Ghar 2025)
    function getCentralSubsidy(capacityKw) {
        if (capacityKw <= 2) {
            return capacityKw * 30000;
        } else if (capacityKw <= 3) {
            return 60000 + (capacityKw - 2) * 18000;
        } else {
            return 78000;
        }
    }

    // EMI
    // Pincode API Function
    async function fetchCityFromPincode(pincode) {
        try {
            pincodeError.innerText = "Fetching city...";
            const response = await fetch(`https://api.postalpincode.in/pincode/${pincode}`);
            const data = await response.json();

            if (data[0].Status === "Success") {
                const city = data[0].PostOffice[0].District;
                const state = data[0].PostOffice[0].State;
                cityInput.value = `${city}, ${state}`;
                pincodeError.innerText = "";
                pincodeError.style.color = "green";
            } else {
                pincodeError.innerText = "Invalid Pincode";
                pincodeError.style.color = "red";
                cityInput.value = "";
            }
        } catch (error) {
            console.error("Error fetching pincode:", error);
            pincodeError.innerText = "Error fetching details";
            cityInput.value = "";
        }
    }

    const INTEREST_RATE = 10.5; // % p.a. (Typical solar loan rate)

    function calculateSolar() {
        const monthlyBill = parseInt(billInput.value);
        const tenureYears = parseInt(emiSlider.value);

        // 1. Calculate Required System Size
        let systemSize = monthlyBill * BILL_TO_KW_RATIO;

        // Round to 2 decimal places, min 1kW
        systemSize = Math.max(1, Math.round(systemSize * 100) / 100);

        // 2. Roof Area
        const roofArea = Math.round(systemSize * ROOF_AREA_PER_KW);

        // 3. Financials
        const totalCost = Math.round(getSystemCost(systemSize));
        let centralSubsidy = Math.round(getCentralSubsidy(systemSize));

        // Cap subsidy if it exceeds cost
        centralSubsidy = Math.min(centralSubsidy, totalCost);

        // State Subsidy (Additional ~₹15k-30k in some states, keep conservative)
        let stateSubsidy = 0;
        if (systemSize > 0) {
            stateSubsidy = Math.min(systemSize * 15000, 30000);
        }

        const netCost = totalCost - centralSubsidy - stateSubsidy;

        // 4. Savings (SolarSquare Model: 1% Degradation, 3% Inflation)
        const annualSavingsStart = Math.round(systemSize * YEARLY_SAVINGS_PER_KW);

        let lifetimeSavings = 0;
        let currentAnnualSavings = annualSavingsStart;

        for (let year = 1; year <= 25; year++) {
            lifetimeSavings += currentAnnualSavings;
            // Combined effect: degradation reduces gen but inflation increases value
            // Gen * 0.99, Tariff * 1.03 -> Savings * (0.99 * 1.03) = Savings * 1.0197
            currentAnnualSavings *= 1.0197;
        }

        const annualSavings = annualSavingsStart;
        const monthlySavings = Math.round(systemSize * MONTHLY_SAVINGS_PER_KW);
        lifetimeSavings = Math.round(lifetimeSavings);

        // 5. ROI
        // ROI % = (Year 1 Savings / Net Cost) * 100
        const roiPercent = (annualSavings / netCost) * 100;

        // 6. EMI
        // Assumption: Subsidy is credited later, so loan is on Net Cost + Subsidy usually, 
        // but for "Zero Investment" marketing, we often show Net Cost financing.
        // Let's stick to the previous pattern: Down Payment = Subsidy Amount (Client pays upfront, gets back)
        // OR Net Cost financing.
        // User's previous logic: "Net Down Payment 0" -> Subsidy adjusted.
        const totalSubsidy = centralSubsidy + stateSubsidy;
        const downPayment = totalSubsidy;

        // Loan Amount = Net Cost (Assumption: Client finances the rest)
        const loanAmount = netCost;
        const monthlyInterest = INTEREST_RATE / 12 / 100;
        const months = tenureYears * 12;

        const emi = (loanAmount * monthlyInterest * Math.pow(1 + monthlyInterest, months)) / (Math.pow(1 + monthlyInterest, months) - 1);

        // 7. Environmental Impact
        // User example: 10.26kW -> 12,066 kg CO2. Ratio: ~1176 kg/kW
        const co2Mitigated = Math.round(systemSize * 1176);
        const treesPlanted = Math.round(systemSize * 40); // Approx 
        const distanceDriven = Math.round(systemSize * 10500); // Approx

        // Update UI
        recSystemSize.innerText = systemSize.toFixed(2) + " kW";
        roofAreaEl.innerText = roofArea + " sq. ft.";

        monthlySavingsEl.innerText = formatCurrency(monthlySavings);
        annualSavingsEl.innerText = formatCurrency(annualSavings);

        systemCostEl.innerText = formatCurrency(totalCost);
        centralSubsidyEl.innerText = "-" + formatCurrency(centralSubsidy);
        stateSubsidyEl.innerText = "-" + formatCurrency(stateSubsidy);
        netCostEl.innerText = formatCurrency(netCost);

        lifetimeSavingsEl.innerText = formatCurrency(lifetimeSavings);
        roiPercentEl.innerText = roiPercent.toFixed(2) + "% p.a.";

        downPaymentEl.innerText = formatCurrency(downPayment);
        subsidyAdjustmentEl.innerText = "-" + formatCurrency(totalSubsidy);

        monthlyEMIEl.innerText = formatCurrency(Math.round(emi));

        co2MitigatedEl.innerText = new Intl.NumberFormat('en-IN').format(co2Mitigated) + " Kg";
        treesPlantedEl.innerText = new Intl.NumberFormat('en-IN').format(treesPlanted);
        distanceDrivenEl.innerText = new Intl.NumberFormat('en-IN').format(distanceDriven) + " Kms";
    }

    // Impact Dashboard Counters (Hero Section)
    const impactSection = document.querySelector('.impact-dashboard');
    const impactCounters = document.querySelectorAll('.impact-number');
    let impactStarted = false;

    const startImpactCounters = () => {
        impactCounters.forEach(counter => {
            const target = +counter.getAttribute('data-target');
            const duration = 2500;
            const increment = target / (duration / 16);

            let current = 0;
            const updateCounter = () => {
                current += increment;
                if (current < target) {
                    counter.innerText = Math.ceil(current).toLocaleString();
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.innerText = target.toLocaleString() + '+';
                }
            };
            updateCounter();
        });
    };

    if (impactSection) {
        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting && !impactStarted) {
                startImpactCounters();
                impactStarted = true;
            }
        }, { threshold: 0.5 });
        observer.observe(impactSection);
    }

    // Initial Calculation
    calculateSolar();
});

function openLeadForm() {
    alert("Opening consultation booking form...");
}
