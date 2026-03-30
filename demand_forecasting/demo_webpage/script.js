mapboxgl.accessToken = "pk.eyJ1IjoiZHJhd2luZW5peCIsImEiOiJjbWhxMnN2bWMwcXh4MmlwZ3U1NW1lajZ4In0.W4PXC4PjsbhOz3YTCDtD1w"; //

let globalData = [];
const countrySelect = document.getElementById("countrySelect");
const citySelect = document.getElementById("citySelect");
const dateSelect = document.getElementById("dateSelect");
const barContainer = document.getElementById("barContainer");
const barTitle = document.getElementById("barTitle");

const map = new mapboxgl.Map({
    container: "map",
    style: "mapbox://styles/mapbox/light-v11",
    center: [0, 20],
    zoom: 1.5
});

let markers = [];

fetch('sample_data.json')
    .then(res => res.json())
    .then(data => {
        globalData = data;
        initFilters();
        updateMap();
    });

function initFilters() {

    const countries = [...new Set(globalData.map(d => d.country))].sort();
    countrySelect.innerHTML = countries.map(c => `<option value="${c}">${c}</option>`).join('');


    const dates = globalData.map(d => d.date);
    dateSelect.value = dates.includes("2024-11-14") ? "2024-11-14" : dates[0];

    updateCityOptions();
}

function updateCityOptions() {
    const selectedCountry = countrySelect.value;
    const cities = [...new Set(globalData.filter(d => d.country === selectedCountry).map(d => d.city))].sort();
    citySelect.innerHTML = cities.map(c => `<option value="${c}">${c}</option>`).join('');
}

function updateMap() {
    markers.forEach(m => m.remove());
    markers = [];
    barContainer.classList.add("hidden");

    const country = countrySelect.value;
    const city = citySelect.value;
    const date = dateSelect.value;

    const filtered = globalData.filter(d => d.country === country && d.city === city && d.date === date);

    filtered.forEach(d => {

        const el = document.createElement("div");
        el.className = 'marker';

        el.style.backgroundImage = "url(https://cdn-icons-png.flaticon.com/512/1356/1356596.png)";
        el.style.width = "35px";
        el.style.height = "35px";
        el.style.backgroundSize = "contain";
        el.style.backgroundRepeat = "no-repeat";
        el.style.cursor = "pointer";

        const marker = new mapboxgl.Marker(el)
            .setLngLat([d.lon, d.lat])
            .addTo(map);

        el.addEventListener("click", () => showBarChart(d));
        markers.push(marker);
    });

    if (filtered.length > 0) {
        map.flyTo({ 
            center: [filtered[0].lon, filtered[0].lat], 
            zoom: 12 
        });
    }
}

function showBarChart(storeData) {
    barContainer.classList.remove("hidden");
    barTitle.innerText = storeData.store_name;

    const products = storeData.products.map(p => `SKU ${p.id}`);
    const sales = storeData.products.map(p => p.weekly_sale);
    const forecasts = storeData.products.map(p => p.weekly_forecast);

    const rowHeight = 40; 
    const dynamicHeight = Math.max(300, products.length * rowHeight);

    const traces = [
        { 
            y: products, x: sales, type: "bar", orientation: "h", 
            name: "Thực tế", marker: { color: "#3498db" } 
        },
        { 
            y: products, x: forecasts, type: "bar", orientation: "h", 
            name: "Dự báo", marker: { color: "#e74c3c", opacity: 0.7 } 
        }
    ];

    const layout = {
        barmode: "group",
        height: dynamicHeight,
        margin: { l: 80, r: 20, t: 0, b: 0 },
        yaxis: { autorange: "reversed", automargin: true },
        xaxis: { visible: true },
        showlegend: false,
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)'
    };

    Plotly.newPlot("barChart", traces, layout, { responsive: true, displayModeBar: false });
    
    document.querySelector('.bar-body').scrollTop = 0;
}

function closeChart() { barContainer.classList.add("hidden"); }

countrySelect.addEventListener("change", () => { updateCityOptions(); updateMap(); });
citySelect.addEventListener("change", updateMap);
dateSelect.addEventListener("change", updateMap);