import { Link } from 'react-router-dom';
import './Home.css';

function Home() {
  return (
    <div className="home">
      <header className="home__header">
        <h1 className="home__title">ФруктовыйМикс — свежие фрукты каждый день</h1>
        <p className="home__subtitle">
          У нас — спелые фрукты, быстрая доставка и честные цены. 
          Выбирайте любимые товары и оформляйте заказ онлайн.
        </p>

        <div className="home__actions">
          <Link to="/catalog" className="btn-primary">Перейти в каталог</Link>
        </div>
      </header>

      <section className="home__features">
        <div className="feature-card">
          <div className="feature-card__icon">🍎</div>
          <h3 className="feature-card__title">Только свежие поставки</h3>
          <p className="feature-card__desc">
            Фрукты поступают к нам напрямую от фермеров и проходят контроль качества.
          </p>
        </div>
        <div className="feature-card">
          <div className="feature-card__icon">🚚</div>
          <h3 className="feature-card__title">Быстрая доставка</h3>
          <p className="feature-card__desc">
            Доставим заказ в течение 2 часов или в удобное для вас время.
          </p>
        </div>
        <div className="feature-card">
          <div className="feature-card__icon">💰</div>
          <h3 className="feature-card__title">Выгодные цены</h3>
          <p className="feature-card__desc">
            Регулярные акции и скидки на сезонные фрукты.
          </p>
        </div>
      </section>
    </div>
  );
}

export default Home;