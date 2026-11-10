import { useState, useEffect } from 'react'
import { Link, useParams } from 'react-router-dom';
import { useAuth } from '../context/Auth';
import './OrderItems.css';

function OrderItems() {
  const { user, getOrderItems } = useAuth();
  const { orderId } = useParams();
  const [items, setItems] = useState([]);      
  const [loading, setLoading] = useState(true);     
  const [error, setError] = useState(null);         

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await getOrderItems(user, orderId);
        console.log(data)

        const items = Array.isArray(data) ? data : [];

        setItems(items);
      } catch (err) {
        console.error(err);
        setError(err.message || 'Не удалось загрузить состав заказа');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [user, getOrderItems, orderId]);
  if (loading) return <div className="order-items__loading">Загрузка...</div>;
  if (error) return <div className="order-items__error">{error}</div>;

  const totalSum = items.reduce((sum, it) => sum + Number(it.price_at_time || 0), 0);

  return (
    <div className="order-items">
      <h2 className="order-items__title">Состав заказа</h2>
      <p className="order-items__subtitle">Заказ №{orderId}</p>

      {items.length === 0 ? (
        <div className="order-items__empty">
          В этом заказе пока нет позиций
        </div>
      ) : (
        <>
          <div className="order-items__list">
            {items.map((it) => (
              <div className="order-item" key={it.id}>
                <p className="order-item__name">{it.product['name']}</p>
                <p className="order-item__meta">{it.quantity} шт.</p>
                <p className="order-item__price">{it.price_at_time} ₽</p>
              </div>
            ))}
          </div>

          <div className="order-items__summary">
            <p className="order-items__total">
              <span>Итого по заказу</span>
              {totalSum} ₽
            </p>
          </div>
        </>
      )}

      <Link to="/myorders" className="order-items__back">
        ← Назад к заказам
      </Link>
    </div>
  );
}

export default OrderItems;
