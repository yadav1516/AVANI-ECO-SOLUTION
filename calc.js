document.addEventListener('DOMContentLoaded', function () {
    // Elements
    const billInput = document.getElementById('billInput');
    const billSlider = document.getElementById('billSlider');
    const pincodeInput = document.getElementById('pincode');
    const cityInput = document.getElementById('city');
    const pincodeError = document.getElementById('pincodeError');
    const emiSlider = document.getElementById('emiSlider');
    const emiTenureDisplay = document.getElementById('emiTenureDisplay');

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

    // Constants & Calibration
    // Calibration based on user example: ₹10,694 bill -> 10.26 kW system
    const BILL_TO_KW_RATIO = 10.26 / 10694;
    const ROOF_AREA_PER_KW = 608 / 10.26; // ~59.2 sq ft per kW
    const COST_PER_KW = 588000 / 10.26; // ~₹57,310 per kW

    // Subsidies (PM Surya Ghar 2025)
    const SUBSIDY_1KW = 30000;
    const SUBSIDY_2KW = 60000;
    const SUBSIDY_MAX = 78000;
    const STATE_SUBSIDY_FLAT = 30000; // Assuming flat state subsidy for now based on example

    // EMI
    const INTEREST_RATE = 12; // % p.a.

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

    function formatCurrency(num) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            maximumFractionDigits: 0
        }).format(num);
    }

    function calculateSolar() {
        const monthlyBill = parseInt(billInput.value);
        const tenureYears = parseInt(emiSlider.value);

        // 1. System Size
        let systemSize = monthlyBill * BILL_TO_KW_RATIO;
        // Round to 2 decimal places
        systemSize = Math.round(systemSize * 100) / 100;

        // 2. Roof Area
        const roofArea = Math.round(systemSize * ROOF_AREA_PER_KW);

        // 3. Financials
        const totalCost = Math.round(systemSize * COST_PER_KW);

        // Central Subsidy
        // Central Subsidy (PM Surya Ghar 2025)
        // Rule: ₹30,000/kW for first 2 kW. ₹18,000/kW for additional capacity up to 3 kW. Max ₹78,000.
        let centralSubsidy = 0;
        if (systemSize <= 2) {
            centralSubsidy = systemSize * 30000;
        } else if (systemSize <= 3) {
            centralSubsidy = 60000 + (systemSize - 2) * 18000;
        } else {
            centralSubsidy = 78000;
        }

        // Cap subsidy if it exceeds cost (unlikely but safe)
        centralSubsidy = Math.min(centralSubsidy, totalCost);

        // State Subsidy (Mock logic: UP/Haryana style, max 30k)
        // Many states like UP give ₹15,000/kW up to max ₹30,000.
        let stateSubsidy = 0;
        if (systemSize > 0) {
            stateSubsidy = Math.min(systemSize * 15000, 30000);
        }

        const netCost = totalCost - centralSubsidy - stateSubsidy;

        // 4. Savings
        // User example: ₹10,694 bill -> ₹10,694 monthly savings (100% offset)
        const monthlySavings = monthlyBill;
        const annualSavings = monthlySavings * 12;
        const lifetimeSavings = annualSavings * 25;

        // 5. ROI
        // ROI % = (Annual Savings / Net Cost) * 100
        const roiPercent = (annualSavings / netCost) * 100;

        // 6. EMI
        // Down Payment logic from user example:
        // Total Cost: 588k. Subsidy: 108k (78+30). Net: 480k.
        // User example shows "Minimum Down Payment ₹108,000" and "Subsidy -₹108,000" -> Net Down Payment ₹0.
        // This implies the subsidy is used as the down payment.
        const totalSubsidy = centralSubsidy + stateSubsidy;
        const downPayment = totalSubsidy; // Subsidy covers down payment
        const netDownPayment = 0;

        // Loan Amount = Net Cost
        const loanAmount = netCost;
        const monthlyInterest = INTEREST_RATE / 12 / 100;
        const months = tenureYears * 12;

        const emi = (loanAmount * monthlyInterest * Math.pow(1 + monthlyInterest, months)) / (Math.pow(1 + monthlyInterest, months) - 1);

        // 7. Environmental Impact
        // User example: 10.26kW -> 12,066 kg CO2
        // Ratio: 12066 / 10.26 = ~1176 kg/kW/year? No, likely lifetime or specific period.
        // Let's use the ratio from the example directly.
        const co2Mitigated = Math.round(systemSize * (12066 / 10.26));
        const treesPlanted = Math.round(systemSize * (402 / 10.26));
        const distanceDriven = Math.round(systemSize * (107730 / 10.26));

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
        // netDownPayment is static 0 in UI for now as per design pattern

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
