/* ==========================================================================
   ASMEBEL / QAVS MEBEL TELEGRAM MINI APP LOGIC (app.js)
   ========================================================================== */

// Telegram WebApp SDK initialization
const tg = window.Telegram?.WebApp || {
  expand: () => {},
  ready: () => {},
  close: () => {},
  sendData: (data) => console.log('Telegram SendData:', data),
  initDataUnsafe: {
    user: { id: 12345678, first_name: "Foydalanuvchi", last_name: "", username: "telegram_user" }
  }
};

tg.expand();
tg.ready();

// API base URL - Telegram ichida window.location.origin ngrok/server URL ni beradi
let API_BASE = window.location.origin || '';
// Agar WEBAPP_URL environment'dan kelsa, uni ishlatamiz
if (!API_BASE || API_BASE === 'null') {
  API_BASE = 'http://localhost:8080';
}

// State Management
let currentTab = 'home';
let currentLang = 'uz';

let selectedKitchenShape = 'straight';
let selectedKitchenColor = { hex: '#ffffff', name: 'Oq Gloss' };
let kitchenPaymentType = 'full'; // 'full', '3m', '6m', '12m'
let kitchenCalculatedTotal = 0;

let selectedWardrobeType = 'kupe';
let selectedWardrobeColor = { hex: '#ffffff', name: 'Oq Gloss' };
let wardrobePaymentType = 'full';
let wardrobeCalculatedTotal = 0;

let cart = [];
let userOrders = JSON.parse(localStorage.getItem('asmebel_orders') || '[]');
let productsList = [];

