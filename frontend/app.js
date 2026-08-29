let scenario = 1;

const samples = {
    1: {
        product: "Premium Coffee Beans",
        recommended_quantity: 800,
        current_inventory: 300,
        expected_demand: 850,
        open_purchase_orders: 200,
        supplier_lead_time_days: 5,
        supplier_minimum_order: 100,
        available_budget: 25000,
        unit_price: 20,
        storage_capacity: 1500
    },
    2: {
        product: "Organic Milk",
        original_purchase_order: 500,
        supplier_confirmed_quantity: 250,
        current_inventory: 80,
        expected_demand: 400,
        alternative_supplier_available: true,
        alternative_supplier_quantity: 250,
        alternative_supplier_unit_price: 24,
        current_supplier_unit_price: 20,
        available_budget: 10000
    }
};

const $ = id => document.getElementById(id);

document.querySelectorAll(".nav").forEach(btn => {
    btn.addEventListener("click", () => setScenario(Number(btn.dataset.scenario)));
});

$("sample").addEventListener("click", loadSample);
$("reset").addEventListener("click", () => {
    loadSample();
    clearOutput();
});

function setScenario(value) {
    scenario = value;

    document.querySelectorAll(".nav").forEach(btn =>
        btn.classList.toggle("active", Number(btn.dataset.scenario) === scenario)
    );

    $("form1").classList.toggle("hidden", scenario !== 1);
    $("form2").classList.toggle("hidden", scenario !== 2);

    $("scenarioNo").textContent = scenario === 1 ? "01" : "02";
    $("pageTitle").textContent = scenario === 1
        ? "Purchase Recommendation Review"
        : "Supplier Shortfall";
    $("pageSubtitle").textContent = scenario === 1
        ? "Investigate constraints before approving a purchasing recommendation."
        : "Decide what should happen when a supplier cannot fulfil the original PO.";
    $("formTitle").textContent = scenario === 1
        ? "Purchasing situation"
        : "Supplier situation";
    $("heroTitle").textContent = scenario === 1
        ? "Should we buy 800 units?"
        : "Supplier can only fulfil 250 units";
    $("heroText").textContent = scenario === 1
        ? "The agent checks inventory, demand, open POs, supplier constraints, budget and storage before deciding."
        : "The agent checks the shortfall, inventory coverage, alternative suppliers and budget before choosing the next action.";

    loadSample();
    clearOutput();
}

function loadSample() {
    const data = samples[scenario];
    const form = scenario === 1 ? $("form1") : $("form2");

    Object.entries(data).forEach(([name, value]) => {
        const input = form.querySelector(`[name="${name}"]`);
        if (!input) return;
        if (input.type === "checkbox") input.checked = value;
        else input.value = value;
    });
}

function getData() {
    const container = scenario === 1 ? $("form1") : $("form2");
    const data = {};

    container.querySelectorAll("[name]").forEach(input => {
        data[input.name] = input.type === "checkbox"
            ? input.checked
            : input.type === "number"
                ? Number(input.value)
                : input.value;
    });

    return data;
}

$("form").addEventListener("submit", async event => {
    event.preventDefault();

    const button = document.querySelector(".analyze");
    button.disabled = true;
    button.innerHTML = "<span>◌</span> Agent investigating...";

    try {
        const endpoint = scenario === 1
            ? "/api/scenario1/analyze"
            : "/api/scenario2/analyze";

        const response = await fetch(endpoint, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(getData())
        });

        if (!response.ok) {
            const text = await response.text();
            throw new Error(text);
        }

        render(await response.json());
    } catch (error) {
        console.error(error);
        alert("Backend connection failed. Make sure uvicorn is running.");
    } finally {
        button.disabled = false;
        button.innerHTML = "<span>✦</span> Analyze with Purchasing Agent";
    }
});

function render(result) {
    $("empty").classList.add("hidden");
    $("output").classList.remove("hidden");

    $("metric").textContent = result.decision;
    $("metricHint").textContent = result.validation_passed
        ? "Validated action"
        : "Needs investigation";

    $("decision").textContent = result.decision;
    $("summary").textContent = result.summary;
    $("action").textContent = result.action;
    $("validation").textContent = result.validation_message;
    $("icon").textContent = result.validation_passed ? "✓" : "!";

    const badge = $("badge");
    badge.textContent = result.validation_passed ? "VALIDATED" : "FAILED";
    badge.className = "badge " + (result.validation_passed ? "pass" : "fail");

    fill("factors", result.important_factors);
    fill("risks", result.risks.length ? result.risks : ["No material risks identified."]);
}

function fill(id, items) {
    const element = $(id);
    element.innerHTML = "";
    items.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        element.appendChild(li);
    });
}

function clearOutput() {
    $("empty").classList.remove("hidden");
    $("output").classList.add("hidden");
    $("metric").textContent = "—";
    $("metricHint").textContent = "Run analysis to calculate";
    $("badge").textContent = "PENDING";
    $("badge").className = "badge pending";
}

setScenario(1);
