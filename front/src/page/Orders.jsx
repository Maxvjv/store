import { useState, useEffect } from 'react'
import { Link, useParams } from 'react-router-dom';
import { useAuth } from '../context/Auth';
import './Orders.css';

function Orders() {
  const { user, getOrders } = useAuth();
  const [listorders, setListorders] = useState([]);    
  const [loading, setLoading] = useState(true);     
  const [error, setError] = useState(null);        

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await getOrders(user);
        console.log(data)

        const listorders = Array.isArray(data) ? data : [];

        setListorders(listorders);
      } catch (err) {
        console.error(err);
        setError(err.message || 'Не удалось загрузить заказы');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [user, getOrders]);

  if (loading) return <div className="orders__loading">Загрузка...</div>;
  if (error) return <div className="orders__error">{error}</div>;

  return (
    <div className="orders">
      <h2 className="orders__title">Мои заказы</h2>

      {listorders.length === 0 ? (
        <div className="orders__empty">
          Заказов пока нет — самое время заглянуть в <Link to="/catalog">каталог</Link> 😊
        </div>
      ) : (
        <div className="orders__grid">
          {listorders.map((ord) => (
            <div className="order-card" key={ord.id}>
              <p className="order-card__amount">
                <span>Итого со скидками</span>
                {ord.total_amount}
              </p>

              <p className="order-card__field">
                <span>Адрес: </span>{ord.shipping_address}
              </p>
              <p className="order-card__field">
                <span>Телефон: </span>{ord.contact_phone}
              </p>

              <Link to={`/myorders/${ord.id}`} className="order-card__link">
                Детали заказа →
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Orders;