// Multilingual i18n Translations
const i18n = {
  uz: {
    top_badge: "ASMEBEL Premium 3D Konstruktor",
    home_subtitle: "BOSH SAHIFA",
    card_kitchen_title: "Oshxona konstruktori",
    card_kitchen_desc: "Oshxona loyihangizni yarating",
    card_wardrobe_title: "Shkof konstruktori",
    card_wardrobe_desc: "Shkof va gardirob loyihasi",
    card_shop_title: "Do'kon",
    card_orders_title: "Buyurtmalarim",
    measurer_title: "Uyga bepul o'lchovchi chaqirish",
    measurer_desc: "Mutaxassisimiz manzilingizga borib o'lchov va 3D maslahat beradi",
    promo_title: "💳 Bo'lib to'lash imkoniyati",
    promo_desc: "Barcha mebellarni 3, 6 va 12 oyga muddatli to'lovga xarid qilishingiz mumkin!",
    kitchen_header: "Oshxona Konstruktori",
    kitchen_sub: "Oshxona o'lchami, materiali va rangini tanlang hamda narxini hisoblang",
    preview_title: "🎮 Interaktiv Visual Ko'rinish",
    color_label: "Fasad va Mebel Rangi",
    shape_label: "Oshxona shakli",
    shape_straight: "To'g'ri (I)",
    shape_lshape: "L-simon (L)",
    shape_ushape: "U-simon (U)",
    len_label: "Uzunligi",
    height_label: "Balandligi",
    facade_label: "Fasad materiali",
    top_label: "Stoleshnitsa (Stol usti) materiali",
    payment_type_label: "To'lov Turi",
    total_label: "Taxminiy Loyiha Narxi:",
    calc_note: "* Yakuniy narx aniq o'lchovdan so'ng belgilanadi",
    wardrobe_header: "Shkof & Gardirob Konstruktori",
    wardrobe_sub: "Shkof turini tanlang, bo'limlarni sozlang va narxni hisoblang",
    preview_w_title: "🚪 Shkof Modellari va Tuzilishi",
    w_type_label: "Shkof turi",
    width_label: "Kengligi",
    doors_label: "Eshiklar soni",
    drawers_label: "Tortmalar soni",
    w_mat_label: "Material",
    mirror_label: "Fasadga oyna o'rnatish (🪞 Oyna eshik)",
    total_w_label: "Taxminiy Shkof Narxi:",
    calc_w_note: "* Mexanizmlar va yetkazib berish o'z ichiga olingan",
    shop_header: "Mebel Do'koni",
    shop_sub: "Tayyor va buyurtma mebellar katalogi",
    cat_all: "Barchasi",
    cat_kitchen: "Oshxona",
    cat_bedroom: "Yotoqxona",
    cat_tv: "TV Zona",
    cat_wardrobe: "Gardirob",
    cat_office: "Ofis",
    orders_header: "Mening Buyurtmalarim",
    orders_sub: "Yuborilgan va faol buyurtmalaringiz holati",
    profile_header: "Foydalanuvchi Profili",
    phone_label: "Telefon raqamingiz",
    address_label: "Yetkazib berish manzili",
    save_btn: "💾 Ma'lumotlarni Saqlash",
    support_title: "💬 Qo'llab-quvvatlash va Konsultatsiya",
    support_desc: "Savollaringiz bormi? Administrator bilan to'g'ridan-to'g'ri bog'laning.",
    admin_btn: "👨‍💼 Admin bilan bog'lanish",
    cart_title: "🛒 Xarid Savatchasi",
    total_cart: "Jami summa:",
    checkout_btn: "✅ Buyurtmani rasmiylashtirish",
    measurer_modal_title: "📐 Uyga Bepul O'lchovchi Chaqirish",
    nav_home: "Bosh sahifa",
    nav_kitchen: "Oshxona",
    nav_wardrobe: "Shkof",
    nav_shop: "Do'kon",
    nav_orders: "Buyurtmalar",
    nav_profile: "Profil"
  },
  ru: {
    top_badge: "ASMEBEL Премиум 3D Конструктор",
    home_subtitle: "ГЛАВНАЯ СТРАНИЦА",
    card_kitchen_title: "Конструктор кухни",
    card_kitchen_desc: "Создайте проект вашей кухни",
    card_wardrobe_title: "Конструктор шкафов",
    card_wardrobe_desc: "Проект шкафа и гардероба",
    card_shop_title: "Магазин",
    card_orders_title: "Мои заказы",
    measurer_title: "Вызов замерщика на дом бесплатно",
    measurer_desc: "Наш специалист приедет для замера и 3D консультации",
    promo_title: "💳 Рассрочка платежа",
    promo_desc: "Всю мебель можно приобрести в рассрочку на 3, 6 и 12 месяцев!",
    kitchen_header: "Конструктор Кухни",
    kitchen_sub: "Выберите размеры, материалы и цвет кухни для расчета стоимости",
    preview_title: "🎮 Интерактивный 2D Просмотр",
    color_label: "Цвет фасада и мебели",
    shape_label: "Форма кухни",
    shape_straight: "Прямая (I)",
    shape_lshape: "Г-образная (L)",
    shape_ushape: "П-образная (U)",
    len_label: "Длина",
    height_label: "Высота",
    facade_label: "Материал фасада",
    top_label: "Материал столешницы",
    payment_type_label: "Тип оплаты",
    total_label: "Примерная стоимость проекта:",
    calc_note: "* Окончательная цена определяется после точного замера",
    wardrobe_header: "Конструктор Шкафов",
    wardrobe_sub: "Выберите тип шкафа, настройте секции и рассчитайте стоимость",
    preview_w_title: "🚪 Модель и структура шкафа",
    w_type_label: "Тип шкафа",
    width_label: "Ширина",
    doors_label: "Количество дверей",
    drawers_label: "Количество ящиков",
    w_mat_label: "Материал",
    mirror_label: "Зеркало на фасаде (🪞 Зеркальная дверь)",
    total_w_label: "Примерная цена шкафа:",
    calc_w_note: "* Механизмы и доставка включены в стоимость",
    shop_header: "Магазин Мебели",
    shop_sub: "Каталог готовой мебели и на заказ",
    cat_all: "Все",
    cat_kitchen: "Кухни",
    cat_bedroom: "Спальни",
    cat_tv: "ТВ Зоны",
    cat_wardrobe: "Шкафы",
    cat_office: "Офисная",
    orders_header: "Мои Заказы",
    orders_sub: "Статус ваших отправленных заказов",
    profile_header: "Профиль Пользователя",
    phone_label: "Ваш номер телефона",
    address_label: "Адрес доставки",
    save_btn: "💾 Сохранить данные",
    support_title: "💬 Поддержка и Консультация",
    support_desc: "Есть вопросы? Свяжитесь с администратором напрямую.",
    admin_btn: "👨‍💼 Связаться с админом",
    cart_title: "🛒 Корзина Покупок",
    total_cart: "Итоговая сумма:",
    checkout_btn: "✅ Оформить заказ",
    measurer_modal_title: "📐 Бесплатный Вызов Замерщика",
    nav_home: "Главная",
    nav_kitchen: "Кухня",
    nav_wardrobe: "Шкафы",
    nav_shop: "Магазин",
    nav_orders: "Заказы",
    nav_profile: "Профиль"
  },
  en: {
    top_badge: "ASMEBEL Premium 3D Constructor",
    home_subtitle: "HOME PAGE",
    card_kitchen_title: "Kitchen Constructor",
    card_kitchen_desc: "Create your kitchen design",
    card_wardrobe_title: "Wardrobe Constructor",
    card_wardrobe_desc: "Wardrobe and cabinet design",
    card_shop_title: "Shop",
    card_orders_title: "My Orders",
    measurer_title: "Free Home Measurement",
    measurer_desc: "Our specialist will come to take measurements and give 3D advice",
    promo_title: "💳 Installment Payment Available",
    promo_desc: "Buy all furniture on installment for 3, 6, or 12 months!",
    kitchen_header: "Kitchen Constructor",
    kitchen_sub: "Select kitchen size, material, and color to calculate cost",
    preview_title: "🎮 Interactive 2D Preview",
    color_label: "Facade and Furniture Color",
    shape_label: "Kitchen Shape",
    shape_straight: "Straight (I)",
    shape_lshape: "L-Shaped (L)",
    shape_ushape: "U-Shaped (U)",
    len_label: "Length",
    height_label: "Height",
    facade_label: "Facade Material",
    top_label: "Countertop Material",
    payment_type_label: "Payment Type",
    total_label: "Estimated Project Cost:",
    calc_note: "* Final price determined after accurate measurement",
    wardrobe_header: "Wardrobe & Cabinet Constructor",
    wardrobe_sub: "Select cabinet type, configure sections, and calculate cost",
    preview_w_title: "🚪 Cabinet Models and Structure",
    w_type_label: "Cabinet Type",
    width_label: "Width",
    doors_label: "Number of Doors",
    drawers_label: "Number of Drawers",
    w_mat_label: "Material",
    mirror_label: "Mirror on Facade (🪞 Mirror Door)",
    total_w_label: "Estimated Cabinet Price:",
    calc_w_note: "* Mechanisms and delivery included",
    shop_header: "Furniture Shop",
    shop_sub: "Catalog of ready-made and custom furniture",
    cat_all: "All",
    cat_kitchen: "Kitchens",
    cat_bedroom: "Bedrooms",
    cat_tv: "TV Zones",
    cat_wardrobe: "Wardrobes",
    cat_office: "Office",
    orders_header: "My Orders",
    orders_sub: "Status of your submitted orders",
    profile_header: "User Profile",
    phone_label: "Your Phone Number",
    address_label: "Delivery Address",
    save_btn: "💾 Save Data",
    support_title: "💬 Support and Consultation",
    support_desc: "Have questions? Contact administrator directly.",
    admin_btn: "👨‍💼 Contact Admin",
    cart_title: "🛒 Shopping Cart",
    total_cart: "Total Amount:",
    checkout_btn: "✅ Place Order",
    measurer_modal_title: "📐 Free Home Measurement Request",
    nav_home: "Home",
    nav_kitchen: "Kitchen",
    nav_wardrobe: "Wardrobe",
    nav_shop: "Shop",
    nav_orders: "Orders",
    nav_profile: "Profile"
  }
};

