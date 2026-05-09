let token = null;
const initData = window.Bale.WebApp.initData;


const res = await fetch("/auth/miniapp", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
        initData: initData
    })
});

// 📌 گرفتن user از Bale (Mock اگر نبود)
function getBaleUser() {
    if (window.Bale && Bale.WebApp) {
        return Bale.WebApp.initDataUnsafe.user;
    }

    // fallback تست
    return {
        id: 12345,
        first_name: "Test"
    };
}

// 🔐 login
async function login() {
    const user = getBaleUser();

    const res = await fetch("/auth/miniapp", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({user})
    });

    const data = await res.json();
    token = data.token;
}

// 📦 گرفتن پلن‌ها
async function loadPlans() {
    const res = await fetch("/plans");
    const plans = await res.json();

    const container = document.getElementById("plans");
    container.innerHTML = "";

    plans.forEach(p => {
        const div = document.createElement("div");
        div.className = "card";

        div.innerHTML = `
            <h3>${p.name}</h3>
            <p>${p.price} تومان</p>
            <p>${p.duration} روز</p>
            <button onclick="buy(${p.id})">خرید</button>
        `;

        container.appendChild(div);
    });
}

// 💰 خرید
async function buy(planId) {
    const res = await fetch("/subscription/buy", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({plan_id: planId})
    });

    const data = await res.json();
    alert(JSON.stringify(data));
}

// 🚀 init
(async function () {
    await login();
    await loadPlans();
})();