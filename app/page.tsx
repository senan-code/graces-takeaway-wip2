const hours = [
  ["Monday", "Closed"],
  ["Tuesday", "Closed"],
  ["Wednesday", "4:00 – 10:30 pm"],
  ["Thursday", "4:00 – 10:30 pm"],
  ["Friday", "3:00 – 11:00 pm"],
  ["Saturday", "4:00 – 11:00 pm"],
  ["Sunday", "4:00 – 11:00 pm"],
];

const favourites = [
  { name: "Fresh Fish & Chips", note: "Golden, crisp and made to order", icon: "fish" },
  { name: "Chicken Fillet Wrap", note: "A Piltown favourite", icon: "wrap" },
  { name: "Classic Burgers", note: "Hot, hearty and satisfying", icon: "burger" },
];

function FoodIcon({ type }: { type: string }) {
  if (type === "fish") return <span className="food-emoji" aria-hidden="true">🐟</span>;
  if (type === "wrap") return <span className="food-emoji" aria-hidden="true">🌯</span>;
  return <span className="food-emoji" aria-hidden="true">🍔</span>;
}

function ArrowIcon() {
  return (
    <svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 10h11M11 5l5 5-5 5" /></svg>
  );
}

export default function Home() {
  return (
    <main>
      <header className="site-header">
        <a className="brand" href="#top" aria-label="Grace’s Takeaway home">
          <span className="brand-mark">G</span>
          <span>Grace’s<small>Takeaway · Piltown</small></span>
        </a>
        <nav aria-label="Main navigation">
          <a href="#favourites">Favourites</a>
          <a href="#hours">Hours</a>
          <a href="#visit">Find us</a>
        </nav>
        <a className="header-call" href="tel:+35351643759">Call to order</a>
      </header>

      <section className="hero" id="top">
        <div className="hero-copy">
          <p className="eyebrow"><span /> Proudly serving Piltown</p>
          <h1>Good food.<br /><em>Done right.</em></h1>
          <p className="hero-intro">Freshly cooked takeaway favourites, generous portions, and a warm local welcome—right here on Main Street.</p>
          <div className="hero-actions">
            <a className="button button-primary" href="tel:+35351643759">Call 051 643 759 <ArrowIcon /></a>
            <a className="text-link" href="#hours">See opening hours <ArrowIcon /></a>
          </div>
          <div className="trust-row">
            <span><b>25+</b> years local</span>
            <span><b>4.3</b> Google rating*</span>
            <span><b>Fresh</b> cooked to order</span>
          </div>
        </div>
        <div className="hero-art" aria-label="Fresh takeaway food illustration">
          <div className="sun" />
          <div className="chip-box">
            <i /><i /><i /><i /><i /><i /><i />
            <strong>G</strong>
          </div>
          <div className="hero-badge"><span>Made</span><b>FRESH</b><span>for you</span></div>
          <p>Simple ingredients.<br />Big flavour.</p>
        </div>
      </section>

      <section className="favourites section" id="favourites">
        <div className="section-heading">
          <div><p className="eyebrow"><span /> Local favourites</p><h2>What are you<br />in the mood for?</h2></div>
          <p>From crispy chips to stacked burgers, there’s something to sort every craving.</p>
        </div>
        <div className="food-grid">
          {favourites.map((item, index) => (
            <article className="food-card" key={item.name}>
              <span className="card-number">0{index + 1}</span>
              <div className="icon-disc"><FoodIcon type={item.icon} /></div>
              <h3>{item.name}</h3>
              <p>{item.note}</p>
            </article>
          ))}
        </div>
        <p className="menu-note">For today’s full menu and prices, give us a call — we’ll be happy to help.</p>
      </section>

      <section className="hours-section section" id="hours">
        <div className="hours-copy">
          <p className="eyebrow light"><span /> Plan your visit</p>
          <h2>Your evening,<br /><em>sorted.</em></h2>
          <p>Call ahead and we’ll have your order cooking. Collection from our Main Street takeaway in the heart of Piltown.</p>
          <a className="button button-light" href="tel:+35351643759">Call to order <ArrowIcon /></a>
        </div>
        <div className="hours-card">
          <div className="hours-card-title"><h3>Opening hours</h3><span>Weekly</span></div>
          <dl>
            {hours.map(([day, time]) => <div key={day} className={time === "Closed" ? "closed" : ""}><dt>{day}</dt><dd>{time}</dd></div>)}
          </dl>
          <p>Hours can change on bank holidays. Call ahead to confirm.</p>
        </div>
      </section>

      <section className="visit section" id="visit">
        <div className="visit-card">
          <p className="eyebrow"><span /> Find us</p>
          <h2>Right in the heart<br />of Piltown.</h2>
          <address>Main Street, Banagher<br />Piltown, Co. Kilkenny</address>
          <a className="button button-primary" href="https://www.google.com/maps/search/?api=1&query=Graces+Takeaway+Main+Street+Piltown+Kilkenny" target="_blank" rel="noreferrer">Get directions <ArrowIcon /></a>
        </div>
        <div className="map-art" aria-hidden="true">
          <svg viewBox="0 0 800 430" preserveAspectRatio="none">
            <path className="road" d="M-30 385C145 320 95 210 280 214s233-5 310-110S700 10 850 25" />
            <path className="road thin" d="M10 30c120 90 160 90 270 184s200 80 290 210" />
            <path className="water" d="M-20 90c170-80 214 30 318 19S477 20 820 155" />
          </svg>
          <div className="pin"><span>G</span></div>
          <b>MAIN STREET</b><small>PILTOWN</small>
        </div>
      </section>

      <footer>
        <div className="footer-brand"><span className="brand-mark">G</span><div><b>Grace’s Takeaway</b><span>Main Street · Piltown</span></div></div>
        <a href="tel:+35351643759">051 643 759</a>
        <p>© {new Date().getFullYear()} Grace’s Takeaway. <span>*Rating shown from public listings at time of publication.</span></p>
      </footer>
    </main>
  );
}