// Initialize on DOM Loaded
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initLanguage();
  initUserProfile();
  fetchProducts();
  updateKitchenCalc();
  updateWardrobeCalc();
  renderOrders();
  updateCartUI();
  updateBadges();
});

/* ================= Multilingual i18n Handler ================= */
function setLanguage(lang) {
  currentLang = lang;
  document.getElementById('lang-uz').classList.toggle('active', lang === 'uz');
  document.getElementById('lang-ru').classList.toggle('active', lang === 'ru');
  document.getElementById('lang-en').classList.toggle('active', lang === 'en');

  document.querySelectorAll('[data-i18n]').forEach(elem => {
    const key = elem.getAttribute('data-i18n');
    if (i18n[lang] && i18n[lang][key]) {
      elem.innerText = i18n[lang][key];
    }
  });

  localStorage.setItem('asmebel_language', lang);
  updateKitchenCalc();
  updateWardrobeCalc();
}

function toggleTheme() {
  const root = document.documentElement;
  const isDark = root.getAttribute('data-theme') === 'dark';
  const newTheme = isDark ? 'light' : 'dark';

  root.setAttribute('data-theme', newTheme);
  localStorage.setItem('asmebel_theme', newTheme);

  const btn = document.querySelector('.theme-toggle-btn');
  if (btn) btn.innerText = newTheme === 'dark' ? '☀️' : '🌙';
}

function initTheme() {
  const saved = localStorage.getItem('asmebel_theme') || 'dark';
  document.documentElement.setAttribute('data-theme', saved);

  const btn = document.querySelector('.theme-toggle-btn');
  if (btn) btn.innerText = saved === 'dark' ? '☀️' : '🌙';
}

function initLanguage() {
  const saved = localStorage.getItem('asmebel_language') || 'uz';
  setLanguage(saved);
}

/* ================= Tab Navigation ================= */
function switchTab(tabName) {
  currentTab = tabName;

  document.querySelectorAll('.tab-page').forEach(page => page.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));

  const targetPage = document.getElementById(`tab-${tabName}`);
  const targetNav = document.getElementById(`nav-${tabName}`);

  if (targetPage) targetPage.classList.add('active');
  if (targetNav) targetNav.classList.add('active');

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/* ================= Color Swatches Selector ================= */
function setKitchenColor(hex, name, btn) {
  selectedKitchenColor = { hex, name };
  const parent = btn.parentElement;
  parent.querySelectorAll('.swatch-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');

  const textElem = document.getElementById('kitchen-selected-color-text');
  if (textElem) textElem.innerText = `Tanlangan rang: ${name}`;

  updateKitchenCalc();
}

function setWardrobeColor(hex, name, btn) {
  selectedWardrobeColor = { hex, name };
  const parent = btn.parentElement;
  parent.querySelectorAll('.swatch-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');

  const textElem = document.getElementById('wardrobe-selected-color-text');
  if (textElem) textElem.innerText = `Tanlangan rang: ${name}`;

  updateWardrobeCalc();
}

/* ================= Payment Type / Installment Logic ================= */
function setPaymentType(type, btn, module) {
  const parent = btn.parentElement;
  parent.querySelectorAll('.opt-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');

  if (module === 'k') {
    kitchenPaymentType = type;
    updateKitchenCalc();
  } else {
    wardrobePaymentType = type;
    updateWardrobeCalc();
  }
}

/* ================= Kitchen Constructor Logic ================= */
function setKitchenShape(shape, btn) {
  selectedKitchenShape = shape;
  const parent = btn.parentElement;
  parent.querySelectorAll('.opt-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  updateKitchenCalc();
}

function updateKitchenCalc() {
  const length = parseFloat(document.getElementById('k-length').value);
  const height = parseFloat(document.getElementById('k-height').value);
  const facadeSelect = document.getElementById('k-facade');
  const topSelect = document.getElementById('k-top');

  document.getElementById('val-k-length').innerText = length.toFixed(1);
  document.getElementById('val-k-height').innerText = height.toFixed(1);

  const facadePrice = parseFloat(facadeSelect.options[facadeSelect.selectedIndex].getAttribute('data-price') || 0);
  const topPrice = parseFloat(topSelect.options[topSelect.selectedIndex].getAttribute('data-price') || 0);

  let shapeCoeff = 1.0;
  if (selectedKitchenShape === 'lshape') shapeCoeff = 1.45;
  if (selectedKitchenShape === 'ushape') shapeCoeff = 1.85;

  kitchenCalculatedTotal = Math.round((length * height * facadePrice + length * topPrice) * shapeCoeff);
  document.getElementById('kitchen-total-price').innerText = formatCurrency(kitchenCalculatedTotal);

  // Installment Text Update
  const instElem = document.getElementById('kitchen-installment-text');
  if (instElem) {
    if (kitchenPaymentType === 'full') {
      instElem.innerText = "";
    } else {
      const months = parseInt(kitchenPaymentType);
      const monthly = Math.round(kitchenCalculatedTotal / months);
      instElem.innerText = `💳 Muddatli to'lov (${months} oy): ${formatCurrency(monthly)} / oyiga`;
    }
  }

  renderKitchenVisual(length);
}

function renderKitchenVisual(length) {
  const canvas = document.getElementById('kitchen-preview-canvas');
  if (!canvas) {
    console.error('Canvas element not found!');
    return;
  }

  const width = 320;
  const height = 180;
  const color = selectedKitchenColor.hex;

  console.log('Rendering kitchen with color:', color);

  let svg = `
    <svg viewBox="0 0 ${width} ${height}" style="width: 100%; height: auto; filter: drop-shadow(0 4px 12px rgba(0,0,0,0.3));">
      <rect width="${width}" height="${height}" fill="rgba(0,0,0,0.1)" rx="8"/>
      <rect x="20" y="140" width="280" height="30" fill="rgba(100,120,140,0.2)" rx="4"/>
      <rect x="20" y="20" width="280" height="120" fill="rgba(180,200,220,0.08)" rx="4"/>

      <!-- Upper Cabinets -->
      <rect x="30" y="30" width="40" height="35" fill="${color}" stroke="rgba(255,255,255,0.3)" stroke-width="1" rx="2"/>
      <rect x="75" y="30" width="40" height="35" fill="${color}" stroke="rgba(255,255,255,0.3)" stroke-width="1" rx="2"/>
      <rect x="120" y="30" width="40" height="35" fill="${color}" stroke="rgba(255,255,255,0.3)" stroke-width="1" rx="2"/>
      <rect x="165" y="30" width="40" height="35" fill="${color}" stroke="rgba(255,255,255,0.3)" stroke-width="1" rx="2"/>
      <rect x="210" y="30" width="60" height="35" fill="${color}" stroke="rgba(255,255,255,0.3)" stroke-width="1" rx="2"/>

      <!-- Countertop -->
      <rect x="30" y="68" width="240" height="8" fill="rgba(212,175,55,0.4)" stroke="rgba(212,175,55,0.6)" stroke-width="1" rx="1"/>

      <!-- Lower Cabinets -->
      <rect x="30" y="78" width="50" height="55" fill="${color}" stroke="rgba(255,255,255,0.3)" stroke-width="1" rx="2"/>
      <rect x="85" y="78" width="50" height="55" fill="${color}" stroke="rgba(255,255,255,0.3)" stroke-width="1" rx="2"/>
      <rect x="140" y="78" width="50" height="55" fill="${color}" stroke="rgba(255,255,255,0.3)" stroke-width="1" rx="2"/>
      <rect x="195" y="78" width="75" height="55" fill="${color}" stroke="rgba(255,255,255,0.3)" stroke-width="1" rx="2"/>

      <!-- Sink -->
      <ellipse cx="110" cy="120" rx="8" ry="6" fill="rgba(200,200,200,0.3)" stroke="rgba(255,255,255,0.4)" stroke-width="1"/>

      <!-- Stove -->
      <rect x="155" y="100" width="25" height="25" fill="rgba(100,100,100,0.3)" stroke="rgba(255,255,255,0.4)" stroke-width="1" rx="1"/>
      <circle cx="160" cy="105" r="2" fill="rgba(255,150,0,0.4)"/>
      <circle cx="170" cy="105" r="2" fill="rgba(255,150,0,0.4)"/>
      <circle cx="160" cy="115" r="2" fill="rgba(255,150,0,0.4)"/>
      <circle cx="170" cy="115" r="2" fill="rgba(255,150,0,0.4)"/>
    </svg>
  `;

  try {
    canvas.innerHTML = svg;
    console.log('✅ Kitchen rendered successfully');
  } catch (e) {
    console.error('Error rendering kitchen:', e);
  }
}

function submitKitchenOrder() {
  const length = document.getElementById('k-length').value;
  const height = document.getElementById('k-height').value;
  const facadeName = document.getElementById('k-facade').options[document.getElementById('k-facade').selectedIndex].text;
  const topName = document.getElementById('k-top').options[document.getElementById('k-top').selectedIndex].text;
  const price = document.getElementById('kitchen-total-price').innerText;

  const orderData = {
    type: 'kitchen_constructor',
    title: `Oshxona Loyihasi (${selectedKitchenShape.toUpperCase()})`,
    length: `${length}m`,
    height: `${height}m`,
    facade: facadeName,
    top: topName,
    color: selectedKitchenColor.name,
    payment_type: kitchenPaymentType === 'full' ? 'Naqd' : `${kitchenPaymentType} oy muddatli`,
    total_price: price,
    user: tg.initDataUnsafe?.user || {}
  };

  sendOrderToBot(orderData);
}

/* ================= Wardrobe Constructor Logic ================= */
function setWardrobeType(type, btn) {
  selectedWardrobeType = type;
  const parent = btn.parentElement;
  parent.querySelectorAll('.opt-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  updateWardrobeCalc();
}

function updateWardrobeCalc() {
  const width = parseInt(document.getElementById('w-width').value);
  const height = parseInt(document.getElementById('w-height').value);
  const doors = parseInt(document.getElementById('w-doors').value);
  const drawers = parseInt(document.getElementById('w-drawers').value);
  const materialSelect = document.getElementById('w-material');
  const hasMirror = document.getElementById('w-mirror-check').checked;

  document.getElementById('val-w-width').innerText = width;
  document.getElementById('val-w-height').innerText = height;
  document.getElementById('val-w-doors').innerText = doors;
  document.getElementById('val-w-drawers').innerText = drawers;

  const matPrice = parseFloat(materialSelect.options[materialSelect.selectedIndex].getAttribute('data-price') || 0);
  const areaM2 = (width / 100) * (height / 100);
  let baseCost = areaM2 * matPrice + drawers * 150000;
  if (hasMirror) baseCost += 350000;

  wardrobeCalculatedTotal = Math.round(baseCost);
  document.getElementById('wardrobe-total-price').innerText = formatCurrency(wardrobeCalculatedTotal);

  // Installment Text Update
  const instElem = document.getElementById('wardrobe-installment-text');
  if (instElem) {
    if (wardrobePaymentType === 'full') {
      instElem.innerText = "";
    } else {
      const months = parseInt(wardrobePaymentType);
      const monthly = Math.round(wardrobeCalculatedTotal / months);
      instElem.innerText = `💳 Muddatli to'lov (${months} oy): ${formatCurrency(monthly)} / oyiga`;
    }
  }

  renderWardrobeVisual(doors, hasMirror);
}

function renderWardrobeVisual(doorsCount, hasMirror) {
  const renderBox = document.getElementById('w-render-box');
  if (!renderBox) return;

  const width = 320;
  const height = 200;
  const doorWidth = Math.floor((width - 40) / doorsCount);
  const color = selectedWardrobeColor.hex;

  let doorsHTML = '';
  for (let i = 0; i < doorsCount; i++) {
    const x = 20 + (i * doorWidth);
    const isMirrorDoor = hasMirror && (i === Math.floor(doorsCount / 2));

    if (isMirrorDoor) {
      doorsHTML += `
        <!-- Mirror Door -->
        <g>
          <rect x="${x}" y="30" width="${doorWidth - 2}" height="140" fill="rgba(200,220,240,0.5)" stroke="rgba(255,255,255,0.4)" stroke-width="1.5" rx="2"/>
          <line x1="${x + 5}" y1="35" x2="${x + doorWidth - 7}" y2="35" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
          <line x1="${x + 5}" y1="55" x2="${x + doorWidth - 7}" y2="55" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
          <line x1="${x + 5}" y1="75" x2="${x + doorWidth - 7}" y2="75" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
          <line x1="${x + 5}" y1="95" x2="${x + doorWidth - 7}" y2="95" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
          <line x1="${x + 5}" y1="115" x2="${x + doorWidth - 7}" y2="115" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
          <line x1="${x + 5}" y1="135" x2="${x + doorWidth - 7}" y2="135" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
          <circle cx="${x + doorWidth / 2}" cy="100" r="3" fill="rgba(229,193,88,0.6)"/>
        </g>
      `;
    } else {
      doorsHTML += `
        <!-- Regular Door -->
        <g>
          <rect x="${x}" y="30" width="${doorWidth - 2}" height="140" fill="${color}" stroke="rgba(255,255,255,0.3)" stroke-width="1.5" rx="2"/>
          <rect x="${x + 3}" y="40" width="${doorWidth - 8}" height="120" fill="rgba(255,255,255,0.08)" rx="1"/>
          <circle cx="${x + doorWidth - 8}" cy="100" r="2.5" fill="rgba(212,175,55,0.7)"/>
          <line x1="${x + 5}" y1="70" x2="${x + doorWidth - 7}" y2="70" stroke="rgba(255,255,255,0.2)" stroke-width="0.5"/>
          <line x1="${x + 5}" y1="100" x2="${x + doorWidth - 7}" y2="100" stroke="rgba(255,255,255,0.2)" stroke-width="0.5"/>
        </g>
      `;
    }
  }

  const svg = `
    <svg viewBox="0 0 ${width} ${height}" style="width: 100%; height: auto; filter: drop-shadow(0 4px 12px rgba(0,0,0,0.3));">
      <!-- Background -->
      <rect width="${width}" height="${height}" fill="rgba(0,0,0,0.1)" rx="8"/>

      <!-- Floor/Base -->
      <rect x="20" y="175" width="280" height="15" fill="rgba(100,120,140,0.2)" rx="2"/>

      <!-- Wall -->
      <rect x="20" y="20" width="280" height="160" fill="rgba(180,200,220,0.08)" rx="4"/>

      <!-- Cabinet Body -->
      <rect x="20" y="25" width="280" height="155" fill="rgba(50,70,90,0.1)" stroke="rgba(255,255,255,0.2)" stroke-width="1" rx="3"/>

      <!-- Doors Group -->
      <defs>
        <linearGradient id="wardrobeGlow" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color:rgba(229,193,88,0.12);stop-opacity:1" />
          <stop offset="100%" style="stop-color:rgba(229,193,88,0);stop-opacity:1" />
        </linearGradient>
      </defs>

      ${doorsHTML}

      <!-- Lighting Effect -->
      <rect x="20" y="25" width="280" height="155" fill="url(#wardrobeGlow)" rx="3"/>

      <!-- Top Trim -->
      <rect x="20" y="20" width="280" height="4" fill="rgba(212,175,55,0.3)" rx="2"/>

      <!-- Decorative Elements -->
      <circle cx="40" cy="175" r="3" fill="rgba(212,175,55,0.4)"/>
      <circle cx="80" cy="175" r="3" fill="rgba(212,175,55,0.4)"/>
      <circle cx="120" cy="175" r="3" fill="rgba(212,175,55,0.4)"/>
      <circle cx="160" cy="175" r="3" fill="rgba(212,175,55,0.4)"/>
      <circle cx="200" cy="175" r="3" fill="rgba(212,175,55,0.4)"/>
      <circle cx="240" cy="175" r="3" fill="rgba(212,175,55,0.4)"/>
      <circle cx="280" cy="175" r="3" fill="rgba(212,175,55,0.4)"/>
    </svg>
  `;

  renderBox.innerHTML = svg;
}

function submitWardrobeOrder() {
  const width = document.getElementById('w-width').value;
  const height = document.getElementById('w-height').value;
  const doors = document.getElementById('w-doors').value;
  const drawers = document.getElementById('w-drawers').value;
  const materialName = document.getElementById('w-material').options[document.getElementById('w-material').selectedIndex].text;
  const hasMirror = document.getElementById('w-mirror-check').checked ? "Ha" : "Yo'q";
  const price = document.getElementById('wardrobe-total-price').innerText;

  const orderData = {
    type: 'wardrobe_constructor',
    title: `Shkof Loyihasi (${selectedWardrobeType.toUpperCase()})`,
    dimensions: `${width}x${height} sm`,
    doors: `${doors} ta`,
    drawers: `${drawers} ta`,
    mirror: hasMirror,
    color: selectedWardrobeColor.name,
    material: materialName,
    payment_type: wardrobePaymentType === 'full' ? 'Naqd' : `${wardrobePaymentType} oy muddatli`,
    total_price: price,
    user: tg.initDataUnsafe?.user || {}
  };

  sendOrderToBot(orderData);
}

/* ================= Export Summary / Receipt Modal ================= */
function exportSummary(moduleType) {
  const modal = document.getElementById('export-modal');
  const content = document.getElementById('export-modal-content');
  if (!modal || !content) return;

  const now = new Date().toLocaleDateString('uz-UZ');
  let receiptHTML = '';

  if (moduleType === 'kitchen') {
    const length = document.getElementById('k-length').value;
    const height = document.getElementById('k-height').value;
    const facadeName = document.getElementById('k-facade').options[document.getElementById('k-facade').selectedIndex].text;
    const topName = document.getElementById('k-top').options[document.getElementById('k-top').selectedIndex].text;
    const total = document.getElementById('kitchen-total-price').innerText;

    receiptHTML = `
      <div style="text-align:center; border-bottom: 2px dashed #ccc; padding-bottom: 8px; margin-bottom: 8px;">
        <h2>ASMEBEL SMETA CHEKI</h2>
        <p>Sana: ${now} | Loyiha: Oshxona (${selectedKitchenShape.toUpperCase()})</p>
      </div>
      <p><strong>Fasad:</strong> ${facadeName}</p>
      <p><strong>Stoleshnitsa:</strong> ${topName}</p>
      <p><strong>Rang:</strong> ${selectedKitchenColor.name}</p>
      <p><strong>O'lchamlari:</strong> Uzunlik ${length}m x Balandlik ${height}m</p>
      <p><strong>To'lov Turi:</strong> ${kitchenPaymentType === 'full' ? 'Naqd / Bir yo\'la' : kitchenPaymentType + ' oy muddatli to\'lov'}</p>
      <hr style="margin: 10px 0;">
      <h3 style="color:#d4af37; text-align:right;">JAMI: ${total}</h3>
    `;
  } else {
    const width = document.getElementById('w-width').value;
    const height = document.getElementById('w-height').value;
    const doors = document.getElementById('w-doors').value;
    const materialName = document.getElementById('w-material').options[document.getElementById('w-material').selectedIndex].text;
    const total = document.getElementById('wardrobe-total-price').innerText;

    receiptHTML = `
      <div style="text-align:center; border-bottom: 2px dashed #ccc; padding-bottom: 8px; margin-bottom: 8px;">
        <h2>ASMEBEL SMETA CHEKI</h2>
        <p>Sana: ${now} | Loyiha: Shkof (${selectedWardrobeType.toUpperCase()})</p>
      </div>
      <p><strong>Material:</strong> ${materialName}</p>
      <p><strong>Rang:</strong> ${selectedWardrobeColor.name}</p>
      <p><strong>O'lcham:</strong> ${width}x${height} sm (${doors} eshikli)</p>
      <p><strong>To'lov Turi:</strong> ${wardrobePaymentType === 'full' ? 'Naqd / Bir yo\'la' : wardrobePaymentType + ' oy muddatli to\'lov'}</p>
      <hr style="margin: 10px 0;">
      <h3 style="color:#d4af37; text-align:right;">JAMI: ${total}</h3>
    `;
  }

  content.innerHTML = receiptHTML;
  modal.classList.add('open');
}

function toggleExportModal() {
  const modal = document.getElementById('export-modal');
  if (modal) modal.classList.toggle('open');
}

/* ================= Measurer Modal ================= */
function toggleMeasurerModal() {
  const modal = document.getElementById('measurer-modal');
  if (modal) modal.classList.toggle('open');
}

function submitMeasurerRequest() {
  const date = document.getElementById('measurer-date-input').value;
  const time = document.getElementById('measurer-time-input').value;
  const phone = document.getElementById('measurer-phone-input').value;

  if (!date || !phone) {
    alert("Iltimos, sana va telefon raqamingizni kiriting!");
    return;
  }

  const orderData = {
    type: 'measurer_call',
    title: "📐 Uyga O'lchovchi Chaqiruv So'rovi",
    preferred_date: date,
    preferred_time: time,
    phone: phone,
    user: tg.initDataUnsafe?.user || {}
  };

  toggleMeasurerModal();
  sendOrderToBot(orderData);
}

/* ================= Geolocation / Location Picker ================= */
function fetchUserLocation() {
  const statusElem = document.getElementById('location-coords-status');
  if (statusElem) statusElem.innerText = "🔍 Joylashuv aniqlanmoqda...";

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const lat = pos.coords.latitude.toFixed(5);
        const lng = pos.coords.longitude.toFixed(5);
        const locStr = `GPS: ${lat}, ${lng}`;
        document.getElementById('user-address-input').value = locStr;
        if (statusElem) statusElem.innerText = `✅ Aniqlandi: ${locStr}`;
      },
      (err) => {
        if (statusElem) statusElem.innerText = "⚠️ Joylashuvni avto-aniqlashga ruxsat berilmadi. Manzilni qo'lda kiriting.";
      }
    );
  } else {
    if (statusElem) statusElem.innerText = "Manzilni matn ko'rinishida kiriting.";
  }
}

/* ================= Shop & Products Catalog ================= */
async function fetchProducts() {
  try {
    const res = await fetch(API_BASE + '/api/products', {
      headers: { 'ngrok-skip-browser-warning': '1' },
      method: 'GET'
    });

    if (res.ok) {
      const data = await res.json();
      productsList = [];

      if (data && typeof data === 'object') {
        Object.keys(data).forEach(catKey => {
          const cat = data[catKey];
          if (cat && cat.products && Array.isArray(cat.products)) {
            cat.products.forEach(p => {
              if (p) {
                productsList.push({
                  id: p.id || Math.random(),
                  category: catKey,
                  name: p.caption ? p.caption.split('\n')[0] : (cat.name || 'Mahsulot'),
                  price: p.price || 5000000,
                  image: p.photo_url || 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=500&auto=format&fit=crop&q=60'
                });
              }
            });
          }
        });
      }
      console.log('Mahsulotlar yuklandi:', productsList.length);
    } else {
      console.warn('API xatoligi:', res.status, res.statusText);
      // Mahsulot bo'lmasa ham, boş katalog ko'rsatamiz
    }
  } catch (err) {
    console.warn('API ulanish xatoligi:', err);
  }

  renderProducts('all');
}

function filterCategory(cat, btn) {
  const parent = btn.parentElement;
  parent.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderProducts(cat);
}

function renderProducts(category) {
  const container = document.getElementById('products-container');
  if (!container) return;

  const filtered = (category === 'all') 
    ? productsList 
    : productsList.filter(p => p.category === category);

  if (filtered.length === 0) {
    container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 20px;">Ushbu bo'limda hozircha mahsulotlar yo'q.</div>`;
    return;
  }

  container.innerHTML = filtered.map(p => `
    <div class="product-card">
      <img src="${p.image}" alt="${p.name}" class="product-img" onerror="this.src='https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=500&auto=format&fit=crop&q=60'">
      <div class="product-details">
        <h4 class="product-name">${p.name}</h4>
        <div class="product-price">${formatCurrency(p.price)}</div>
        <button class="add-cart-btn" onclick="addToCart(${p.id})">+ Savatga</button>
      </div>
    </div>
  `).join('');
}

/* ================= Shopping Cart ================= */
function addToCart(productId) {
  const prod = productsList.find(p => p.id === productId);
  if (!prod) return;

  const existing = cart.find(item => item.id === productId);
  if (existing) {
    existing.qty += 1;
  } else {
    cart.push({ ...prod, qty: 1 });
  }

  updateCartUI();
}

function updateCartUI() {
  const countSpan = document.getElementById('cart-count');
  const itemsContainer = document.getElementById('cart-items-container');
  const totalPriceSpan = document.getElementById('cart-total-price');

  const totalCount = cart.reduce((sum, i) => sum + i.qty, 0);
  const totalPrice = cart.reduce((sum, i) => sum + (i.price * i.qty), 0);

  if (countSpan) countSpan.innerText = totalCount;
  if (totalPriceSpan) totalPriceSpan.innerText = formatCurrency(totalPrice);

  if (itemsContainer) {
    if (cart.length === 0) {
      itemsContainer.innerHTML = `<div style="text-align: center; color: var(--text-muted); padding: 20px;">Savatchangiz bo'sh</div>`;
    } else {
      itemsContainer.innerHTML = cart.map(item => `
        <div class="cart-item">
          <div>
            <div class="cart-item-title">${item.name}</div>
            <div class="cart-item-price">${formatCurrency(item.price)} x ${item.qty}</div>
          </div>
          <button style="background: transparent; border: none; color: #ff4d4d; font-size: 16px; cursor: pointer;" onclick="removeFromCart(${item.id})">🗑️</button>
        </div>
      `).join('');
    }
  }
}

function removeFromCart(productId) {
  cart = cart.filter(item => item.id !== productId);
  updateCartUI();
}

function toggleCartModal() {
  const modal = document.getElementById('cart-modal');
  if (modal) modal.classList.toggle('open');
}

function checkoutCart() {
  if (cart.length === 0) {
    alert("Savatingiz bo'sh!");
    return;
  }

  const totalPrice = cart.reduce((sum, i) => sum + (i.price * i.qty), 0);
  const orderData = {
    type: 'shop_cart_checkout',
    title: "Do'kon Xaridi",
    items: cart.map(i => `${i.name} (${i.qty} ta)`).join(', '),
    total_price: formatCurrency(totalPrice),
    user: tg.initDataUnsafe?.user || {}
  };

  cart = [];
  updateCartUI();
  toggleCartModal();
  sendOrderToBot(orderData);
}

/* ================= Send Order to Bot / Storage ================= */
async function sendOrderToBot(orderData) {
  const newOrder = {
    id: `ORD-${Math.floor(1000 + Math.random() * 9000)}`,
    date: new Date().toLocaleDateString('uz-UZ'),
    title: orderData.title,
    details: orderData.items || `${orderData.facade || orderData.material || ''}`,
    price: orderData.total_price,
    status: 'Qabul qilindi'
  };

  userOrders.unshift(newOrder);
  localStorage.setItem('asmebel_orders', JSON.stringify(userOrders));
  renderOrders();

  try {
    const payload = JSON.stringify(orderData);
    tg.sendData(payload);

    await fetch(API_BASE + '/api/order', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'ngrok-skip-browser-warning': '1'
      },
      body: payload
    });
  } catch (e) {
    console.log('Sending fallback');
  }

  alert("🚀 Buyurtmangiz qabul qilindi! Menejerimiz tez orada bog'lanadi.");
  switchTab('orders');
}

function renderOrders() {
  const container = document.getElementById('orders-container');
  if (!container) return;

  if (userOrders.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; color: var(--text-muted); padding: 40px 20px;">
        <span style="font-size: 40px; display: block; margin-bottom: 10px;">📦</span>
        Sizda hali buyurtmalar yo'q. Oshxona yoki Shkof konstruktorida yangi loyiha yarating!
      </div>
    `;
    return;
  }

  container.innerHTML = userOrders.map(o => `
    <div class="order-card">
      <div class="order-header">
        <span class="order-id">${o.id}</span>
        <span class="order-status received">⚡ ${o.status}</span>
      </div>
      <div class="order-items-text"><strong>${o.title}</strong> - ${o.details || ''}</div>
      <div class="order-total">Summa: ${o.price}</div>
    </div>
  `).join('');
}

/* ================= Profile & Helpers ================= */
function initUserProfile() {
  const user = tg.initDataUnsafe?.user || {};
  const name = user.first_name ? `${user.first_name} ${user.last_name || ''}` : "Foydalanuvchi";
  
  const nameElem = document.getElementById('user-full-name');
  const idElem = document.getElementById('user-telegram-id');
  const avatarElem = document.getElementById('user-avatar-initials');

  if (nameElem) nameElem.innerText = name;
  if (idElem) idElem.innerText = user.id ? `ID: ${user.id}` : "ID: Mehmon";
  if (avatarElem) avatarElem.innerText = name.charAt(0).toUpperCase();

  const savedPhone = localStorage.getItem('asmebel_user_phone') || '';
  const savedAddress = localStorage.getItem('asmebel_user_address') || '';

  if (document.getElementById('user-phone-input')) document.getElementById('user-phone-input').value = savedPhone;
  if (document.getElementById('user-address-input')) document.getElementById('user-address-input').value = savedAddress;
}

function saveUserProfile() {
  const phone = document.getElementById('user-phone-input').value;
  const address = document.getElementById('user-address-input').value;

  localStorage.setItem('asmebel_user_phone', phone);
  localStorage.setItem('asmebel_user_address', address);

  alert("✅ Ma'lumotlaringiz muvaffaqiyatli saqlandi!");
}

function formatCurrency(amount) {
  return amount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + " so'm";
}

function updateBadges() {
  const shopBadge = document.getElementById('shop-product-count');
  const ordersBadge = document.getElementById('orders-count');

  if (shopBadge) {
    shopBadge.innerText = productsList.length;
    if (productsList.length === 0) shopBadge.style.display = 'none';
    else shopBadge.style.display = 'flex';
  }

  if (ordersBadge) {
    ordersBadge.innerText = userOrders.length;
    if (userOrders.length === 0) ordersBadge.style.display = 'none';
    else ordersBadge.style.display = 'flex';
  }
}
